"""약물-약물 상호작용(DDI): 양성/음성."""
from helpers import (
    ACETAMINOPHEN,
    AMIODARONE,
    APIXABAN,
    ASPIRIN,
    CLARITHROMYCIN,
    DIGOXIN,
    IBUPROFEN,
    KCL,
    LEVOFLOXACIN,
    LOSARTAN,
    METOPROLOL,
    RAMIPRIL,
    SERTRALINE,
    SIMVASTATIN,
    SPIRONOLACTONE,
    TRAMADOL,
    WARFARIN,
    by_category,
    order,
    patient,
)


def test_warfarin_nsaid_bleeding(engine):
    """대표 케이스: 와파린 + NSAID → CRITICAL 출혈 경고."""
    alerts = by_category(engine.evaluate(patient(), [order(WARFARIN), order(IBUPROFEN)]), "drug_drug")
    assert any(a.severity.label == "CRITICAL" for a in alerts)


def test_warfarin_with_existing_med_triggers(engine):
    """기존 복용 와파린 + 신규 NSAID 처방도 감지."""
    p = patient(current_meds=(WARFARIN,))
    alerts = by_category(engine.evaluate(p, [order(IBUPROFEN)]), "drug_drug")
    assert any(a.severity.label == "CRITICAL" for a in alerts)


def test_warfarin_antiplatelet_bleeding(engine):
    alerts = by_category(engine.evaluate(patient(), [order(WARFARIN), order(ASPIRIN)]), "drug_drug")
    assert any(a.severity.label == "CRITICAL" for a in alerts)


def test_simvastatin_enzyme_inhibitor_myopathy_critical(engine):
    alerts = by_category(engine.evaluate(patient(), [order(SIMVASTATIN), order(CLARITHROMYCIN)]), "drug_drug")
    assert any("근병증" in a.title or a.severity.label == "CRITICAL" for a in alerts)


def test_hyperkalemia_pair_warning(engine):
    alerts = by_category(engine.evaluate(patient(), [order(RAMIPRIL), order(SPIRONOLACTONE)]), "drug_drug")
    assert any("고칼륨" in a.title for a in alerts)


def test_hyperkalemia_polypharmacy_aggregated_to_single_alert(engine):
    """가산 위험은 쌍마다 띄우지 않고 하나의 경고로 집계한다(경고 피로 방지)."""
    p = patient(current_meds=(RAMIPRIL, SPIRONOLACTONE))
    alerts = [a for a in by_category(engine.evaluate(p, [order(LOSARTAN), order(KCL)]), "drug_drug")
              if "고칼륨" in a.title]
    assert len(alerts) == 1
    # 관련 약물 4종이 모두 한 경고에 집계됨
    assert len(alerts[0].related_drugs) == 4


def test_qt_pair_warning(engine):
    alerts = by_category(engine.evaluate(patient(), [order(CLARITHROMYCIN), order(LEVOFLOXACIN)]), "drug_drug")
    assert any("QT" in a.title for a in alerts)


def test_digoxin_amiodarone_warning(engine):
    alerts = by_category(engine.evaluate(patient(), [order(DIGOXIN), order(AMIODARONE)]), "drug_drug")
    assert any("디곡신" in a.title for a in alerts)


def test_serotonin_pair_warning(engine):
    alerts = by_category(engine.evaluate(patient(), [order(TRAMADOL), order(SERTRALINE)]), "drug_drug")
    assert any("세로토닌" in a.title for a in alerts)


def test_doac_nsaid_warning(engine):
    alerts = by_category(engine.evaluate(patient(), [order(APIXABAN), order(IBUPROFEN)]), "drug_drug")
    assert any(a.severity.label == "WARNING" for a in alerts)


# ── 음성 케이스 ─────────────────────────────────────────────────────
def test_no_interaction_between_unrelated_drugs(engine):
    alerts = by_category(engine.evaluate(patient(), [order(METOPROLOL), order(ACETAMINOPHEN)]), "drug_drug")
    assert alerts == []


def test_single_drug_no_ddi(engine):
    assert by_category(engine.evaluate(patient(), [order(WARFARIN)]), "drug_drug") == []


def test_two_existing_meds_only_no_ddi(engine):
    """기존-기존 조합만 있으면 신규 처방이 없어 DDI를 띄우지 않는다(노이즈 억제)."""
    p = patient(current_meds=(WARFARIN, IBUPROFEN))
    assert by_category(engine.evaluate(p, []), "drug_drug") == []
