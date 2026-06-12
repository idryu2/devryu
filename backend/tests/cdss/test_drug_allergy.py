"""약물-알레르기 금기: 양성/음성."""
from helpers import AMOXICILLIN, CEFTRIAXONE, by_category, order, patient


def test_direct_penicillin_allergy_is_critical(engine):
    p = patient(allergies=("penicillin",))
    alerts = by_category(engine.evaluate(p, [order(AMOXICILLIN)]), "drug_allergy")
    assert len(alerts) == 1
    assert alerts[0].severity.label == "CRITICAL"


def test_penicillin_allergy_cross_reacts_with_cephalosporin_as_warning(engine):
    p = patient(allergies=("penicillin",))
    alerts = by_category(engine.evaluate(p, [order(CEFTRIAXONE)]), "drug_allergy")
    assert len(alerts) == 1
    assert alerts[0].severity.label == "WARNING"


def test_no_allergy_no_alert(engine):
    p = patient(allergies=())
    assert by_category(engine.evaluate(p, [order(AMOXICILLIN)]), "drug_allergy") == []


def test_unrelated_allergy_no_alert(engine):
    p = patient(allergies=("sulfonamide",))
    assert by_category(engine.evaluate(p, [order(AMOXICILLIN)]), "drug_allergy") == []
