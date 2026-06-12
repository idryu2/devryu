from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.cdss import AlertOut, OrderIn


class SignRequest(BaseModel):
    patient_id: str
    orders: list[OrderIn] = Field(default_factory=list)
    # CRITICAL 경고가 있을 때 서명하려면 사유가 필수(서버에서 검증)
    override_reason: str | None = None
    acknowledged_alerts: list[AlertOut] = Field(default_factory=list)
    actor: str = "demo-prescriber"


class SignResponse(BaseModel):
    signed: bool
    audit_id: int
    overridden: bool
    message: str
