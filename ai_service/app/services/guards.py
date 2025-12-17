# services/ai_service/guards.py
from typing import Dict, Any
from .redaction_mcp import build_redaction_client

async def ensure_redacted(*, request_id: str, actor: Dict[str, Any], text: str, purpose: str) -> str:
    client = build_redaction_client()
    tools = await client.get_tools()
    out = await tools["redact_text"].ainvoke({
        "request_id": request_id,
        "actor": actor,
        "text": text,
        "purpose": purpose,      # log|tool|export|memory
        "return_map": False,
    })
    return out["redacted_text"]
