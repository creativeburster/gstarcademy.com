"""Replace placeholder data-URI favicons with path-based favicon.svg."""

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

BLOCK = """    <link
      rel="icon"
      type="image/svg+xml"
      href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3C/svg%3E"
    />
    <link rel="shortcut icon" href="data:image/x-icon;," />
    <link rel="apple-touch-icon" href="data:image/png;," />"""

BLOCK_PILOT = """    <link
      rel="icon"
      type="image/svg+xml"
      href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3C/svg%3E"
    />"""

TOPIC_OLD = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 16 16\'%3E%3C/svg%3E" type="image/svg+xml" />'


def main() -> int:
    for p in REPO.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        changed = False
        if BLOCK in t:
            depth = len(p.relative_to(REPO).parts) - 1
            prefix = "../" * depth if depth else "./"
            rep = f'    <link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg" />'
            t = t.replace(BLOCK, rep, 1)
            changed = True
        if BLOCK_PILOT in t:
            depth = len(p.relative_to(REPO).parts) - 1
            prefix = "../" * depth if depth else "./"
            rep = f'    <link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg" />'
            t = t.replace(BLOCK_PILOT, rep, 1)
            changed = True
        if TOPIC_OLD in t:
            depth = len(p.relative_to(REPO).parts) - 1
            prefix = "../" * depth if depth else "./"
            t = t.replace(
                TOPIC_OLD,
                f'<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg" />',
                1,
            )
            changed = True
        if changed:
            p.write_text(t, encoding="utf-8")
            print("+", p.relative_to(REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
