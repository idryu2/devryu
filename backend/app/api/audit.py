from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import AuditLog
from app.schemas.audit import AuditOut

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=list[AuditOut])
def list_audit(limit: int = 100, db: Session = Depends(get_db)) -> list[AuditLog]:
    return list(
        db.scalars(select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)).all()
    )
