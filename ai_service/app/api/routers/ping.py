"""Simple ping-check endpoint."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def ping_check() -> dict[str, str]:
    """Provide a quick readiness/ping probe response."""
    return {"status": "ok", "service": "ai_service"}
