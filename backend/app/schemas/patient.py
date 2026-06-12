from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class AllergyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    substance: str
    reaction: str | None = None
    severity: str | None = None


class ConditionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    display: str


class LabOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    display: str
    value: float
    unit: str | None = None
    abnormal: bool
    ref_low: float | None = None
    ref_high: float | None = None


class MedicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    drug_code: str
    dose: str | None = None


class PatientSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    age: int
    sex: str
    encounter_type: str
    ward: str | None = None
    bed: str | None = None


class PatientDetail(PatientSummary):
    weight_kg: float
    egfr: float | None = None
    creatinine: float | None = None
    pregnant: bool
    allergies: list[AllergyOut] = []
    conditions: list[ConditionOut] = []
    labs: list[LabOut] = []
    medications: list[MedicationOut] = []
