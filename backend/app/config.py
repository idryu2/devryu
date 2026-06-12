"""애플리케이션 설정 (환경변수 → Pydantic Settings).

키가 비어 있으면 LLM/임베딩이 자동으로 mock으로 폴백하도록 effective_* 속성을 둔다.
이 폴백 덕분에 API 키 없이도 전체 데모가 동작한다(핵심 요구사항).
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "demo"

    # Database
    database_url: str = "postgresql+psycopg://cdss:cdss@localhost:5432/cdss"

    # LLM
    llm_provider: str = "mock"  # anthropic | openai | mock
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Embeddings
    embedding_provider: str = "mock"  # openai | mock
    embedding_dim: int = 1536

    @property
    def effective_llm_provider(self) -> str:
        """키가 없으면 무조건 mock으로 폴백한다."""
        if self.llm_provider == "anthropic" and self.anthropic_api_key:
            return "anthropic"
        if self.llm_provider == "openai" and self.openai_api_key:
            return "openai"
        return "mock"

    @property
    def effective_embedding_provider(self) -> str:
        if self.embedding_provider == "openai" and self.openai_api_key:
            return "openai"
        return "mock"


@lru_cache
def get_settings() -> Settings:
    return Settings()
