import paramiko
import re

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

print("=== SAFE DRY-RUN: Generating Alt Texts for Missing Images ===")

# Let's retrieve a list of attachments that lack ALT text
# We can do this using wp db query
sql = """
SELECT a.ID, a.post_title, a.post_parent, p.post_title as parent_title 
FROM zfa_posts a 
LEFT JOIN zfa_posts p ON a.post_parent = p.ID 
WHERE a.post_type = 'attachment' 
  AND a.post_mime_type LIKE 'image/%' 
  AND a.ID NOT IN (
    SELECT post_id FROM zfa_postmeta WHERE meta_key = '_wp_attachment_image_alt' AND meta_value != ''
  )
LIMIT 20;
"""

out, err = run_command(f'wp --path={wp_path} db query "{sql}"')
if err:
    print("Error:", err)
    exit()

# Parse the tab-separated output
lines = out.split("\n")
if len(lines) <= 1:
    print("No missing alt text images found or error parsing.")
    exit()

header = lines[0].split("\t")
rows = [line.split("\t") for line in lines[1:] if line.strip()]

print(f"\nFound {len(rows)} sample images missing Alt text. Let's see what we can generate for them:")

def clean_alt_text(img_title, parent_title):
    # If there is a parent article title, use that as the primary source
    if parent_title and parent_title != "NULL" and parent_title.strip():
        base = parent_title.strip()
    else:
        base = img_title.strip()
    
    # Clean up common patterns
    # Remove "How to" prefixes if appropriate, or keep them. Let's make it highly descriptive.
    # Replace dashes/underscores in image filenames
    base = base.replace("-", " ").replace("_", " ")
    # Remove "Pasted into" or similar junk prefixes
    base = re.sub(r'(?i)pasted\s+into\s+', '', base)
    base = re.sub(r'(?i)screen\s*shot\s*\d{4}-\d{2}-\d{2}.*', 'Screenshot', base)
    
    # Capitalize words and strip extra spaces
    base = " ".join([w.capitalize() for w in base.split()])
    return base

print("\nID\t| Original Image Title\t| Parent Article Title\t| Proposed Alt Text")
print("-" * 100)
for r in rows:
    if len(r) < 3:
        continue
    img_id = r[0]
    img_title = r[1]
    parent_id = r[2]
    parent_title = r[3] if len(r) > 3 else ""
    
    proposed_alt = clean_alt_text(img_title, parent_title)
    print(f"{img_id}\t| {img_title[:20]}\t| {parent_title[:20]}\t| => {proposed_alt}")
