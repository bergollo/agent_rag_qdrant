"""Tests for the LLM query endpoint."""

from __future__ import annotations


def test_query_ai_returns_answer(api_client):
    client, stub = api_client

    payload = {"query": "What is Qdrant?"}
    resp = client.post("/v1/query/", json=payload)

    assert resp.status_code == 200
    assert resp.json() == {"answer": "answer for What is Qdrant?"}

    assert stub.semantic_queries == [payload["query"]]
    assert len(stub.llm_calls) == 1
    prompt, matches = stub.llm_calls[0]
    assert prompt == payload["query"]
    assert matches[0]["payload"]["text"].startswith("context for")
