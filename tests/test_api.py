import os
import tempfile

# Use a dedicated database for this test module.
_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite3")
os.environ["BORDERWISE_DB_PATH"] = _db_file.name
_db_file.close()

import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


BASE = {
    "student_reference": "STUDENT-DEMO",
    "recipient_name": "Example University",
    "recipient_reference": "UNI-001",
    "amount": 1200,
    "currency": "AUD",
    "purpose": "tuition",
}


def post_payment(client, payload=None, key="test-key-default"):
    return client.post(
        "/api/transactions/prepare",
        headers={"Idempotency-Key": key},
        json=payload or BASE,
    )


def test_health_simulation_only(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "simulation", "real_money_moved": False}


def test_demo_info_discloses_simulation(client):
    info = client.get("/api/demo-info").json()
    assert info["live_banking_enabled"] is False
    assert info["risk_engine"] == "explainable-rule-based-demo"


def test_negative_amount_rejected(client):
    response = post_payment(client, {**BASE, "amount": -2}, "test-key-negative")
    assert response.status_code == 422


def test_amount_over_limit_rejected(client):
    response = post_payment(client, {**BASE, "amount": 100001}, "test-key-over-limit")
    assert response.status_code == 422


def test_unknown_fields_rejected(client):
    response = post_payment(client, {**BASE, "account_password": "should-not-be-accepted"}, "test-key-extra")
    assert response.status_code == 422


def test_prepare_transaction_is_simulation_only(client):
    response = post_payment(client, key="test-key-prepare")
    assert response.status_code == 201
    data = response.json()
    assert data["risk"]["decision"] == "allow_demo"
    assert data["provider"]["real_money_moved"] is False
    assert data["status"] == "prepared_demo"


def test_idempotency_key_returns_same_transaction(client):
    first = post_payment(client, key="test-key-repeat")
    second = post_payment(client, key="test-key-repeat")
    assert first.status_code == second.status_code == 201
    assert first.json()["id"] == second.json()["id"]


def test_idempotency_key_rejects_different_payload(client):
    post_payment(client, key="test-key-conflict")
    changed = {**BASE, "amount": 1300}
    response = post_payment(client, changed, "test-key-conflict")
    assert response.status_code == 409


def test_high_amount_and_unverified_recipient_are_blocked_by_demo_policy(client):
    payload = {**BASE, "amount": 6000, "recipient_name": "unknown", "purpose": "other"}
    response = post_payment(client, payload, "test-key-block")
    assert response.status_code == 201
    assert response.json()["risk"]["decision"] == "block_demo"
    assert response.json()["risk"]["score"] == 90
    assert response.json()["status"] == "needs_review"


def test_risk_assessment_does_not_create_transaction(client):
    before = len(client.get("/api/transactions").json()["items"])
    response = client.post("/api/risk/assess", json={**BASE, "amount": 2000})
    after = len(client.get("/api/transactions").json()["items"])
    assert response.status_code == 200
    assert response.json()["risk"]["decision"] == "allow_demo"
    assert response.json()["real_money_moved"] is False
    assert before == after


def test_security_headers_and_correlation_id(client):
    response = client.get("/api/health", headers={"X-Correlation-ID": "demo-correlation-123"})
    assert response.headers["X-Correlation-ID"] == "demo-correlation-123"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in response.headers


def test_transaction_history_and_audit_endpoints(client):
    assert client.get("/api/transactions").status_code == 200
    audit = client.get("/api/audit")
    assert audit.status_code == 200
    assert isinstance(audit.json()["items"], list)
