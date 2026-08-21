import pytest

from app.db.models import Segment, Video

pytestmark = pytest.mark.asyncio


async def test_list_videos_returns_the_precomputed_set(api_client, fake_repo):
    fake_repo.insert_video(Video(id="vid-1", title="Lobby Camera", filename="lobby.mp4", duration_seconds=60))

    res = await api_client.get("/api/videos")

    assert res.status_code == 200
    assert res.json() == [
        {"id": "vid-1", "title": "Lobby Camera", "filename": "lobby.mp4", "duration_seconds": 60}
    ]


async def test_chat_on_unknown_video_returns_404(api_client):
    res = await api_client.post("/api/videos/does-not-exist/chat", json={"question": "what happened?"})

    assert res.status_code == 404


async def test_chat_returns_an_answer_with_citations(api_client, fake_repo):
    fake_repo.insert_video(Video(id="vid-1", title="Lobby Camera", filename="lobby.mp4", duration_seconds=60))
    fake_repo.insert_segments(
        [
            Segment(
                id="seg-1",
                video_id="vid-1",
                start_ts=10.0,
                end_ts=20.0,
                description="a person leaves a backpack near the counter",
                embedding=[1.0, 0.0],
            )
        ]
    )

    res = await api_client.post("/api/videos/vid-1/chat", json={"question": "did anyone leave a bag?"})

    assert res.status_code == 200
    body = res.json()
    assert body["answer"] == "stub answer"
    assert body["citations"] == [{"start_ts": 10.0, "end_ts": 20.0}]
