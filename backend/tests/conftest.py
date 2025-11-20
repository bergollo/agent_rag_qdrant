"""Shared pytest fixtures for the backend FastAPI service."""

from __future__ import annotations

from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_ai_client
from app.main import create_app


class StubAIClient:
    """Simple stub that records calls and returns canned responses."""

    def __init__(self) -> None:
        self.health_called = False
        self.uploaded_files: list[str] = []
        self.queries: list[str] = []

    async def health_check(self) -> Dict[str, str]:
        self.health_called = True
        return {"status": "ok", "service": "ai_service"}

    async def upload_document(self, file) -> Dict[str, Any]:  # type: ignore[override]
        payload = await file.read()
        self.uploaded_files.append(file.filename or "upload")
        return {"id": "stub-doc", "size": len(payload)}

    async def query(self, query: str) -> str:
        self.queries.append(query)
        return f"answer for {query}"


@pytest.fixture()
def api_client():
    """Provide a FastAPI TestClient with the AI client dependency overridden."""
    app = create_app()
    stub = StubAIClient()
    app.dependency_overrides[get_ai_client] = lambda: stub
    client = TestClient(app)
    yield client, stub
    app.dependency_overrides.clear()
