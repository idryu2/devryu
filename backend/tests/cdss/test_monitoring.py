"""약물-검사 연계 모니터링 안내(INFO): 양성/음성."""
from helpers import ATORVASTATIN, METOPROLOL, WARFARIN, by_category, order, patient


def test_warfarin_inr_monitoring_info(engine):
    alerts = by_category(engine.evaluate(patient(), [order(WARFARIN)]), "monitoring")
    assert len(alerts) == 1
    assert alerts[0].severity.label == "INFO"
    assert "INR" in alerts[0].title


def test_statin_lft_monitoring_info(engine):
    alerts = by_category(engine.evaluate(patient(), [order(ATORVASTATIN)]), "monitoring")
    assert any(a.severity.label == "INFO" for a in alerts)


def test_drug_without_monitoring_rule_no_alert(engine):
    assert by_category(engine.evaluate(patient(), [order(METOPROLOL)]), "monitoring") == []
