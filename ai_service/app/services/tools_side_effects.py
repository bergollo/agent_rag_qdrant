# services/ai_service/tools_side_effects.py
import os
import httpx
from typing import Dict, Any
from pydantic import BaseModel, Field, AnyHttpUrl

from langchain_core.tools import tool
from .guards import ensure_redacted

ALLOWED_WEBHOOK_HOSTS = set(os.getenv("ALLOWED_WEBHOOK_HOSTS", "hooks.mycorp.com").split(","))

class SendWebhookArgs(BaseModel):
    request_id: str
    actor: Dict[str, Any]
    url: AnyHttpUrl
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

@tool(
    "safe_send_webhook",
    args_schema=SendWebhookArgs,
    description=(
        "Send text to an approved external webhook destination in a safe way. "
        "This tool ALWAYS redacts PII and secrets from the text before sending. "
        "Use this when the user explicitly asks to notify, post, or send information "
        "to an external system (e.g. Slack, Teams, internal webhooks). "
        "The destination must be on the approved allowlist. "
        "Do NOT use this tool for storage or internal logging."
    ),
)
async def safe_send_webhook(request_id: str, actor: Dict[str, Any], url: str, text: str, metadata: Dict[str, Any] | None = None):
    print(f"safe_send_webhook called with url: {url}")  # Debug statement
    # 1) allowlist destination
    host = httpx.URL(url).host
    if host not in ALLOWED_WEBHOOK_HOSTS:
        return {"ok": False, "error": f"Destination not allowed: {host}"}

    # 2) redact before sending
    redacted = await ensure_redacted(request_id=request_id, actor=actor, text=text, purpose="tool")

    # 3) send
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json={"text": redacted, "metadata": metadata or {}})
        return {"ok": r.is_success, "status_code": r.status_code}


class StoreMemoryArgs(BaseModel):
    request_id: str
    actor: Dict[str, Any]
    key: str
    value: str
    scope: str = "user"

@tool(
    "safe_store_memory",
    args_schema=StoreMemoryArgs,
    description=(
        "Store long-lived information or preferences for future conversations. "
        "This tool ALWAYS redacts PII and secrets before storing data. "
        "Use this only for durable facts the user wants remembered "
        "(e.g. preferences, project context, decisions), not for transient chat logs. "
        "Choose an appropriate scope (user, tenant, or session). "
        "Do NOT store sensitive identifiers, credentials, or private data."
    ),
)
async def safe_store_memory(request_id: str, actor: Dict[str, Any], key: str, value: str, scope: str = "user"):
    print(f"safe_store_memory called with key: {key}, scope: {scope}")  # Debug statement
    # 1) redact before storing
    redacted = await ensure_redacted(request_id=request_id, actor=actor, text=value, purpose="memory")

    # 2) store (replace with your DB call)
    # await memory_db.put(tenant_id=actor["tenant_id"], user_id=actor["user_id"], key=key, value=redacted, scope=scope)
    return {"ok": True, "stored_key": key, "scope": scope}
