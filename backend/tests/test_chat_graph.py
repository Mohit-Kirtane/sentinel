from app.chat.answer import NO_MATCH_ANSWER
from app.chat.graph import build_chat_graph
from app.db.models import Segment

from .fakes import FakeRepository


def test_graph_retrieves_then_generates_when_a_match_is_found():
    repo = FakeRepository()
    repo.segments.append(
        Segment(
            id="seg-1",
            video_id="vid-1",
            start_ts=10.0,
            end_ts=20.0,
            description="a person leaves a backpack near the counter",
            embedding=[1.0, 0.0],
        )
    )

    def fake_embed(text):
        return [1.0, 0.0]

    def fake_chat(messages):
        assert "backpack" in messages[0]["content"]
        return "Someone left a backpack around 10-20s."

    graph = build_chat_graph(repo, fake_embed, fake_chat, k=5, similarity_threshold=0.3)
    result = graph.invoke({"video_id": "vid-1", "question": "did anyone leave a bag?"})

    assert result["answer"] == "Someone left a backpack around 10-20s."
    assert result["citations"] == [{"start_ts": 10.0, "end_ts": 20.0}]


def test_graph_routes_to_no_match_without_calling_the_llm_when_nothing_matches():
    repo = FakeRepository()

    def fake_embed(text):
        return [1.0, 0.0]

    def fake_chat(messages):
        raise AssertionError("chat_fn should not be called when there are no segments")

    graph = build_chat_graph(repo, fake_embed, fake_chat, k=5, similarity_threshold=0.3)
    result = graph.invoke({"video_id": "vid-1", "question": "did anyone leave a bag?"})

    assert result["answer"] == NO_MATCH_ANSWER
    assert result["citations"] == []
