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


def test_deduplicates_near_duplicate_descriptions_of_the_same_tracked_entity():
    # DAM rephrases near-identical consecutive-frame detections of the same
    # real-world object slightly differently each time, so exact-string
    # matching alone barely dedupes anything in a busy scene.
    descriptions = [
        {
            "timestamp": 0.0,
            "region_label": "person",
            "description": (
                "A man with short, dark hair is wearing a light blue, long-sleeved "
                "button-up shirt with the sleeves rolled up to the elbows. He is also "
                "wearing dark blue jeans. His hands are clasped together in front of him."
            ),
        },
        {
            "timestamp": 1.5,
            "region_label": "person",
            "description": (
                "A man with short, dark hair is wearing a light-colored, long-sleeved "
                "shirt with a dark collar. He is also wearing blue jeans."
            ),
        },
        {
            "timestamp": 3.0,
            "region_label": "car",
            "description": "A silver hatchback car is parked on the right side of the image.",
        },
    ]

    segments = build_segments(descriptions, window_seconds=10.0)

    assert len(segments) == 1
    kept_count = segments[0]["description"].count("dark hair")
    assert kept_count == 1
    assert "silver hatchback" in segments[0]["description"]


def test_keeps_genuinely_different_descriptions_with_the_same_label():
    descriptions = [
        {"timestamp": 0.0, "region_label": "person", "description": "A woman in a red dress rides a bicycle."},
        {"timestamp": 1.0, "region_label": "person", "description": "An elderly man with a cane crosses the street."},
    ]

    segments = build_segments(descriptions, window_seconds=10.0)

    assert "red dress" in segments[0]["description"]
    assert "elderly man" in segments[0]["description"]
