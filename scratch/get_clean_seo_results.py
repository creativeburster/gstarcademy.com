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

results = []

def audit_log(section, content):
    results.append(f"=== {section} ===")
    results.append(content)
    results.append("\n" + "="*40 + "\n")

# 1. Search Engine Visibility
out, err = run_command(f"wp --path={wp_path} option get blog_public")
audit_log("1. Search Engine Visibility (blog_public)", f"Value: {out}\n(1 = Public, 0 = Discouraged)")

# 2. robots.txt
out, err = run_command(f"cat {wp_path}/robots.txt")
audit_log("2. robots.txt File Content", out if out else "(No physical robots.txt, handled dynamically by WordPress)")

# 3. sitemap_index.xml headers
out, err = run_command("curl -s -I https://blog.dwgfastview.com/sitemap_index.xml")
audit_log("3. Sitemap Index Headers", out)

# 4. Permalink Structure
out, err = run_command(f"wp --path={wp_path} option get permalink_structure")
audit_log("4. Permalink Structure", out)

# 5. SSL Redirection
out, err = run_command("curl -s -IL http://blog.dwgfastview.com | grep -E 'HTTP/|Location:'")
audit_log("5. HTTP to HTTPS Redirection Headers", out)

# 6. Meta Tags on Homepage
out, err = run_command("curl -s https://blog.dwgfastview.com | grep -E -i '<title>|<meta name=\"description\"|<meta name=\"robots\"|<meta property=\"og:|<link rel=\"canonical\"' | head -n 30")
audit_log("6. Homepage Meta Tags", out)

# 7. Check if sitemap contains post types
out, err = run_command(f"wp --path={wp_path} option get wpseo_titles --format=json")
audit_log("7. Yoast SEO Titles Settings (JSON)", out)

# Write to local file for model to read
with open(r"f:\CAD-tutorial\scratch\seo_audit_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))
print("SEO Audit results compiled successfully in local file!")
