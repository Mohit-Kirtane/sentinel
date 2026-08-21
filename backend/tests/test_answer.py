from app.chat.answer import build_answer
from app.db.models import Segment


def test_build_answer_with_no_segments_says_nothing_matches():
    result = build_answer("did anyone leave a bag?", segments=[], chat_fn=lambda messages: "should not be called")

    assert result["citations"] == []
    assert "nothing" in result["answer"].lower()


def test_build_answer_cites_the_retrieved_segments():
    segments = [
        Segment(id="seg-1", video_id="vid-1", start_ts=10.0, end_ts=20.0, description="a person leaves a backpack", embedding=[0.1]),
    ]

    def fake_chat(messages):
        content = messages[0]["content"]
        assert "a person leaves a backpack" in content
        assert "10.0" in content and "20.0" in content
        return "Someone left a backpack near the counter around 10-20s."

    result = build_answer("did anyone leave a bag?", segments=segments, chat_fn=fake_chat)

    assert result["answer"] == "Someone left a backpack near the counter around 10-20s."
    assert result["citations"] == [{"start_ts": 10.0, "end_ts": 20.0}]
