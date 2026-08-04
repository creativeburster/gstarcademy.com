#!/usr/bin/env python3
"""
IndexNow 提交工具
=================
用法:
  python indexnow_submit.py                # 全量提交（sitemap 全部 URL）
  python indexnow_submit.py --changed-only # 增量提交（仅本次 git push 变动的 URL）
  python indexnow_submit.py --dry-run      # 预览，不实际提交（可与上面任意组合）
"""

import sys
import json
import time
import subprocess
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

# =========================================================
# 配置
# =========================================================
SITE_HOST    = "gstarcademy.com"
SITE_URL     = f"https://{SITE_HOST}"
# 优先从 GitHub Actions Secret（环境变量）读取，本地回退到硬编码
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY", "971d09674aa0434e8e9a4a0b62165f2e")
KEY_LOCATION = f"{SITE_URL}/{INDEXNOW_KEY}.txt"
API_ENDPOINT = "https://api.indexnow.org/IndexNow"
BATCH_SIZE   = 100   # 每批上限（IndexNow 支持最多 10,000）
DELAY_SEC    = 2     # 批次间隔，防限流

# 脚本所在目录的上一级 = 项目根目录
ROOT_DIR     = Path(__file__).resolve().parent.parent
SITEMAP_PATH = ROOT_DIR / "sitemap.xml"
# =========================================================


# ── 文件名 → URL 映射规则 ──────────────────────────────
def file_to_url(filepath: str) -> str | None:
    """
    将仓库内文件路径转换为线上 URL。
    支持：
      index.html          → https://gstarcademy.com/
      about.html          → https://gstarcademy.com/about
      kb/concepts/foo.html→ https://gstarcademy.com/kb/concepts/foo
      sitemap.xml / *.txt → 不提交
    """
    p = Path(filepath)
    # 只处理 .html 文件
    if p.suffix != ".html":
        return None
    # 去掉扩展名
    stem = p.with_suffix("")
    # index → 根路径
    if stem.name == "index" and stem.parent == Path("."):
        return SITE_URL + "/"
    # 其余：直接拼接相对路径（无 .html）
    rel = stem.as_posix()
    return f"{SITE_URL}/{rel}"


# ── 全量：从 sitemap 获取 URL ──────────────────────────
def urls_from_sitemap() -> list[str]:
    if not SITEMAP_PATH.exists():
        print(f"[ERROR] 找不到 sitemap: {SITEMAP_PATH}")
        sys.exit(1)
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    ns   = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in root.findall(".//sm:loc", ns) if loc.text]
    return [u for u in urls if SITE_HOST in u]


# ── 增量：从 git diff 获取本次变动的 HTML 文件 ──────────
def urls_from_git_diff() -> list[str]:
    """
    比较 HEAD~1..HEAD 变动文件，提取 .html 对应的线上 URL。
    若 git 不可用或无变化，回退到全量模式。
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True, text=True, cwd=ROOT_DIR, timeout=15
        )
        changed_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except Exception as e:
        print(f"[WARN] git diff 失败（{e}），回退到全量模式")
        return urls_from_sitemap()

    urls = []
    skipped = []
    for f in changed_files:
        url = file_to_url(f)
        if url:
            urls.append(url)
        else:
            skipped.append(f)

    if skipped:
        print(f"  跳过非 HTML 变动文件 ({len(skipped)} 个): "
              + ", ".join(skipped[:5]) + ("..." if len(skipped) > 5 else ""))

    if not urls:
        print("[INFO] 本次 push 无 HTML 变动，回退到全量模式（sitemap）")
        return urls_from_sitemap()

    return urls


# ── 批量提交 ────────────────────────────────────────────
def submit_batch(url_list: list[str], dry_run: bool = False) -> bool:
    payload = {
        "host":        SITE_HOST,
        "key":         INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList":     url_list,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    if dry_run:
        print(f"  [DRY-RUN] 待提交 {len(url_list)} 个 URL:")
        for u in url_list[:5]:
            print(f"    {u}")
        if len(url_list) > 5:
            print(f"    ...（另 {len(url_list) - 5} 个）")
        return True

    req = urllib.request.Request(
        API_ENDPOINT,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.status
            if code in (200, 202):
                tag = "已接受" if code == 202 else "成功"
                print(f"  ✅ {tag}（HTTP {code}）— {len(url_list)} 个 URL")
                return True
            else:
                print(f"  ⚠️  HTTP {code} — {len(url_list)} 个 URL")
                return False
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP {e.code} {e.reason}")
        hints = {
            403: "密钥验证失败：确认 key 文件已部署至网站根目录",
            422: "URL 不属于指定 host 或密钥格式错误",
            429: "请求过于频繁，请稍后重试",
        }
        if e.code in hints:
            print(f"     → {hints[e.code]}")
        return False
    except Exception as ex:
        print(f"  ❌ 请求异常: {ex}")
        return False


# ── 主程序 ───────────────────────────────────────────────
def main():
    args         = set(sys.argv[1:])
    dry_run      = "--dry-run"      in args
    changed_only = "--changed-only" in args

    mode_label = "增量（git diff）" if changed_only else "全量（sitemap）"
    print("=" * 60)
    print(f"IndexNow 提交 | {SITE_HOST}")
    print(f"模式: {mode_label}" + ("  [DRY-RUN]" if dry_run else ""))
    print("=" * 60)

    urls = urls_from_git_diff() if changed_only else urls_from_sitemap()
    print(f"\n📋 待提交 URL 数量: {len(urls)}")

    if not urls:
        print("无需提交，退出。")
        sys.exit(0)

    total_batches = (len(urls) + BATCH_SIZE - 1) // BATCH_SIZE
    submitted = 0

    for i in range(0, len(urls), BATCH_SIZE):
        batch     = urls[i : i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        print(f"\n📦 批次 {batch_num}/{total_batches}")
        if submit_batch(batch, dry_run=dry_run):
            submitted += len(batch)
        if not dry_run and batch_num < total_batches:
            time.sleep(DELAY_SEC)

    print("\n" + "=" * 60)
    status = "✅" if submitted == len(urls) else "⚠️ "
    print(f"{status} 完成：{submitted}/{len(urls)} 个 URL 已提交")
    print("=" * 60)
    if not dry_run and submitted > 0:
        print(f"\n验证：https://www.bing.com/webmasters/")


if __name__ == "__main__":
    main()
