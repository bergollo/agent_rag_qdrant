# ./ai_service/app/services/redaction_mcp.py

import os
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.config import get_settings

import logging
logger = logging.getLogger("ai_service")

def build_redaction_client() -> MultiServerMCPClient:
    logger.info("Building Redaction MCP Client...")
    settings = get_settings()
    url = settings.REDACTION_GATE_URL
    return MultiServerMCPClient(
        {
            "redaction": {
                "transport": "http",
                "url": url,
                "headers": {"Authorization": f"Bearer {settings.REDACTION_GATE_TOKEN}"},
                "timeout": settings.MCP_TIMEOUT_S,
            }
        },
        tool_name_prefix=True,
    )
