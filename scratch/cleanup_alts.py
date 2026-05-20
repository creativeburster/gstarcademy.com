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

print("=== RUNNING INTELLIGENT ALT TEXT CLEANUP SCRIPT (STRIPPING TIMESTAMPS & HASHES) ===")

# The cleanup script that runs on the remote server
execution_py_code = """
import json
import subprocess
import re
import os

wp_path = 'www/blog.dwgfastview.com/public_html'

def clean_alt(alt_text, post_title):
    words = alt_text.split()
    clean_words = []
    for w in words:
        # 1. Skip Unix timestamps (10 digits starting with 1)
        if re.match(r'^\\d{10}$', w) or re.match(r'^1\\d{9}$', w):
            continue
        # 2. Skip long hash/key-like strings (more than 12 chars with letters and digits mixed)
        if len(w) > 12 and any(c.isdigit() for c in w) and any(c.isalpha() for c in w):
            continue
        # 3. Skip generic suffixes
        if w.lower() in ['scaled', 'image', 'png', 'jpg', 'jpeg', 'gif', 'screenshot', 'pasted']:
            continue
        # 4. Skip single separators
        if w in ['-', '–', '|']:
            continue
        clean_words.append(w)
        
    cleaned_filename = " ".join(clean_words)
    post_title_clean = " ".join([word.capitalize() for word in post_title.split() if word])
    
    if not cleaned_filename or len(cleaned_filename) < 3:
        proposed_alt = post_title_clean
    else:
        # Avoid duplication if the title is already in the cleaned filename
        if post_title_clean.lower() in cleaned_filename.lower():
            proposed_alt = cleaned_filename
        else:
            proposed_alt = f"{cleaned_filename} - {post_title_clean}"
            
    proposed_alt = " ".join([word.capitalize() for word in proposed_alt.split() if word])
    proposed_alt = proposed_alt.replace('"', '&quot;').replace("'", "&#39;")
    return proposed_alt

# Get all published posts
cmd = ['wp', '--path=' + wp_path, 'post', 'list', '--post_type=post', '--post_status=publish', '--posts_per_page=9999', '--format=json', '--fields=ID,post_title,post_content']
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
posts = json.loads(res.stdout.decode())

print(f"Loaded {len(posts)} active posts. Beginning selective cleanup...")

posts_cleaned = 0
images_cleaned = 0

for p in posts:
    content = p['post_content']
    img_tags = re.findall(r'<img[^>]+>', content)
    modified = False
    
    for tag in img_tags:
        # Check if the tag has a non-empty alt
        alt_match = re.search(r'alt=\\s*["\\']([^"\\']+)["\\']', tag)
        if alt_match:
            original_alt = alt_match.group(1)
            # Check if it contains a timestamp (10 digits starting with 1) or MD5 hash-like string (letters & digits mixed, len > 12)
            has_timestamp = re.search(r'\\b1\\d{9}\\b', original_alt)
            has_hash = False
            for w in original_alt.split():
                if len(w) > 12 and any(c.isdigit() for c in w) and any(c.isalpha() for c in w):
                    has_hash = True
                    break
                    
            if has_timestamp or has_hash or 'scaled' in original_alt.lower() or 'image' in original_alt.lower():
                cleaned_alt = clean_alt(original_alt, p['post_title'])
                
                # Replace inside the tag
                new_tag = tag.replace(f'alt="{original_alt}"', f'alt="{cleaned_alt}"')
                new_tag = new_tag.replace(f"alt='{original_alt}'", f'alt="{cleaned_alt}"')
                
                content = content.replace(tag, new_tag)
                modified = True
                images_cleaned += 1
                
                # Also find the attachment ID from DB and update its zfa_postmeta
                src_match = re.search(r'src=\\s*["\\']([^"\\']+)["\\']', tag)
                if src_match:
                    clean_src = src_match.group(1).split('/')[-1]
                    sql_find = f"SELECT ID FROM zfa_posts WHERE post_type='attachment' AND guid LIKE '%{clean_src}%' LIMIT 1;"
                    cmd_db = ['wp', '--path=' + wp_path, 'db', 'query']
                    res_db = subprocess.run(cmd_db, input=sql_find.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    att_id = res_db.stdout.decode().strip()
                    if att_id and att_id.isdigit():
                        sql_up = f"UPDATE zfa_postmeta SET meta_value='{cleaned_alt}' WHERE post_id={att_id} AND meta_key='_wp_attachment_image_alt';"
                        subprocess.run(cmd_db, input=sql_up.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if modified:
        temp_file = 'www/temp_post.txt'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        cmd_up = ['wp', '--path=' + wp_path, 'post', 'update', str(p['ID']), temp_file]
        subprocess.run(cmd_up, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        posts_cleaned += 1

print(f"SUCCESS! Finished selective Alt text cleaning.")
print(f"Total Posts Cleaned: {posts_cleaned}")
print(f"Total Page HTML Images Cleaned: {images_cleaned}")
"""

# Upload the file to the remote server via echo redirection
run_command(f"cat << 'EOF' > www/cleanup_alts.py\n{execution_py_code}\nEOF")

# Execute
out, err = run_command("python3 www/cleanup_alts.py")
print("Results:")
print(out)
if err:
    print("Error:", err)

# Cleanup remote execution file
run_command("rm www/cleanup_alts.py")
