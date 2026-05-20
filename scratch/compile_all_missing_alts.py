import paramiko
import json

hostname = "c1100271.sgvps.net"
username = "u2-74dmvatthvme"
port = 18765
key_path = r"C:\Users\willp\Desktop\26年5月\siteground_key"
passphrase_file = r"C:\Users\willp\Desktop\26年5月\key_passphrase.txt"
wp_path = "www/blog.dwgfastview.com/public_html"

def run_command(cmd):
    with open(passphrase_file, "r", encoding="utf-8") as f:
        passphrase_val = f.read().strip()
        
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase_val)
        ssh.connect(hostname, port=port, username=username, pkey=key, timeout=15)
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        ssh.close()
        return out, err
    except Exception as e:
        return "", str(e)

print("=== SAFE DB QUERY: Auditing all missing Alt images inside published posts ===")

# Let's write the helper python script to a file on the remote server
remote_py_code = """
import json
import subprocess
import re

wp_path = 'www/blog.dwgfastview.com/public_html'

# Get ALL published posts
cmd = ['wp', '--path=' + wp_path, 'post', 'list', '--post_type=post', '--post_status=publish', '--posts_per_page=9999', '--format=json', '--fields=ID,post_title,post_name,post_content']
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
posts = json.loads(res.stdout.decode())

audit_list = []

for p in posts:
    content = p['post_content']
    img_tags = re.findall(r'<img[^>]+>', content)
    for tag in img_tags:
        # Check if alt is missing or empty
        has_empty_alt = False
        if 'alt=' not in tag:
            has_empty_alt = True
        else:
            # Check for empty alt: alt="" or alt=''
            if re.search(r'alt=\\s*["\\']["\\']', tag) or re.search(r'alt=\\s*$', tag):
                has_empty_alt = True
        
        if has_empty_alt:
            src_match = re.search(r'src=\\s*["\\']([^"\\']+)["\\']', tag)
            src = src_match.group(1) if src_match else 'Unknown Src'
            
            # Categorize the image type based on filename
            filename = src.split('/')[-1].lower() if src else ''
            img_type = 'Article Content Image'
            if any(x in filename for x in ['logo', 'cropped', 'icon']):
                img_type = 'Theme Asset/Logo'
            elif any(x in filename for x in ['button', 'banner', 'pasted-15', 'buy']):
                img_type = 'Button/Promo Banner'
            
            audit_list.append({
                'post_title': p['post_title'],
                'post_url': 'https://blog.dwgfastview.com/' + p['post_name'],
                'image_src': src,
                'image_type': img_type
            })

print(json.dumps(audit_list))
"""

# Upload the helper python script
run_command(f"cat << 'EOF' > www/compile_missing.py\n{remote_py_code}\nEOF")

# Execute
out, err = run_command("python3 www/compile_missing.py")

# Cleanup remote helper
run_command("rm www/compile_missing.py")

if err:
    print("Error executing remote script:", err)
    exit()

try:
    audit_data = json.loads(out)
    print(f"Audit completed. Found {len(audit_data)} missing alt instances in active post content.")
    
    # Generate a beautiful Markdown file locally
    md_lines = [
        "# 📋 blog.dwgfastview.com 所有缺失 Alt 属性的图片审计列表\n",
        "这份报告详细列出了您博客中**所有已发布文章的正文里**，实际存在且目前缺失 `alt` 属性（或 `alt` 为空）的图片。\n",
        "我已对图片进行了分类整理（区分了 **普通文章内容插图**、**推广条幅/按钮** 以及 **网站 Logo/图标**），以便您和运营团队进行精确筛选。\n",
        "---",
        "## 1. 核心文章插图列表 (Article Content Images) —— 💡 建议优化",
        "以下是真实存在于教程和内容正文里的插图，优化这部分 Alt 属性对 SEO 图片流量提升最大：\n",
        "| 文章标题 | 页面链接 | 图片源文件链接 | 属性类别 |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    content_imgs = [x for x in audit_data if x['image_type'] == 'Article Content Image']
    other_imgs = [x for x in audit_data if x['image_type'] != 'Article Content Image']
    
    for x in content_imgs:
        md_lines.append(f"| {x['post_title']} | [点击查看]({x['post_url']}) | [{x['image_src'].split('/')[-1]}]({x['image_src']}) | 🟢 {x['image_type']} |")
        
    md_lines.append("\n---\n")
    md_lines.append("## 2. 推广条幅/按钮/Logo 列表 (Theme Assets & Promo Banners) —— ⚠️ 可选择不修改")
    md_lines.append("以下是导航按钮、标志或侧边栏推广，通常不需要设置特别的 SEO Alt 描述（可忽略）：\n")
    md_lines.append("| 文章标题 | 页面链接 | 图片源文件链接 | 属性类别 |")
    md_lines.append("| :--- | :--- | :--- | :--- |")
    
    for x in other_imgs:
        md_lines.append(f"| {x['post_title']} | [点击查看]({x['post_url']}) | [{x['image_src'].split('/')[-1]}]({x['image_src']}) | ⚠️ {x['image_type']} |")
        
    # Write the artifact file
    artifact_path = r"C:\Users\willp\.gemini\antigravity\brain\8d461473-cce1-4f43-a0f2-412744f2f718\all_missing_alt_images.md"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print(f"Artifact created successfully: {artifact_path}")
    
except Exception as e:
    print("Error parsing json output or writing file:", e)
    print("Raw output:", out[:500])
