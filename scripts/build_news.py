#!/usr/bin/env python3
"""
Compile curated CAD/AEC industry news from data/news.json
and patch the news.html dynamic feed.

Usage:
    python scripts/build_news.py
"""

from __future__ import annotations

import html
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NEWS_JSON = REPO / "data" / "news.json"
NEWS_HTML = REPO / "news.html"

MARK_BEGIN = "            <!-- news-build:begin -->"
MARK_END = "            <!-- news-build:end -->"


def load_news() -> list[dict]:
    if not NEWS_JSON.is_file():
        print(f"Error: {NEWS_JSON} not found!")
        return []
    try:
        return json.loads(NEWS_JSON.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return []


def format_date_long(iso_date: str) -> str:
    # "2026-04-26" -> "April 26, 2026"
    try:
        parts = iso_date.split("-")
        if len(parts) != 3:
            return iso_date
        y, m, d = parts
        months = {
            "01": "January", "02": "February", "03": "March", "04": "April",
            "05": "May", "06": "June", "07": "July", "08": "August",
            "09": "September", "10": "October", "11": "November", "12": "December"
        }
        month_name = months.get(m, m)
        day_val = int(d)
        return f"{month_name} {day_val}, {y}"
    except Exception:
        return iso_date


def render_news_cards(news_items: list[dict]) -> str:
    lines = []
    for item in news_items:
        title = html.escape(item.get("title") or "")
        date_iso = html.escape(item.get("date") or "")
        date_long = html.escape(format_date_long(date_iso))
        source = html.escape(item.get("source") or "")
        summary = html.escape(item.get("summary") or "")
        url = html.escape(item.get("url") or "", quote=True)
        thumb_label = html.escape(item.get("thumb_label") or "News")
        
        tags = item.get("tags") or []
        tag_html = "".join(
            f'<span class="tag">{html.escape(str(t))}</span>' for t in tags[:6]
        )
        
        # Build tags for semantic metadata line
        meta_tags = ", ".join(tags)
        
        lines.append('            <article class="tutorial-item news-curated-item">')
        lines.append(f'              <div class="thumb" aria-hidden="true">{thumb_label}</div>')
        lines.append('              <div class="item-body">')
        lines.append(f'                <h3>{title}</h3>')
        lines.append('                <p class="meta">')
        lines.append(f'                  <time datetime="{date_iso}">{date_long}</time> · Source: {source} · Tags: {meta_tags}')
        lines.append('                </p>')
        lines.append(f'                <p class="meta">{summary}</p>')
        lines.append(f'                <div class="item-tags">{tag_html}</div>')
        lines.append('                <div class="actions">')
        lines.append(f'                  <a class="btn btn-primary" href="{url}" rel="noopener noreferrer" target="_blank">Read at {source}</a>')
        lines.append('                </div>')
        lines.append('              </div>')
        lines.append('            </article>')
        
    return "\n".join(lines) + "\n"


def main() -> int:
    news_items = load_news()
    if not news_items:
        print("No news items curated.")
        return 0
        
    fragment = render_news_cards(news_items)
    
    text = NEWS_HTML.read_text(encoding="utf-8")
    if MARK_BEGIN not in text or MARK_END not in text:
        raise RuntimeError(f"Markers missing in {NEWS_HTML}")
        
    pre, rest = text.split(MARK_BEGIN, 1)
    _, post = rest.split(MARK_END, 1)
    
    new_text = pre + MARK_BEGIN + "\n" + fragment + MARK_END + post
    NEWS_HTML.write_text(new_text, encoding="utf-8")
    print(f"Successfully compiled {len(news_items)} news items into {NEWS_HTML.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
