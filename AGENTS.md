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
- Quiz behavior regression (run before committing quiz changes): `node tests/engine-harness.js`

## Quiz engine (quiz.html + quiz.js → quiz.min.js)

- Structure: **6 career tracks × 7 lessons** (`bim`/`mcad`/`civil`/`draft`/`sim`/`viz`, ~289 questions) + `placement` (draws 12 of 15, gate = 10 correct). Lesson ids are **contiguous 1..7** — never insert gaps; the unlock chain is `progress includes (lessonId - 1)`.
- Progress keys (localStorage, prefix `gstarcademy_`): `lessons_progress`, `roadmap_progress` (per-track `nodesToMaster` ids, 40 nodes total), `concept_mastery` (question slugs), `mistakes` (slugs), `total_xp`, `streak_v1`. The mistake book and concept mastery are **slug-keyed**; two questions may share a slug only when they test the same concept (7 intentional pairs as of 2026-08).
- XP: +10 per correct, lesson pass +20 (final lesson of a track +30 and lights its nodes), mistake review pass +20 (flat), placement pass +150 (lights all 6 tracks).
- The browser executes **`*.min.js`, not the sources**. Rebuild with esbuild after any source change:
  `npx esbuild quiz.js --minify --target=es2018 --outfile=quiz.min.js` (same for app/search/knowledge). A previous minifier stripped spaces *inside strings* ("Question 1of 3") — do not reintroduce it. CI (`.github/workflows/quiz-regression.yml`) fails if min files are stale or behavior regresses.
- Quiz copy promises must match engine constants (XP amounts, node totals, pass gates) — these drifted apart once; check both sides.

## Implementation discipline

- Match existing HTML/CSS patterns; bump cache query (`?v=`) when changing linked CSS/JS.
- Prefer separate KB pages over huge single-page anchor navigation for primary IA (already split).
- Keep tutorial entries **link-out** with clear source attribution; no scraped paywalled body text.

## Skill-sized checklist (for coding agents)

When adding features, tag the work to **one pillar** above. If a change touches both (e.g. linking from graph to a tutorial), make the **dependency direction explicit** in copy and URLs (KB → tutorials).
