from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient

from log_monitor.main import app

client = TestClient(app)


def _valid_payload() -> dict[str, object]:
    return {
        "timestamp": "2026-02-14T17:00:00Z",
        "level": "INFO",
        "message": "User signup completed",
        "service": "api-gateway",
        "metadata": {"request_id": "abc123", "status_code": 201},
    }


def test_ingest_log_accepts_valid_payload() -> None:
    response = client.post(
        "/v1/logs",
        json=_valid_payload(),
        headers={"X-Tenant-ID": "tenant-acme"},
    )

    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "accepted"
    assert body["tenant_id"] == "tenant-acme"
    UUID(body["event_id"])
    assert "received_at" in body


def test_ingest_log_rejects_missing_tenant_header() -> None:
    response = client.post("/v1/logs", json=_valid_payload())

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(
        entry["loc"][0] == "header" and str(entry["loc"][1]).lower() == "x-tenant-id"
        for entry in detail
    )


def test_ingest_log_rejects_invalid_log_level() -> None:
    payload = _valid_payload()
    payload["level"] = "NOTICE"

    response = client.post(
        "/v1/logs",
        json=payload,
        headers={"X-Tenant-ID": "tenant-acme"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(entry["loc"][-1] == "level" for entry in detail)


def test_ingest_log_rejects_malformed_timestamp() -> None:
    payload = _valid_payload()
    payload["timestamp"] = "14-02-2026 17:00:00"

    response = client.post(
        "/v1/logs",
        json=payload,
        headers={"X-Tenant-ID": "tenant-acme"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(entry["loc"][-1] == "timestamp" for entry in detail)


def test_ingest_log_rejects_empty_message() -> None:
    payload = _valid_payload()
    payload["message"] = "   "

    response = client.post(
        "/v1/logs",
        json=payload,
        headers={"X-Tenant-ID": "tenant-acme"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(entry["loc"][-1] == "message" for entry in detail)
