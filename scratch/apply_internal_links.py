import paramiko

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

print("=== DEPLOYING OPTIMIZED MULTI-LINGUAL INTERNAL LINK WEB ===")

# The real execution python script that will run on the server
execution_py_code = """
import json
import subprocess
import re
import os

wp_path = 'www/blog.dwgfastview.com/public_html'

# Language-specific keyword-to-destination mappings
# Groups terms by their language and lists target destinations within that language
language_clusters = {
    # 1. English Cluster (en)
    'en': {
        'https://blog.dwgfastview.com/free-rvt-viewer-view-rvt-files-online-free-best-revit-viewer-recommended/': [
            'Revit Viewer', 'RVT Viewer', 'view RVT files', 'Revit', 'RVT'
        ],
        'https://blog.dwgfastview.com/view-sldprt-and-sldasm-files-easily-and-free/': [
            'SolidWorks Viewer', 'SLDPRT Viewer', 'view SLDPRT', 'SolidWorks', 'SLDPRT', 'SLDASM'
        ],
        'https://blog.dwgfastview.com/best-free-step-stp-file-viewer-dwg-fastview/': [
            'STEP Viewer', 'STP Viewer', 'STP file viewer', 'STP', 'STEP'
        ]
    },
    
    # 2. Spanish Cluster (es)
    'es': {
        'https://blog.dwgfastview.com/es/free-rvt-viewer-view-rvt-files-online-free-best-revit-viewer-recommended/': [
            'visualizador Revit', 'visualizar archivos RVT', 'lector RVT', 'Revit', 'RVT'
        ],
        'https://blog.dwgfastview.com/es/visualiza-archivos-sldprt-y-sldasm-de-forma-facil-y-gratuita/': [
            'visualizar archivos SLDPRT', 'visor SLDPRT', 'visor de SolidWorks', 'SolidWorks', 'SLDPRT'
        ]
    },
    
    # 3. Traditional/Simplified Chinese Cluster (zh)
    'zh': {
        'https://blog.dwgfastview.com/zh/最好的免費步驟-stp-檔案檢視器-dwg-fastview/': [
            'STP 檔案檢視', 'STP 檢視器', 'STEP 檔案', 'STP檔案', 'STP檢視', 'STP查看', 'STP'
        ],
        'https://blog.dwgfastview.com/zh/輕鬆免費地查看-sldprt-和-sldasm-文件/': [
            '查看 SLDPRT', 'SLDPRT 檢視', 'SLDPRT 檔案', 'SLDPRT檔案', 'SLDPRT查看', 'SolidWorks'
        ],
        'https://blog.dwgfastview.com/zh/使用dwg-fastview完全替代dwg-trueview/': [
            '替代 DWG TrueView', 'TrueView 替代', 'DWG TrueView', '替代TrueView', 'TrueView'
        ]
    },
    
    # 4. Russian Cluster (ru)
    'ru': {
        'https://blog.dwgfastview.com/ru/бесплатно-rvt-viewer-view-rvt-files-online-free-best-revit-viewer-рекомендуется/': [
            'просмотр RVT', 'просмотра файлов RVT', 'RVT просмотрщик', 'Revit', 'RVT'
        ],
        'https://blog.dwgfastview.com/ru/просматривать-файлы-sldprt-и-sldasm-легко-и-беспл/': [
            'просмотр SLDPRT', 'просмотра файлов SLDPRT', 'открыть SLDPRT', 'SolidWorks', 'SLDPRT'
        ]
    }
}

def detect_language(title, content):
    # Russian Cyrillic check
    if re.search(r'[а-яА-Я]', title) or re.search(r'[а-яА-Я]', content):
        return 'ru'
    # Chinese check
    if re.search(r'[\u4e00-\u9fff]', title) or re.search(r'[\u4e00-\u9fff]', content):
        return 'zh'
    # Spanish check
    spanish_words = ['visor', 'cómo', 'archivo', 'gratis', 'paso', 'medir', 'visualizar', 'línea', 'alternativas']
    title_lower = title.lower()
    if any(w in title_lower for w in spanish_words):
        return 'es'
    return 'en'

# Get all published posts
cmd = ['wp', '--path=' + wp_path, 'post', 'list', '--post_type=post', '--post_status=publish', '--posts_per_page=9999', '--format=json', '--fields=ID,post_title,post_name,post_content']
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
posts = json.loads(res.stdout.decode())

print(f"Loaded {len(posts)} active posts. Beginning targeted internal link injection...")

links_inserted = 0
posts_updated = 0
log_details = []

for p in posts:
    post_id = p['ID']
    post_content = p['post_content']
    post_name = p['post_name']
    post_title = p['post_title']
    
    # 1. Detect language to apply only the correct localized cluster keywords
    lang = detect_language(post_title, post_content)
    mappings = language_clusters.get(lang, {})
    
    inserted_in_post = 0
    modified = False
    
    # Split post_content by HTML tags to safely preserve attributes & text within <a> tags
    parts = re.split(r'(<[^>]+>)', post_content)
    
    inside_link = False
    inside_heading = False
    
    for i in range(len(parts)):
        part = parts[i]
        if not part:
            continue
            
        if part.startswith('<'):
            tag_lower = part.lower()
            if tag_lower.startswith('<a ') or tag_lower == '<a>':
                inside_link = True
            elif tag_lower == '</a>':
                inside_link = False
            elif re.match(r'^<h[1-6]', tag_lower):
                inside_heading = True
            elif tag_lower.startswith('</h'):
                inside_heading = False
            continue
            
        if inside_link or inside_heading:
            continue
            
        if inserted_in_post >= 2:
            break
            
        # Match against our language specific mappings
        for dest_url, keywords in mappings.items():
            # Don't link a post to itself
            if post_name in dest_url:
                continue
                
            for kw in keywords:
                if inserted_in_post >= 2:
                    break
                    
                kw_escaped = re.escape(kw)
                
                # If Chinese, use direct matching without \b boundaries
                # Else (English/Russian/Spanish), use standard word boundary \b
                if lang == 'zh':
                    pattern = re.compile(rf'(?i){kw_escaped}')
                else:
                    pattern = re.compile(rf'(?i)\\b{kw_escaped}\\b')
                
                # Check for match
                match = pattern.search(part)
                if match:
                    matched_text = match.group(0)
                    link_html = f'<a href="{dest_url}">{matched_text}</a>'
                    parts[i] = pattern.sub(link_html, part, count=1)
                    
                    inserted_in_post += 1
                    links_inserted += 1
                    modified = True
                    log_details.append(f"({lang.upper()}) Linked '{matched_text}' -> {dest_url} in Post {post_id} ('{post_title}')")
                    break # Break keyword loop for this text block once matched

    if modified:
        new_content = "".join(parts)
        temp_file = 'www/temp_post.txt'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        cmd_up = ['wp', '--path=' + wp_path, 'post', 'update', str(post_id), temp_file]
        subprocess.run(cmd_up, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        posts_updated += 1

print("\\nSUCCESS! Finished multi-lingual internal link web optimization.")
print(f"Total Posts Updated: {posts_updated}")
print(f"Total Internal Links Injected: {links_inserted}")
print("\\nLink Injection Log details:")
for log in log_details:
    print(f" - {log}")
"""

# Upload execution script to the remote server via echo redirection
run_command(f"cat << 'EOF' > www/apply_links.py\n{execution_py_code}\nEOF")

# Execute
out, err = run_command("python3 www/apply_links.py")
print("Results:")
print(out)
if err:
    print("Error:", err)

# Cleanup remote execution file
run_command("rm www/apply_links.py")
