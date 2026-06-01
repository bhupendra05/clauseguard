"""Data models for ClauseGuard findings and reports."""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FindingType(str, Enum):
    RISKY = "risky_clause_present"
    MISSING = "expected_clause_missing"


class Finding(BaseModel):
    id: str
    name: str
    type: FindingType
    severity: Severity
    explanation: str
    suggestion: str
    snippet: Optional[str] = None


class Report(BaseModel):
    document: str = ""
    findings: List[Finding] = Field(default_factory=list)
    risk_score: int = 0
    risk_level: RiskLevel = RiskLevel.LOW

    @property
    def risky(self) -> List[Finding]:
        return [f for f in self.findings if f.type is FindingType.RISKY]

    @property
    def missing(self) -> List[Finding]:
        return [f for f in self.findings if f.type is FindingType.MISSING]
