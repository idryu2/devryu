"""중복 처방(동일 성분/동일 계열): 양성/음성."""
from helpers import IBUPROFEN, WARFARIN, by_category, make_drug, order, patient


def test_same_ingredient_duplicate_warning(engine):
    ibu2 = make_drug("ibuprofen_brand2", ingredient="ibuprofen", drug_class="NSAID")
    alerts = by_category(engine.evaluate(patient(), [order(IBUPROFEN), order(ibu2)]), "duplicate")
    assert any(a.severity.label == "WARNING" for a in alerts)


def test_same_class_different_ingredient_info(engine):
    naproxen = make_drug("naproxen", ingredient="naproxen", drug_class="NSAID")
    alerts = by_category(engine.evaluate(patient(), [order(IBUPROFEN), order(naproxen)]), "duplicate")
    assert any(a.severity.label == "INFO" for a in alerts)


def test_duplicate_with_current_medication(engine):
    naproxen = make_drug("naproxen", ingredient="naproxen", drug_class="NSAID")
    p = patient(current_meds=(IBUPROFEN,))
    alerts = by_category(engine.evaluate(p, [order(naproxen)]), "duplicate")
    assert alerts  # 동일 계열 중복 감지


def test_different_class_no_duplicate(engine):
    alerts = by_category(engine.evaluate(patient(), [order(IBUPROFEN), order(WARFARIN)]), "duplicate")
    assert alerts == []
