from __future__ import annotations

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


class SourceOut(BaseModel):
    doc_title: str
    section: str
    source_label: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceOut]
    disclaimer: str
