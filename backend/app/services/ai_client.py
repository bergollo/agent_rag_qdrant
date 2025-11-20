"""Async HTTP client wrapper around the ai_service FastAPI app."""

from typing import Any, Dict

import httpx
from fastapi import UploadFile


class AIClient:
    """Thin HTTP client for delegating work to the ai_service FastAPI app."""

    def __init__(self, base_url: str, timeout: float = 40.0):
        self.base_url = base_url
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def health_check(self) -> Dict[str, Any]:
        """Call the ai_service health endpoint."""
        resp = await self._client.get("/health/")
        resp.raise_for_status()
        return resp.json()

    async def upload_document(self, file: UploadFile) -> Dict[str, Any]:
        """Forward file uploads to the ai_service vectorstore endpoint."""
        file_bytes = await file.read()
        if not file_bytes:
            raise ValueError("empty file upload")

        # httpx expects (filename, bytes, content_type) triples per field.
        files = {
            "file": (
                file.filename or "upload",
                file_bytes,
                file.content_type or "application/octet-stream",
            )
        }

        resp = await self._client.post("/v1/vectorstore/upload", files=files)
        resp.raise_for_status()
        return resp.json()

    async def uploadDocument(self, file: UploadFile) -> Dict[str, Any]:  # pragma: no cover
        """Backward-compatible alias for legacy callers."""
        return await self.upload_document(file)

    async def query(self, text: str) -> str:
        """Send a user query to ai_service and return the answer text."""
        resp = await self._client.post("/v1/query/", json={"query": text})
        resp.raise_for_status()
        data = resp.json()
        return data.get("answer") or data.get("result")
