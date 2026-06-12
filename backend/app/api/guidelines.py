from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.rag.pipeline import answer_guideline_question
from app.schemas.guideline import AskRequest, AskResponse

router = APIRouter(prefix="/guidelines", tags=["guidelines"])


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest, db: Session = Depends(get_db)) -> AskResponse:
    """RAG Q&A: pgvector 검색 + LLM 답변 + 출처 표시(참고용)."""
    result = answer_guideline_question(db, req.question, req.top_k)
    return AskResponse(**result)
