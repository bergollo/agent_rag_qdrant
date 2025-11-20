"""LLM query endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import get_openai_client
from app.services.open_ai import OpenAIClient

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/", response_model=QueryResponse)
async def query_ai(
    req: QueryRequest,
    ai_client: OpenAIClient = Depends(get_openai_client),
) -> QueryResponse:
    """Run semantic search + LLM completion for the provided query string."""
    try:
        matches = await ai_client.qdrant_semantic_search(req.query)
        answer = await ai_client.llm_with_context(req.query, matches)
        return QueryResponse(answer=answer)
    except Exception as exc:  # pragma: no cover - defensive HTTP error mapping
        raise HTTPException(status_code=500, detail=str(exc)) from exc
