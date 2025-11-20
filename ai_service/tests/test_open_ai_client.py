"""Unit tests for the OpenAIClient utility methods."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.services.open_ai import OpenAIClient


@pytest.mark.asyncio
async def test_ensure_collection_skips_when_ready(monkeypatch):
    client = OpenAIClient(openai_api_key="dummy", qdrant_url="http://qdrant")
    client._collection_ready = True
    mocked_qdrant = AsyncMock()
    client._qdrant = mocked_qdrant

    await client._ensure_collection()

    mocked_qdrant.collection_exists.assert_not_called()


@pytest.mark.asyncio
async def test_qdrant_semantic_search_raises_on_empty_query():
    client = OpenAIClient(openai_api_key="dummy", qdrant_url="http://qdrant")
    with pytest.raises(Exception) as exc:
        await client.qdrant_semantic_search("  ")
    assert "query text is empty" in str(exc.value)


@pytest.mark.asyncio
async def test_qdrant_semantic_search_parses_http_response(monkeypatch):
    client = OpenAIClient(openai_api_key="dummy", qdrant_url="http://qdrant")

    fake_embedding = [0.1, 0.2]
    monkeypatch.setattr(client, "_create_embedding", lambda text: fake_embedding)

    async def fake_collection_exists(*args, **kwargs):
        return True

    client._qdrant.collection_exists = fake_collection_exists  # type: ignore
    client._collection_ready = True

    class DummyResponse:
        def __init__(self):
            self.status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return {
                "result": [
                    {"id": "1", "score": 0.5, "payload": {"text": "hello"}}
                ]
            }

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            self.post = AsyncMock(return_value=DummyResponse())

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    with patch("app.services.open_ai.httpx.AsyncClient", DummyAsyncClient):
        results = await client.qdrant_semantic_search("hello", timeout=0.1)

    assert results[0]["id"] == "1"
    assert results[0]["payload"]["text"] == "hello"
