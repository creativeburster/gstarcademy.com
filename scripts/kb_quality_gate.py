#!/usr/bin/env python3
"""
KB quality gate for gstarcademy.com.

1. --strip   Remove generic boilerplate <p>/<li> blocks (sentences repeated on
             >= STRIP_FREQ pages after substituting the page's own term name).
2. --gate    noindex + drop from sitemap.xml any KB page that is still mostly
             template text (ratio >= MAX_TEMPLATE_RATIO) or has too little
             page-specific text (unique words < MIN_UNIQUE_WORDS). Pages that
             were gated earlier and now pass are restored (index + sitemap).

Only pages carrying the gate's own marker (data-quality-gate) are ever
restored, so manual noindex decisions are left alone.

Usage:
  python scripts/kb_quality_gate.py              # dry run report
  python scripts/kb_quality_gate.py --strip --gate --write
"""
import argparse, collections, datetime, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_DIRS = ("concepts", "software", "vendors", "guides", "faq")
TEMPLATE_FREQ = 15        # sentence shared by >= N pages counts as template
STRIP_FREQ = 50           # sentence shared by >= N pages is stripped outright
MAX_TEMPLATE_RATIO = 0.70
MIN_UNIQUE_WORDS = 200
GATE_META = '<meta name="robots" content="noindex, follow" data-quality-gate="1" />'
INDEX_META = '<meta name="robots" content="index, follow, max-image-preview:large" />'
# Site chrome / widget copy that legitimately repeats on every page.
CHROME_RE = re.compile("|".join([
    r"^Article text is official engineering documentation",
    r"(?:Vendor|Software) names and trademarks belong",
    r"^Pricing is approximate",
    r"^Direct answers from our technical editorial desk",
    r"^Test your understanding of this concept",
    r"^Explore cross-referenced learning lanes",
    r"^Core glossary, interactive graph",
    r"^Parent design environments and platforms",
    r"^The official engineering education team at Suzhou Gstarsoft",
    r"^Step-by-step practical exercises and certification-aligned paths",
    r"^Ready to benchmark GstarCAD",
    r"^Download the full-function 30-day trial",
]), re.I)
ROBOTS_RE = re.compile(r'<meta\s+(?:name="robots"\s+content="[^"]*"|content="[^"]*"\s+name="robots")[^>]*/?>', re.I)


def load_pages():
    pages = {}
    for sub in KB_DIRS:
        d = os.path.join(ROOT, "kb", sub)
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            rel = f"kb/{sub}/{f}"
            html = open(os.path.join(d, f), encoding="utf-8").read()
            robots = ROBOTS_RE.search(html)
            gated = 'data-quality-gate' in html
            manual_noindex = bool(robots and 'noindex' in robots.group(0).lower() and not gated)
            if manual_noindex or 'http-equiv="refresh"' in html.lower():
                continue
            pages[rel] = {"html": html, "gated": gated}
    return pages


def term_name(html):
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', html)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ""


def plain(fragment):
    t = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', fragment)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', re.sub(r'&[a-z#0-9]+;', ' ', t)).strip()


def norm_sentences(text, name, min_len=60):
    # "PythonParts (Allplan)" -> term "PythonParts", family "Allplan"; both are
    # substituted so per-family templates ("Deploying X (Y) in a commercial…")
    # are recognised as the same sentence across every software family.
    short = re.sub(r'\s*\(.*?\)\s*', '', name).strip()
    fam_m = re.search(r'\(([^()]+)\)\s*$', name)
    family = fam_m.group(1).strip() if fam_m else ""
    out = []
    for s in re.split(r'(?<=[.!?:])\s+|\n', text):
        s = s.strip()
        if len(s) < min_len:
            continue
        t = s
        for n in (name, short):
            if n:
                t = t.replace(n, "X")
        if len(family) >= 3:
            t = t.replace(family, "Y")
        t = re.sub(r'\s+', ' ', t.lower()).strip()
        if CHROME_RE.search(s) or re.fullmatch(r'[xy\W]*', t):
            continue
        out.append((s, t))
    return out


