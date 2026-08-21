from openai import OpenAI

from app.core.config import get_settings


def get_client() -> OpenAI:
    settings = get_settings()
    return OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)


def embed_text(text: str, client: OpenAI | None = None, model: str | None = None) -> list[float]:
    client = client or get_client()
    settings = get_settings()
    model = model or settings.llm_embedding_model
    response = client.embeddings.create(
        model=model, input=text, dimensions=settings.llm_embedding_dimensions
    )
    return response.data[0].embedding


def chat_complete(messages: list[dict], client: OpenAI | None = None, model: str | None = None) -> str:
    client = client or get_client()
    model = model or get_settings().llm_chat_model
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    return response.choices[0].message.content
