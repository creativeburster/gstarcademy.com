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

print("=== BACKING UP AND UPDATING PHYSICAL ROBOTS.TXT ON THE SERVER ===")

# Step 1: Backup current robots.txt
run_command(f"cp {wp_path}/robots.txt {wp_path}/robots_backup_current.txt")

# New customized robots.txt content
new_robots_txt = """# START YOAST BLOCK

# Global rules
# -----------------
User-agent: *
Disallow: /wp-json/

# Prevent crawling dynamic and legacy forum sections (SEO Clean-up)
Disallow: */community/*
Disallow: */participant/*

# Prevent crawling broken relative email URLs from legacy articles
Disallow: */support@dwgfastview.com*
Disallow: */will@blog.dwgfastview.com*

# ---------------------------
User-agent: *
Disallow: /wp-content/uploads/wpo-plugins-tables-list.json

# We're experimenting with blocking search results to prevent search result spam
Disallow: /?s=*
Disallow: /search/*

# Prevent crawling CF challenge URLs
Disallow: /cdn-cgi/bm/cv/
Disallow: /cdn-cgi/challenge-platform/

Sitemap: https://blog.dwgfastview.com/sitemap_index.xml
# ---------------------------

# Ban bots that don't benefit us.
# --------------------------------

User-agent: Nuclei
User-agent: WikiDo
User-agent: Riddler
User-agent: PetalBot
User-agent: Zoominfobot
User-agent: Go-http-client
User-agent: Node/simplecrawler
User-agent: CazoodleBot
User-agent: dotbot/1.0
User-agent: Gigabot
User-agent: Barkrowler
User-agent: BLEXBot
User-agent: magpie-crawler
Disallow: /
# END YOAST BLOCK
"""

# Step 2: Upload new robots.txt via echo redirection
# Using a clean method to avoid character issues
escaped_robots = new_robots_txt.replace("'", "'\\''")
cmd_upload = f"cat << 'EOF' > {wp_path}/robots.txt\n{new_robots_txt}\nEOF"
run_command(cmd_upload)

# Step 3: Verify upload
out, err = run_command(f"cat {wp_path}/robots.txt")
print("Verification of new robots.txt:")
print(out)