def main_text(html):
    m = re.search(r'<main[\s\S]*?</main>', html)
    body = m.group(0) if m else html
    body = re.sub(r'<div class="ink-byline"[\s\S]*?</div>', ' ', body)
    # keep block boundaries so sentences never span two <p>/<li> blocks
    body = re.sub(r'</(?:p|li|h[1-6]|td|th|dd|dt|div|section|figcaption)>', '\n', body, flags=re.I)
    body = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'&[a-z#0-9]+;', ' ', body)
    return "\n".join(re.sub(r'[ \t\r\f\v]+', ' ', ln).strip() for ln in body.split("\n") if ln.strip())


def sentence_freq(pages):
    freq = collections.Counter()
    for p in pages.values():
        p["name"] = term_name(p["html"])
        for t in {t for _, t in norm_sentences(main_text(p["html"]), p["name"], min_len=25)}:
            freq[t] += 1
    return freq


def strip_boilerplate(html, name, freq):
    removed = 0

    def is_boiler(block_inner):
        txt = re.sub(r'<br\s*/?>|</?(?:div|span)[^>]*>', '\n', block_inner)
        txt = re.sub(r'<[^>]+>', ' ', txt)
        txt = "\n".join(re.sub(r'\s+', ' ', ln).strip() for ln in re.sub(r'&[a-z#0-9]+;', ' ', txt).split("\n"))
        ss = norm_sentences(txt, name, min_len=25)
        return bool(ss) and all(freq[t] >= STRIP_FREQ for _, t in ss)

    def kill(m):
        nonlocal removed
        inner = m.group(2)
        if '<li' in inner and m.group(1) == 'li':
            return m.group(0)
        # never strip sources, citations or standards references
        if re.search(r'href=["\']https?://', inner) or \
                re.search(r'\b(?:ISO|ASME|ASTM|IEC|EN|DIN|AASHTO|NAFEMS|CEMA|CMH)[\s\-]?[0-9/]', plain(inner)):
            return m.group(0)
        if is_boiler(inner):
            removed += 1
            return ''
        return m.group(0)

    m = re.search(r'<main[\s\S]*?</main>', html)
    if not m:
        return html, 0
    main = m.group(0)
    main = re.sub(r'<(p|li|pre)\b[^>]*>([\s\S]*?)</\1>', kill, main)
    for _ in range(3):  # cascade: empty lists -> empty wrappers -> orphaned headings
        main = re.sub(r'<(ul|ol)\b[^>]*>\s*</\1>', '', main)
        main = re.sub(r'<div\b[^>]*>\s*</div>', '', main)
        # heading body may not contain another heading tag, so a match can never span sections
        main = re.sub(r'<h([2-4])\b[^>]*>(?:(?!</?h[1-6]\b)[\s\S])*?</h\1>\s*(?=<h[1-4]\b|</section>|</div>|</article>|</main>)', '', main)

    def drop_empty_section(sm):
        inner = re.sub(r'<h[23][^>]*>[\s\S]*?</h[23]>', '', sm.group(0))
        if re.search(r'href=["\']https?://', inner):
            return sm.group(0)  # sections holding external sources are always kept
        return '' if len(plain(inner)) < 5 else sm.group(0)
    main = re.sub(r'<section\b[^>]*>(?:(?!<section)[\s\S])*?</section>', drop_empty_section, main)
    return html.replace(m.group(0), main), removed


STRUCT_TAGS = ("section", "div", "ul", "ol", "article", "main", "table", "pre")


def balance(html):
    return {t: len(re.findall(rf"<{t}\b", html)) - len(re.findall(rf"</{t}>", html)) for t in STRUCT_TAGS}


