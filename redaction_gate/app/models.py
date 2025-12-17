from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, JSON, Text
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc)

class Base(DeclarativeBase):
    pass

class RedactionEvent(Base):
    __tablename__ = "redaction_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

    tenant_id: Mapped[str] = mapped_column(String(128), index=True)
    actor_id_hash: Mapped[str] = mapped_column(String(128), index=True)

    policy_version: Mapped[str] = mapped_column(String(32), default="v0")
    action: Mapped[str] = mapped_column(String(32), default="redact_text")  # redact_text|classify

    input_len: Mapped[int] = mapped_column(Integer)
    output_len: Mapped[int] = mapped_column(Integer)

    # only store minimal metadata—no raw text
    summary_json: Mapped[dict] = mapped_column(JSON, default=dict)  # counts by type, etc.

class TenantRedactionPolicy(Base):
    __tablename__ = "tenant_redaction_policies"

    tenant_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    policy_json: Mapped[dict] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
