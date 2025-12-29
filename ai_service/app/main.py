"""FastAPI application entrypoint for the AI microservice."""
import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routers import ping, llm, vectorstore


def create_app() -> FastAPI:
    """Create and configure the FastAPI app with routers and middleware."""
    settings = get_settings()

    LOG_LEVEL = logging.INFO
    logging.basicConfig(
        level=LOG_LEVEL,
        format="LOG - [%(levelname)s] %(name)s:-> %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    
    app = FastAPI(title=settings.AI_SERVICE_APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten in prod if callers are known
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ping.router, prefix="/healthz", tags=["healthz"])
    app.include_router(vectorstore.router, prefix="/v1/vectorstore", tags=["vector"])
    app.include_router(llm.router, prefix="/v1/query", tags=["ai"])

    return app


app = create_app()
