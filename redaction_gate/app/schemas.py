from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class Actor(BaseModel):
    user_id: str
    tenant_id: str
    roles: List[str] = Field(default_factory=list)

class RedactTextIn(BaseModel):
    request_id: str
    actor: Actor
    text: str
    policy: Dict[str, Any] = Field(default_factory=dict)  # overrides or hints (optional)
    purpose: str = "log"  # log|tool|export|memory
    return_map: bool = True

class RedactionItem(BaseModel):
    kind: str                  # email|phone|ssn|api_key|url|ip|credit_card|name?
    start: int
    end: int
    replacement: str           # e.g. "[REDACTED:email]"
    confidence: float = 1.0

class RedactTextOut(BaseModel):
    redacted_text: str
    redactions: List[RedactionItem] = Field(default_factory=list)
    counts: Dict[str, int] = Field(default_factory=dict)
    policy_version: str = "v0"

class ClassifySensitivityIn(BaseModel):
    request_id: str
    actor: Actor
    text: str

class ClassifySensitivityOut(BaseModel):
    level: str                 # low|medium|high
    reasons: List[str] = Field(default_factory=list)
    policy_version: str = "v0"
