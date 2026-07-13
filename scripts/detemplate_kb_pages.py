#!/usr/bin/env python3
"""Safe de-templating of batch-generated KB concept pages.

Some `*-term-N` concept pages were produced by a template engine that fills the
same rhetorical skeleton with the term name substituted in. The result is
duplicated across ~283 pages and sometimes topically wrong (e.g. NURBS surface
theory on a gear-tools page). Per the editorial decision (option A), we remove
the generated boilerplate so pages are shorter but honest, keeping only:

  * Definition (real first paragraph; generic filler sentence dropped)
  * Why it matters (real first paragraph; generic filler sentence dropped)
  * Common pitfalls (page-specific)
  * All navigational chrome (Related Concepts, Ecosystem Context, Relevant FAQs,
    Self-Test, Semantic Crossroads)

Removed:
  * Sections: Technical Deep Dive & Core Mechanics, Step-by-Step Professional
    Implementation, Advanced Troubleshooting & Error Diagnostics,
    Cross-Discipline Collaboration & Handoff, Practical Workflow Tips
  * Generic filler <p> in Definition and Why it matters
  * JSON-LD HowTo (mirrors the removed Step-by-Step) and FAQPage (embeds the
    generic definition/why text)

Idempotent. Only touches pages that carry the template signatures.
"""

from __future__ import annotations

import glob
import re
import sys

# Signatures that identify a batch-generated page.
SIGNATURES = (
    "establishing precise standards early",
    "STEP AP214/AP242",
    "Set Up the Part/Assembly Template",
    "Rebuild errors after feature reorder",
)

# Section <h2> titles to remove wholesale (plain sections, no style attribute).
REMOVE_SECTIONS = (
    "Technical Deep Dive &amp; Core Mechanics",
    "Step-by-Step Professional Implementation",
    "Advanced Troubleshooting &amp; Error Diagnostics",
    "Cross-Discipline Collaboration &amp; Handoff",
    "Practical Workflow Tips",
)

# Generic filler paragraphs (term-agnostic) to drop from Definition / Why.
FILLER_P = re.compile(
    r"\s*<p>(?:By establishing precise standards early"
    r"|Without it, downstream fabrication)[^<]*</p>",
    re.S,
)


def _remove_section(html: str, title: str) -> str:
    # Match a plain kb-concept-section (no style attr) whose first child is the
    # target <h2>. Sections do not nest, so non-greedy up to </section> is safe.
    pat = re.compile(
        r'\n?\s*<section class="kb-concept-section">\s*<h2[^>]*>'
        + re.escape(title)
        + r"</h2>.*?</section>",
        re.S,
    )
    return pat.sub("", html)


def _remove_jsonld(html: str, typ: str) -> str:
    pat = re.compile(
        r'\s*<script type="application/ld\+json">\{[^<]*?"@type":\s*"'
        + re.escape(typ)
        + r'".*?</script>',
        re.S,
    )
    return pat.sub("", html)


def process(text: str) -> str:
    for title in REMOVE_SECTIONS:
        text = _remove_section(text, title)
    text = FILLER_P.sub("", text)
    text = _remove_jsonld(text, "HowTo")
    text = _remove_jsonld(text, "FAQPage")
    return text


def main() -> int:
    dry = "--apply" not in sys.argv
    files = sorted(glob.glob("kb/concepts/*.html"))
    targeted = [
        f for f in files if any(s in open(f, encoding="utf-8").read() for s in SIGNATURES)
    ]
    changed = 0
    for f in targeted:
        orig = open(f, encoding="utf-8").read()
        new = process(orig)
        if new != orig:
            changed += 1
            if not dry:
                open(f, "w", encoding="utf-8").write(new)
    mode = "DRY-RUN (use --apply to write)" if dry else "APPLIED"
    print(f"{mode}: {changed}/{len(targeted)} targeted pages would change.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
