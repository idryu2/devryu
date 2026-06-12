"""RAG 파이프라인: 가이드라인 인덱싱 + 질의응답.

인덱싱: 가이드라인 청크 → 임베딩 → pgvector 저장(출처 메타 포함).
질의: 질문 임베딩 → pgvector 코사인 검색 top-k → LLM에 근거 첨부 → 답변+출처.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.llm.base import DISCLAIMER
from app.llm.factory import get_llm_provider
from app.models.guideline import GuidelineChunk
from app.rag.embeddings import embed_texts


def index_guidelines(db: Session) -> int:
    """가이드라인을 청크로 인덱싱(멱등: 기존 데이터가 있으면 건너뜀)."""
    # 지연 import: app.seed 패키지와의 순환 import 방지
    from app.seed.guidelines import GUIDELINES

    existing = db.scalar(select(GuidelineChunk).limit(1))
    if existing is not None:
        return 0

    chunks: list[GuidelineChunk] = []
    texts: list[str] = []
    for doc_title, source_label, sections in GUIDELINES:
        for section, text in sections:
            texts.append(f"{section}. {text}")
            chunks.append(
                GuidelineChunk(
                    doc_title=doc_title,
                    section=section,
                    source_label=source_label,
                    text=text,
                )
            )
    embeddings = embed_texts(texts)
    for chunk, emb in zip(chunks, embeddings, strict=True):
        chunk.embedding = emb
    db.add_all(chunks)
    db.commit()
    return len(chunks)


def search_guidelines(db: Session, question: str, top_k: int = 3) -> list[dict]:
    """pgvector 코사인 거리 기반 top-k 검색."""
    q_emb = embed_texts([question])[0]
    rows = db.scalars(
        select(GuidelineChunk)
        .order_by(GuidelineChunk.embedding.cosine_distance(q_emb))
        .limit(top_k)
    ).all()
    return [
        {
            "doc_title": r.doc_title,
            "section": r.section,
            "source_label": r.source_label,
            "text": r.text,
        }
        for r in rows
    ]


def answer_guideline_question(db: Session, question: str, top_k: int = 3) -> dict:
    contexts = search_guidelines(db, question, top_k)
    answer = get_llm_provider().answer_question(question, contexts)
    return {
        "answer": answer,
        "sources": [
            {"doc_title": c["doc_title"], "section": c["section"], "source_label": c["source_label"]}
            for c in contexts
        ],
        "disclaimer": DISCLAIMER,
    }
