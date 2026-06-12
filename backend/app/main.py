"""FastAPI 진입점.

처방 CDSS 시연 백엔드. 모든 응답은 Pydantic 스키마로 타입 명시되며 OpenAPI 문서가
/docs에 자동 생성된다.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="처방 CDSS 시연 API",
    description="DEMO · 가상 데이터 · 실제 진료 사용 불가. "
    "환자 안전 판단은 결정론적 규칙 엔진으로만 수행하며 LLM은 보조 역할만 합니다.",
    version="0.1.0",
)

# 프론트엔드(Vite dev server) 접근 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 데모: 모든 origin 허용
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {
        "status": "ok",
        "env": settings.app_env,
        "llm_provider": settings.effective_llm_provider,
        "embedding_provider": settings.effective_embedding_provider,
        "banner": "DEMO · 가상 데이터 · 실제 진료 사용 불가",
    }
