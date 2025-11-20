"""Basic health-check endpoint for the backend API."""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health_check() -> dict[str, str]:
    """Return a simple status payload for uptime checks."""
    return {"status": "ok"}
