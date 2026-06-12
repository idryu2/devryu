from __future__ import annotations

from pydantic import BaseModel, Field


class OrderIn(BaseModel):
    drug_code: str
    dose: str | None = None
    route: str | None = None


class EvaluateRequest(BaseModel):
    patient_id: str
    orders: list[OrderIn] = Field(default_factory=list)


class AlertOut(BaseModel):
    severity: str  # CRITICAL | WARNING | INFO
    category: str
    title: str
    description: str
    recommendation: str
    evidence: str
    related_drugs: list[str] = []


class EvaluateResponse(BaseModel):
    patient_id: str
    alerts: list[AlertOut]
    counts: dict[str, int]  # 등급별 개수 (경고 피로 분석용)
    has_critical: bool


class ExplainRequest(BaseModel):
    patient_id: str
    alert: AlertOut


class ExplainResponse(BaseModel):
    explanation: str
    disclaimer: str
