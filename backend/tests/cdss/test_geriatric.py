"""고령자 주의 약물(Beers 일부): 양성/음성."""
from helpers import LORAZEPAM, by_category, order, patient


def test_benzodiazepine_in_elderly_warning(engine):
    p = patient(age=80)
    alerts = by_category(engine.evaluate(p, [order(LORAZEPAM)]), "geriatric")
    assert len(alerts) == 1
    assert alerts[0].severity.label == "WARNING"


def test_benzodiazepine_in_younger_no_alert(engine):
    p = patient(age=40)
    assert by_category(engine.evaluate(p, [order(LORAZEPAM)]), "geriatric") == []


def test_boundary_age_65_triggers(engine):
    p = patient(age=65)
    assert by_category(engine.evaluate(p, [order(LORAZEPAM)]), "geriatric")
