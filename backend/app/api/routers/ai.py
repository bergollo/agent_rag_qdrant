"""Routes that proxy frontend requests to the ai_service backend."""

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from pydantic import BaseModel

from app.api.deps import get_ai_client
from app.services.ai_client import AIClient

router = APIRouter()


class QueryRequest(BaseModel):
    """Schema for user-issued natural language questions."""

    query: str


class QueryResponse(BaseModel):
    """Single-field schema returned by the AI query endpoint."""

    answer: str


@router.get("/healthz")
async def ping_check(ai_client: AIClient = Depends(get_ai_client)) -> Dict[str, Any]:
    """Check that the downstream ai_service is reachable."""
    try:
        return await ai_client.ping_check()
    except Exception as exc:  # pragma: no cover - defensive HTTP mapping
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/vectorstore/upload")
async def upload_document(
    file: UploadFile = File(...),
    ai_client: AIClient = Depends(get_ai_client),
) -> Dict[str, Any]:
    """Forward a document to the ai_service vectorstore."""
    try:
        return await ai_client.upload_document(file)
    except Exception as exc:  # pragma: no cover - defensive HTTP mapping
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/query", response_model=QueryResponse)
async def query_ai(
    req: QueryRequest,
    ai_client: AIClient = Depends(get_ai_client),
) -> QueryResponse:
    """Proxy a user query to ai_service and repackage the answer."""
    try:
        answer = await ai_client.query(req.query)
        return QueryResponse(answer=answer)
    except Exception as exc:  # pragma: no cover - defensive HTTP mapping
        raise HTTPException(status_code=500, detail=str(exc)) from exc
