from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from app.chat.answer import build_answer
from app.chat.retrieval import retrieve_segments
from app.core.config import get_settings
from app.core.llm import chat_complete, embed_text, get_client
from app.db.repository import PostgresRepository
from app.db.session import get_session

router = APIRouter()


def get_repo():
    session = get_session()
    try:
        yield PostgresRepository(session)
    finally:
        session.close()


def get_embed_fn():
    client = get_client()
    return lambda text: embed_text(text, client=client)


def get_chat_fn():
    client = get_client()
    return lambda messages: chat_complete(messages, client=client)


class VideoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    filename: str
    duration_seconds: int


class ChatRequest(BaseModel):
    question: str


class Citation(BaseModel):
    start_ts: float
    end_ts: float


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]


@router.get("/videos", response_model=list[VideoOut])
def list_videos(repo=Depends(get_repo)):
    return repo.list_videos()


@router.post("/videos/{video_id}/chat", response_model=ChatResponse)
def chat(
    video_id: str,
    payload: ChatRequest,
    repo=Depends(get_repo),
    embed_fn=Depends(get_embed_fn),
    chat_fn=Depends(get_chat_fn),
):
    video = repo.get_video(video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    settings = get_settings()
    segments = retrieve_segments(
        video_id,
        payload.question,
        repo=repo,
        embed_fn=embed_fn,
        k=settings.retrieval_top_k,
        similarity_threshold=settings.retrieval_similarity_threshold,
    )
    return build_answer(payload.question, segments, chat_fn=chat_fn)
