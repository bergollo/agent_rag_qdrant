"""Shared pytest fixtures for ai_service tests."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_openai_client
from app.main import create_app


class StubOpenAIClient:
    """Minimal async stub that mimics the OpenAIClient behavior for tests."""

    def __init__(self) -> None:
        self.semantic_queries: List[str] = []
        self.llm_calls: List[Tuple[str, List[Dict[str, Any]]]] = []
        self.uploaded_files: List[Dict[str, Any]] = []

    async def qdrant_semantic_search(self, query: str, *args: Any, **kwargs: Any):
        self.semantic_queries.append(query)
        # Return a deterministic fake match structure
        return [
            {
                "id": "stub-point",
                "score": 0.99,
                "payload": {"text": f"context for {query}"},
            }
        ]

    async def llm_with_context(
        self,
        prompt: str,
        matches: List[Dict[str, Any]],
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.llm_calls.append((prompt, matches))
        return f"answer for {prompt}"

    async def qdrant_upload(self, file, *args: Any, **kwargs: Any):  # type: ignore[override]
        contents = await file.read()
        self.uploaded_files.append({
            "filename": file.filename,
            "size": len(contents),
        })
        return {"id": "stub-doc", "status": "uploaded"}


@pytest.fixture()
def api_client():
    """FastAPI TestClient with the OpenAI dependency overridden by the stub."""
    app = create_app()
    stub = StubOpenAIClient()
    app.dependency_overrides[get_openai_client] = lambda: stub
    client = TestClient(app)
    yield client, stub
    app.dependency_overrides.clear()
