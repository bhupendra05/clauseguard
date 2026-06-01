"""Document text extraction — plain text now, PDF when pypdf is installed."""
from __future__ import annotations

import os


def read_document(path: str) -> str:
    """Read a contract file to text. Supports .txt/.md directly and .pdf via pypdf."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return _read_pdf(path)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _read_pdf(path: str) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise RuntimeError(
            "PDF support needs pypdf. Install with: pip install 'clauseguard[pdf]'"
        ) from e
    reader = PdfReader(path)
    return "\n".join((page.extract_text() or "") for page in reader.pages)
