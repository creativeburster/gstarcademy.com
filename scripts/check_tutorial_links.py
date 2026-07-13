#!/usr/bin/env python3
"""Tutorial link health checker.

Verifies that outbound tutorial links are still reachable so the aggregation
stays trustworthy. Two sources are checked:

  * data/tutorials_premium.json  -> each item's "url" (HTTP HEAD/GET)
  * data/tutorials_youtube.json  -> each video's "video_id" via the public
    oEmbed endpoint (a 404 there means the video was removed/made private)

The script does NOT modify site data. It prints a human-readable report and
writes data/tutorial_link_report.json (gitignored scratch) so a reviewer /
automation can open a PR removing or replacing dead links after human judgment.

Usage:
    python scripts/check_tutorial_links.py
    python scripts/check_tutorial_links.py --timeout 20
    python scripts/check_tutorial_links.py --json-only   # suppress stdout table

Exit code is 0 when every link is healthy, 1 when one or more are broken, so a
scheduled automation can branch on it. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PREMIUM_JSON = REPO / "data" / "tutorials_premium.json"
YOUTUBE_JSON = REPO / "data" / "tutorials_youtube.json"
REPORT_JSON = REPO / "data" / "tutorial_link_report.json"

UA = "Mozilla/5.0 (compatible; gstarcademy-linkcheck/1.0; +https://gstarcademy.com)"
YT_OEMBED = "https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v="


# Codes where the resource is almost certainly still live but the host blocks
# bots/HEAD. We flag these as "inconclusive" rather than broken so the
# automation does not churn PRs over false positives.
INCONCLUSIVE_CODES = {401, 403, 405, 406, 429, 501, 503}
# States, in priority order: True=ok, None=inconclusive, False=broken.


def _check_url(url: str, timeout: int) -> tuple[object, str]:
    """Return (state, detail). state is True (ok), None (inconclusive), False (broken)."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        if method == "GET":
            req.add_header("Range", "bytes=0-2047")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return True, f"{resp.status}"
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in INCONCLUSIVE_CODES:
                continue  # retry as GET before deciding
            if e.code in INCONCLUSIVE_CODES:
                return None, f"HTTP {e.code} (bot-blocked, manual check)"
            return False, f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if method == "HEAD":
                continue
            return None, f"{type(e).__name__} (manual check)"
        except Exception as e:  # noqa: BLE001 - report anything unexpected
            return None, f"{type(e).__name__} (manual check)"
    return False, "unreachable"


def _check_youtube(video_id: str, timeout: int) -> tuple[object, str]:
    req = urllib.request.Request(
        YT_OEMBED + video_id, headers={"User-Agent": UA}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return (resp.status == 200) or None, f"{resp.status}"
    except urllib.error.HTTPError as e:
        # oEmbed returns 401/404 for removed or private videos.
        if e.code in (401, 404):
            return False, f"HTTP {e.code} (removed/private)"
        return None, f"HTTP {e.code} (manual check)"
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return None, "network error (manual check)"
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__} (manual check)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--json-only", action="store_true")
    args = ap.parse_args()

    results: list[dict] = []

    def _state(v: object) -> str:
        return "ok" if v is True else ("broken" if v is False else "inconclusive")

    if PREMIUM_JSON.exists():
        for item in json.loads(PREMIUM_JSON.read_text(encoding="utf-8")):
            url = item.get("url")
            if not url:
                continue
            st, detail = _check_url(url, args.timeout)
            results.append({
                "source": "premium",
                "id": item.get("id", ""),
                "title": item.get("title", ""),
                "url": url,
                "state": _state(st),
                "detail": detail,
            })

    if YOUTUBE_JSON.exists():
        data = json.loads(YOUTUBE_JSON.read_text(encoding="utf-8"))
        for v in data.get("videos", []):
            vid = v.get("video_id")
            if not vid:
                continue
            st, detail = _check_youtube(vid, args.timeout)
            results.append({
                "source": "youtube",
                "id": vid,
                "title": v.get("title", ""),
                "url": f"https://www.youtube.com/watch?v={vid}",
                "state": _state(st),
                "detail": detail,
            })

    broken = [r for r in results if r["state"] == "broken"]
    inconclusive = [r for r in results if r["state"] == "inconclusive"]
    REPORT_JSON.write_text(
        json.dumps(
            {"checked": len(results), "broken": broken, "inconclusive": inconclusive},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if not args.json_only:
        print(
            f"Checked {len(results)} tutorial link(s); "
            f"{len(broken)} broken, {len(inconclusive)} inconclusive.\n"
        )
        for r in results:
            mark = {"ok": "OK ", "broken": "DEAD", "inconclusive": "??? "}[r["state"]]
            print(f"  [{mark}] {r['source']:<7} {r['detail']:<32} {r['title'][:56]}")
        if broken:
            print("\nBroken links (curate a replacement before removing):")
            for r in broken:
                print(f"  - {r['source']} :: {r['title']}\n      {r['url']}  ({r['detail']})")
        print(f"\nReport written -> {REPORT_JSON.relative_to(REPO)}")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
