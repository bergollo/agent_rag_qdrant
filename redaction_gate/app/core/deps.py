"""FastAPI dependency helpers and auth utilities."""

import hashlib
import logging

from fastapi import Header, HTTPException, Request
from starlette.responses import JSONResponse

from app.core.config import get_settings

logger = logging.getLogger("mcp.auth")


def get_settings_dep():
    """Thin wrapper to keep dependency injection explicit for tests."""
    return get_settings()


def actor_hash(user_id: str) -> str:
    """Stable hash for a user identifier to avoid storing raw PII."""
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()


def require_bearer(authorization: str | None = Header(default=None)) -> None:
    """Validate bearer tokens for FastAPI dependencies."""
    settings = get_settings_dep()
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    if token != settings.REDACTION_GATE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")


def mcp_auth_middleware():
    """
    Factory that returns a FastAPI-compatible middleware function for MCP routes.
    """

    async def middleware(request: Request, call_next):
        settings = get_settings()
        if request.url.path.startswith("/mcp"):
            auth = request.headers.get("authorization", "")
            if not auth.startswith("Bearer "):
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)

            token = auth.removeprefix("Bearer ").strip()
            if token != settings.REDACTION_GATE_TOKEN:
                return JSONResponse({"detail": "Forbidden"}, status_code=403)

        return await call_next(request)

    return middleware
