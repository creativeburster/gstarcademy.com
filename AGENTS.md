# CAD Learn Hub — agent notes

Use this file as **project memory** when editing this repo. Product direction is authoritative in `PRD-知识库导航聚合站.md` (currently V1.1).

## Product pillars (do not conflate)

1. **Knowledge base** (`knowledge-*.html`): **Structured literacy + knowledge graph**, derived from **AI understanding and LLM output**. Human review and compliance before publish. No third-party video hosting; PDFs = index + short original notes + links, not full republication.
2. **Tutorials** (`tutorials.html`, etc.): **Navigation and aggregation** — outbound links to YouTube, MOOCs (Coursera, Udemy), vendor sites, training vendors. Filters, editorial blurbs, **paid-common sources marked** (e.g. 💳).
3. **News** (`news.html`): **Industry curation** — outbound links to vendor blogs, industry journals, and AEC/MFG news. Curated headlines and short summaries only.

User journey to preserve: **understand (KB) → find (tutorials) → stay updated (news)**.

## Key paths

- Visual / UX intent: `DESIGN.md`
- PRD (Chinese): `PRD-知识库导航聚合站.md`
- KB split generator (needs monolith backup before re-run): `scripts/split_knowledge_pages.py`
- PDF index tooling: `scripts/extract_pdf_snippets.py` → `data/pdf_extract_index.json`
- KB behavior: `knowledge.js`

## Implementation discipline

- Match existing HTML/CSS patterns; bump cache query (`?v=`) when changing linked CSS/JS.
- Prefer separate KB pages over huge single-page anchor navigation for primary IA (already split).
- Keep tutorial entries **link-out** with clear source attribution; no scraped paywalled body text.

## Skill-sized checklist (for coding agents)

When adding features, tag the work to **one pillar** above. If a change touches both (e.g. linking from graph to a tutorial), make the **dependency direction explicit** in copy and URLs (KB → tutorials).
