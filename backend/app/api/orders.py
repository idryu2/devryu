from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.cdss import service
from app.db import get_db
from app.models import AuditLog, Patient
from app.schemas.order import SignRequest, SignResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/sign", response_model=SignResponse)
def sign(req: SignRequest, db: Session = Depends(get_db)) -> SignResponse:
    """처방 서명. CRITICAL 경고가 있으면 override 사유 없이는 서명 차단(Human-in-the-loop).

    서명/override는 모두 감사 로그에 기록한다.
    """
    patient = db.get(Patient, req.patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="환자를 찾을 수 없습니다.")

    # 서버 측 재평가: 클라이언트 신뢰 대신 동일 엔진으로 다시 판단(안전).
    alerts = service.evaluate(db, patient, [o.model_dump() for o in req.orders])
    has_critical = any(a.severity.label == "CRITICAL" for a in alerts)
    overridden = False

    if has_critical:
        if not (req.override_reason and req.override_reason.strip()):
            raise HTTPException(
                status_code=400,
                detail="CRITICAL 경고가 있어 override 사유 없이는 서명할 수 없습니다.",
            )
        overridden = True

    log = AuditLog(
        patient_id=req.patient_id,
        actor=req.actor,
        action="override" if overridden else "sign",
        detail={
            "orders": [o.model_dump() for o in req.orders],
            "override_reason": req.override_reason,
            "alerts": [service.alert_to_dict(a) for a in alerts],
            "acknowledged_alerts": [a.model_dump() for a in req.acknowledged_alerts],
        },
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    msg = "override 사유와 함께 서명되었습니다." if overridden else "처방이 서명되었습니다."
    return SignResponse(signed=True, audit_id=log.id, overridden=overridden, message=msg)
