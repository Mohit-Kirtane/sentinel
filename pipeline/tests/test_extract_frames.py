import subprocess

import pytest

from pipeline.extract_frames import extract_frames


@pytest.fixture
def synthetic_video(tmp_path):
    video_path = tmp_path / "synthetic.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "lavfi",
            "-i",
            "testsrc=duration=5:size=64x64:rate=1",
            "-y",
            str(video_path),
        ],
        check=True,
        capture_output=True,
    )
    return video_path


def test_extracts_one_frame_per_interval(synthetic_video, tmp_path):
    output_dir = tmp_path / "frames"

    frames = extract_frames(str(synthetic_video), str(output_dir), interval_seconds=2.0)

    # A 5-second clip sampled every 2s yields frames at 0s, 2s, 4s.
    assert [f["timestamp"] for f in frames] == [0.0, 2.0, 4.0]


def test_frame_files_actually_exist_on_disk(synthetic_video, tmp_path):
    output_dir = tmp_path / "frames"

    frames = extract_frames(str(synthetic_video), str(output_dir), interval_seconds=2.0)

    import os

    for frame in frames:
        assert os.path.isfile(frame["frame_path"])
