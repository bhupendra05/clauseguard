"""Render a Report as markdown or JSON."""
from __future__ import annotations

from .models import Report, Severity

_EMOJI = {Severity.HIGH: "🔴", Severity.MEDIUM: "🟠", Severity.LOW: "🟡"}


def to_markdown(report: Report) -> str:
    title = report.document or "Contract"
    risky, missing = report.risky, report.missing
    lines = [
        f"# ClauseGuard Report — {title}",
        "",
        f"**Overall risk: {report.risk_level.value}**  (score {report.risk_score})",
        "",
        f"- 🚩 Risky clauses found: **{len(risky)}**",
        f"- ❓ Expected clauses missing: **{len(missing)}**",
        "",
    ]

    if risky:
        lines.append("## 🚩 Risky clauses")
        for f in risky:
            lines.append(f"### {_EMOJI[f.severity]} {f.name}  ({f.severity.value})")
            lines.append(f"- **Why it matters:** {f.explanation}")
            lines.append(f"- **Suggested fix:** {f.suggestion}")
            if f.snippet:
                lines.append(f'- **Found:** "{f.snippet}"')
            lines.append("")

    if missing:
        lines.append("## ❓ Missing / expected clauses")
        for f in missing:
            lines.append(f"### {_EMOJI[f.severity]} {f.name} — not found  ({f.severity.value})")
            lines.append(f"- **Why it matters:** {f.explanation}")
            lines.append(f"- **Suggested fix:** {f.suggestion}")
            lines.append("")

    if not findings_exist(report):
        lines.append("✅ No risky clauses or missing protections detected.")
        lines.append("")

    lines.append("---")
    lines.append(
        "_ClauseGuard flags common contract risks to help you ask better questions. "
        "It is not legal advice — review anything important with a qualified lawyer._"
    )
    return "\n".join(lines)


def findings_exist(report: Report) -> bool:
    return bool(report.findings)


def to_json(report: Report) -> str:
    return report.model_dump_json(indent=2)
