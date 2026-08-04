#!/usr/bin/env python3
"""
meta description 批量修复脚本
==============================
扫描 kb/ 下所有 HTML，找出 meta description 长度 < 120 字符的页面，
从页面内容（hero-sub + 正文段落）自动生成 150-165 字符描述，
同步更新 name="description" / og:description / twitter:description。

用法:
  python scripts/fix_meta_descriptions.py --dry-run   # 仅预览
  python scripts/fix_meta_descriptions.py             # 正式修改
"""

import re
import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT       = Path(__file__).resolve().parent.parent
KB_DIR     = ROOT / "kb"
MIN_LEN    = 120   # 短于此视为需要修复
TARGET_LEN = 158   # 目标长度
DRY_RUN    = "--dry-run" in sys.argv


# ── HTML 解析器 ────────────────────────────────────────────

class MetaParser(HTMLParser):
    """提取 meta description、hero-sub、h1、所有正文段落"""

    def __init__(self):
        super().__init__()
        self.meta_desc  = ""
        self.og_desc    = ""
        self.tw_desc    = ""
        self.title_tag  = ""
        self.h1_text    = ""
        self.paragraphs: list[str] = []
        self._in_title  = False
        self._in_h1     = False
        self._in_p      = False
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta":
            name    = d.get("name", "")
            prop    = d.get("property", "")
            content = d.get("content", "")
            if name == "description":
                self.meta_desc = content
            elif prop == "og:description":
                self.og_desc = content
            elif name == "twitter:description":
                self.tw_desc = content
        elif tag == "title":
            self._in_title = True
            self._buf = []
        elif tag == "h1":
            self._in_h1 = True
            self._buf = []
        elif tag == "p" and not self._in_p:
            self._in_p = True
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self._in_title = False
            self.title_tag = "".join(self._buf).strip()
        elif tag == "h1" and self._in_h1:
            self._in_h1 = False
            self.h1_text = "".join(self._buf).strip()
        elif tag == "p" and self._in_p:
            self._in_p = False
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if len(text) > 20:
                self.paragraphs.append(text)
            self._buf = []

    def handle_data(self, data):
        if self._in_title or self._in_h1 or self._in_p:
            self._buf.append(data)


# ── 描述生成 ────────────────────────────────────────────────

def strip_suffix(title: str) -> str:
    return re.sub(r"\s*\|.*$", "", title).strip()


def trim_to(text: str, max_len: int) -> str:
    """在单词边界截断到 max_len，末尾加省略号"""
    if len(text) <= max_len:
        return text
    cut = text[:max_len]
    sp  = cut.rfind(" ")
    if sp > max_len - 25:
        cut = cut[:sp]
    return cut + "…"


def build_description(parser: MetaParser, filename: str) -> str:
    """合成 MIN_LEN ~ TARGET_LEN+5 字符的 meta description"""
    topic = (
        parser.h1_text
        or strip_suffix(parser.title_tag)
        or Path(filename).stem.replace("-", " ").title()
    )
    SUFFIX = " | Gstarcademy CAD/BIM knowledge base."

    # 拼接所有段落（去重）
    seen, unique = set(), []
    for p in parser.paragraphs:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    body = " ".join(unique)
    body = re.sub(r"\s+", " ", body).strip()

    if body:
        candidate = body + SUFFIX
        result = trim_to(candidate, TARGET_LEN)

        # 如果段落太短导致结果仍不足，追加通用补语
        if len(result) < MIN_LEN:
            extra = (
                f" Covers tools, workflows, best practices, and tips "
                f"for {topic} in professional CAD and BIM environments."
            )
            result = trim_to(body + extra + SUFFIX, TARGET_LEN + 10)
        return result

    # 无正文：纯通用句
    return (
        f"In-depth guide to {topic}: definitions, key features, software support, "
        f"workflows, and best practices for engineers and designers using CAD and BIM tools."
    )[:TARGET_LEN + 5]


# ── HTML 就地替换 ─────────────────────────────────────────

_RE_META  = re.compile(r'(<meta\s+name="description"\s+content=")[^"]*(")', re.I)
_RE_OG    = re.compile(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', re.I)
_RE_TW    = re.compile(r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")', re.I)


def update_html(path: Path, new_desc: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    orig = text
    repl = lambda m: m.group(1) + new_desc + m.group(2)
    text = _RE_META.sub(repl, text, count=1)
    text = _RE_OG.sub(repl, text, count=1)
    text = _RE_TW.sub(repl, text, count=1)
    if text != orig:
        if not DRY_RUN:
            path.write_text(text, encoding="utf-8")
        return True
    return False


# ── 主程序 ─────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"Meta Description 修复工具{'  [DRY-RUN]' if DRY_RUN else ''}")
    print("=" * 60)

    html_files = sorted(KB_DIR.rglob("*.html"))
    print(f"\n扫描 {len(html_files)} 个 HTML 文件...\n")

    need_fix: list[tuple[Path, str]] = []
    for path in html_files:
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"  [ERR] {path.name}: {e}")
            continue
        p = MetaParser()
        p.feed(raw)
        if len(p.meta_desc.strip()) < MIN_LEN:
            need_fix.append((path, p.meta_desc.strip()))

    print(f"需修复：{len(need_fix)} 个（meta description < {MIN_LEN} 字符）\n")

    fixed = 0
    still_short = 0
    for path, old_desc in need_fix:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        parser = MetaParser()
        parser.feed(raw)

        new_desc = build_description(parser, path.name)
        rel = path.relative_to(ROOT)

        flag = "⚠️ " if len(new_desc) < MIN_LEN else "✅"
        if len(new_desc) < MIN_LEN:
            still_short += 1

        print(f"{'[DRY]' if DRY_RUN else '[FIX]'} {flag} {rel}")
        print(f"  旧({len(old_desc)}): {old_desc[:70]}")
        print(f"  新({len(new_desc)}): {new_desc[:70]}{'…' if len(new_desc)>70 else ''}")

        if update_html(path, new_desc):
            fixed += 1

    print("\n" + "=" * 60)
    print(f"{'预览' if DRY_RUN else '完成'}：{fixed} 个文件已修复")
    if still_short:
        print(f"⚠️  {still_short} 个页面正文极短，新描述仍 < {MIN_LEN} 字符（需人工补充内容）")
    print("=" * 60)


if __name__ == "__main__":
    main()
