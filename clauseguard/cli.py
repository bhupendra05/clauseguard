"""Command-line entrypoint: `clauseguard`."""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional, Sequence

from .analyzer import analyze
from .extract import read_document
from .models import RiskLevel
from .report import to_json, to_markdown

# Non-zero exit for HIGH/CRITICAL so the tool can gate CI / approval workflows.
_EXIT = {RiskLevel.LOW: 0, RiskLevel.MEDIUM: 0, RiskLevel.HIGH: 1, RiskLevel.CRITICAL: 2}


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="clauseguard",
        description="Scan a contract for risky clauses and missing protections.",
    )
    p.add_argument("file", help="Path to the contract (.txt, .md, or .pdf)")
    p.add_argument("--json", action="store_true", help="Output JSON instead of markdown")
    p.add_argument("--out", default=None, help="Write the report to a file")
    args = p.parse_args(argv)

    try:
        text = read_document(args.file)
    except (FileNotFoundError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3

    report = analyze(text, document=os.path.basename(args.file))
    rendered = to_json(report) if args.json else to_markdown(report)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"Report written to {args.out}  (risk: {report.risk_level.value})")
    else:
        print(rendered)
    return _EXIT[report.risk_level]


if __name__ == "__main__":
    sys.exit(main())
