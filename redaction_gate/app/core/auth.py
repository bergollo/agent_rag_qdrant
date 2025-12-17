# services/policy_gate/app/auth.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import os

POLICY_GATE_TOKEN = os.getenv("POLICY_GATE_TOKEN", "dev-token")

class BearerAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("Auth Middleware: Checking authorization for path:", request.url.path)
        if request.url.path.startswith("/mcp"):
            auth = request.headers.get("authorization") or ""
            if not auth.startswith("Bearer "):
                return JSONResponse({"detail": "Missing bearer token"}, status_code=401)
            token = auth.removeprefix("Bearer ").strip()
            if token != POLICY_GATE_TOKEN:
                return JSONResponse({"detail": "Invalid token"}, status_code=403)
        print("Auth Middleware: Authorization successful")
        return await call_next(request)
