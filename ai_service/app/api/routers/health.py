"""Simple health-check endpoint."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check() -> dict[str, str]:
    """Provide a quick readiness/health probe response."""
    return {"status": "ok", "service": "ai_service"}
