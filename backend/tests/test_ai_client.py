"""Unit tests for the backend AIClient helper."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.ai_client import AIClient


@pytest.mark.asyncio
async def test_health_check_calls_endpoint():
    client = AIClient(base_url="http://ai")
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok", "service": "ai_service"}
    mock_response.raise_for_status.return_value = None

    with patch.object(client, "_client") as mock_http:
        mock_http.get = AsyncMock(return_value=mock_response)
        resp = await client.ping_check()

    assert resp == {"status": "ok", "service": "ai_service"}
    mock_http.get.assert_awaited_once_with("/healthz/")


@pytest.mark.asyncio
async def test_upload_document_validates_file(tmp_path):
    client = AIClient(base_url="http://ai")

    class DummyUpload:
        filename = "doc.txt"
        content_type = "text/plain"

        async def read(self):
            return b"hello"

    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "1"}
    mock_response.raise_for_status.return_value = None

    with patch.object(client, "_client") as mock_http:
        mock_http.post = AsyncMock(return_value=mock_response)
        resp = await client.upload_document(DummyUpload())

    assert resp == {"id": "1"}
    mock_http.post.assert_awaited()


@pytest.mark.asyncio
async def test_query_returns_answer(monkeypatch):
    client = AIClient(base_url="http://ai")
    mock_response = MagicMock()
    mock_response.json.return_value = {"answer": "42"}
    mock_response.raise_for_status.return_value = None

    with patch.object(client, "_client") as mock_http:
        mock_http.post = AsyncMock(return_value=mock_response)
        answer = await client.query("life?")

    assert answer == "42"
