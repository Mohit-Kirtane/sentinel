from app.chat.retrieval import retrieve_segments
from app.db.models import Segment

from .fakes import FakeRepository


def test_retrieve_segments_embeds_the_question_and_asks_the_repo_for_top_k():
    repo = FakeRepository()
    repo.segments.append(
        Segment(id="seg-1", video_id="vid-1", start_ts=0, end_ts=10, description="a person walks in", embedding=[1.0, 0.0])
    )
    repo.segments.append(
        Segment(id="seg-2", video_id="vid-1", start_ts=10, end_ts=20, description="a car drives by", embedding=[0.0, 1.0])
    )

    def fake_embed(text):
        assert text == "did anyone walk in?"
        return [1.0, 0.0]

    results = retrieve_segments("vid-1", "did anyone walk in?", repo=repo, embed_fn=fake_embed, k=1)

    assert len(results) == 1
    assert results[0].description == "a person walks in"


def test_retrieve_segments_filters_out_weak_matches_below_the_threshold():
    repo = FakeRepository()
    repo.segments.append(
        Segment(id="seg-1", video_id="vid-1", start_ts=0, end_ts=10, description="unrelated content", embedding=[0.0, 1.0])
    )

    def fake_embed(text):
        return [1.0, 0.0]  # orthogonal to the stored segment -> similarity 0.0

    results = retrieve_segments(
        "vid-1", "did anyone walk in?", repo=repo, embed_fn=fake_embed, k=5, similarity_threshold=0.3
    )

    assert results == []
