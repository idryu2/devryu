"""DB 모델 → 엔진 도메인 변환 + 평가 오케스트레이션.

엔진 자체는 순수하다. 이 레이어가 DB에서 데이터를 읽어 도메인 객체로 변환한 뒤
엔진을 호출하고, 결과를 API 스키마 형태(dict)로 돌려준다.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.cdss.domain import (
    Alert,
    AlertSeverity,
    EngineDrug,
    EngineOrder,
    EnginePatient,
)
from app.cdss.engine import RuleEngine
from app.cdss.loader import get_ruleset
from app.models import Drug, Patient


def _to_engine_drug(drug: Drug) -> EngineDrug:
    return EngineDrug(
        code=drug.code,
        name=drug.name,
        ingredient=drug.ingredient,
        drug_class=drug.drug_class,
        flags=tuple(drug.flags or ()),
        renal_adjust=drug.renal_adjust,
        pregnancy_category=drug.pregnancy_category,
        beers=drug.beers,
    )


def _drug_map(db: Session, codes: set[str]) -> dict[str, Drug]:
    if not codes:
        return {}
    rows = db.scalars(select(Drug).where(Drug.code.in_(codes))).all()
    return {d.code: d for d in rows}


def build_engine_patient(db: Session, patient: Patient) -> EnginePatient:
    med_codes = {m.drug_code for m in patient.medications}
    drugs = _drug_map(db, med_codes)
    current = tuple(
        _to_engine_drug(drugs[m.drug_code])
        for m in patient.medications
        if m.drug_code in drugs
    )
    return EnginePatient(
        id=patient.id,
        age=patient.age,
        sex=patient.sex,
        weight_kg=patient.weight_kg,
        egfr=patient.egfr,
        pregnant=patient.pregnant,
        allergies=tuple(a.substance for a in patient.allergies),
        conditions=tuple(c.code for c in patient.conditions),
        labs={lab.code: lab.value for lab in patient.labs},
        current_meds=current,
    )


def evaluate(db: Session, patient: Patient, orders: list[dict]) -> list[Alert]:
    """orders: [{"drug_code","dose","route"}]. 미존재 약물 코드는 무시한다."""
    eng_patient = build_engine_patient(db, patient)
    codes = {o["drug_code"] for o in orders}
    drugs = _drug_map(db, codes)
    eng_orders = [
        EngineOrder(drug=_to_engine_drug(drugs[o["drug_code"]]), dose=o.get("dose"), route=o.get("route"))
        for o in orders
        if o["drug_code"] in drugs
    ]
    engine = RuleEngine(get_ruleset())
    return engine.evaluate(eng_patient, eng_orders)


def alert_to_dict(alert: Alert) -> dict:
    return {
        "severity": alert.severity.label,
        "category": alert.category,
        "title": alert.title,
        "description": alert.description,
        "recommendation": alert.recommendation,
        "evidence": alert.evidence,
        "related_drugs": list(alert.related_drugs),
    }


def severity_counts(alerts: list[Alert]) -> dict[str, int]:
    counts = {s.label: 0 for s in AlertSeverity}
    for a in alerts:
        counts[a.severity.label] += 1
    return counts
