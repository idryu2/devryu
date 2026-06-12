"""신기능 기반 용량 조정/금기: 양성/음성."""
from helpers import IBUPROFEN, METFORMIN, by_category, order, patient


def test_metformin_contraindicated_below_egfr_30(engine):
    p = patient(egfr=25)
    alerts = by_category(engine.evaluate(p, [order(METFORMIN)]), "renal")
    assert any(a.severity.label == "CRITICAL" for a in alerts)


def test_metformin_adjust_between_30_and_45(engine):
    p = patient(egfr=40)
    alerts = by_category(engine.evaluate(p, [order(METFORMIN)]), "renal")
    # 금기(<30)는 아니고 조정(<45) 경고만
    assert alerts
    assert all(a.severity.label != "CRITICAL" for a in alerts)


def test_metformin_normal_renal_no_alert(engine):
    p = patient(egfr=90)
    assert by_category(engine.evaluate(p, [order(METFORMIN)]), "renal") == []


def test_nsaid_avoid_below_egfr_30(engine):
    p = patient(egfr=20)
    alerts = by_category(engine.evaluate(p, [order(IBUPROFEN)]), "renal")
    assert alerts


def test_no_egfr_no_renal_alert(engine):
    """eGFR 정보가 없으면 신기능 규칙은 평가하지 않는다."""
    p = patient(egfr=None)
    assert by_category(engine.evaluate(p, [order(METFORMIN)]), "renal") == []
