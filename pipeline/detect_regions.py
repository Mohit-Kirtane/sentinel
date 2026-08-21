from functools import lru_cache

from ultralytics import YOLO

TARGET_LABELS = {
    "person",
    "backpack",
    "handbag",
    "suitcase",
    "car",
    "truck",
    "bicycle",
    "motorcycle",
}


@lru_cache
def _model() -> YOLO:
    return YOLO("yolov8n.pt")


def detect_regions(frame_path: str, confidence_threshold: float = 0.4) -> list[dict]:
    """Propose person/object regions in a single frame via YOLOv8n (CPU-friendly).

    Returns a list of {"label": str, "box": [x1, y1, x2, y2], "confidence": float}.
    """
    results = _model().predict(source=frame_path, conf=confidence_threshold, verbose=False)
    regions = []
    for result in results:
        for box in result.boxes:
            label = result.names[int(box.cls[0])]
            if label not in TARGET_LABELS:
                continue
            regions.append(
                {
                    "label": label,
                    "box": [round(v, 1) for v in box.xyxy[0].tolist()],
                    "confidence": round(float(box.conf[0]), 4),
                }
            )
    return regions
