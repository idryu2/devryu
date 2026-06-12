"""JSON 규칙셋 로더.

규칙은 코드가 아닌 app/cdss/rules/*.json에 정의한다. 새 약물/상호작용 추가는
JSON 편집만으로 가능해야 한다(엔진 로직은 카테고리별 평가 절차만 보유).
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

RULES_DIR = Path(__file__).parent / "rules"

# 카테고리 → 파일명
_RULE_FILES = {
    "drug_allergy": "drug_allergy.json",
    "drug_drug": "ddi.json",
    "drug_disease": "drug_disease.json",
    "renal": "renal.json",
    "monitoring": "drug_lab_monitoring.json",
    "geriatric": "geriatric_beers.json",
    "pregnancy": "pregnancy.json",
}


def load_ruleset(rules_dir: Path | None = None) -> dict:
    """카테고리별 규칙 dict 반환. 테스트에서 임의 디렉터리 주입 가능."""
    base = rules_dir or RULES_DIR
    ruleset: dict = {}
    for category, filename in _RULE_FILES.items():
        path = base / filename
        with path.open(encoding="utf-8") as f:
            ruleset[category] = json.load(f)
    return ruleset


@lru_cache
def get_ruleset() -> dict:
    """기본 규칙셋(캐시). API 런타임에서 사용."""
    return load_ruleset()
