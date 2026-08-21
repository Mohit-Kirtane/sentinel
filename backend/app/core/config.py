from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Sentinel"
    cors_origins: list[str] = ["*"]

    database_url: str = "postgresql://localhost:5432/sentinel"

    llm_api_key: str = ""
    llm_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    llm_chat_model: str = "gemini-3.6-flash"

    # Local, free, CPU-friendly embedding model - avoids depending on the
    # LLM provider's embedding endpoint (and its own rate limits/pricing) for
    # every stored segment and every query. Same choice Dossier made.
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    retrieval_top_k: int = 5
    retrieval_similarity_threshold: float = 0.3

    jwt_secret: str = "dev-secret-change-me-in-production"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days
    cookie_secure: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
