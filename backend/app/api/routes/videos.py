from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from app.auth.dependencies import get_current_user
from app.chat.graph import build_chat_graph
from app.core.config import get_settings
from app.core.llm import chat_complete, embed_text
from app.db.repository import PostgresRepository
from app.db.session import get_session

router = APIRouter(dependencies=[Depends(get_current_user)])


def get_repo():
    session = get_session()
    try:
        yield PostgresRepository(session)
    finally:
        session.close()


def get_embed_fn():
    return embed_text


def get_chat_fn():
    return chat_complete


def get_chat_graph(
    repo=Depends(get_repo),
    embed_fn=Depends(get_embed_fn),
    chat_fn=Depends(get_chat_fn),
):
    settings = get_settings()
    return build_chat_graph(
        repo,
        embed_fn,
        chat_fn,
        k=settings.retrieval_top_k,
        similarity_threshold=settings.retrieval_similarity_threshold,
    )


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
    graph=Depends(get_chat_graph),
):
    video = repo.get_video(video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    result = graph.invoke({"video_id": video_id, "question": payload.question})
    return {"answer": result["answer"], "citations": result["citations"]}
