# redaction_gate/app/main.py
import logging
import sys

import contextlib
from typing import Any

from fastapi import FastAPI, Depends
from fastapi.routing import APIRouter
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from .tools.redact_tools import register_mcp_tools
from .db import engine
from .models import Base

from .core.deps import mcp_auth_middleware


def create_app() -> FastAPI:
    """
    Expose health + MCP endpoint from a single FastAPI app.

    IMPORTANT:
    - streamable_http_app() serves the MCP endpoint at /mcp by default
    - mounting it at /mcp => full path becomes /mcp/mcp
    """
    # LOG_LEVEL = logging.DEBUG
    # logging.basicConfig(
    #     level=LOG_LEVEL,
    #     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    #     handlers=[logging.StreamHandler(sys.stdout)],
    # )
    LOG_LEVEL = logging.INFO
    logging.basicConfig(
        level=LOG_LEVEL,
        format="BERGO - [%(levelname)s] %(name)s:-> %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    mcp = FastMCP(
        "RedactionGate",
        stateless_http=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=False
            # allow docker-compose service DNS name
            # allowed_hosts=["redaction_gate", "localhost", "127.0.0.1"],
            # (optional) if your client sends Origin, you may need to allow it too
            # allowed_origins=["http://redaction_gate:8002", "http://localhost:8002"],
        ),
    )

    register_mcp_tools(mcp)

    # Build the MCP ASGI sub-app
    mcp_app = mcp.streamable_http_app()

    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        # Your DB startup
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # MCP session manager lifecycle (recommended even in many stateless setups)
        # See "mount multiple servers" example pattern in MCP docs. :contentReference[oaicite:3]{index=3}
        async with contextlib.AsyncExitStack() as stack:
            await stack.enter_async_context(mcp.session_manager.run())
            yield

    app = FastAPI(title="Redaction Gate (MCP)", lifespan=lifespan)

    app.middleware("http")(mcp_auth_middleware())
    # Mount MCP sub-app
    app.mount("/mcp", mcp_app)

    @app.get("/healthz")
    def healthz():
        return {"ok": True}

    return app

app = create_app()
