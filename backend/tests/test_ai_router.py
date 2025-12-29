"""Tests for the AI proxy router that calls ai_service."""

from __future__ import annotations

from pathlib import Path


def test_ai_health_forwards_call(api_client):
    client, stub = api_client
    resp = client.get("/api/ai/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "service": "ai_service"}
    assert stub.health_called


def test_vectorstore_upload(api_client, tmp_path: Path):
    client, stub = api_client
    sample = tmp_path / "doc.txt"
    sample.write_text("content")

    with sample.open("rb") as fh:
        files = {"file": (sample.name, fh, "text/plain")}
        resp = client.post("/api/ai/vectorstore/upload", files=files)

    assert resp.status_code == 200
    assert resp.json()["id"] == "stub-doc"
    assert stub.uploaded_files == [sample.name]


def test_query_endpoint(api_client):
    client, stub = api_client
    payload = {"query": "What is AI?"}
    resp = client.post("/api/ai/query", json=payload)

    assert resp.status_code == 200
    assert resp.json() == {"answer": "answer for What is AI?"}
    assert stub.queries == ["What is AI?"]
