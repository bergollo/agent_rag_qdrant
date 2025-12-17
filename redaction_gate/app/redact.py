import re
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Finding:
    kind: str
    start: int
    end: int
    replacement: str
    confidence: float = 1.0

# Conservative patterns (tune to your needs)
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
API_KEY = re.compile(r"\b(?:sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16})\b")  # OpenAI-ish + AWS access key
CREDIT_CARD = re.compile(r"\b(?:\d[ -]*?){13,19}\b")

PATTERNS = [
    ("email", EMAIL),
    ("phone", PHONE),
    ("ssn", SSN),
    ("ip", IPV4),
    ("api_key", API_KEY),
    ("credit_card", CREDIT_CARD),
]

def find_pii(text: str) -> List[Finding]:
    findings: List[Finding] = []
    for kind, pat in PATTERNS:
        for m in pat.finditer(text):
            findings.append(Finding(kind=kind, start=m.start(), end=m.end(),
                                    replacement=f"[REDACTED:{kind}]"))
    # merge overlaps by sorting desc start so replacement indices are stable
    findings.sort(key=lambda f: (f.start, -(f.end - f.start)))
    merged: List[Finding] = []
    last_end = -1
    for f in findings:
        if f.start >= last_end:
            merged.append(f)
            last_end = f.end
    return merged

def apply_redactions(text: str, findings: List[Finding]) -> Tuple[str, Dict[str, int]]:
    # apply from end -> start to keep indices valid
    counts: Dict[str, int] = {}
    out = text
    for f in sorted(findings, key=lambda x: x.start, reverse=True):
        out = out[:f.start] + f.replacement + out[f.end:]
        counts[f.kind] = counts.get(f.kind, 0) + 1
    return out, counts

def classify_level(counts: Dict[str, int]) -> str:
    if counts.get("api_key", 0) or counts.get("ssn", 0) or counts.get("credit_card", 0):
        return "high"
    if counts.get("email", 0) or counts.get("phone", 0) or counts.get("ip", 0):
        return "medium"
    return "low"
