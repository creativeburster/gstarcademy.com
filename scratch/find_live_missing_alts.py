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

print("=== SAFE DB QUERY: Finding 5 specific missing ALT images and posts ===")

# Let's write the helper python script to a file on the remote server
remote_py_code = """
import json
import subprocess
import re

wp_path = 'www/blog.dwgfastview.com/public_html'

# Get 50 recent published posts
cmd = ['wp', '--path=' + wp_path, 'post', 'list', '--post_type=post', '--post_status=publish', '--posts_per_page=100', '--format=json', '--fields=ID,post_title,post_name,post_content']
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
posts = json.loads(res.stdout.decode())

found_count = 0
for p in posts:
    content = p['post_content']
    # Find all <img ...> tags
    img_tags = re.findall(r'<img[^>]+>', content)
    for tag in img_tags:
        # Check if alt is missing or empty
        has_empty_alt = False
        if 'alt=' not in tag:
            has_empty_alt = True
        else:
            # Check for empty alt: alt="" or alt='' or alt= ""
            if re.search(r'alt=\\s*["\\']["\\']', tag) or re.search(r'alt=\\s*$', tag):
                has_empty_alt = True
        
        if has_empty_alt:
            src_match = re.search(r'src=\\s*["\\']([^"\\']+)["\\']', tag)
            src = src_match.group(1) if src_match else 'Unknown Src'
            
            print(json.dumps({
                'post_id': p['ID'],
                'post_title': p['post_title'],
                'post_url': 'https://blog.dwgfastview.com/' + p['post_name'],
                'image_tag': tag,
                'image_src': src
            }))
            found_count += 1
            if found_count >= 5:
                break
    if found_count >= 5:
        break
"""

# SFTP upload or echo command to create the file
# Let's use echo to write the remote file, escaping backslashes
remote_py_code_escaped = remote_py_code.replace("'", "'\\''")
run_command(f"cat << 'EOF' > www/find_missing.py\n{remote_py_code}\nEOF")

# Execute the remote python file
out, err = run_command("python3 www/find_missing.py")
print("Results:")
print(out)
if err:
    print("Error:", err)

# Cleanup remote helper file
run_command("rm www/find_missing.py")
