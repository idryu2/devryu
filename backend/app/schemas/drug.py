from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class DrugOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    name: str
    ingredient: str
    drug_class: str
    default_dose: str | None = None
    route: str | None = None
    renal_adjust: bool = False
    pregnancy_category: str | None = None
    beers: bool = False
    flags: list[str] = []
