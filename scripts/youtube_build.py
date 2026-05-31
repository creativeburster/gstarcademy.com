#!/usr/bin/env python3
"""
Refresh YouTube tutorial metadata via YouTube Data API v3 (search + videos),
merge optional editorial fields, write data/tutorials_youtube.json, and patch
the AUTO-GENERATED block in tutorials.html.

Usage:
  set YOUTUBE_API_KEY in the environment (or a .env file you load yourself),
  then from repo root:

    python scripts/youtube_build.py --fetch
    python scripts/youtube_build.py --html-only   # re-render HTML from JSON only

Requires: Python 3.9+ (stdlib only).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

REPO = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO / "config" / "youtube_fetch.json"
DATA_PATH = REPO / "data" / "tutorials_youtube.json"
EDITORIAL_PATH = REPO / "data" / "youtube_editorial.json"
TUTORIALS_HTML = REPO / "tutorials.html"

MARK_BEGIN = "            <!-- youtube-build:begin -->"
MARK_END = "            <!-- youtube-build:end -->"


def load_json(path: Path) -> Any:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def iso_duration_label(iso: str) -> str:
    """PT1H2M3S -> '1h 2m' ; PT15M33S -> '15m 33s'."""
    m = re.match(r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", iso or "")
    if not m:
        return iso or ""
    h, mn, s = (int(x) if x else 0 for x in m.groups())
    parts: list[str] = []
    if h:
        parts.append(f"{h}h")
    if mn:
        parts.append(f"{mn}m")
    if s or not parts:
        parts.append(f"{s}s")
    return " ".join(parts)


def api_request(endpoint: str, params: dict[str, str], api_key: str) -> dict[str, Any]:
    q = dict(params)
    q["key"] = api_key
    url = f"https://www.googleapis.com/youtube/v3/{endpoint}?{urlencode(q)}"
    try:
        with urlopen(url, timeout=45) as resp:
            body = resp.read().decode("utf-8")
    except HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"YouTube API HTTP {e.code}: {err}") from e
    except URLError as e:
        raise RuntimeError(f"YouTube API network error: {e}") from e
    return json.loads(body)


def fetch_videos(api_key: str) -> list[dict[str, Any]]:
    cfg = load_json(CONFIG_PATH)
    if not isinstance(cfg, dict):
        raise RuntimeError(f"Invalid JSON: {CONFIG_PATH}")

    searches = cfg.get("searches") or []
    extra_ids = [str(x) for x in (cfg.get("extra_video_ids") or []) if x]
    seen: set[str] = set()
    ordered_ids: list[str] = []

    for ex in extra_ids:
        if ex not in seen:
            seen.add(ex)
            ordered_ids.append(ex)

    for block in searches:
        if not isinstance(block, dict):
            continue
        query = str(block.get("query") or "").strip()
        if not query:
            continue
        max_results = int(block.get("max_results") or 10)
        max_results = max(1, min(max_results, 50))
        payload = api_request(
            "search",
            {
                "part": "snippet",
                "type": "video",
                "q": query,
                "maxResults": str(max_results),
            },
            api_key,
        )
        for item in payload.get("items") or []:
            vid = ((item.get("id") or {}).get("videoId")) or ""
            if vid and vid not in seen:
                seen.add(vid)
                ordered_ids.append(vid)

    if not ordered_ids:
        return []

    # videos.list allows up to 50 ids per call
    chunks = [ordered_ids[i : i + 50] for i in range(0, len(ordered_ids), 50)]
    out: list[dict[str, Any]] = []
    for chunk in chunks:
        payload = api_request(
            "videos",
            {
                "part": "snippet,contentDetails",
                "id": ",".join(chunk),
            },
            api_key,
        )
        by_id = {it["id"]: it for it in (payload.get("items") or []) if it.get("id")}
        for vid in chunk:
            it = by_id.get(vid)
            if not it:
                continue
            sn = it.get("snippet") or {}
            cd = it.get("contentDetails") or {}
            thumbs = sn.get("thumbnails") or {}
            thumb_url = (
                (thumbs.get("high") or {}).get("url")
                or (thumbs.get("medium") or {}).get("url")
                or (thumbs.get("default") or {}).get("url")
                or ""
            )
            out.append(
                {
                    "video_id": vid,
                    "title": sn.get("title") or "",
                    "description": (sn.get("description") or "")[:500],
                    "channel_title": sn.get("channelTitle") or "",
                    "published_at": sn.get("publishedAt") or "",
                    "thumbnail_url": thumb_url,
                    "duration_iso": cd.get("duration") or "",
                    "duration_label": iso_duration_label(str(cd.get("duration") or "")),
                }
            )
    return out


def merge_editorial(videos: list[dict[str, Any]], editorial: dict[str, Any]) -> None:
    for v in videos:
        vid = v["video_id"]
        ed = editorial.get(vid) if isinstance(editorial, dict) else None
        if not isinstance(ed, dict):
            ed = {}
        v["editorial_note"] = str(ed.get("editorial_note") or "").strip() or (
            "Indexed from public YouTube metadata; opens the original watch page on YouTube."
        )
        v["software"] = str(ed.get("software") or "").strip() or "—"
        v["task"] = str(ed.get("task") or "").strip() or "—"
        v["difficulty"] = str(ed.get("difficulty") or "").strip() or "—"
        v["price"] = "free"
        v["platform"] = "YouTube"
        tags = ed.get("tags")
        if isinstance(tags, list) and tags:
            v["tags"] = [str(t) for t in tags if str(t).strip()]
        else:
            v["tags"] = ["YouTube", "Video"]


def render_youtube_html(
    videos: list[dict[str, Any]],
    meta: Optional[dict[str, Any]] = None,
) -> str:
    meta = meta or {}
    src = str(meta.get("source") or "")
    is_demo = meta.get("demo") is True or src == "demo_static"
    is_hand_curated = "hand_curated" in src or src.endswith("_hand_curated")

    lines: list[str] = []
    lines.append('            <div class="panel">')
    lines.append('              <div class="section-head" style="margin-bottom: 0">')
    lines.append('                <h2 class="panel-title" style="margin: 0">CAD Learning Tutorials</h2>')
    lines.append('                <div class="chips" style="margin-top: 0">')
    lines.append('                  <span class="chip pill-ok">Unified Library</span>')
    lines.append('                  <span class="chip">Link-out only</span>')
    lines.append("                </div>")
    lines.append("              </div>")
    lines.append(
        '              <p class="meta" style="margin-top: 10px">'
        "Discover the best CAD, BIM, and MCAD classes curated from official vendor academies, "
        "Coursera, Udemy, and YouTube. Paid or certified programs are marked with 💳. We never host video files."
        "</p>"
    )
    lines.append("            </div>")

    if not videos:
        lines.append(
            '            <p class="meta">'
            "Curated CAD picks appear here. Check back soon!"
            "</p>"
        )
    else:
        for v in videos:
            title = html.escape(v.get("title") or "")
            platform = html.escape(v.get("platform", "YouTube"))
            price = html.escape(v.get("price", "free"))
            
            # Badges
            price_badge = ""
            if price == "paid":
                price_badge = ' <span class="badge badge-paid">💳 Premium</span>'
            else:
                price_badge = ' <span class="badge badge-free">🎁 Free</span>'
                
            # Meta string
            if platform == "YouTube":
                channel = html.escape(v.get("channel_title") or "")
                pub = html.escape((v.get("published_at") or "")[:10])
                dur = html.escape(v.get("duration_label") or "")
                meta_str = f"Source: YouTube · Channel: {channel} · Published: {pub} · Duration: {dur}"
            else:
                meta_str = html.escape(v.get("meta_info") or "")
                
            note = html.escape(v.get("editorial_note") or "")
            watch = html.escape(v.get("url") or "")
            if not watch and v.get("video_id") and platform == "YouTube":
                watch = f"https://www.youtube.com/watch?v={v['video_id']}"
                
            tags = v.get("tags") or []
            tag_html = "".join(
                f'<span class="tag">{html.escape(str(t))}</span>' for t in tags[:8]
            )
            soft = html.escape(str(v.get("software") or "—"))
            task = html.escape(str(v.get("task") or "—"))
            diff = html.escape(str(v.get("difficulty") or "—"))

            item_class = "tutorial-item tutorial-item--youtube" if platform == "YouTube" else "tutorial-item"
            lines.append(f'            <article class="{item_class}" data-software="{soft.lower()}" data-task="{task.lower()}" data-level="{diff.lower()}" data-price="{price.lower()}">')
            
            if v.get("thumbnail_url"):
                thumb = html.escape(v["thumbnail_url"], quote=True)
                thumb_style = f' style="background-image: url(&quot;{thumb}&quot;)"'
                lines.append(
                    f'              <div class="thumb thumb--cover"{thumb_style} role="img" aria-label="YouTube thumbnail"></div>'
                )
            else:
                lines.append(f'              <div class="thumb">{platform}</div>')
                
            lines.append('              <div class="item-body">')
            lines.append(f"                <h3>{title}{price_badge}</h3>")
            lines.append(f'                <p class="meta">{meta_str}</p>')
            lines.append(f'                <p class="meta">Editorial: {note} · Software: {soft} · Task: {task} · Level: {diff}</p>')
            lines.append(f'                <div class="item-tags">{tag_html}</div>')
            lines.append('                <div class="actions">')
            
            action_label = f"Open {platform}" if platform != "YouTube" else "Watch on YouTube"
            lines.append(
                f'                  <a class="btn btn-primary" href="{watch}" rel="noopener noreferrer" target="_blank">{action_label}</a>'
            )
            lines.append(
                '                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>'
            )
            lines.append("                </div>")
            lines.append("              </div>")
            lines.append("            </article>")

    return "\n".join(lines) + "\n"


def patch_tutorials_html(fragment: str) -> None:
    text = TUTORIALS_HTML.read_text(encoding="utf-8")
    if MARK_BEGIN not in text or MARK_END not in text:
        raise RuntimeError(f"Markers missing in {TUTORIALS_HTML}: {MARK_BEGIN} … {MARK_END}")
    pre, rest = text.split(MARK_BEGIN, 1)
    _, post = rest.split(MARK_END, 1)
    new_text = pre + MARK_BEGIN + "\n" + fragment + MARK_END + post
    TUTORIALS_HTML.write_text(new_text, encoding="utf-8")


def run_fetch(api_key: str) -> None:
    raw = fetch_videos(api_key)
    editorial = load_json(EDITORIAL_PATH)
    if not isinstance(editorial, dict):
        editorial = {}
    merge_editorial(raw, editorial)
    doc = {
        "meta": {
            "source": "youtube_data_api_v3",
            "demo": False,
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "config": str(CONFIG_PATH.relative_to(REPO)).replace("\\", "/"),
        },
        "videos": raw,
    }
    save_json(DATA_PATH, doc)


def load_and_merge_videos() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    doc = load_json(DATA_PATH)
    if not isinstance(doc, dict):
        doc = {"videos": []}
    vids = doc.get("videos")
    if not isinstance(vids, list):
        vids = []
    meta = doc.get("meta") or {}
    editorial = load_json(EDITORIAL_PATH)
    if not isinstance(editorial, dict):
        editorial = {}
    merge_editorial(vids, editorial)
    
    # Load premium/paid tutorials
    premium_path = REPO / "data" / "tutorials_premium.json"
    premium_vids = load_json(premium_path)
    if isinstance(premium_vids, list):
        for p in premium_vids:
            p["difficulty"] = p.get("level") or "beginner"
            p["video_id"] = p.get("id")
            p["published_at"] = ""
            p["thumbnail_url"] = ""
            p["meta_info"] = p.get("meta_info") or f"Source: {p.get('platform')} · Curated Course"
            p["editorial_note"] = p.get("editorial_note") or "Professional curated resource."
        vids.extend(premium_vids)
        
    return vids, meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync YouTube metadata into tutorials page.")
    parser.add_argument("--fetch", action="store_true", help="Call YouTube Data API and refresh JSON.")
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="Regenerate tutorials.html block from data/tutorials_youtube.json only.",
    )
    args = parser.parse_args()
    if args.fetch and args.html_only:
        print("Use only one of --fetch or --html-only", file=sys.stderr)
        return 2
    if not args.fetch and not args.html_only:
        print("Specify --fetch or --html-only.", file=sys.stderr)
        return 2

    if args.fetch:
        key = (os.environ.get("YOUTUBE_API_KEY") or "").strip()
        if not key:
            print("Missing YOUTUBE_API_KEY in environment.", file=sys.stderr)
            return 1
        print("Fetching from YouTube Data API…")
        run_fetch(key)
        doc = load_json(DATA_PATH)
        n = len(doc.get("videos") or []) if isinstance(doc, dict) else 0
        print(f"Wrote {n} videos to {DATA_PATH.relative_to(REPO)}")

    videos, meta = load_and_merge_videos()
    fragment = render_youtube_html(videos, meta)
    patch_tutorials_html(fragment)
    print(f"Patched {TUTORIALS_HTML.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
