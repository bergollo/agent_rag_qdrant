from mcp.server.fastmcp import FastMCP

from app.db import SessionLocal
from app.models import RedactionEvent
from app.schemas import (
    RedactTextIn, RedactTextOut, RedactionItem,
    ClassifySensitivityIn, ClassifySensitivityOut
)
from app.redact import find_pii, apply_redactions, classify_level

from app.core.deps import get_settings, actor_hash

import logging
logger = logging.getLogger("mcp.tools")

def register_mcp_tools(mcp_server: FastMCP):
    settings = get_settings()
    
    @mcp_server.tool(description="Redact common PII/secrets from text before storing/sending.")
    async def redact_text(payload: dict) -> dict:
        logger.info("MCP redact_text called")
        logger.info("text= %s", payload.get("text", "")[:50])  # Log first 50 chars of text

        data = RedactTextIn(**payload)

        findings = find_pii(data.text)
        redacted, counts = apply_redactions(data.text, findings)

        # audit (store no raw text)
        async with SessionLocal() as session:
            session.add(RedactionEvent(
                request_id=data.request_id,
                tenant_id=data.actor.tenant_id,
                actor_id_hash=actor_hash(data.actor.user_id),
                policy_version=settings.REDACTION_POLICY_VERSION,
                action="redact_text",
                input_len=len(data.text),
                output_len=len(redacted),
                summary_json={"counts": counts, "purpose": data.purpose},
            ))
            await session.commit()

        print("data.text:", data.text)  # Debug statement
        out = RedactTextOut(
            redacted_text=redacted,
            redactions=[
                RedactionItem(
                    kind=f.kind, start=f.start, end=f.end,
                    replacement=f.replacement, confidence=f.confidence
                ) for f in findings
            ] if data.return_map else [],
            counts=counts,
            policy_version=settings.REDACTION_POLICY_VERSION,
        )
        return out.model_dump()

    @mcp_server.tool(description="Classify sensitivity level (low/medium/high) based on detected PII/secrets.")
    async def classify_sensitivity(payload: dict) -> dict:

        print("Payload received for classify_sensitivity:", payload)  # Debug statement

        data = ClassifySensitivityIn(**payload)
        findings = find_pii(data.text)
        _, counts = apply_redactions(data.text, findings)
        level = classify_level(counts)

        async with SessionLocal() as session:
            session.add(RedactionEvent(
                request_id=data.request_id,
                tenant_id=data.actor.tenant_id,
                actor_id_hash=actor_hash(data.actor.user_id),
                policy_version=settings.REDACTION_POLICY_VERSION,
                action="classify",
                input_len=len(data.text),
                output_len=len(data.text),
                summary_json={"counts": counts, "level": level},
            ))
            await session.commit()

        return ClassifySensitivityOut(level=level, reasons=list(counts.keys()), policy_version=settings.REDACTION_POLICY_VERSION).model_dump()
