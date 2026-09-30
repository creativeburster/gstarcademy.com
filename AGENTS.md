# GstarCAD Academy (gstarcademy.com) — agent notes

> [!NOTE]
> **🐙 官方 GitHub 仓库与账号规范 (GitHub Repository Info)**
> * 官方仓库地址：`https://github.com/creativeburster/gstarcademy.com`
> * 默认生产分支：`main`
> * **迁移规范**：本项目已全量迁移至新 GitHub 账号 `creativeburster`。旧账号 `gstar-byte` 已废弃，严禁在任何脚本、配置、文档或外链中引用旧账号地址。

Use this file as **project memory** when editing this repo. Product direction is authoritative in `PRD-知识库导航聚合站.md` (V2.0 — 回归浩辰海外业务).

## Product pillars (GstarCAD Global Academy)

1. **AutoCAD to GstarCAD Migration Hub** (`migration.html`): Enterprise AutoCAD replacement gateway — 100% native DWG compatibility, 99%+ command/shortcut parity, direct LISP execution, and 75% TCO perpetual license savings calculator.
2. **Official Learning & Tutorials** (`tutorials.html`): Official GstarCAD courses, GstarCAD Mechanical (standard parts, automated BOM), Architecture (parametric AEC objects), and DWG FastView field workflows.
3. **Skill Certification & Assessment** (`quiz.html`): Official GstarCAD skill credentialing engine across 6 engineering tracks (~289 questions), mistake book, and digital certificate verification.
4. **Developer Hub** (`developers.html`): C++ GRX (ObjectARX equivalent SDK), .NET API, and AutoLISP porting guides for global ISV partners.
5. **Commercial Funnel** (`download.html`): Full 30-day trial downloads, system specs, enterprise quotes, and global distributor locator.
6. **Knowledge base** (`knowledge-*.html`): Engineering fundamentals, ISO/ASME standards, and interactive D3 concept graph.

User journey: **evaluate & migrate (Migration Hub) → master tools (Academy) → certify competence (Certification) → expand enterprise adoption (Distributor/Trial)**.

## Key paths

- Visual / UX intent: `DESIGN.md`
- PRD (Chinese): `PRD-知识库导航聚合站.md`
- AutoCAD Migration Hub: `migration.html`
- Free Trial Download: `download.html`
- Developer GRX Hub: `developers.html`
- KB split generator: `scripts/split_knowledge_pages.py`
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
- Prefer separate pages over huge single-page anchor navigation for primary IA.
- Ensure all brand copy and enterprise ownership consistently attributes **Suzhou Gstarsoft Co., Ltd. (SSE: 688657)**.
