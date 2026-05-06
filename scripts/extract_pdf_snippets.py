"""Extract leading pages + metadata from PDFs under ./PDF for KB indexing.

New PDFs: drop them in PDF/ and run:

    pip install pypdf
    python scripts/extract_pdf_snippets.py
    python scripts/extract_pdf_snippets.py --pages 12

Outputs stay a JSON *array* (one object per file) for simple tooling; each row
gains optional fields: sample_page_indices, chapter_hints, file_size_bytes.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]

# Lines that often flag TOC / chapter structure (for human QA, not perfect)
_CH_HINT = re.compile(
    r"(?i)^(.*\bchapter\s+[\dIVXLC]+\b.*|"
    r".*\bcontents\b.*|"
    r"table\s+of\s+contents.*|"
    r"^\s*\d{1,2}\.\s+[A-Za-z].{3,})$"
)


def clean(t: str, max_chars: int = 12000) -> str:
    t = re.sub(r"\s+", " ", t or "").strip()
    return t[:max_chars]


def chapter_hints_from_text(text: str, max_hints: int = 18) -> list[str]:
    hints: list[str] = []
    seen: set[str] = set()
    for raw in (text or "").splitlines():
        line = raw.strip()
        if len(line) < 6 or len(line) > 160:
            continue
        if not _CH_HINT.match(line):
            continue
        key = line[:100]
        if key in seen:
            continue
        seen.add(key)
        hints.append(line[:140])
        if len(hints) >= max_hints:
            break
    return hints


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sample text from PDFs for KB index JSON.")
    p.add_argument(
        "--pages",
        type=int,
        default=5,
        metavar="N",
        help="Number of leading pages to extract per PDF (default: 5).",
    )
    p.add_argument(
        "--pdf-dir",
        type=Path,
        default=ROOT / "PDF",
        help="Directory containing .pdf files (default: ./PDF).",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data" / "pdf_extract_index.json",
        help="JSON output path.",
    )
    p.add_argument(
        "--out-txt",
        type=Path,
        default=ROOT / "data" / "pdf_sample_text.txt",
        help="Concatenated sample text for grepping.",
    )
    p.add_argument(
        "--meta",
        action="store_true",
        help="Print one JSON line with run metadata to stderr-friendly stdout line.",
    )
    return p.parse_args()


def main() -> None:
    if PdfReader is None:
        raise SystemExit("Install pypdf: pip install pypdf")

    args = parse_args()
    pdf_dir: Path = args.pdf_dir
    n_pages = max(1, args.pages)

    pdf_dir.mkdir(exist_ok=True)
    args.out.parent.mkdir(exist_ok=True)

    rows: list[dict] = []
    sample_blocks: list[str] = []
    generated = datetime.now(timezone.utc).isoformat()

    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if args.meta:
        print(
            json.dumps(
                {
                    "generated_at": generated,
                    "pdf_dir": str(pdf_dir.resolve()),
                    "sample_leading_pages": n_pages,
                    "pdf_count": len(pdfs),
                },
                ensure_ascii=False,
            )
        )

    for pdf in pdfs:
        size = pdf.stat().st_size if pdf.is_file() else 0
        try:
            r = PdfReader(str(pdf))
        except Exception as e:
            rows.append({"file": pdf.name, "error": str(e), "file_size_bytes": size})
            continue

        meta = r.metadata or {}
        title = None
        if meta:
            title = meta.get("/Title") or meta.get("title")
        total = len(r.pages)

        indices = list(range(min(n_pages, total)))
        chunks: list[str] = []
        for i in indices:
            try:
                chunks.append(r.pages[i].extract_text() or "")
            except Exception:
                chunks.append("")
        raw_join = "\n".join(chunks)
        blob = clean(raw_join)
        hints = chapter_hints_from_text(raw_join)

        rows.append(
            {
                "file": pdf.name,
                "pages": total,
                "title_meta": str(title) if title else None,
                "text_sample": blob,
                "sample_page_indices": indices,
                "sample_leading_pages": len(indices),
                "chapter_hints": hints,
                "file_size_bytes": size,
            }
        )
        sample_blocks.append(
            f"===== {pdf.name} ({total} pages, sampled {indices[0]}-{indices[-1]}) =====\n{blob}\n"
        )

    args.out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    args.out_txt.write_text("\n".join(sample_blocks), encoding="utf-8")
    print(f"Wrote {args.out} and {args.out_txt} ({len(rows)} files)")


if __name__ == "__main__":
    main()
