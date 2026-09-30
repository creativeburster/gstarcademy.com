"""Comprehensive audit script to detect Thin Content pages across gstarcademy.com.
Checks:
1. Visible body word count (excluding header, nav, footer, script, style).
2. Status flags: empty (<50 words), thin (<200 words), acceptable (200-400 words), rich (>400 words).
3. Missing or empty <title>, <meta name="description">, or <h1> tags.
4. Identifies specific template-only or placeholder pages.
"""
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parents[1]

EXCLUDE_DIRS = {
    ".git", ".system_generated", "node_modules", "dist", "scratch"
}

EXCLUDE_FILES = {
    "offline.html", "google*.html"
}

def clean_text(soup):
    for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        element.extract()
    text = soup.get_text(separator=" ", strip=True)
    # clean excess whitespace
    text = re.sub(r"\s+", " ", text)
    return text

def audit():
    html_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        # filter dirs in place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(".html") and not f.startswith("google"):
                html_files.append(Path(root) / f)

    total_files = len(html_files)
    print(f"Total HTML files discovered: {total_files}")

    stats = {
        "empty (<50 words)": [],
        "thin (50-200 words)": [],
        "moderate (200-400 words)": [],
        "rich (>400 words)": [],
        "missing_title": [],
        "missing_desc": [],
        "missing_h1": []
    }

    page_details = []

    for path in html_files:
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {rel_path}: {e}")
            continue

        soup = BeautifulSoup(content, "html.parser")
        
        # Meta checks
        title_el = soup.find("title")
        title = title_el.get_text(strip=True) if title_el else ""
        if not title:
            stats["missing_title"].append(rel_path)

        desc_el = soup.find("meta", attrs={"name": "description"})
        desc = desc_el.get("content", "").strip() if desc_el else ""
        if not desc:
            stats["missing_desc"].append(rel_path)

        h1_el = soup.find("h1")
        h1 = h1_el.get_text(strip=True) if h1_el else ""
        if not h1:
            stats["missing_h1"].append(rel_path)

        # Content word count
        text = clean_text(soup)
        words = text.split()
        word_count = len(words)

        page_details.append({
            "path": rel_path,
            "words": word_count,
            "title": title[:60],
            "has_desc": bool(desc),
            "has_h1": bool(h1)
        })

        if word_count < 50:
            stats["empty (<50 words)"].append((rel_path, word_count))
        elif word_count < 200:
            stats["thin (50-200 words)"].append((rel_path, word_count))
        elif word_count <= 400:
            stats["moderate (200-400 words)"].append((rel_path, word_count))
        else:
            stats["rich (>400 words)"].append((rel_path, word_count))

    print("\n===== AUDIT SUMMARY =====")
    print(f"Total Pages Analyzed: {len(page_details)}")
    print(f"Rich Content (>400 words): {len(stats['rich (>400 words)'])} ({len(stats['rich (>400 words)'])/total_files*100:.1f}%)")
    print(f"Moderate Content (200-400 words): {len(stats['moderate (200-400 words)'])} ({len(stats['moderate (200-400 words)'])/total_files*100:.1f}%)")
    print(f"Thin Content (50-200 words): {len(stats['thin (50-200 words)'])} ({len(stats['thin (50-200 words)'])/total_files*100:.1f}%)")
    print(f"Empty Content (<50 words): {len(stats['empty (<50 words)'])} ({len(stats['empty (<50 words)'])/total_files*100:.1f}%)")
    print(f"Missing Title: {len(stats['missing_title'])}")
    print(f"Missing Meta Description: {len(stats['missing_desc'])}")
    print(f"Missing H1 Tag: {len(stats['missing_h1'])}")

    if stats["empty (<50 words)"]:
        print("\n--- EMPTY PAGES (<50 words) ---")
        for p, w in stats["empty (<50 words)"]:
            print(f"  {p} ({w} words)")

    if stats["thin (50-200 words)"]:
        print(f"\n--- THIN PAGES (50-200 words, showing first 15 of {len(stats['thin (50-200 words)'])}) ---")
        for p, w in stats["thin (50-200 words)"][:15]:
            print(f"  {p} ({w} words)")

    # Sort page details by words ascending
    page_details.sort(key=lambda x: x["words"])
    print("\n--- TOP 10 SHORTEST PAGES ---")
    for p in page_details[:10]:
        print(f"  {p['path']}: {p['words']} words | H1: {p['has_h1']} | Desc: {p['has_desc']}")

    return stats

if __name__ == "__main__":
    audit()
