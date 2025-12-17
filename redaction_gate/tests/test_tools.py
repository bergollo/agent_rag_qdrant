import pytest

from app.models import RedactionEvent
from app.tools import redact_tools
from app.tools.redact_tools import register_mcp_tools


class MCPStub:
    def __init__(self):
        self.tools = {}

    def tool(self, description: str = ""):
        def decorator(func):
            self.tools[func.__name__] = func
            return func

        return decorator


class _StubSession:
    def __init__(self, events):
        self.events = events

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def add(self, obj):
        self.events.append(obj)

    async def commit(self):
        return None


def _patch_session(monkeypatch):
    events = []

    def factory():
        return _StubSession(events)

    monkeypatch.setattr(redact_tools, "SessionLocal", factory)
    return events


@pytest.mark.asyncio
async def test_redact_text_tool_writes_event(monkeypatch):
    events = _patch_session(monkeypatch)
    mcp = MCPStub()
    register_mcp_tools(mcp)
    payload = {
        "request_id": "req-1",
        "actor": {"user_id": "alice", "tenant_id": "t1"},
        "text": "email jane@example.com",
        "return_map": True,
    }

    result = await mcp.tools["redact_text"](payload)

    assert result["counts"] == {"email": 1}
    assert "[REDACTED:email]" in result["redacted_text"]
    assert result["redactions"][0]["kind"] == "email"

    assert len(events) == 1
    event = events[0]
    assert isinstance(event, RedactionEvent)
    assert event.action == "redact_text"
    assert event.summary_json["counts"]["email"] == 1


@pytest.mark.asyncio
async def test_classify_sensitivity_tool_records_level(monkeypatch):
    events = _patch_session(monkeypatch)
    mcp = MCPStub()
    register_mcp_tools(mcp)
    payload = {
        "request_id": "req-2",
        "actor": {"user_id": "bob", "tenant_id": "t2"},
        "text": "api key sk-ABCDEFGHIJKLMNOP",
    }

    result = await mcp.tools["classify_sensitivity"](payload)

    assert result["level"] == "high"
    assert "api_key" in result["reasons"]

    assert len(events) == 1
    assert events[0].action == "classify"
