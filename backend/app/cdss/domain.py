"""규칙 엔진의 순수 도메인 모델.

ORM/DB와 분리된 평범한 데이터 구조만 사용해 엔진을 결정론적·단위테스트 가능하게 한다.
API 레이어가 DB 행을 이 도메인 객체로 변환해 엔진에 넘긴다.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class AlertSeverity(IntEnum):
    """정렬을 위해 IntEnum 사용 (값이 작을수록 우선순위 높음)."""

    CRITICAL = 0
    WARNING = 1
    INFO = 2

    @property
    def label(self) -> str:
        return self.name


@dataclass(frozen=True)
class Alert:
    severity: AlertSeverity
    category: str  # drug_allergy | drug_drug | drug_disease | renal | duplicate | monitoring | geriatric | pregnancy
    title: str
    description: str
    recommendation: str
    evidence: str  # 근거/출처 (가이드라인·기준 등)
    related_drugs: tuple[str, ...] = ()


@dataclass(frozen=True)
class EngineDrug:
    code: str
    name: str
    ingredient: str
    drug_class: str
    flags: tuple[str, ...] = ()
    renal_adjust: bool = False
    pregnancy_category: str | None = None
    beers: bool = False

    def matches(self, token: str) -> bool:
        """token이 이 약물의 code/성분/계열/플래그 중 하나와 일치하는지."""
        return (
            token == self.code
            or token == self.ingredient
            or token == self.drug_class
            or token in self.flags
        )


@dataclass(frozen=True)
class EngineOrder:
    drug: EngineDrug
    dose: str | None = None
    route: str | None = None


@dataclass
class EnginePatient:
    id: str
    age: int
    sex: str
    weight_kg: float
    egfr: float | None = None
    pregnant: bool = False
    allergies: tuple[str, ...] = ()  # 성분/계열명
    conditions: tuple[str, ...] = ()  # condition code
    labs: dict[str, float] = field(default_factory=dict)  # code -> value
    current_meds: tuple[EngineDrug, ...] = ()
