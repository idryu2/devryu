"""약물-질환 금기: 양성/음성."""
from helpers import (
    IBUPROFEN,
    METOPROLOL,
    PROPRANOLOL,
    by_category,
    order,
    patient,
)


def test_asthma_nonselective_betablocker_critical(engine):
    p = patient(conditions=("asthma",))
    alerts = by_category(engine.evaluate(p, [order(PROPRANOLOL)]), "drug_disease")
    assert len(alerts) == 1
    assert alerts[0].severity.label == "CRITICAL"


def test_asthma_selective_betablocker_no_disease_alert(engine):
    """심장선택적 베타차단제는 천식 금기 규칙에 걸리지 않는다."""
    p = patient(conditions=("asthma",))
    assert by_category(engine.evaluate(p, [order(METOPROLOL)]), "drug_disease") == []


def test_ckd_nsaid_warning(engine):
    p = patient(conditions=("ckd",))
    alerts = by_category(engine.evaluate(p, [order(IBUPROFEN)]), "drug_disease")
    assert any(a.severity.label == "WARNING" for a in alerts)


def test_no_condition_no_disease_alert(engine):
    p = patient(conditions=())
    assert by_category(engine.evaluate(p, [order(PROPRANOLOL)]), "drug_disease") == []
