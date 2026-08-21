from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

from app.core.config import get_settings


@lru_cache
def get_chat_model() -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=settings.llm_chat_model,
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        temperature=0.2,
    )


@lru_cache
def get_embeddings_model() -> HuggingFaceEmbeddings:
    settings = get_settings()
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )


def embed_text(text: str, embeddings: HuggingFaceEmbeddings | None = None) -> list[float]:
    embeddings = embeddings or get_embeddings_model()
    return embeddings.embed_query(text)


def chat_complete(messages: list[dict], llm: ChatOpenAI | None = None) -> str:
    llm = llm or get_chat_model()
    response = llm.invoke([(m["role"], m["content"]) for m in messages])
    return response.content
