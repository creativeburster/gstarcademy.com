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

print("=== SAFE SEO DIAGNOSTIC AUDIT (Read-Only) ===")

# 1. Check Search Engine Visibility (blog_public option)
# 1 = Public, 0 = Discourage search engines from indexing
print("\n--- 1. Search Engine Visibility Setting ---")
out, err = run_command(f"wp --path={wp_path} option get blog_public")
print("blog_public:", out.strip())
if out.strip() == "0":
    print("WARNING: Search engines are discouraged from indexing this site!")
elif out.strip() == "1":
    print("Success: Site is visible to search engines.")

# 2. Check robots.txt content
print("\n--- 2. Checking robots.txt ---")
out, err = run_command(f"cat {wp_path}/robots.txt")
print("robots.txt contents:")
if out:
    print(out)
else:
    print("(robots.txt file is not physically present, WordPress handles it dynamically)")

# 3. Check Sitemap URL via curl and Yoast Sitemap Status
print("\n--- 3. Checking XML Sitemap ---")
out, err = run_command("curl -s -I https://blog.dwgfastview.com/sitemap_index.xml")
print("Sitemap Index HTTP Header Status:")
print(out)

# 4. Check Permalink Structure
print("\n--- 4. Checking Permalink Structure ---")
out, err = run_command(f"wp --path={wp_path} option get permalink_structure")
print("Permalink Structure:", out.strip())

# 5. Check SSL Redirection Status
print("\n--- 5. Checking SSL redirection status ---")
out, err = run_command("curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\\n' http://blog.dwgfastview.com")
print("HTTP to HTTPS Redirect:")
print(out)

# 6. Check Meta tags on a representative post
print("\n--- 6. Checking Meta Tags on Home Page ---")
out, err = run_command("curl -s https://blog.dwgfastview.com | grep -E -i '<title>|<meta name=\"description\"|<meta property=\"og:|<link rel=\"canonical\"' | head -n 15")
print("Home Meta Tags:")
print(out)

# 7. Check Theme Header.php structure (semantic tags, title)
print("\n--- 7. Checking Theme Header.php for standard SEO tags ---")
out, err = run_command(f"head -n 40 {wp_path}/wp-content/themes/clean-journal-pro/header.php")
print(out)

# 8. Check for crawler PHP errors in the php_errorlog
print("\n--- 8. Checking last 15 lines of php_errorlog ---")
out, err = run_command("tail -n 15 php_errorlog")
print(out)
