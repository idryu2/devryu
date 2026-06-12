"""임신부 금기: 양성/음성."""
from helpers import ATORVASTATIN, RAMIPRIL, WARFARIN, by_category, order, patient


def test_warfarin_in_pregnancy_critical(engine):
    p = patient(sex="F", pregnant=True)
    alerts = by_category(engine.evaluate(p, [order(WARFARIN)]), "pregnancy")
    assert len(alerts) == 1
    assert alerts[0].severity.label == "CRITICAL"


def test_acei_in_pregnancy_critical(engine):
    p = patient(sex="F", pregnant=True)
    alerts = by_category(engine.evaluate(p, [order(RAMIPRIL)]), "pregnancy")
    assert any(a.severity.label == "CRITICAL" for a in alerts)


def test_statin_in_pregnancy_critical(engine):
    p = patient(sex="F", pregnant=True)
    alerts = by_category(engine.evaluate(p, [order(ATORVASTATIN)]), "pregnancy")
    assert any(a.severity.label == "CRITICAL" for a in alerts)


def test_no_pregnancy_no_alert(engine):
    p = patient(sex="F", pregnant=False)
    assert by_category(engine.evaluate(p, [order(WARFARIN)]), "pregnancy") == []
