"""Offline enrichment pipeline entrypoint - run manually per demo video.

Intended to run in a GPU notebook (Colab/Kaggle) alongside a locally-started
DAM server (NVlabs/describe-anything's dam_server.py). Never deployed with
the live app; the live app only ever reads what this script writes to
Postgres.

Usage:
    python -m pipeline.run_pipeline \\
        --video path/to/clip.mp4 \\
        --video-id lobby-01 \\
        --title "Lobby Camera" \\
        --dam-server-url http://localhost:8000 \\
        --frame-skip 2

Requires env vars: DATABASE_URL, LLM_API_KEY (Gemini, for chat generation -
embeddings run locally via sentence-transformers, no API key needed for that
part).
"""

import os

# Must be set before transformers/tokenizers/torch get imported anywhere in
# this process (detect_regions' ultralytics/opencv, then core.llm's
# sentence-transformers both load torch here). tokenizers' Rust extension
# disables its own internal parallelism after a fork (dam_server.py is
# spawned via subprocess.Popen) but that interacts badly with opencv's and
# torch's own native threading in the same process, surfacing as a
# non-Python "free(): invalid pointer" crash rather than a catchable
# exception - reproduced running the real pipeline in Colab.
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import argparse
import logging
import tempfile

from openai import OpenAI
from sqlalchemy.orm import sessionmaker

from app.core.llm import embed_text
from app.db.repository import PostgresRepository
from app.db.session import get_engine
from pipeline.build_segments import build_segments
from pipeline.describe_regions import describe_region
from pipeline.detect_regions import detect_regions
from pipeline.embed_and_store import embed_segments, store_video_and_segments
from pipeline.extract_frames import extract_frames

logger = logging.getLogger(__name__)


def run(
    video_path: str,
    video_id: str,
    title: str,
    dam_server_url: str,
    interval_seconds: float = 2.0,
    frame_skip: int = 1,
):
    """frame_skip: only send every Nth *extracted* frame through DAM (1 = every
    frame). Consecutive sampled frames of a mostly-static scene are highly
    redundant - DAM is the expensive, rate-limited step, so thinning here
    cuts real cost/time on top of extract_frames' own interval_seconds
    sampling, independent of it (e.g. sample every 1.5s for finer
    timestamps, but only describe every 2nd of those)."""
    dam_client = OpenAI(api_key="unused", base_url=dam_server_url)

    with tempfile.TemporaryDirectory() as frames_dir:
        all_frames = extract_frames(video_path, frames_dir, interval_seconds=interval_seconds)
        frames = all_frames[::frame_skip]
        logger.info(
            "Extracted %d frames, describing %d after frame_skip=%d",
            len(all_frames),
            len(frames),
            frame_skip,
        )

        region_descriptions = []
        for frame in frames:
            regions = detect_regions(frame["frame_path"])
            for region in regions:
                try:
                    description = describe_region(frame["frame_path"], region["box"], client=dam_client)
                except Exception:
                    logger.exception(
                        "DAM description failed for frame %s region %s - skipping",
                        frame["frame_path"],
                        region["label"],
                    )
                    continue
                region_descriptions.append(
                    {
                        "timestamp": frame["timestamp"],
                        "region_label": region["label"],
                        "description": description,
                    }
                )

    segments = build_segments(region_descriptions, window_seconds=10.0)
    segments_with_embeddings = embed_segments(segments, embed_fn=embed_text)

    Session = sessionmaker(bind=get_engine())
    with Session() as session:
        repo = PostgresRepository(session)
        duration_seconds = int(segments[-1]["end_ts"]) if segments else 0
        store_video_and_segments(
            video_id=video_id,
            title=title,
            filename=video_path.split("/")[-1],
            duration_seconds=duration_seconds,
            segments_with_embeddings=segments_with_embeddings,
            repo=repo,
        )

    logger.info("Stored %d segments for video %s", len(segments_with_embeddings), video_id)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--dam-server-url", required=True)
    parser.add_argument("--interval-seconds", type=float, default=2.0)
    parser.add_argument(
        "--frame-skip",
        type=int,
        default=1,
        help="Only describe every Nth extracted frame via DAM (1 = every frame).",
    )
    args = parser.parse_args()
    run(
        args.video,
        args.video_id,
        args.title,
        args.dam_server_url,
        args.interval_seconds,
        args.frame_skip,
    )
