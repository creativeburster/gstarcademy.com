"""One-off: rename five KB lane HTML files and rewrite references."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

RENAMES: list[tuple[str, str]] = [
    ("kb-vendors.html", "kb-vendors.html"),
    ("kb-terms.html", "kb-terms.html"),
    ("kb-software.html", "kb-software.html"),
    ("kb-graph.html", "kb-graph.html"),
    ("kb-faq.html", "kb-faq.html"),
]

# Longest old names first (already ordered)
REPL_TEXT_ORDER = RENAMES.copy()

EXTS = {".html", ".js", ".css", ".xml", ".json", ".py", ".md", ".txt"}


def main() -> int:
    edited: list[Path] = []
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.parts):
            continue
        if path.suffix.lower() not in EXTS:
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        for old, newname in REPL_TEXT_ORDER:
            new = new.replace(old, newname)
        if new != text:
            path.write_text(new, encoding="utf-8")
            edited.append(path)

    for old_name, new_name in RENAMES:
        src = REPO / old_name
        dst = REPO / new_name
        if src.is_file():
            src.rename(dst)
            print("renamed", old_name, "->", new_name)

    print("edited", len(edited), "files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
