"""The analysis engine — run the rule library over contract text."""
from __future__ import annotations

import re
from typing import List, Optional

from .models import Finding, FindingType, Report, RiskLevel, Severity
from .rules import EXPECTED_RULES, RISKY_RULES

_SEVERITY_WEIGHT = {Severity.LOW: 1, Severity.MEDIUM: 2, Severity.HIGH: 3}
_SEVERITY_ORDER = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}


def _search(patterns: List[str], text: str) -> Optional["re.Match[str]"]:
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m
    return None


def _snippet(text: str, match: "re.Match[str]", width: int = 90) -> str:
    start = max(0, match.start() - width // 2)
    end = min(len(text), match.end() + width // 2)
    s = re.sub(r"\s+", " ", text[start:end]).strip()
    return ("…" if start > 0 else "") + s + ("…" if end < len(text) else "")


def _risk_level(score: int) -> RiskLevel:
    if score >= 12:
        return RiskLevel.CRITICAL
    if score >= 7:
        return RiskLevel.HIGH
    if score >= 3:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def analyze(text: str, document: str = "") -> Report:
    """Scan contract text and return a Report of risky + missing clauses."""
    findings: List[Finding] = []

    for rule in RISKY_RULES:
        m = _search(rule.patterns, text)
        if m:
            findings.append(Finding(
                id=rule.id, name=rule.name, type=FindingType.RISKY,
                severity=rule.severity, explanation=rule.explanation,
                suggestion=rule.suggestion, snippet=_snippet(text, m),
            ))

    for rule in EXPECTED_RULES:
        if _search(rule.patterns, text) is None:
            findings.append(Finding(
                id=rule.id, name=rule.name, type=FindingType.MISSING,
                severity=rule.severity, explanation=rule.explanation,
                suggestion=rule.suggestion, snippet=None,
            ))

    score = sum(_SEVERITY_WEIGHT[f.severity] for f in findings)
    findings.sort(key=lambda f: (f.type is FindingType.MISSING, _SEVERITY_ORDER[f.severity]))
    return Report(document=document, findings=findings, risk_score=score,
                  risk_level=_risk_level(score))
