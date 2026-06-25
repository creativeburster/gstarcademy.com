"""Normalize site URL/email to https://gstarcademy.com (migrate legacy cadlearnhub.com / learncad.guide / learncad.io)."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXCLUDE = {".git", "node_modules", "__pycache__"}
TEXT_SUFFIX = {
    ".html",
    ".xml",
    ".txt",
    ".js",
    ".py",
    ".json",
    ".md",
    ".css",
    ".svg",
    ".mjs",
    ".cjs",
}


def main() -> int:
    n = 0
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIX:
            continue
        if any(part in EXCLUDE for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        new = (
            text.replace("https://cadlearnhub.com", "https://gstarcademy.com")
            .replace("https://learncad.guide", "https://gstarcademy.com")
            .replace("https://learncad.io", "https://gstarcademy.com")
            .replace("@cadlearnhub.com", "@gstarcademy.com")
            .replace("@learncad.guide", "@gstarcademy.com")
            .replace("@learncad.io", "@gstarcademy.com")
            .replace("cadlearnhub-site-notice", "gstarcademy-site-notice")
            .replace("cadlearnhub-cookie-consent-v1", "gstarcademy-cookie-consent-v1")
            .replace("learncad-site-notice", "gstarcademy-site-notice")
            .replace("learncad-cookie-consent-v1", "gstarcademy-cookie-consent-v1")
        )
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("+", path.relative_to(REPO))
            n += 1
    print("updated", n, "files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
