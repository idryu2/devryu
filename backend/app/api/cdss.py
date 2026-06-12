from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.cdss import service
from app.db import get_db
from app.llm.base import DISCLAIMER
from app.llm.factory import get_llm_provider
from app.models import Patient
from app.schemas.cdss import (
    EvaluateRequest,
    EvaluateResponse,
    ExplainRequest,
    ExplainResponse,
)

router = APIRouter(prefix="/cdss", tags=["cdss"])


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest, db: Session = Depends(get_db)) -> EvaluateResponse:
    """★ 핵심: 결정론적 규칙 엔진으로 처방을 평가해 경고 배열 반환. LLM 미사용."""
    patient = db.get(Patient, req.patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="환자를 찾을 수 없습니다.")
    alerts = service.evaluate(db, patient, [o.model_dump() for o in req.orders])
    counts = service.severity_counts(alerts)
    return EvaluateResponse(
        patient_id=req.patient_id,
        alerts=[service.alert_to_dict(a) for a in alerts],
        counts=counts,
        has_critical=counts.get("CRITICAL", 0) > 0,
    )


@router.post("/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest, db: Session = Depends(get_db)) -> ExplainResponse:
    """경고를 LLM으로 자연어 설명(보조 기능). 키 없으면 mock."""
    patient = db.get(Patient, req.patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="환자를 찾을 수 없습니다.")
    patient_ctx = {"name": patient.name, "age": patient.age, "egfr": patient.egfr}
    explanation = get_llm_provider().explain_alert(req.alert.model_dump(), patient_ctx)
    return ExplainResponse(explanation=explanation, disclaimer=DISCLAIMER)
