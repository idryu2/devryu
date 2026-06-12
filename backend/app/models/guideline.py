"""RAG용 가이드라인 청크 + pgvector 임베딩."""
from __future__ import annotations

from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.config import get_settings
from app.db.base import Base

_dim = get_settings().embedding_dim


class GuidelineChunk(Base):
    __tablename__ = "guideline_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    doc_title: Mapped[str] = mapped_column(String)  # 문서명 (출처 표시)
    section: Mapped[str] = mapped_column(String)  # 섹션명 (출처 표시)
    source_label: Mapped[str] = mapped_column(String)  # 인용 라벨
    text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(_dim))
