"""규칙 엔진 단위 테스트 헬퍼 (도메인 빌더 + 자주 쓰는 약물 상수).

엔진은 순수 함수이므로 DB 없이 도메인 객체를 직접 구성해 검증한다.
실제 app/cdss/rules/*.json 규칙셋을 그대로 로드해 시드 데이터와 동일한 조건으로 본다.
"""
from __future__ import annotations

from app.cdss.domain import EngineDrug, EngineOrder, EnginePatient


# ── 약물 빌더 (시드 마스터의 핵심 속성과 일치) ─────────────────────────
def make_drug(
    code: str,
    *,
    ingredient: str | None = None,
    drug_class: str = "misc",
    flags: tuple[str, ...] = (),
    renal_adjust: bool = False,
    pregnancy_category: str | None = None,
    beers: bool = False,
) -> EngineDrug:
    return EngineDrug(
        code=code,
        name=code,
        ingredient=ingredient or code,
        drug_class=drug_class,
        flags=flags,
        renal_adjust=renal_adjust,
        pregnancy_category=pregnancy_category,
        beers=beers,
    )


# 자주 쓰는 약물들 (rule 토큰과 정합)
WARFARIN = make_drug("warfarin", drug_class="anticoagulant", flags=("bleeding_risk",))
APIXABAN = make_drug("apixaban", drug_class="anticoagulant", flags=("bleeding_risk", "doac"))
IBUPROFEN = make_drug("ibuprofen", drug_class="NSAID", flags=("bleeding_risk", "nephrotoxic"))
ASPIRIN = make_drug("aspirin", drug_class="antiplatelet", flags=("bleeding_risk",))
CLARITHROMYCIN = make_drug("clarithromycin", drug_class="macrolide", flags=("qt_prolong", "enzyme_inhibitor"))
LEVOFLOXACIN = make_drug("levofloxacin", drug_class="fluoroquinolone", flags=("qt_prolong",))
SIMVASTATIN = make_drug("simvastatin", drug_class="statin")
AMIODARONE = make_drug("amiodarone", drug_class="antiarrhythmic", flags=("qt_prolong", "enzyme_inhibitor"))
DIGOXIN = make_drug("digoxin", drug_class="cardiac_glycoside", renal_adjust=True)
RAMIPRIL = make_drug("ramipril", drug_class="ACEi", flags=("hyperkalemia",))
LOSARTAN = make_drug("losartan", drug_class="ARB", flags=("hyperkalemia",))
KCL = make_drug("kcl", ingredient="potassium_chloride", drug_class="electrolyte", flags=("hyperkalemia",))
SPIRONOLACTONE = make_drug("spironolactone", drug_class="potassium_sparing_diuretic", flags=("hyperkalemia",))
PROPRANOLOL = make_drug("propranolol", drug_class="beta_blocker_nonselective")
METOPROLOL = make_drug("metoprolol", drug_class="beta_blocker_selective")
METFORMIN = make_drug("metformin", drug_class="biguanide", renal_adjust=True)
AMOXICILLIN = make_drug("amoxicillin", drug_class="penicillin")
CEFTRIAXONE = make_drug("ceftriaxone", drug_class="cephalosporin")
LORAZEPAM = make_drug("lorazepam", drug_class="benzodiazepine")
TRAMADOL = make_drug("tramadol", drug_class="opioid", flags=("serotonergic",))
SERTRALINE = make_drug("sertraline", drug_class="SSRI", flags=("serotonergic",))
ATORVASTATIN = make_drug("atorvastatin", drug_class="statin")
ACETAMINOPHEN = make_drug("acetaminophen", drug_class="analgesic")


def patient(**kw) -> EnginePatient:
    base = dict(id="T", age=50, sex="M", weight_kg=70.0)
    base.update(kw)
    return EnginePatient(**base)


def order(drug: EngineDrug) -> EngineOrder:
    return EngineOrder(drug=drug)


def categories(alerts) -> set[str]:
    return {a.category for a in alerts}


def by_category(alerts, category: str):
    return [a for a in alerts if a.category == category]
