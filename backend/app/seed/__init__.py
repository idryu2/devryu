"""시드 실행: 스키마 초기화 → 약물/환자 → 가이드라인 인덱싱. 멱등."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models import (
    Allergy,
    Condition,
    Drug,
    LabResult,
    Patient,
    PatientMedication,
)
from app.rag.pipeline import index_guidelines
from app.seed.data import DRUGS, PATIENTS


def _seed_drugs(db: Session) -> int:
    if db.scalar(select(Drug).limit(1)) is not None:
        return 0
    db.add_all([Drug(**d) for d in DRUGS])
    db.commit()
    return len(DRUGS)


def _seed_patients(db: Session) -> int:
    if db.scalar(select(Patient).limit(1)) is not None:
        return 0
    for p in PATIENTS:
        patient = Patient(
            id=p["id"], name=p["name"], age=p["age"], sex=p["sex"],
            weight_kg=p["weight_kg"], egfr=p["egfr"], creatinine=p["creatinine"],
            pregnant=p["pregnant"], encounter_type=p["encounter_type"],
            ward=p["ward"], bed=p["bed"],
        )
        patient.allergies = [Allergy(substance=s) for s in p["allergies"]]
        patient.conditions = [Condition(code=c, display=d) for c, d in p["conditions"]]
        patient.labs = [
            LabResult(code=code, display=disp, value=val, unit=unit,
                      abnormal=abn, ref_low=lo, ref_high=hi)
            for code, disp, val, unit, abn, lo, hi in p["labs"]
        ]
        patient.medications = [PatientMedication(drug_code=m) for m in p["medications"]]
        db.add(patient)
    db.commit()
    return len(PATIENTS)


def run() -> None:
    init_db()
    db = SessionLocal()
    try:
        n_drugs = _seed_drugs(db)
        n_patients = _seed_patients(db)
        n_chunks = index_guidelines(db)
        print(f"[seed] drugs+={n_drugs} patients+={n_patients} guideline_chunks+={n_chunks}")
    finally:
        db.close()
