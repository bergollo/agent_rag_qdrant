"""FastAPI app factory for the backend gateway service."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.api.routers import ping, ai


def create_app() -> FastAPI:
    """Configure middleware, routers, and static file serving."""
    settings = get_settings()
    app = FastAPI(title=settings.BACKEND_APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten in prod once caller domains are known
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ping.router, prefix="/api/healthz", tags=["healthz"])
    app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

    # Serve the compiled React app (copied into backend/static during deployment).
    # app.mount("/", StaticFiles(directory="static", html=True), name="static")

    return app


app = create_app()
