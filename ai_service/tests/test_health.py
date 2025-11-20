"""Smoke tests for the health endpoint."""

from __future__ import annotations


def test_health_endpoint(api_client):
    client, _ = api_client
    resp = client.get("/health/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "service": "ai_service"}
