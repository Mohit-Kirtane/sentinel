from uuid import uuid4

from app.db.models import Segment, Video


def embed_segments(segments: list[dict], embed_fn) -> list[dict]:
    """Add an "embedding" key to each segment dict via embed_fn(description) -> list[float]."""
    return [{**segment, "embedding": embed_fn(segment["description"])} for segment in segments]


def store_video_and_segments(
    video_id: str,
    title: str,
    filename: str,
    duration_seconds: int,
    segments_with_embeddings: list[dict],
    repo,
) -> None:
    repo.insert_video(
        Video(id=video_id, title=title, filename=filename, duration_seconds=duration_seconds)
    )
    repo.insert_segments(
        [
            Segment(
                id=str(uuid4()),
                video_id=video_id,
                start_ts=segment["start_ts"],
                end_ts=segment["end_ts"],
                description=segment["description"],
                embedding=segment["embedding"],
            )
            for segment in segments_with_embeddings
        ]
    )
