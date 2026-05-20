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

print("=== VERIFYING UPDATE: Fetching post content for Measure Radius tutorial ===")

remote_py_code = """
import json
import subprocess
import re

wp_path = 'www/blog.dwgfastview.com/public_html'

# Query the post 'how-to-measure-radius-in-dwg-fastview-for-mobile'
cmd = ['wp', '--path=' + wp_path, 'post', 'list', '--name=how-to-measure-radius-in-dwg-fastview-for-mobile', '--format=json', '--fields=ID,post_title,post_content']
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
posts = json.loads(res.stdout.decode())

for p in posts:
    print("Post Title:", p['post_title'])
    img_tags = re.findall(r'<img[^>]+>', p['post_content'])
    for tag in img_tags:
        print("Image Tag:", tag)
"""

run_command(f"cat << 'EOF' > www/verify.py\n{remote_py_code}\nEOF")
out, err = run_command("python3 www/verify.py")
print("Verification Results:")
print(out)
run_command("rm www/verify.py")
