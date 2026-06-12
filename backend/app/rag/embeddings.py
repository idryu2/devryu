"""임베딩 공급자: Mock(결정론적 로컬) / OpenAI.

키가 없으면 결정론적 해시 기반 임베딩으로 폴백한다. 검색 품질은 낮지만 키 없이도
RAG 파이프라인 전체가 동작한다(데모 요구사항).
"""
from __future__ import annotations

import hashlib
import math
from functools import lru_cache

import httpx

from app.config import get_settings


class MockEmbedder:
    """단어 단위 해시를 버킷에 누적해 결정론적 임베딩 생성(가벼운 bag-of-words 근사)."""

    name = "mock"

    def __init__(self, dim: int):
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            vec = [0.0] * self.dim
            for token in _tokenize(text):
                h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
                vec[h % self.dim] += 1.0
            vectors.append(_normalize(vec))
        return vectors


class OpenAIEmbedder:
    name = "openai"

    def __init__(self, api_key: str, dim: int):
        self.api_key = api_key
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:  # pragma: no cover - 네트워크
        resp = httpx.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": "text-embedding-3-small", "input": texts, "dimensions": self.dim},
            timeout=30,
        )
        resp.raise_for_status()
        return [item["embedding"] for item in resp.json()["data"]]


def _tokenize(text: str) -> list[str]:
    # 한글/영문 혼용: 공백 분리 + 2글자 슬라이딩(부분 일치 강화)
    raw = text.lower().replace("\n", " ").split()
    tokens = list(raw)
    for word in raw:
        tokens += [word[i : i + 2] for i in range(max(len(word) - 1, 1))]
    return tokens


def _normalize(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


@lru_cache
def get_embedder():
    s = get_settings()
    if s.effective_embedding_provider == "openai":
        return OpenAIEmbedder(s.openai_api_key, s.embedding_dim)
    return MockEmbedder(s.embedding_dim)


def embed_texts(texts: list[str]) -> list[list[float]]:
    return get_embedder().embed(texts)
