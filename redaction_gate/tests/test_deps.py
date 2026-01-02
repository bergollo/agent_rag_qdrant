import os

import pytest
from fastapi import HTTPException

from app.core import deps


def test_require_bearer_missing_header():
    with pytest.raises(HTTPException) as exc:
        deps.require_bearer(None)
    assert exc.value.status_code == 401


def test_require_bearer_invalid_token(monkeypatch):
    monkeypatch.setenv("REDACTION_GATE_TOKEN", "expected")
    monkeypatch.setenv("REDACTION_DB_URL", os.environ["REDACTION_DB_URL"])

    with pytest.raises(HTTPException) as exc:
        deps.require_bearer("Bearer nope")
    assert exc.value.status_code == 403


def test_require_bearer_valid_token(monkeypatch):
    token = "expected"
    monkeypatch.setenv("REDACTION_GATE_TOKEN", token)
    monkeypatch.setenv("REDACTION_DB_URL", os.environ["REDACTION_DB_URL"])

    assert deps.require_bearer(f"Bearer {token}") is None
