import pytest

from app.redact import apply_redactions, classify_level, find_pii


def test_find_pii_and_apply_redactions():
    text = "Contact me at jane@example.com or 555-123-4567."

    findings = find_pii(text)
    redacted, counts = apply_redactions(text, findings)

    assert redacted.startswith("Contact me at [REDACTED:email]")
    assert "[REDACTED:phone]" in redacted
    assert counts == {"email": 1, "phone": 1}


@pytest.mark.parametrize(
    ("counts", "expected"),
    [
        ({"api_key": 1}, "high"),
        ({"credit_card": 2}, "high"),
        ({"email": 1}, "medium"),
        ({"phone": 1}, "medium"),
        ({}, "low"),
    ],
)
def test_classify_level(counts, expected):
    assert classify_level(counts) == expected
