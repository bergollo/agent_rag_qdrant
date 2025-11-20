import asyncio
import uuid
from io import BytesIO
from typing import Any, Dict, List, Optional

import httpx
from fastapi import File, HTTPException, UploadFile
from openai import OpenAI
from pdfminer.high_level import extract_text_to_fp
from qdrant_client import AsyncQdrantClient, models as qmodels

try:  # pragma: no cover - optional dependency on newer qdrant-client
    from qdrant_client.http import exceptions as qdrant_errors
except ImportError:  # pragma: no cover
    qdrant_errors = None

from app.core.config import get_settings

try:
    from openai.error import OpenAIError  # newer SDKs
except Exception:  # pragma: no cover - fallback for older clients
    OpenAIError = Exception

import faulthandler


class OpenAIClient:
    def __init__(self, openai_api_key: str, qdrant_url: Optional[str] = None):
        if not openai_api_key:
            raise ValueError("OpenAI API key is not set")

        settings = get_settings()
        self._model: str = "gpt-3.5-turbo"
        self._embedding_model: str = "text-embedding-3-small"
        self._collection_name: str = "documents"
        self._vector_size: int = 1536
        self._qdrant_url: str = (qdrant_url or settings.QDRANT_URL or "http://qdrant:6333").rstrip("/")

        self._client = OpenAI(api_key=openai_api_key)
        self._qdrant = AsyncQdrantClient(
            url=self._qdrant_url,
            timeout=30.0,
            prefer_grpc=False,
        )
        self._collection_ready = False

    async def llm(self, prompt: str, timeout: Optional[float] = 30.0) -> str:
        """
        Send a prompt to the OpenAI chat completions and return the assistant text as a plain string.
        Raises OpenAIError on API errors.
        """
        try:
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                timeout=timeout,
            )
            content = None
            if getattr(resp, "choices", None):
                choice = resp.choices[0]
                msg = getattr(choice, "message", None)
                if msg is not None:
                    content = getattr(msg, "content", None)

            if not content:
                raise OpenAIError("No content returned")
            return str(content)
        except OpenAIError | Exception as e:  # noqa: E722 - we want to wrap unknowns
            raise OpenAIError(str(e)) from e

    async def llm_with_context(
        self,
        prompt: str,
        matches: Optional[List[Dict[str, Any]]] = None,
        timeout: Optional[float] = 30.0,
    ) -> str:
        """
        Inject vector-search matches as reference context before calling the chat model.
        """
        matches = matches or []
        context_sections: List[str] = []
        for idx, match in enumerate(matches, start=1):
            payload = match.get("payload") or {}
            snippet = (
                payload.get("text")
                or payload.get("content")
                or payload.get("snippet")
                or ""
            ).strip()
            if not snippet:
                continue

            filename = payload.get("filename") or f"Document {idx}"
            context_sections.append(
                f"[{idx}] {filename}\nScore: {match.get('score', 0.0):.3f}\n{snippet[:1000]}"
            )

        context_block = (
            "\n\n".join(context_sections)
            if context_sections
            else "No relevant reference documents were retrieved."
        )

        user_prompt = (
            "You are a helpful assistant. Use the reference documents below when they are relevant. "
            "If the context does not contain the answer, say you do not know.\n\n"
            f"Reference documents:\n{context_block}\n\n"
            f"User question:\n{prompt}\n\n"
            "Answer:"
        )

        try:
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": user_prompt}],
                timeout=timeout,
            )
            content = None
            if getattr(resp, "choices", None):
                choice = resp.choices[0]
                msg = getattr(choice, "message", None)
                if msg is not None:
                    content = getattr(msg, "content", None)

            if not content:
                raise OpenAIError("No content returned")
            return str(content)
        except OpenAIError | Exception as e:  # noqa: E722
            raise OpenAIError(str(e)) from e

    @staticmethod
    def _extract_text(data: bytes, filename: str, content_type: str) -> str:
        """Pull readable text from PDFs (via pdfminer) or fallback to a string decode."""
        if filename.lower().endswith(".pdf") or "pdf" in (content_type or "").lower():
            out = BytesIO()
            extract_text_to_fp(BytesIO(data), out)
            return out.getvalue().decode(errors="ignore")

        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("latin-1", errors="ignore")

    def _create_embedding(self, text: str) -> List[float]:
        resp = self._client.embeddings.create(
            input=text,
            model=self._embedding_model,
        )
        data = getattr(resp, "data", None)
        if not data:
            raise OpenAIError("No embedding returned")
        embedding = getattr(data[0], "embedding", None)
        if embedding is None:
            raise OpenAIError("Embedding payload missing vector")
        return list(embedding)

    async def _ensure_collection(self) -> None:
        if self._collection_ready:
            return

        exists = await self._qdrant.collection_exists(
            collection_name=self._collection_name
        )
        if not exists:
            await self._qdrant.recreate_collection(
                collection_name=self._collection_name,
                vectors_config=qmodels.VectorParams(
                    size=self._vector_size,
                    distance=qmodels.Distance.COSINE,
                ),
            )
        self._collection_ready = True

    async def qdrant_upload(
        self,
        file: UploadFile = File(...),
        timeout: Optional[float] = 30.0,
    ) -> Dict[str, str]:
        """
        Extract text from an uploaded document, embed it with OpenAI, and store it in Qdrant.
        """
        data = await file.read()
        if not data:
            raise HTTPException(status_code=400, detail="empty file")

        text = self._extract_text(data, file.filename or "file", file.content_type or "")
        if not text.strip():
            raise HTTPException(status_code=400, detail="no extractable text")

        embedding = await asyncio.to_thread(self._create_embedding, text)
        await asyncio.wait_for(self._ensure_collection(), timeout or 30.0)

        doc_id = str(uuid.uuid4())
        payload = {
            "filename": file.filename,
            "content_type": file.content_type,
            "text": text[:5000],
        }
        point = qmodels.PointStruct(id=doc_id, vector=embedding, payload=payload)

        await self._qdrant.upsert(
            collection_name=self._collection_name,
            points=[point],
        )
        return {"id": doc_id, "status": "uploaded"}

    async def qdrant_semantic_search(
        self,
        query: str,
        top_k: int = 3,
        timeout: Optional[float] = 15.0,
    ) -> List[Dict[str, Any]]:
        """
        Embed the user query and return the top-k similar documents from Qdrant.
        """
        if not query.strip():
            raise HTTPException(status_code=400, detail="query text is empty")

        query_embedding = await asyncio.to_thread(self._create_embedding, query)

        await asyncio.wait_for(self._ensure_collection(), timeout or 15.0)

        search_timeout = timeout or 15.0

        faulthandler.dump_traceback_later(30, repeat=False)
        matches: List[Any] = []
        try:
            url = f"{self._qdrant_url}/collections/{self._collection_name}/points/search"

            payload = {
                "vector": query_embedding,
                "limit": max(1, top_k),
                "with_payload": True,
            }

            timeout_config = httpx.Timeout(search_timeout, connect=5.0)
            async with httpx.AsyncClient(timeout=timeout_config) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                body: Dict[str, Any] = resp.json()
                matches = body.get("result") or []

        except asyncio.TimeoutError as exc:
            raise RuntimeError(
                f"Qdrant search timed out after {search_timeout}s"
            ) from exc
        except httpx.TimeoutException as exc:
            raise RuntimeError(
                f"Qdrant HTTP search timed out after {search_timeout}s"
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Qdrant API responded with {exc.response.status_code}") from exc
        except ValueError as exc:
            raise RuntimeError("Unable to parse Qdrant search response") from exc
        except Exception as exc:
            if qdrant_errors and isinstance(
                exc, qdrant_errors.ResponseHandlingException
            ):
                raise RuntimeError(f"Qdrant API error during search: {exc}") from exc
            raise RuntimeError(f"Unexpected error during Qdrant search: {exc}") from exc
        finally:
            faulthandler.cancel_dump_traceback_later()

        results: List[Dict[str, Any]] = []
        for match in matches:
            if isinstance(match, dict):
                match_id = match.get("id", "")
                score = float(match.get("score", 0.0) or 0.0)
                payload = match.get("payload") or {}
            else:
                match_id = getattr(match, "id", "")
                score = float(getattr(match, "score", 0.0) or 0.0)
                payload = getattr(match, "payload", {}) or {}
            results.append(
                {
                    "id": str(match_id),
                    "score": score,
                    "payload": payload,
                }
            )
        return results
