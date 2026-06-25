"""Regenerate sitemap.xml with:
1. Real lastmod dates from git log per file
2. Priority and changefreq based on URL patterns
3. Sorted by priority (homepage first, then major sections, then content)

Usage: python scripts/regenerate_sitemap.py
"""
from __future__ import annotations
import subprocess
import re
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
SITE = "https://gstarcademy.com"
SITEMAP = REPO / "sitemap.xml"

# Pages to exclude from sitemap (noindex, redirect, or non-content)
EXCLUDE_PATTERNS = [
    "tutorial-detail",
    "kb-vendors",
    "offline",
    "topic",
]


def git_lastmod(filepath: str) -> str:
    """Get last git commit date for a file as YYYY-MM-DD."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", filepath],
            capture_output=True, text=True, cwd=str(REPO),
        )
        if result.returncode == 0 and result.stdout.strip():
            dt = datetime.fromisoformat(result.stdout.strip())
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def url_to_filepath(url: str) -> str | None:
    """Convert sitemap URL to local file path."""
    path = url.replace(SITE, "").lstrip("/")
    if path == "":
        return "index.html"
    # Try .html extension
    if not path.endswith(".html"):
        html_path = f"{path}.html"
        if (REPO / html_path).exists():
            return html_path
        # Try as directory index
        index_path = f"{path}/index.html"
        if (REPO / index_path).exists():
            return index_path
        # Try without extension (cleanUrls)
        if (REPO / path).exists():
            return path
        return f"{path}.html"
    return path


def get_priority_changefreq(url_path: str) -> tuple[str, str]:
    """Determine priority and changefreq based on URL pattern."""
    path = url_path.lstrip("/")

    if path == "" or path == "/":
        return "1.0", "daily"

    # Major section pages
    major_sections = [
        "knowledge-base", "tutorials", "news", "kb-software", "kb-terms",
        "kb-faq", "kb-graph", "quiz", "about", "contact",
    ]
    if path in major_sections:
        return "0.9", "weekly"

    # Knowledge sub-sections
    knowledge_sections = [
        "knowledge-cax", "knowledge-curriculum", "knowledge-domains",
        "knowledge-glossary", "knowledge-learn", "knowledge-library",
        "knowledge-roadmap",
    ]
    if path in knowledge_sections:
        return "0.8", "weekly"

    # KB software index
    if path == "kb/software/":
        return "0.8", "weekly"

    # KB vendor pages
    if path.startswith("kb/vendors/"):
        return "0.6", "monthly"

    # KB software profile pages
    if path.startswith("kb/software/"):
        return "0.7", "monthly"

    # KB concept pages
    if path.startswith("kb/concepts/"):
        return "0.7", "monthly"

    # Legal/policy pages
    legal_pages = ["legal", "privacy", "terms", "editorial-process"]
    if path in legal_pages:
        return "0.3", "yearly"

    return "0.5", "monthly"


def is_excluded(url_path: str) -> bool:
    path = url_path.lstrip("/")
    for pattern in EXCLUDE_PATTERNS:
        if path == pattern or path.startswith(pattern + "/"):
            return True
    return False


def main() -> int:
    # Read existing sitemap to get all URLs
    content = SITEMAP.read_text(encoding="utf-8")
    url_pattern = re.compile(r"<loc>([^<]+)</loc>")
    urls = url_pattern.findall(content)

    entries = []
    for url in urls:
        url_path = url.replace(SITE, "")
        if is_excluded(url_path):
            continue

        filepath = url_to_filepath(url)
        lastmod = git_lastmod(filepath) if filepath else datetime.now().strftime("%Y-%m-%d")
        priority, changefreq = get_priority_changefreq(url_path)

        entries.append((url, lastmod, priority, changefreq))

    # Sort by priority descending, then by URL
    priority_order = {"1.0": 0, "0.9": 1, "0.8": 2, "0.7": 3, "0.6": 4, "0.5": 5, "0.3": 6}
    entries.sort(key=lambda e: (priority_order.get(e[2], 9), e[0]))

    # Write sitemap
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, lastmod, priority, changefreq in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")

    SITEMAP.write_text("\n".join(lines), encoding="utf-8")
    print(f"Sitemap regenerated: {len(entries)} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
