"""약물 마스터.

규칙 엔진은 약물의 성분(ingredient)/계열(drug_class)/플래그를 키로 상호작용·금기를
판단한다. flags 예: bleeding_risk, qt_prolong, enzyme_inhibitor, hyperkalemia,
nephrotoxic, serotonergic.
"""
from __future__ import annotations

from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Drug(Base):
    __tablename__ = "drugs"

    code: Mapped[str] = mapped_column(String, primary_key=True)  # 예: "warfarin"
    name: Mapped[str] = mapped_column(String)  # 표시명 (예: "와파린")
    ingredient: Mapped[str] = mapped_column(String)  # 성분명 (중복 판단 키)
    drug_class: Mapped[str] = mapped_column(String)  # 계열 (예: "anticoagulant")
    atc: Mapped[str | None] = mapped_column(String, nullable=True)

    default_dose: Mapped[str | None] = mapped_column(String, nullable=True)
    route: Mapped[str | None] = mapped_column(String, nullable=True)  # PO|IV|...

    renal_adjust: Mapped[bool] = mapped_column(Boolean, default=False)
    pregnancy_category: Mapped[str | None] = mapped_column(String, nullable=True)  # A|B|C|D|X
    beers: Mapped[bool] = mapped_column(Boolean, default=False)  # 고령자 주의(Beers)

    # 상호작용/금기 판단용 속성 플래그
    flags: Mapped[list[str]] = mapped_column(JSON, default=list)
