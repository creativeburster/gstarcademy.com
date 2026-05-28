import paramiko
import os
import re

hostname = "c1100271.sgvps.net"
username = "u2-74dmvatthvme"
port = 18765
key_path = r"C:\Users\willp\Desktop\26年5月\siteground_key"
passphrase_file = r"C:\Users\willp\Desktop\26年5月\key_passphrase.txt"
wp_path = "www/blog.dwgfastview.com/public_html"

def get_passphrase():
    if os.path.exists(passphrase_file):
        with open(passphrase_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def run_ssh_command(cmd):
    passphrase = get_passphrase()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
    ssh.connect(hostname, port=port, username=username, pkey=key)
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    ssh.close()
    return out, err

print("=== INTERNAL SSH VERIFICATION OF SEO FIXES ===")

# 1. Verify robots.txt physical content
print("\n--- 1. Verification of robots.txt physical file ---")
out, err = run_ssh_command(f"cat {wp_path}/robots.txt")
if "Disallow: */community/*" in out and "Disallow: */support@dwgfastview.com*" in out:
    print("  [PASS] robots.txt contains our custom disallow rules!")
else:
    print("  [FAIL] robots.txt does not contain our custom disallow rules.")
    print("Content read from server:")
    print(out[:200])

# 2. Verify Post 2343 (FAQ) content
print("\n--- 2. Verification of Post 2343 (FAQ) ---")
out, err = run_ssh_command(f"wp post get 2343 --field=post_content --path={wp_path}")
if 'href="mailto:will@blog.dwgfastview.com"' in out:
    print("  [PASS] Found corrected mailto: href=\"mailto:will@blog.dwgfastview.com\"")
else:
    print("  [FAIL] Corrected link NOT found in database post_content.")
if 'href="will@blog.dwgfastview.com"' in out:
    print("  [FAIL] Legacy bad relative link is STILL present.")
else:
    print("  [PASS] Legacy bad relative link is completely gone!")

# 3. Verify Post 9959 (Holiday Notice) content
print("\n--- 3. Verification of Post 9959 (Holiday Notice) ---")
out, err = run_ssh_command(f"wp post get 9959 --field=post_content --path={wp_path}")
if 'href="mailto:support@dwgfastview.com"' in out:
    print("  [PASS] Found corrected mailto: href=\"mailto:support@dwgfastview.com\"")
else:
    print("  [FAIL] Corrected link NOT found in database post_content.")
if 'href="support@dwgfastview.com"' in out:
    print("  [FAIL] Legacy bad relative link is STILL present.")
else:
    print("  [PASS] Legacy bad relative link is completely gone!")

print("\n=== INTERNAL VERIFICATION COMPLETE ===")
