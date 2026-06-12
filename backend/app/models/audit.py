"""감사 로그 (CDSS 거버넌스): 서명/override/경고확인 이력."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    patient_id: Mapped[str | None] = mapped_column(String, nullable=True)
    actor: Mapped[str] = mapped_column(String, default="demo-prescriber")
    action: Mapped[str] = mapped_column(String)  # sign | override | ack

    # 처방 내역, override 사유, 확인한 경고 등 구조화 상세
    detail: Mapped[dict] = mapped_column(JSON, default=dict)
