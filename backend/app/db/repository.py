from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Segment, Video


class VideoRepository(Protocol):
    def list_videos(self) -> list[Video]: ...
    def get_video(self, video_id: str) -> Video | None: ...


class SegmentRepository(Protocol):
    def top_k_similar(self, video_id: str, query_embedding: list[float], k: int) -> list[Segment]: ...
    def insert_video(self, video: Video) -> None: ...
    def insert_segments(self, segments: list[Segment]) -> None: ...


class PostgresRepository:
    """Real implementation, backed by a pgvector-enabled Postgres database.

    Exercised manually against a real Neon Postgres instance - unit tests use
    an in-memory fake implementing the same interface instead, since pgvector's
    similarity operators have no SQLite equivalent.
    """

    def __init__(self, session: Session):
        self.session = session

    def list_videos(self) -> list[Video]:
        return list(self.session.execute(select(Video)).scalars().all())

    def get_video(self, video_id: str) -> Video | None:
        return self.session.get(Video, video_id)

    def top_k_similar(self, video_id: str, query_embedding: list[float], k: int) -> list[Segment]:
        stmt = (
            select(Segment)
            .where(Segment.video_id == video_id)
            .order_by(Segment.embedding.cosine_distance(query_embedding))
            .limit(k)
        )
        return list(self.session.execute(stmt).scalars().all())

    def insert_video(self, video: Video) -> None:
        self.session.add(video)
        self.session.commit()

    def insert_segments(self, segments: list[Segment]) -> None:
        self.session.add_all(segments)
        self.session.commit()
