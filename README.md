# ClauseGuard ⚖️

**A red-flag linter for contracts.** Paste any agreement — NDA, MSA, lease, vendor contract —
and ClauseGuard flags the **risky clauses** and the **protections that are missing**, with a
plain-English reason and a suggested fix for each.

> Built for the 99% of small businesses and freelancers who sign contracts without a lawyer.

```bash
clauseguard contract.pdf
```

```
# ClauseGuard Report — contract.pdf

**Overall risk: CRITICAL**  (score 22)

- 🚩 Risky clauses found: 8
- ❓ Expected clauses missing: 1

## 🚩 Risky clauses
### 🔴 Unlimited liability  (HIGH)
- Why it matters: Your liability is uncapped — exposure could exceed the contract value.
- Suggested fix: Negotiate a liability cap (e.g., fees paid in the last 12 months).
...
```

## What it catches

**Risky clauses present** — auto-renewal, unlimited liability, one-sided termination,
broad indemnity, full IP assignment, non-compete, exclusivity, unilateral amendment,
perpetual confidentiality, liquidated damages, and more.

**Protections missing** — no liability cap, no confidentiality clause, no termination
rights, no governing law, no dispute resolution, no defined term.

Every finding comes with **why it matters** and a **suggested fix** — and an overall
risk score so you know whether to sign, negotiate, or call a lawyer.

## Install

```bash
pip install clauseguard            # core (.txt)
pip install "clauseguard[pdf]"     # + scan PDFs
pip install "clauseguard[llm]"     # + AI-written plain-English summary
```

## Usage

```bash
clauseguard agreement.txt              # markdown report to stdout
clauseguard agreement.pdf --json       # machine-readable JSON
clauseguard agreement.pdf --out report.md
```

Exit code is non-zero for HIGH/CRITICAL risk — so you can **block risky contracts in CI**
or an approval workflow.

```python
from clauseguard.analyzer import analyze
report = analyze(open("contract.txt").read())
print(report.risk_level, report.risk_score)
```

## How it works

ClauseGuard runs a transparent rule engine (`clauseguard/rules.py`) over the contract text:
each rule has detection patterns, a severity, an explanation, and a fix. Rules are data —
add or tune them without touching logic. No data leaves your machine.

## Who it's for

Freelancers, agencies, founders, and SMBs signing contracts without in-house legal — plus
legal teams who want a fast first-pass triage.

## ⚠️ Disclaimer

ClauseGuard highlights common contract risks to help you ask better questions. It is **not
legal advice**. For anything important, review with a qualified lawyer.

## License

MIT
