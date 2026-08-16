"""Regenerate sitemap.xml with high performance git log caching:
1. Batch fetch git lastmod dates in a single git invocation
2. Priority and changefreq based on URL patterns
3. Complete coverage of all 900+ valid content pages
4. Sorted by priority (homepage first, then major sections, then content)

Usage: python scripts/regenerate_sitemap.py
"""
from __future__ import annotations
import subprocess
import os
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

def build_git_lastmod_cache() -> dict[str, str]:
    """Fast batch fetch of last modified date for all files."""
    cache = {}
    today_str = datetime.now().strftime("%Y-%m-%d")
    try:
        cmd = ["git", "log", "--name-only", "--format=COMMIT:%cI"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO), encoding="utf-8")
        if res.returncode == 0:
            current_date = None
            for line in res.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("COMMIT:"):
                    try:
                        raw_date = line.replace("COMMIT:", "").strip()
                        current_date = datetime.fromisoformat(raw_date).strftime("%Y-%m-%d")
                    except Exception:
                        current_date = today_str
                else:
                    norm_path = line.replace("\\", "/")
                    if norm_path not in cache and current_date:
                        cache[norm_path] = current_date
    except Exception as e:
        print("Git log batch error:", e)
    return cache


def filepath_to_url(path: Path) -> str:
    """Convert local Path object to sitemap URL format."""
    rel = path.relative_to(REPO).as_posix()
    if rel.endswith(".html"):
        rel = rel[:-5]
    if rel == "index":
        return SITE + "/"
    if rel.endswith("/index"):
        rel = rel[:-6]
    return f"{SITE}/{rel}"


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

    # KB FAQ individual pages
    if path.startswith("kb/faq"):
        return "0.8", "weekly"

    # KB guides
    if path.startswith("kb/guides"):
        return "0.8", "weekly"

    # KB learning paths
    if path.startswith("kb/learning-paths"):
        return "0.8", "weekly"

    # KB software index & profile pages
    if path.startswith("kb/software"):
        return "0.8", "weekly"

    # KB concept pages
    if path.startswith("kb/concepts"):
        return "0.7", "monthly"

    # KB vendor pages
    if path.startswith("kb/vendors"):
        return "0.6", "monthly"

    # Legal/policy pages
    legal_pages = ["legal", "privacy", "terms", "editorial-process", "authors"]
    if path in legal_pages:
        return "0.3", "yearly"

    return "0.5", "monthly"


def is_excluded(url_path: str) -> bool:
    path = url_path.lstrip("/")
    for pattern in EXCLUDE_PATTERNS:
        if path == pattern or path.startswith(pattern + "/"):
            return True
    return False


def is_noindex(filepath: str | None) -> bool:
    if not filepath:
        return False
    p = REPO / filepath
    if not p.exists():
        return False
    try:
        content = p.read_text(encoding="utf-8")
    except Exception:
        content = p.read_text(encoding="utf-8-sig")
    return 'content="noindex' in content


def main() -> int:
    print("Building Git lastmod cache...")
    git_cache = build_git_lastmod_cache()
    today_str = datetime.now().strftime("%Y-%m-%d")

    print("Scanning repository for all HTML files...")
    html_files = []
    # Root level
    for p in REPO.glob("*.html"):
        html_files.append(p)
    # Sub directories
    sub_dirs = ["kb/concepts", "kb/software", "kb/vendors", "kb/guides", "kb/learning-paths", "kb/faq"]
    for sd in sub_dirs:
        folder = REPO / sd
        if folder.exists():
            for p in folder.glob("*.html"):
                html_files.append(p)

    entries = []
    seen_urls = set()
    for path in html_files:
        url = filepath_to_url(path)
        url_path = url.replace(SITE, "")
        
        # Skip duplicate URLs or excluded patterns
        if url in seen_urls or is_excluded(url_path):
            continue

        filepath = path.relative_to(REPO).as_posix()
        if is_noindex(filepath):
            continue
            
        lastmod = git_cache.get(filepath, today_str)
        priority, changefreq = get_priority_changefreq(url_path)

        seen_urls.add(url)
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
    print(f"Sitemap regenerated successfully! Total URLs in sitemap.xml: {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
