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

print("=== TESTING BROAD KEYWORDS FOR HIGHER SEO LINK DENSITY ===")

remote_py_code = """
import json
import subprocess
import re

wp_path = 'www/blog.dwgfastview.com/public_html'

broad_keywords = [
    'Revit', 'RVT', 'SolidWorks', 'SLDPRT', 'SLDASM',
    'STP', 'STEP', 'TrueView', '3DM'
]

# Get all published posts
cmd = ['wp', '--path=' + wp_path, 'post', 'list', '--post_type=post', '--post_status=publish', '--posts_per_page=9999', '--format=json', '--fields=ID,post_title,post_content']
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
posts = json.loads(res.stdout.decode())

print(f"Loaded {len(posts)} posts. Testing broad matches...")

for kw in broad_keywords:
    kw_escaped = re.escape(kw)
    pattern_with_b = re.compile(rf'(?i)\\b{kw_escaped}\\b')
    pattern_direct = re.compile(rf'(?i){kw_escaped}')
    
    matches_b = 0
    matches_dir = 0
    
    for p in posts:
        content = p['post_content']
        plain_text = re.sub(r'<[^>]+>', ' ', content)
        
        if pattern_with_b.search(plain_text):
            matches_b += 1
        if pattern_direct.search(plain_text):
            matches_dir += 1
            
    print(f"Keyword: '{kw}' | Matches with \\\\b: {matches_b} | Matches direct: {matches_dir}")
"""

run_command(f"cat << 'EOF' > www/test_broad.py\n{remote_py_code}\nEOF")
out, err = run_command("python3 www/test_broad.py")
print("Diagnostic Results:")
print(out)
run_command("rm www/test_broad.py")
