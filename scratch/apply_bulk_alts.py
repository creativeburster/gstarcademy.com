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

print("=== EXECUTING SECURE BATCH WP-CLI FILE-BASED POST UPDATE ===")

# The real execution python script that will run on the server
execution_py_code = """
import json
import subprocess
import re
import os

wp_path = 'www/blog.dwgfastview.com/public_html'

# Get all published posts
cmd = ['wp', '--path=' + wp_path, 'post', 'list', '--post_type=post', '--post_status=publish', '--posts_per_page=9999', '--format=json', '--fields=ID,post_title,post_content']
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
posts = json.loads(res.stdout.decode())

print(f"Loaded {len(posts)} active posts. Beginning selective alt-text update...")

meta_updates = 0
content_updates = 0
posts_updated = 0

for p in posts:
    # 1. SPECIFIC EXCLUSION: Skip the Acrobat post as requested by user
    if "8 Best Alternatives of Adobe Acrobat in 2026" in p['post_title'] or p['ID'] == 13360:
        continue
        
    content = p['post_content']
    img_tags = re.findall(r'<img[^>]+>', content)
    modified = False
    
    for tag in img_tags:
        # Check if alt is missing or empty
        has_empty_alt = False
        if 'alt=' not in tag:
            has_empty_alt = True
        else:
            if re.search(r'alt=\\s*["\\']["\\']', tag) or re.search(r'alt=\\s*$', tag):
                has_empty_alt = True
        
        if has_empty_alt:
            src_match = re.search(r'src=\\s*["\\']([^"\\']+)["\\']', tag)
            src = src_match.group(1) if src_match else ''
            
            # Extract filename from src
            filename = ''
            if src:
                filename = src.split('/')[-1].split('.')[0]
                filename = filename.replace('-', ' ').replace('_', ' ')
                filename = re.sub(r'(?i)pasted\\s+image|微信截图|screenshot', '', filename).strip()
            
            # 2. SPECIFIC EXCLUSION: Skip Camp 2 (Theme Assets / Logos / Buttons)
            filename_lower = filename.lower()
            if any(x in filename_lower for x in ['logo', 'cropped', 'icon', 'button', 'banner', 'pasted-15', 'buy']):
                continue
                
            # Build Alt text
            title = p['post_title'].strip()
            title = re.sub(r'\\?$', '', title) # Remove trailing question mark
            
            if filename and len(filename) > 3:
                proposed_alt = f"{filename.capitalize()} - {title}"
            else:
                proposed_alt = title
            
            # Clean proposed Alt text
            proposed_alt = " ".join([w.capitalize() for w in proposed_alt.split() if w])
            proposed_alt = proposed_alt.replace('"', '&quot;').replace("'", "&#39;")
            
            # Replace tag in content
            new_tag = tag
            if 'alt=' in tag:
                new_tag = re.sub(r'alt=\\s*["\\']["\\']', f'alt="{proposed_alt}"', new_tag)
            else:
                new_tag = new_tag.replace('/>', f'alt="{proposed_alt}" />').replace('>', f'alt="{proposed_alt}" >')
            
            content = content.replace(tag, new_tag)
            modified = True
            content_updates += 1
            
            # Also find the attachment ID from DB and update its zfa_postmeta so Media Library is correct
            if src:
                clean_src = src.split('/')[-1]
                sql_find = f"SELECT ID FROM zfa_posts WHERE post_type='attachment' AND guid LIKE '%{clean_src}%' LIMIT 1;"
                # Since sql_find is a simple query without HTML, we can pass it via db query stdin
                cmd_db = ['wp', '--path=' + wp_path, 'db', 'query']
                res_db = subprocess.run(cmd_db, input=sql_find.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                att_id = res_db.stdout.decode().strip()
                if att_id and att_id.isdigit():
                    sql_check = f"SELECT meta_id FROM zfa_postmeta WHERE post_id={att_id} AND meta_key='_wp_attachment_image_alt' LIMIT 1;"
                    res_ch = subprocess.run(cmd_db, input=sql_check.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    meta_id = res_ch.stdout.decode().strip()
                    if meta_id and meta_id.isdigit():
                        sql_up = f"UPDATE zfa_postmeta SET meta_value='{proposed_alt}' WHERE meta_id={meta_id};"
                    else:
                        sql_up = f"INSERT INTO zfa_postmeta (post_id, meta_key, meta_value) VALUES ({att_id}, '_wp_attachment_image_alt', '{proposed_alt}');"
                    subprocess.run(cmd_db, input=sql_up.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    meta_updates += 1

    if modified:
        # Write to temporary file on the remote server
        temp_file = 'www/temp_post.txt'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Execute post update via file (handles escaping automatically)
        cmd_up = ['wp', '--path=' + wp_path, 'post', 'update', str(p['ID']), temp_file]
        res_up = subprocess.run(cmd_up, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        posts_updated += 1

print(f"SUCCESS! Finished batch SEO updates.")
print(f"Total Posts Updated: {posts_updated}")
print(f"Total Page HTML (post_content) Alt updates: {content_updates}")
print(f"Total Media Library (postmeta) Alt updates: {meta_updates}")
"""

# Upload the file to the remote server via echo redirection
run_command(f"cat << 'EOF' > www/apply_alts.py\n{execution_py_code}\nEOF")

# Execute
out, err = run_command("python3 www/apply_alts.py")
print("Results:")
print(out)
if err:
    print("Error:", err)

# Cleanup remote execution file
run_command("rm www/apply_alts.py")
