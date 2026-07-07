"""Shared enrichment library for KB phase-1 content-moat work.

Replaces the body sections of thin KB concept pages with richer, topic-specific
content while preserving page chrome (header, byline, editorial aside).

Section region replaced: everything between the byline </div> and the trailing
editorial <aside ...>. We rebuild kb-concept-section blocks from structured data.
"""
import re


def build_sections(data):
    """data keys:
      definition: list[str] paragraphs (HTML allowed)
      why: str paragraph (HTML)  -- 'Why It Matters'
      practices: list[str] bullet items (HTML)
      pitfalls: list[str] bullet items (HTML)
      software: list[str] -- optional 'Tools & Software' items
      standards: list[str] -- optional 'Standards & References' items with <a>
      refs: list[(label,url)] -- external references
    """
    out = []

    def sec(title, inner):
        out.append(
            '        <section class="kb-concept-section">\n'
            f'          <h2>{title}</h2>\n{inner}        </section>\n'
        )

    defs = "".join(f"          <p>{p}</p>\n" for p in data["definition"])
    sec("Definition &amp; Context", defs)

    if data.get("why"):
        sec("Why It Matters", f"          <p>{data['why']}</p>\n")

    if data.get("software"):
        items = "".join(f"            <li>{i}</li>\n" for i in data["software"])
        sec("Tools &amp; Software", f"          <ul>\n{items}          </ul>\n")

    prac = "".join(f"            <li>{i}</li>\n" for i in data["practices"])
    sec("Best Practices", f"          <ul>\n{prac}          </ul>\n")

    pit = "".join(f"            <li>{i}</li>\n" for i in data["pitfalls"])
    sec("Common Pitfalls", f"          <ul>\n{pit}          </ul>\n")

    if data.get("standards"):
        items = "".join(f"            <li>{i}</li>\n" for i in data["standards"])
        sec("Standards &amp; Interoperability",
            f"          <ul>\n{items}          </ul>\n")

    if data.get("refs"):
        links = "".join(
            f'            <li><a href="{u}" target="_blank" rel="noopener nofollow">{lbl}</a></li>\n'
            for lbl, u in data["refs"]
        )
        sec("Sources &amp; Further Reading",
            f"          <ul>\n{links}          </ul>\n")

    return "".join(out)


SECTION_BLOCK = re.compile(
    r'(<div class="ink-byline".*?</div>\s*\n)(.*?)(\s*<aside)',
    re.S,
)


def enrich_file(path, data):
    with open(path, encoding="utf-8") as f:
        c = f.read()

    new_sections = build_sections(data)
    m = SECTION_BLOCK.search(c)
    if not m:
        return False, "no byline/aside region"
    new_c = c[:m.start(2)] + "\n" + new_sections + c[m.end(2):]

    # Refresh description meta + review byline signal
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_c)
    return True, "ok"
