"""Tests for the ClauseGuard analysis engine."""
from clauseguard.analyzer import analyze
from clauseguard.models import FindingType, RiskLevel

RISKY_SAMPLE = """
1. Term. Effective as of the Effective Date, this Agreement shall remain in force for two
years and shall automatically renew for successive one-year terms unless terminated.
2. Confidentiality. Each party shall keep all non-public information confidential. These
obligations shall survive in perpetuity.
3. Intellectual Property. The Vendor assigns all right, title and interest in the work
product, which shall be deemed work made for hire.
4. Indemnification. The Vendor shall indemnify and hold harmless the Company from any and
all claims.
5. Liability. The Vendor shall bear unlimited liability for any breach.
6. Non-Compete. The Vendor shall not compete with the Company for three years.
7. Exclusivity. The Vendor shall be the exclusive provider of services.
8. Termination. The Company may terminate at its sole discretion.
9. Governing Law. Governed by the laws of Delaware; disputes resolved by arbitration.
"""

CLEAN_SAMPLE = (
    "This Agreement is effective as of the Effective Date for a term of one year. "
    "Each party shall keep information confidential for three years after termination. "
    "Either party may terminate this Agreement with thirty days written notice. "
    "The aggregate liability of each party shall not exceed the fees paid in the prior "
    "twelve months. This Agreement is governed by the laws of India and any dispute shall "
    "be resolved by arbitration seated in Mumbai."
)


def test_detects_core_risky_clauses():
    r = analyze(RISKY_SAMPLE, "sample")
    ids = {f.id for f in r.risky}
    expected = {
        "auto_renewal", "unlimited_liability", "ip_assignment", "broad_indemnity",
        "non_compete", "exclusivity", "unilateral_termination", "perpetual_confidentiality",
    }
    assert expected <= ids


def test_flags_missing_liability_cap():
    r = analyze(RISKY_SAMPLE, "sample")
    assert "limitation_of_liability" in {f.id for f in r.missing}


def test_risky_sample_is_critical():
    r = analyze(RISKY_SAMPLE, "sample")
    assert r.risk_level is RiskLevel.CRITICAL
    assert r.risk_score >= 12


def test_clean_contract_is_low_risk():
    r = analyze(CLEAN_SAMPLE, "clean")
    assert r.risk_level in (RiskLevel.LOW, RiskLevel.MEDIUM)
    # It has a liability cap, so that protection is NOT reported missing.
    assert "limitation_of_liability" not in {f.id for f in r.missing}
    # And no risky clauses should trip on a clean contract.
    assert len(r.risky) == 0


def test_every_finding_has_help_text():
    r = analyze(RISKY_SAMPLE, "sample")
    assert r.findings
    for f in r.findings:
        assert f.explanation and f.suggestion
        if f.type is FindingType.RISKY:
            assert f.snippet


def test_empty_text_reports_missing_clauses():
    r = analyze("", "empty")
    # Everything expected is absent -> all expected rules fire as missing.
    assert len(r.missing) >= 5
    assert len(r.risky) == 0
