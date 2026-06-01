"""The rule library — risky clauses to flag, and expected clauses that should exist.

Rules are plain data: detection patterns (case-insensitive regex), a severity, a
plain-English explanation, and a suggested fix. Add or tune rules here without
touching the analyzer logic.
"""
from __future__ import annotations

from typing import List, NamedTuple

from .models import Severity


class RiskyRule(NamedTuple):
    id: str
    name: str
    severity: Severity
    patterns: List[str]
    explanation: str
    suggestion: str


class ExpectedRule(NamedTuple):
    id: str
    name: str
    severity: Severity  # severity applied when this clause is MISSING
    patterns: List[str]
    explanation: str
    suggestion: str


RISKY_RULES: List[RiskyRule] = [
    RiskyRule(
        "auto_renewal", "Auto-renewal", Severity.HIGH,
        [r"automatically renew", r"auto-?renew", r"evergreen",
         r"renew\w*\s+for\s+(successive|additional)"],
        "The contract renews automatically — you can be locked into another term if you "
        "miss the cancellation window.",
        "Add a clear non-renewal notice window (e.g., 30 days before term end).",
    ),
    RiskyRule(
        "unlimited_liability", "Unlimited liability", Severity.HIGH,
        [r"unlimited liability", r"without (any )?limitation of liability",
         r"liability (shall|will) not be limited"],
        "Your liability is uncapped — exposure could far exceed the contract value.",
        "Negotiate a liability cap (e.g., fees paid in the last 12 months).",
    ),
    RiskyRule(
        "broad_indemnity", "Broad indemnification", Severity.HIGH,
        [r"indemnif\w+.{0,40}(any and all|all claims)", r"hold harmless"],
        "Broad indemnity can make you liable for a wide range of third-party claims.",
        "Limit indemnity to direct claims caused by your own breach or negligence.",
    ),
    RiskyRule(
        "ip_assignment", "Full IP assignment", Severity.HIGH,
        [r"assigns?\s+all\s+right.{0,12}title", r"work made for hire",
         r"all intellectual property.{0,25}(assigned|belong|vest)"],
        "You may be assigning away all IP — potentially including pre-existing or "
        "background IP, not just the deliverables.",
        "Carve out background/pre-existing IP; assign only the specific deliverables.",
    ),
    RiskyRule(
        "non_compete", "Non-compete", Severity.MEDIUM,
        [r"non-?compete", r"shall not\s+.{0,20}compete", r"non-?competition"],
        "A non-compete can restrict your future business and may be hard to escape.",
        "Narrow the scope, geography, and duration; confirm it is enforceable locally.",
    ),
    RiskyRule(
        "unilateral_termination", "One-sided termination", Severity.MEDIUM,
        [r"terminate.{0,30}sole discretion", r"terminate for convenience",
         r"may terminate.{0,20}at any time"],
        "The other party can end the deal at will, leaving you exposed.",
        "Make termination rights mutual, with reasonable written notice.",
    ),
    RiskyRule(
        "exclusivity", "Exclusivity", Severity.MEDIUM,
        [r"\bexclusiv", r"sole (provider|supplier|source)"],
        "Exclusivity can block you from working with other clients or partners.",
        "Limit exclusivity scope/territory or tie it to minimum commitments.",
    ),
    RiskyRule(
        "unilateral_amendment", "Unilateral amendment", Severity.MEDIUM,
        [r"(amend|modify|change)\w*.{0,30}(sole discretion|at any time without)"],
        "The other side can change the terms unilaterally, even after signing.",
        "Require mutual written consent for any amendment.",
    ),
    RiskyRule(
        "liquidated_damages", "Liquidated damages / penalty", Severity.MEDIUM,
        [r"liquidated damages", r"\bpenalt(y|ies)\b"],
        "Pre-set penalty amounts can be costly and may exceed actual loss.",
        "Tie damages to actual, provable loss; review enforceability.",
    ),
    RiskyRule(
        "perpetual_confidentiality", "Perpetual confidentiality", Severity.LOW,
        [r"in perpetuity", r"survive indefinitely", r"perpetual"],
        "Confidentiality with no end date is burdensome and often unnecessary.",
        "Set a fixed survival period (e.g., 3–5 years after termination).",
    ),
    RiskyRule(
        "late_payment_interest", "Late-payment interest", Severity.LOW,
        [r"interest.{0,20}per month", r"late (fee|payment).{0,25}(charge|interest|%)"],
        "Late-payment interest terms — confirm the rate is reasonable and capped.",
        "Cap the interest rate and align it with market norms.",
    ),
]


EXPECTED_RULES: List[ExpectedRule] = [
    ExpectedRule(
        "limitation_of_liability", "Limitation of liability (cap)", Severity.HIGH,
        [r"limitation of liability", r"liability.{0,30}(shall not exceed|capped|limited to)",
         r"aggregate liability"],
        "No liability cap was found — your financial exposure may be unlimited.",
        "Add a clause capping each party's aggregate liability.",
    ),
    ExpectedRule(
        "confidentiality", "Confidentiality clause", Severity.MEDIUM,
        [r"confidential"],
        "No confidentiality clause was found to protect shared information.",
        "Add a mutual confidentiality clause with a defined survival period.",
    ),
    ExpectedRule(
        "termination", "Termination clause", Severity.MEDIUM,
        [r"terminat"],
        "No termination clause was found — it is unclear how either side exits.",
        "Add termination for convenience and for cause, each with notice periods.",
    ),
    ExpectedRule(
        "governing_law", "Governing law", Severity.LOW,
        [r"governing law", r"governed by the laws"],
        "No governing-law clause was found.",
        "Specify the governing law and jurisdiction for the contract.",
    ),
    ExpectedRule(
        "dispute_resolution", "Dispute resolution", Severity.LOW,
        [r"arbitration", r"jurisdiction", r"dispute"],
        "No dispute-resolution mechanism was found.",
        "Add arbitration or a clearly chosen court/jurisdiction.",
    ),
    ExpectedRule(
        "term_duration", "Defined term / duration", Severity.LOW,
        [r"term of this agreement", r"effective date",
         r"shall (commence|remain in (force|effect))"],
        "No clear term or duration was found.",
        "State the start date and the duration of the agreement.",
    ),
]
