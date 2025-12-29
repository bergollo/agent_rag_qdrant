import asyncio
import logging
import uuid
from io import BytesIO
from typing import Any, Dict, List, Optional

import httpx
from fastapi import File, HTTPException, UploadFile
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from openai import OpenAI
from pdfminer.high_level import extract_text_to_fp
from qdrant_client import AsyncQdrantClient, models as qmodels

from .redaction_mcp import build_redaction_client
from .tools_side_effects import safe_send_webhook, safe_store_memory

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

import traceback

import logging
logger = logging.getLogger("ai_service")

import json

class OpenAIClient:
    def __init__(self, openai_api_key: str, qdrant_url: Optional[str] = None):
        if not openai_api_key:
            raise ValueError("OpenAI API key is not set")

        settings = get_settings()
        self._model: str = "gpt-3.5-turbo"  # primary chat model
        self._embedding_model: str = "text-embedding-3-small"
        self._collection_name: str = "documents"
        self._vector_size: Optional[int] = None

        self._qdrant_url: str = (qdrant_url or settings.QDRANT_URL or "http://qdrant:6333").rstrip("/")

        self._client = OpenAI(api_key=openai_api_key)
        self._qdrant = AsyncQdrantClient(
            url=self._qdrant_url,
            timeout=30.0,
            prefer_grpc=False,
        )
        self._collection_ready = False


    async def build_mcp_tool(self) -> List[BaseTool]:
        """
        Build and return MCP + local tools used by chat completions to execute side effects safely.
        """
        logger.info("Building MCP tools for OpenAI client")
        mcp = build_redaction_client()
        mcp_tools: Dict[str, BaseTool] = {t.name: t for t in await mcp.get_tools()} # includes "redact_text", "classify_sensitivity"
        tools: List[BaseTool] = [
            mcp_tools["redaction_redact_text"],
            mcp_tools["redaction_classify_sensitivity"],
            # safe_send_webhook,
            # safe_store_memory,
            # add retrieve_docs, summarize, etc.
        ]

        self._tool_impls: Dict[str, BaseTool] = {t.name: t for t in tools}

        openai_tools = [convert_to_openai_tool(t) for t in tools]
        return openai_tools

    async def _execute_tool_call(self, tool_name: str, tool_args: Dict[str, Any], text: str) -> str:
        """
        Execute a tool requested by the LLM and return a STRING for the OpenAI "tool" message.
        """
        tool: BaseTool | None = getattr(self, "_tool_impls", {}).get(tool_name)
        if tool is None:
            # Return an error payload instead of raising (model can recover)
            return json.dumps({"error": f"Unknown tool: {tool_name}", "args": tool_args}, ensure_ascii=False)

        # ----------------------------
        # Detect payload-shaped tools
        # ----------------------------
        expects_payload = False
        payload_field_name = None

        args_schema = getattr(tool, "args_schema", None)
        if args_schema:
            required_fields = args_schema.get("required") or []
            if len(required_fields) > 0 and "payload" in required_fields:
                expects_payload = True
                payload_field_name = "payload"

        # ----------------------------
        # Inject dummy payload if needed
        # ----------------------------
        if expects_payload and payload_field_name not in tool_args:
            tool_args = dict(tool_args)  # shallow copy
            tool_args["payload"] = {
                "request_id": str(uuid.uuid4()),
                "text": (
                    str(text)[:1000]  # pass up to 1000 chars of text for redaction
                ),
                "purpose": "llm_assisted_redaction",
                "actor": {
                    "tenant_id": "default-tenant",
                    "user_id": "system-agent",
                },
            }
        
        try:
            # LangChain BaseTool typically supports ainvoke (async). Some tools only have invoke (sync).
            if hasattr(tool, "ainvoke"):
                result = await tool.ainvoke(tool_args)
            else:
                result = await asyncio.to_thread(tool.invoke, tool_args)

            # OpenAI tool message content must be a string
            if isinstance(result, str):
                return result
            return json.dumps(result, ensure_ascii=False)

        except Exception as e:
            return json.dumps(
                {"error": str(e), "tool": tool_name, "args": tool_args},
                ensure_ascii=False,
            )

    async def llm(self, prompt: str, timeout: Optional[float] = 30.0) -> str:
        """
        Send a prompt to the OpenAI chat completions and return the assistant text as a plain string.
        Raises OpenAIError on API errors.
        """
        try:
            tools = await self.build_mcp_tool()
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                tools=tools,
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
        except (OpenAIError, Exception) as e:  # noqa: E722 - we want to wrap unknowns
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
            "Step 1: Call redaction_redact_text with payload.text equal to the User question.\n"
            "Step 2: Answer using the redacted text.\n\n"
            f"Redaction payload template (fill payload.text from the User question):\n"
            f"Reference documents:\n{context_block}\n\n"
            f"User question:\n{prompt}\n\n"
            "Answer:"
        )

        # Conversation state for the tool loop
        messages: List[Dict[str, Any]] = [{"role": "user", "content": user_prompt}]

        try:
            tools = await self.build_mcp_tool()

            resp = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=tools,
                tool_choice="auto",   # "auto"  or force one tool: {"type":"function","function":{"name":"redaction_redact_text"}}
                timeout=timeout,
            )

            if not getattr(resp, "choices", None):
                raise OpenAIError("No choices returned")

            choice = resp.choices[0]
            msg = getattr(choice, "message", None)
            if msg is None:
                raise OpenAIError("No message returned")

            tool_calls = getattr(msg, "tool_calls", None)
            content = getattr(msg, "content", None)

            # If no tool calls, we’re done.
            if not tool_calls:
                if not content:
                    raise OpenAIError("No content returned")
                return str(content)

            # Append the assistant message that contains tool_calls (important for tool linking)
            assistant_message: Dict[str, Any] = {
                "role": "assistant",
                "content": content,  # often None when tool_calls exist; that’s fine
                "tool_calls": [],
            }

            # tool_calls are typed objects; convert them into the dict shape OpenAI expects in messages
            for tc in tool_calls:
                # OpenAI SDK objects typically have: tc.id, tc.type, tc.function.name, tc.function.arguments
                assistant_message["tool_calls"].append(
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                )
        
            messages.append(assistant_message)

            # Execute each tool call and append tool results
            for tc in tool_calls:
                tool_name = tc.function.name
                raw_args = tc.function.arguments

                try:
                    tool_args = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
                except Exception:
                    # If the model produced non-JSON args, pass through as a string payload
                    tool_args = {"_raw": raw_args}

                tool_output = await self._execute_tool_call(tool_name, tool_args, user_prompt)

                # Tool response message MUST include tool_call_id
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_output if isinstance(tool_output, str) else json.dumps(tool_output),
                    }
                )

            # Final LLM call after tool executions
            final_resp = await asyncio.to_thread(
                self._client.chat.completions.create,
                model=self._model,
                messages=messages,
                timeout=timeout,
            )

            final_msg = final_resp.choices[0].message

            if not final_msg.content:
                raise OpenAIError("Final LLM response was empty")

            return final_msg.content

        except (OpenAIError, Exception) as e:  # noqa: E722
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
        vector = list(embedding)

        # Capture the vector size the first time we request an embedding so the Qdrant collection matches.
        if self._vector_size is None:
            self._vector_size = len(vector)

        return vector

    async def _ensure_collection(self) -> None:
        if self._collection_ready:
            return

        if self._vector_size is None:
            raise RuntimeError(
                "Vector size is not initialized; create an embedding before ensuring the collection."
            )

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