def score(html, name, freq):
    ss = norm_sentences(main_text(html), name)
    total = sum(len(s.split()) for s, _ in ss) or 1
    templ = sum(len(s.split()) for s, t in ss if freq[t] >= TEMPLATE_FREQ)
    return templ / total, total - templ


def set_robots(html, gate):
    new = GATE_META if gate else INDEX_META
    if ROBOTS_RE.search(html):
        return ROBOTS_RE.sub(new, html, count=1)
    return html.replace('</title>', '</title>\n    ' + new, 1)


def page_url(rel):
    return "https://gstarcademy.com/" + (rel[:-len("index.html")] if rel.endswith("/index.html") else rel[:-5])


def update_sitemap(to_remove, to_add):
    path = os.path.join(ROOT, "sitemap.xml")
    sm = open(path, encoding="utf-8").read()
    for rel in to_remove:
        loc = page_url(rel)
        sm = re.sub(r'\s*<url>\s*<loc>' + re.escape(loc) + r'</loc>[\s\S]*?</url>', '', sm)
    today = datetime.date.today().isoformat()
    add = "".join(
        f"\n  <url>\n    <loc>{page_url(rel)}</loc>\n    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        for rel in to_add if f"<loc>{page_url(rel)}</loc>" not in sm)
    sm = sm.replace("</urlset>", add + "\n</urlset>", 1) if add else sm
    open(path, "w", encoding="utf-8", newline="\n").write(sm)


def run(args):
    pages = load_pages()
    freq = sentence_freq(pages)
    stripped_blocks = stripped_pages = 0
    if args.strip:
        for rel, p in pages.items():
            new, n = strip_boilerplate(p["html"], p["name"], freq)
            if n and balance(new) != balance(p["html"]):
                print("  SKIP (would change tag balance):", rel)
                continue
            if n:
                p["html"], stripped_blocks, stripped_pages = new, stripped_blocks + n, stripped_pages + 1
                p["dirty"] = True
        freq = sentence_freq(pages)  # rescore on stripped corpus

    gate, restore, keep_gated = [], [], 0
    for rel, p in pages.items():
        ratio, unique = score(p["html"], p["name"], freq)
        p["ratio"], p["unique"] = ratio, unique
        fails = ratio >= MAX_TEMPLATE_RATIO or unique < MIN_UNIQUE_WORDS
        if rel.endswith("/index.html"):
            fails = False  # hub/listing pages are navigation, never gated
        if args.gate and fails and not p["gated"]:
            gate.append(rel)
        elif args.gate and not fails and p["gated"]:
            restore.append(rel)
        elif fails and p["gated"]:
            keep_gated += 1

    print(f"KB pages evaluated: {len(pages)}")
    if args.strip:
        print(f"boilerplate blocks stripped: {stripped_blocks} across {stripped_pages} pages")
    print(f"failing gate (ratio>={MAX_TEMPLATE_RATIO} or unique<{MIN_UNIQUE_WORDS}): "
          f"{sum(1 for p in pages.values() if p['ratio'] >= MAX_TEMPLATE_RATIO or p['unique'] < MIN_UNIQUE_WORDS)}")
    print(f"  newly gated: {len(gate)} | restored: {len(restore)} | still gated: {keep_gated}")
    by_dir = collections.Counter(r.split('/')[1] for r in gate)
    print("  newly gated by dir:", dict(by_dir))

    if args.write:
        for rel in gate:
            pages[rel]["html"] = set_robots(pages[rel]["html"], True); pages[rel]["dirty"] = True
        for rel in restore:
            pages[rel]["html"] = set_robots(pages[rel]["html"], False); pages[rel]["dirty"] = True
        for rel, p in pages.items():
            if p.get("dirty"):
                open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="\n").write(p["html"])
        update_sitemap(gate, restore)
        print("written.")
    return pages


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--strip", action="store_true")
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--min-unique", type=int, default=MIN_UNIQUE_WORDS)
    a = ap.parse_args()
    MIN_UNIQUE_WORDS = a.min_unique
    run(a)
