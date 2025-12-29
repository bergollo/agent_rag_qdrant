"""Tests for the backend health router."""

from __future__ import annotations


def test_backend_health(api_client):
    client, _ = api_client
    resp = client.get("/api/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "service": "backend"}
