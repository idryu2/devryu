"""환경설정에 따라 LLM 공급자를 선택. 키가 없으면 MockProvider로 폴백."""
from __future__ import annotations

from functools import lru_cache

from app.config import get_settings
from app.llm.base import LLMProvider
from app.llm.providers import AnthropicProvider, MockProvider, OpenAIProvider


@lru_cache
def get_llm_provider() -> LLMProvider:
    s = get_settings()
    provider = s.effective_llm_provider  # 키 없으면 'mock'
    if provider == "anthropic":
        return AnthropicProvider(s.anthropic_api_key, s.anthropic_model)
    if provider == "openai":
        return OpenAIProvider(s.openai_api_key, s.openai_model)
    return MockProvider()
