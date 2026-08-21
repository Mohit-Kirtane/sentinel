from pipeline.build_segments import build_segments


def test_groups_descriptions_into_fixed_windows():
    descriptions = [
        {"timestamp": 0.5, "region_label": "person", "description": "A person in a blue jacket walks in."},
        {"timestamp": 3.0, "region_label": "backpack", "description": "A backpack is set down near the counter."},
        {"timestamp": 12.0, "region_label": "person", "description": "A person in a red shirt enters the frame."},
    ]

    segments = build_segments(descriptions, window_seconds=10.0)

    assert len(segments) == 2
    assert segments[0]["start_ts"] == 0.0
    assert segments[0]["end_ts"] == 10.0
    assert "blue jacket" in segments[0]["description"]
    assert "backpack" in segments[0]["description"]
    assert segments[1]["start_ts"] == 10.0
    assert segments[1]["end_ts"] == 20.0
    assert "red shirt" in segments[1]["description"]


def test_empty_input_returns_no_segments():
    assert build_segments([], window_seconds=10.0) == []


def test_deduplicates_identical_consecutive_descriptions_within_a_window():
    descriptions = [
        {"timestamp": 1.0, "region_label": "person", "description": "A person stands near the door."},
        {"timestamp": 2.0, "region_label": "person", "description": "A person stands near the door."},
    ]

    segments = build_segments(descriptions, window_seconds=10.0)

    assert len(segments) == 1
    assert segments[0]["description"].count("A person stands near the door.") == 1
