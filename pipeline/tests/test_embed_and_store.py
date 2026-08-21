from app.db.models import Segment, Video

from pipeline.embed_and_store import embed_segments, store_video_and_segments


class _FakeRepository:
    def __init__(self):
        self.videos: dict[str, Video] = {}
        self.segments: list[Segment] = []

    def get_video(self, video_id):
        return self.videos.get(video_id)

    def top_k_similar(self, video_id, query_embedding, k):
        return [s for s in self.segments if s.video_id == video_id][:k]

    def insert_video(self, video):
        self.videos[video.id] = video

    def insert_segments(self, segments):
        self.segments.extend(segments)


def test_embed_segments_adds_an_embedding_to_each_segment():
    segments = [
        {"start_ts": 0.0, "end_ts": 10.0, "description": "a person walks in"},
        {"start_ts": 10.0, "end_ts": 20.0, "description": "a person leaves a bag"},
    ]

    def fake_embed(text):
        return [float(len(text))]

    result = embed_segments(segments, embed_fn=fake_embed)

    assert result[0]["embedding"] == [float(len("a person walks in"))]
    assert result[1]["embedding"] == [float(len("a person leaves a bag"))]
    assert result[0]["description"] == "a person walks in"


def test_store_video_and_segments_writes_to_the_repository():
    repo = _FakeRepository()
    segments_with_embeddings = [
        {"start_ts": 0.0, "end_ts": 10.0, "description": "a person walks in", "embedding": [0.1, 0.2]},
    ]

    store_video_and_segments(
        video_id="vid-1",
        title="Lobby Camera",
        filename="lobby.mp4",
        duration_seconds=60,
        segments_with_embeddings=segments_with_embeddings,
        repo=repo,
    )

    assert repo.get_video("vid-1").title == "Lobby Camera"
    stored = repo.top_k_similar("vid-1", [0.1, 0.2], k=5)
    assert len(stored) == 1
    assert stored[0].description == "a person walks in"
