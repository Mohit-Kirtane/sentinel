import os
import subprocess


def extract_frames(video_path: str, output_dir: str, interval_seconds: float = 2.0) -> list[dict]:
    """Sample one frame every `interval_seconds` from `video_path` into `output_dir`.

    Returns a list of {"timestamp": float, "frame_path": str}, ordered by timestamp.
    """
    os.makedirs(output_dir, exist_ok=True)
    fps = 1.0 / interval_seconds
    pattern = os.path.join(output_dir, "frame_%05d.png")

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video_path,
            "-vf",
            f"fps={fps}",
            "-y",
            pattern,
        ],
        check=True,
        capture_output=True,
    )

    frame_files = sorted(f for f in os.listdir(output_dir) if f.startswith("frame_"))
    return [
        {
            "timestamp": index * interval_seconds,
            "frame_path": os.path.join(output_dir, filename),
        }
        for index, filename in enumerate(frame_files)
    ]
