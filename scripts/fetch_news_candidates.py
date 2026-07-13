#!/usr/bin/env python3
"""Weekly News workflow — step 1: fetch RSS candidates for manual curation.

This is the "RSS 抓取" half of the weekly news cadence. It pulls recent items
from a curated list of CAD / AEC / manufacturing industry feeds, normalizes
them, de-duplicates against the already-published ``data/news.json``, and
writes the leftovers to ``data/news_candidates.json`` for a human to review.

It deliberately does NOT publish anything. An editor reviews the candidates,
picks the worthwhile ones, writes an original short summary + tags for each,
appends them to ``data/news.json``, and then runs ``scripts/build_news.py`` to
regenerate the on-page feed. This keeps the "人工筛选" (manual curation) gate
and honors AGENTS.md: News = curated headlines + short original summaries +
outbound links, never scraped article bodies.

Usage:
    python scripts/fetch_news_candidates.py            # fetch, default 21-day window
    python scripts/fetch_news_candidates.py --days 30  # widen the window
    python scripts/fetch_news_candidates.py --limit 5  # cap per-feed items

Standard library only (urllib + xml.etree) so it runs anywhere without extra
dependencies. Feeds that fail to fetch/parse are skipped with a warning; a
weekly run should never hard-fail because one vendor changed their feed URL.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NEWS_JSON = REPO / "data" / "news.json"
CANDIDATES_JSON = REPO / "data" / "news_candidates.json"

# Curated industry feeds. Keys are the display "source" name used in news.json.
# Grouped by pillar: CAD/MCAD vendors, AEC/BIM, simulation, standards, trade.
FEEDS: dict[str, str] = {
    # CAD / MCAD vendors and communities
    "Autodesk": "https://adsknews.autodesk.com/en/feed/",
    "Blender Foundation": "https://www.blender.org/feed/",
    "DEVELOP3D": "https://develop3d.com/feed/",
    # AEC / BIM
    "Graphisoft": "https://www.graphisoft.com/feed",
    "AEC Magazine": "https://aecmag.com/feed/",
    "Construction Dive": "https://www.constructiondive.com/feeds/news/",
    # Engineering / manufacturing trade press
    "Engineering.com": "https://www.engineering.com/feed/",
    # Graphics / visualization
    "NVIDIA": "https://blogs.nvidia.com/feed/",
}

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _strip_html(text: str) -> str:
    text = _TAG_RE.sub(" ", text or "")
    text = html.unescape(text)
    return _WS_RE.sub(" ", text).strip()


def _local(tag: str) -> str:
    """Strip an XML namespace: '{http://...}title' -> 'title'."""
    return tag.rsplit("}", 1)[-1]


def _parse_date(raw: str) -> str | None:
    """Return an ISO 'YYYY-MM-DD' date string from RSS/Atom date formats."""
    raw = (raw or "").strip()
    if not raw:
        return None
    # RFC 822 (RSS pubDate)
    try:
        return parsedate_to_datetime(raw).date().isoformat()
    except (TypeError, ValueError):
        pass
    # ISO 8601 (Atom updated/published)
    try:
        return _dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        pass
    m = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
    return m.group(1) if m else None


def _fetch(url: str, timeout: int = 15) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (news-curation-bot)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception as exc:  # noqa: BLE001 - one bad feed shouldn't abort the run
        print(f"  ! fetch failed: {exc}", file=sys.stderr)
        return None


def _parse_feed(raw: bytes) -> list[dict]:
    """Parse RSS 2.0 or Atom into a list of {title, url, date, summary}."""
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        print(f"  ! parse failed: {exc}", file=sys.stderr)
        return []

    items: list[dict] = []

    # RSS 2.0: rss/channel/item
    channel = root.find("channel")
    if channel is not None:
        entries = channel.findall("item")
    else:
        # Atom: feed/entry (children carry namespaces)
        entries = [e for e in root if _local(e.tag) == "entry"]

    for entry in entries:
        fields: dict[str, str] = {}
        link = ""
        for child in entry:
            name = _local(child.tag)
            if name == "link":
                # RSS: text content; Atom: href attribute (prefer rel=alternate)
                href = child.attrib.get("href")
                if href:
                    if child.attrib.get("rel", "alternate") == "alternate" or not link:
                        link = href
                elif child.text:
                    link = child.text.strip()
            elif name in ("title", "summary", "description", "pubDate",
                          "published", "updated", "date"):
                fields[name] = (child.text or "").strip()

        title = _strip_html(fields.get("title", ""))
        if not title or not link:
            continue
        date = (_parse_date(fields.get("pubDate", ""))
                or _parse_date(fields.get("published", ""))
                or _parse_date(fields.get("updated", ""))
                or _parse_date(fields.get("date", "")))
        summary = _strip_html(fields.get("summary") or fields.get("description") or "")
        if len(summary) > 320:
            summary = summary[:317].rstrip() + "..."
        items.append({"title": title, "url": link, "date": date, "summary": summary})

    return items


def _load_published() -> list[dict]:
    if not NEWS_JSON.is_file():
        return []
    try:
        return json.loads(NEWS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _norm_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch RSS candidates for weekly news curation.")
    ap.add_argument("--days", type=int, default=21, help="only keep items newer than N days (default 21)")
    ap.add_argument("--limit", type=int, default=8, help="max items kept per feed (default 8)")
    args = ap.parse_args()

    cutoff = (_dt.date.today() - _dt.timedelta(days=args.days)).isoformat()

    published = _load_published()
    seen_urls = {i.get("url", "").rstrip("/") for i in published}
    seen_titles = {_norm_title(i.get("title", "")) for i in published}

    candidates: list[dict] = []
    for source, url in FEEDS.items():
        print(f"- {source}: {url}")
        raw = _fetch(url)
        if not raw:
            continue
        kept = 0
        for item in _parse_feed(raw):
            if kept >= args.limit:
                break
            if item["date"] and item["date"] < cutoff:
                continue
            if item["url"].rstrip("/") in seen_urls:
                continue
            if _norm_title(item["title"]) in seen_titles:
                continue
            candidates.append({
                "source": source,
                "title": item["title"],
                "date": item["date"] or "",
                "url": item["url"],
                "summary_raw": item["summary"],
                # editor fills these in before moving into news.json:
                "summary": "",
                "tags": [],
            })
            seen_urls.add(item["url"].rstrip("/"))
            seen_titles.add(_norm_title(item["title"]))
            kept += 1
        print(f"    kept {kept}")

    candidates.sort(key=lambda c: c.get("date") or "", reverse=True)
    CANDIDATES_JSON.write_text(
        json.dumps(candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"\nWrote {len(candidates)} candidate(s) -> {CANDIDATES_JSON.relative_to(REPO)}")
    print("Next: curate (write original 'summary' + 'tags'), append the keepers to")
    print("data/news.json with a unique 'id' and 'thumb_label', then run build_news.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
