"""Vector store document ingestion endpoints."""

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile

from app.api.deps import get_openai_client
from app.services.open_ai import OpenAIClient


router = APIRouter()

# class UploadRequest(BaseModel):
#     upload: UploadFile

@router.post("/upload")
async def vector_upload(
    file: UploadFile = File(...),
    ai_client: OpenAIClient = Depends(get_openai_client),
):
    """Store the uploaded document in Qdrant after extracting embeddings."""
    try:
        return await ai_client.qdrant_upload(file)
    except Exception as exc:  # pragma: no cover - defensive HTTP error mapping
        raise HTTPException(status_code=500, detail=str(exc)) from exc
