#!/usr/bin/env python3
"""
Compile search index corpus from knowledge.js and output data/search_nodes.json.
This ensures search.js has access to all 550+ nodes with exact URLs.

Usage:
    python scripts/build_search_index.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KNOWLEDGE_JS = REPO / "knowledge.js"
SEARCH_NODES_JSON = REPO / "data" / "search_nodes.json"


def clean_js_string(s: str) -> str:
    # "AutoCAD Layer States" -> AutoCAD Layer States
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    return s


def parse_js_array(s: str) -> list[str]:
    # '["autocad", "2d"]' or "['autocad', '2d']" -> ["autocad", "2d"]
    s = s.strip()
    if not s.startswith('[') or not s.endswith(']'):
        # Maybe it's a comma-separated list or plain string
        return [clean_js_string(x) for x in s.split(",") if x.strip()]
    content = s[1:-1]
    # Split by comma but ignore commas inside quotes (simple split works if no nested commas)
    items = []
    for part in re.split(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)", content):
        part = part.strip()
        if part:
            items.append(clean_js_string(part))
    return items


def main() -> int:
    if not KNOWLEDGE_JS.is_file():
        print(f"Error: {KNOWLEDGE_JS} not found!")
        return 1

    js_content = KNOWLEDGE_JS.read_text(encoding="utf-8")

    # 1. Parse nodeUrlMap to get custom URLs
    # nodeUrlMap is structured as:
    #     const nodeUrlMap = {
    #       "CAD Basics": "./knowledge-base.html",
    #       ...
    #     };
    node_url_map = {}
    map_match = re.search(r"const\s+nodeUrlMap\s*=\s*\{([^}]+)\}", js_content)
    if map_match:
        map_body = map_match.group(1)
        for line in map_body.splitlines():
            line = line.strip()
            if not line or ":" not in line or line.startswith("//"):
                continue
            # "CAD Basics": "./knowledge-base.html",
            try:
                parts = line.split(":", 1)
                k = clean_js_string(parts[0].strip())
                v = clean_js_string(parts[1].strip().rstrip(","))
                node_url_map[k] = v
            except Exception:
                pass

    # 2. Extract nodes from const nodes = [ ... ];
    # nodes block can be large, find from "const nodes = [" to first "];" after it
    nodes_match = re.search(r"const\s+nodes\s*=\s*\[(.*?)\];", js_content, re.DOTALL)
    if not nodes_match:
        print("Error: Could not find 'const nodes' array in knowledge.js")
        return 1

    nodes_body = nodes_match.group(1)
    nodes_list = []

    # Parse node object lines like:
    # { id: "AutoCAD Layer States", group: 2, type: "concept", radius: 8, tags: ["autocad", "2d"] }
    # { id: "Autodesk", type: "vendor", tags: ["terms", "aec", "mfg"], hint: "..." }
    node_pattern = re.compile(r"\{\s*id:\s*([\"'][^\"']+[\"'])(.*?)\}")

    for match in node_pattern.finditer(nodes_body):
        node_id = clean_js_string(match.group(1))
        meta_body = match.group(2)

        node_type = "concept"
        tags = []
        hint = ""

        # Extract type:
        type_m = re.search(r"type:\s*([\"'][^\"']+[\"'])", meta_body)
        if type_m:
            node_type = clean_js_string(type_m.group(1))

        # Extract tags:
        # can be tags: ["a", "b"] or tags: 'a' or tags: ["a"]
        tags_m = re.search(r"tags:\s*(\[[^\]]+\]|[\"'][^\"']+[\"'])", meta_body)
        if tags_m:
            tags = parse_js_array(tags_m.group(1))

        # Extract hint:
        hint_m = re.search(r"hint:\s*([\"'][^\"']+[\"'])", meta_body)
        if hint_m:
            hint = clean_js_string(hint_m.group(1))

        # Determine exact URL:
        if node_id in node_url_map:
            url = node_url_map[node_id]
        else:
            url = f"./kb/concepts/{node_id.lower().replace(' ', '-').replace('/', '-')}.html"

        # Special cleaning for concepts relative URLs:
        # e.g., if we are inside /kb/concepts/, URLs like "./kb/concepts/layer.html" need to be mapped.
        # Let's keep them as root-relative or simple relative and let search.js handle it
        nodes_list.append({
            "id": node_id,
            "type": node_type,
            "tags": tags,
            "hint": hint,
            "url": url
        })

    SEARCH_NODES_JSON.parent.mkdir(parents=True, exist_ok=True)
    SEARCH_NODES_JSON.write_text(json.dumps(nodes_list, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Successfully compiled {len(nodes_list)} nodes into {SEARCH_NODES_JSON.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
