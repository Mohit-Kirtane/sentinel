import math

from app.db.models import Segment, Video


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class FakeRepository:
    """In-memory stand-in for PostgresRepository, used in unit tests.

    pgvector's similarity search has no SQLite equivalent, so tests exercise
    this brute-force implementation instead of a real database.
    """

    def __init__(self):
        self.videos: dict[str, Video] = {}
        self.segments: list[Segment] = []

    def list_videos(self) -> list[Video]:
        return list(self.videos.values())

    def get_video(self, video_id: str) -> Video | None:
        return self.videos.get(video_id)

    def top_k_similar(self, video_id: str, query_embedding: list[float], k: int) -> list[Segment]:
        candidates = [s for s in self.segments if s.video_id == video_id]
        candidates.sort(key=lambda s: _cosine_similarity(s.embedding, query_embedding), reverse=True)
        return candidates[:k]

    def insert_video(self, video: Video) -> None:
        self.videos[video.id] = video

    def insert_segments(self, segments: list[Segment]) -> None:
        self.segments.extend(segments)
