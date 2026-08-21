def build_segments(descriptions: list[dict], window_seconds: float = 10.0) -> list[dict]:
    """Merge per-frame region descriptions into fixed-width time-window segments.

    descriptions: list of {"timestamp": float, "region_label": str, "description": str}
    returns: list of {"start_ts": float, "end_ts": float, "description": str}, ordered by start_ts.
    """
    if not descriptions:
        return []

    windows: dict[int, list[str]] = {}
    for item in descriptions:
        window_index = int(item["timestamp"] // window_seconds)
        bucket = windows.setdefault(window_index, [])
        if item["description"] not in bucket:
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
