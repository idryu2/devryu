"""임상 데이터 모델 (HL7 FHIR 리소스 구조 참고).

Patient ← Patient, Allergy ← AllergyIntolerance, Condition ← Condition,
LabResult ← Observation, PatientMedication ← MedicationStatement.
"""
from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # 예: "P001"
    name: Mapped[str] = mapped_column(String)  # 가상 이름
    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[str] = mapped_column(String)  # M | F
    weight_kg: Mapped[float] = mapped_column(Float)

    # 신기능 (renal dosing 판단에 사용)
    egfr: Mapped[float | None] = mapped_column(Float, nullable=True)  # mL/min/1.73m^2
    creatinine: Mapped[float | None] = mapped_column(Float, nullable=True)  # mg/dL

    pregnant: Mapped[bool] = mapped_column(Boolean, default=False)

    encounter_type: Mapped[str] = mapped_column(String)  # inpatient | outpatient
    ward: Mapped[str | None] = mapped_column(String, nullable=True)
    bed: Mapped[str | None] = mapped_column(String, nullable=True)

    allergies: Mapped[list[Allergy]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    conditions: Mapped[list[Condition]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    labs: Mapped[list[LabResult]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    medications: Mapped[list[PatientMedication]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )


class Allergy(Base):
    __tablename__ = "allergies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[str] = mapped_column(ForeignKey("patients.id"))
    # 성분명 또는 약물 계열명 (예: "penicillin", "NSAID", "sulfonamide")
    substance: Mapped[str] = mapped_column(String)
    reaction: Mapped[str | None] = mapped_column(String, nullable=True)
    severity: Mapped[str | None] = mapped_column(String, nullable=True)  # mild|moderate|severe

    patient: Mapped[Patient] = relationship(back_populates="allergies")


class Condition(Base):
    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[str] = mapped_column(ForeignKey("patients.id"))
    code: Mapped[str] = mapped_column(String)  # 내부 코드 (예: "asthma", "ckd", "afib")
    display: Mapped[str] = mapped_column(String)  # 표시명 (예: "천식")

    patient: Mapped[Patient] = relationship(back_populates="conditions")


class LabResult(Base):
    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[str] = mapped_column(ForeignKey("patients.id"))
    code: Mapped[str] = mapped_column(String)  # 예: "K", "INR", "ALT", "eGFR"
    display: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str | None] = mapped_column(String, nullable=True)
    abnormal: Mapped[bool] = mapped_column(Boolean, default=False)
    ref_low: Mapped[float | None] = mapped_column(Float, nullable=True)
    ref_high: Mapped[float | None] = mapped_column(Float, nullable=True)

    patient: Mapped[Patient] = relationship(back_populates="labs")


class PatientMedication(Base):
    """현재 복용약 (처방 평가 시 상호작용/중복 판단의 한 축)."""

    __tablename__ = "patient_medications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[str] = mapped_column(ForeignKey("patients.id"))
    drug_code: Mapped[str] = mapped_column(ForeignKey("drugs.code"))
    dose: Mapped[str | None] = mapped_column(String, nullable=True)

    patient: Mapped[Patient] = relationship(back_populates="medications")
