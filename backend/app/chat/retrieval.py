import math

from app.db.models import Segment


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def retrieve_segments(
    video_id: str,
    question: str,
    repo,
    embed_fn,
    k: int = 5,
    similarity_threshold: float = 0.3,
) -> list[Segment]:
    query_embedding = embed_fn(question)
    candidates = repo.top_k_similar(video_id, query_embedding, k)
    return [
        segment
        for segment in candidates
        if _cosine_similarity(segment.embedding, query_embedding) >= similarity_threshold
    ]
