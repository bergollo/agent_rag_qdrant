"""LLM query endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Header, Request
from pydantic import BaseModel

from app.api.deps import get_openai_client
from app.services.open_ai import OpenAIClient

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

def actor_from_headers(authorization: str, tenant_id: str) -> dict:
    # Replace with JWT parsing in your app
    return {"user_id": "user123", "tenant_id": tenant_id, "roles": ["user"]}

@router.post("/", response_model=QueryResponse)
async def query_ai(
    req: QueryRequest,
    authorization: str = Header(default=""),
    x_tenant_id: str = Header(default="unknown"),
    x_request_id: str = Header(default=""),
    ai_client: OpenAIClient = Depends(get_openai_client),
) -> QueryResponse:
    """Run semantic search + LLM completion for the provided query string."""

    request_id = x_request_id or str(uuid.uuid4())
    actor = actor_from_headers(authorization, x_tenant_id)
    user_text = req.query

    prompt = (
        f"request_id={request_id}\n"
        f"actor={actor}\n"
        f"user_message={user_text}"
    )

    try:
        matches = await ai_client.qdrant_semantic_search(req.query)
        answer = await ai_client.llm_with_context(req.query, matches)
        return QueryResponse(answer=answer)
    except Exception as exc:  # pragma: no cover - defensive HTTP error mapping
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.post("/chat-agentic")
async def chat_agentic(
    request: Request,
    body: dict,
    authorization: str = Header(default=""),
    x_tenant_id: str = Header(default="unknown"),
    x_request_id: str = Header(default=""),
):
    request_id = x_request_id or str(uuid.uuid4())
    actor = actor_from_headers(authorization, x_tenant_id)
    user_text = body.get("message", "")

    agent = await build_agent()

    # Provide request_id + actor as part of the prompt so the LLM can pass them into tools
    # (You can also inject these via tool wrappers, but for full agentic we allow model to supply them.)
    prompt = (
        f"request_id={request_id}\n"
        f"actor={actor}\n"
        f"user_message={user_text}"
    )

    result = await agent.ainvoke({"input": prompt})
    return {"request_id": request_id, "answer": result.get("output", "")}