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

print("=== SAFE STATIC CODE ANALYSIS Part 2 ===")

print("\n--- 1. Searching for 'max-age=3' in active theme CLEAN JOURNAL PRO ---")
out, err = run_command(f"grep -rn 'max-age' {wp_path}/wp-content/themes/ 2>/dev/null")
print("Theme Matches:")
print(out if out else "(No 'max-age' found in themes)")

print("\n--- 2. Searching for 'max-age' in wp-config.php and root directory php files ---")
out, err = run_command(f"grep -rn 'max-age' {wp_path}/*.php {wp_path}/.htaccess 2>/dev/null")
print("Root Matches:")
print(out if out else "(No matches in root php or htaccess)")

print("\n--- 3. Checking SiteGround Speed Optimizer configuration from database options ---")
# Let's check what settings are stored in database for sg_cachepress
out, err = run_command(f"wp --path={wp_path} option get wp_cachepress_settings --format=json")
print("SG Cachepress Settings:")
print(out)
