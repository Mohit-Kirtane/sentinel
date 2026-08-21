from difflib import SequenceMatcher

NEAR_DUPLICATE_SIMILARITY_THRESHOLD = 0.6


def _is_near_duplicate(candidate: str, existing: str) -> bool:
    # SequenceMatcher.ratio() isn't symmetric - its autojunk heuristic treats
    # the second argument differently, so take the max of both orderings.
    forward = SequenceMatcher(None, candidate, existing).ratio()
    backward = SequenceMatcher(None, existing, candidate).ratio()
    return max(forward, backward) >= NEAR_DUPLICATE_SIMILARITY_THRESHOLD


def build_segments(descriptions: list[dict], window_seconds: float = 10.0) -> list[dict]:
    """Merge per-frame region descriptions into fixed-width time-window segments.

    descriptions: list of {"timestamp": float, "region_label": str, "description": str}
    returns: list of {"start_ts": float, "end_ts": float, "description": str}, ordered by start_ts.

    Within a window, a description is dropped if it's a near-duplicate (by text
    similarity, not exact match) of one already kept - DAM rephrases repeated
    detections of the same tracked entity across consecutive frames slightly
    differently each time, so exact-string dedup alone barely helps.
    """
    if not descriptions:
        return []

    windows: dict[int, list[str]] = {}
    for item in descriptions:
        window_index = int(item["timestamp"] // window_seconds)
        bucket = windows.setdefault(window_index, [])
        if not any(_is_near_duplicate(item["description"], kept) for kept in bucket):
            bucket.append(item["description"])

    segments = []
    for window_index in sorted(windows):
        start_ts = window_index * window_seconds
        segments.append(
            {
                "start_ts": start_ts,
                "end_ts": start_ts + window_seconds,
                "description": " ".join(windows[window_index]),
            }
        )
    return segments
