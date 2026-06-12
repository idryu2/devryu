"""백엔드 API 통합 테스트(일부).

실제 DB(PostgreSQL+pgvector)와 시드 데이터가 필요하다. DB에 연결할 수 없으면
모듈 전체를 skip 한다(규칙 엔진 단위 테스트는 DB 없이도 항상 동작).
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db.session import engine


def _db_available() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _db_available(), reason="DB 미연결 - 통합 테스트 skip")


@pytest.fixture(scope="module")
def client() -> TestClient:
    from app.main import app

    return TestClient(app)


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_patients_seeded(client: TestClient):
    r = client.get("/patients")
    assert r.status_code == 200
    assert len(r.json()) >= 8  # 시드 환자 8~12명


def test_evaluate_warfarin_nsaid_critical(client: TestClient):
    r = client.post("/cdss/evaluate", json={"patient_id": "P003", "orders": [{"drug_code": "ibuprofen"}]})
    assert r.status_code == 200
    body = r.json()
    assert body["has_critical"] is True
    assert any(a["category"] == "drug_drug" and a["severity"] == "CRITICAL" for a in body["alerts"])


def test_sign_blocked_without_override(client: TestClient):
    r = client.post("/orders/sign", json={"patient_id": "P003", "orders": [{"drug_code": "ibuprofen"}]})
    assert r.status_code == 400


def test_sign_allowed_with_override(client: TestClient):
    r = client.post(
        "/orders/sign",
        json={
            "patient_id": "P003",
            "orders": [{"drug_code": "ibuprofen"}],
            "override_reason": "임상적 판단상 단기 사용",
        },
    )
    assert r.status_code == 200
    assert r.json()["overridden"] is True


def test_guidelines_ask_returns_sources(client: TestClient):
    r = client.post("/guidelines/ask", json={"question": "CKD 환자에서 metformin 사용은?"})
    assert r.status_code == 200
    body = r.json()
    assert body["sources"]
    assert "disclaimer" in body
