"""Fix duplicated meta descriptions in kb/concepts/*.html files.

Older generation code produced descriptions like:
  "Title — Title — definition_truncated..."
The correct description should be the short_def from the DefinedTerm JSON-LD.

This script:
1. Reads each kb/concepts/*.html
2. Extracts the correct description from the DefinedTerm JSON-LD
3. Replaces meta[name=description], og:description, twitter:description
"""

from __future__ import annotations
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONCEPTS_DIR = REPO / "kb" / "concepts"


def extract_definedterm_desc(html: str) -> str | None:
    """Extract description from DefinedTerm JSON-LD block."""
    pattern = re.compile(
        r'"@type":"DefinedTerm".*?"description":"((?:[^"\\]|\\.)*)"',
        re.DOTALL,
    )
    m = pattern.search(html)
    if m:
        raw = m.group(1)
        # Unescape JSON string
        try:
            return json.loads(f'"{raw}"')
        except Exception:
            return raw
    return None


def extract_title(html: str) -> str | None:
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if m:
        full = m.group(1).strip()
        # Title format: "Term Name · Software · CAD Knowledge Base · Gstarcademy"
        # or "Term Name · Gstarcademy"
        parts = full.split(" · ")
        return parts[0].strip()
    return None


def fix_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html

    desc = extract_definedterm_desc(html)
    if not desc:
        return False

    title = extract_title(html)
    if not title:
        return False

    # Check if meta description has the duplication pattern
    meta_desc_match = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>',
        html,
        re.IGNORECASE,
    )
    if not meta_desc_match:
        return False

    current_desc = meta_desc_match.group(1)
    # Check for duplication: title appears twice at the start
    dup_prefix = f"{title} — {title} — "
    if not current_desc.startswith(title + " — " + title):
        # Also check with HTML entities
        import html as html_mod
        escaped_title = html_mod.escape(title)
        dup_prefix_escaped = f"{escaped_title} — {escaped_title} — "
        if not current_desc.startswith(escaped_title + " — " + escaped_title):
            return False  # No duplication detected, skip

    # Build replacement description (truncate to 160 chars)
    new_desc = desc[:160]
    if len(desc) > 160:
        new_desc = desc[:157] + "..."

    # Escape for HTML attribute
    import html as html_mod
    escaped_new_desc = html_mod.escape(new_desc, quote=True)

    # Replace meta description
    html = re.sub(
        r'(<meta\s+name="description"\s+content=")([^"]*)("\s*/?>)',
        lambda m: m.group(1) + escaped_new_desc + m.group(3),
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    # Replace og:description
    html = re.sub(
        r'(<meta\s+property="og:description"\s+content=")([^"]*)("\s*/?>)',
        lambda m: m.group(1) + escaped_new_desc + m.group(3),
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    # Replace twitter:description
    html = re.sub(
        r'(<meta\s+name="twitter:description"\s+content=")([^"]*)("\s*/?>)',
        lambda m: m.group(1) + escaped_new_desc + m.group(3),
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> int:
    fixed = 0
    skipped = 0
    for path in sorted(CONCEPTS_DIR.glob("*.html")):
        if fix_file(path):
            fixed += 1
            print(f"  fixed: {path.name}")
        else:
            skipped += 1
    print(f"Concept description fix: {fixed} fixed, {skipped} unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
