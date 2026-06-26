import json
import os
import re

def convert_config():
    vercel_json_path = "vercel.json"
    if not os.path.exists(vercel_json_path):
        print(f"Error: {vercel_json_path} not found.")
        return

    with open(vercel_json_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 1. 转换 Redirects
    redirects = config.get("redirects", [])
    redirect_lines = []
    for r in redirects:
        source = r.get("source")
        destination = r.get("destination")
        permanent = r.get("permanent", True)
        status = 301 if permanent else 302
        
        # 简单转换正则通配符为 Cloudflare 格式
        # 我们的 vercel.json 大多是固定路径重定向，这里做基本的字符串清理
        redirect_lines.append(f"{source} {destination} {status}")

    with open("_redirects", "w", encoding="utf-8") as f:
        f.write("\n".join(redirect_lines) + "\n")
    print(f"Successfully generated _redirects with {len(redirect_lines)} rules.")

    # 2. 转换 Headers
    headers = config.get("headers", [])
    header_lines = []
    for h in headers:
        source = h.get("source")
        # 将 Vercel 的正则匹配转换成 Cloudflare Pages 的通配符匹配
        # 比如 /(.*).min.css -> /*.min.css
        # /(.*) -> /*
        cf_source = source
        if "(.*)" in cf_source:
            cf_source = cf_source.replace("(.*)", "*")
        
        header_lines.append(cf_source)
        for header_item in h.get("headers", []):
            key = header_item.get("key")
            value = header_item.get("value")
            header_lines.append(f"  {key}: {value}")
        # 空行分隔
        header_lines.append("")

    with open("_headers", "w", encoding="utf-8") as f:
        f.write("\n".join(header_lines) + "\n")
    print(f"Successfully generated _headers with {len(headers)} blocks.")

if __name__ == "__main__":
    convert_config()
