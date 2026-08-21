import os

from pipeline.detect_regions import detect_regions

SAMPLE_IMAGE = os.path.join(
    os.path.dirname(__import__("ultralytics").__file__), "assets", "bus.jpg"
)


def test_detects_person_regions_in_a_known_image():
    regions = detect_regions(SAMPLE_IMAGE, confidence_threshold=0.4)

    assert len(regions) > 0
    for region in regions:
        assert set(region.keys()) == {"label", "box", "confidence"}
        assert len(region["box"]) == 4
        assert 0.0 <= region["confidence"] <= 1.0
    assert any(region["label"] == "person" for region in regions)


def test_confidence_threshold_filters_out_low_confidence_boxes():
    loose = detect_regions(SAMPLE_IMAGE, confidence_threshold=0.01)
    strict = detect_regions(SAMPLE_IMAGE, confidence_threshold=0.99)

    assert len(strict) <= len(loose)
