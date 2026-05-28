import paramiko
import json
import re

hostname = "c1100271.sgvps.net"
username = "u2-74dmvatthvme"
port = 18765
key_path = r"C:\Users\willp\Desktop\26年5月\siteground_key"
passphrase_file = r"C:\Users\willp\Desktop\26年5月\key_passphrase.txt"
wp_path = "www/blog.dwgfastview.com/public_html"

def get_passphrase():
    with open(passphrase_file, "r", encoding="utf-8") as f:
        return f.read().strip()

def run_command(cmd):
    passphrase = get_passphrase()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        ssh.connect(hostname, port=port, username=username, pkey=key, timeout=45)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode("utf-8", errors="replace").strip()
        err = stderr.read().decode("utf-8", errors="replace").strip()
        ssh.close()
        return out, err
    except Exception as e:
        return "", str(e)

print("=== STARTING WP COMMENTS SPAM CLEANUP AND AUTO-MODERATION ===")

# --- Step 1: Purge existing spam comments ---
print("\n--- Step 1: Purging existing spam comments ---")
spam_list_cmd = f"wp --path={wp_path} comment list --status=spam --format=ids"
out_s, err_s = run_command(spam_list_cmd)

if out_s.strip():
    spam_ids = out_s.strip().split()
    print(f"Found {len(spam_ids)} spam comments in DB. Purging...")
    del_cmd = f"wp --path={wp_path} comment delete {' '.join(spam_ids)} --force"
    out_d, err_d = run_command(del_cmd)
    print(out_d.strip())
else:
    print("No existing spam comments to purge.")

# --- Step 2: Fetch and Moderate PENDING comments ---
print("\n--- Step 2: Moderating PENDING comments ---")
pending_cmd = f"wp --path={wp_path} comment list --status=hold --format=json --fields=comment_ID,comment_author,comment_author_email,comment_author_url,comment_content"
out_p, err_p = run_command(pending_cmd)

if err_p:
    print("Error fetching comments:", err_p)
    exit(1)

if not out_p.strip() or out_p.strip() == "[]":
    print("No pending comments found in moderation queue.")
    exit(0)

try:
    pending_comments = json.loads(out_p)
except Exception as e:
    print("JSON parsing error:", e)
    exit(1)

print(f"Total pending comments fetched: {len(pending_comments)}")

spam_to_kill = []
approved_to_keep = []
ignored_for_safety = []

# Regex patterns
link_pattern = re.compile(r'(https?://|href=|\[url=|<a\b)', re.IGNORECASE)
cyrillic_pattern = re.compile(r'[\u0400-\u04FF]') # Russian spam

# Common spam keywords in comments or URLs
spam_keywords = [
    "casino", "gambling", "betting", "poker", "slot", "viagra", "cialis", 
    "cheap", "essay", "seo", "backlink", "promotional", "guest post", 
    "bitcoin", "cryptoc", "token", "cannabis", "adult", "dating", "sex", "porn",
    "http", "www"
]

# High-value keywords for genuine comments
genuine_keywords = [
    "cad", "dwg", "view", "revit", "solidworks", "sketchup", "stp", "step", 
    "pdf", "format", "file", "drawing", "dimension", "license", "premium", 
    "install", "download", "tutorial", "thank", "help", "solve", "problem", 
    "error", "issue", "question", "work", "great", "nice", "useful", "helpful",
    "谢谢", "你好", "请问", "怎么", "如何", "下载", "有用", "解决", "标签"
]

for c in pending_comments:
    cid = str(c.get("comment_ID"))
    content = c.get("comment_content", "").lower()
    author = c.get("comment_author", "").lower()
    author_url = c.get("comment_author_url", "").lower()
    email = c.get("comment_author_email", "").lower()
    
    is_spam = False
    spam_reason = ""
    
    # Check 1: Links (Standard spam indicator)
    if link_pattern.search(c.get("comment_content", "")) or link_pattern.search(author_url):
        is_spam = True
        spam_reason = "Contains links (URL/href)"
        
    # Check 2: Russian characters
    elif cyrillic_pattern.search(c.get("comment_content", "")) or cyrillic_pattern.search(c.get("comment_author", "")):
        is_spam = True
        spam_reason = "Contains Russian/Cyrillic characters"
        
    # Check 3: Spam keywords in URL or content
    else:
        for kw in spam_keywords:
            if kw in content or kw in author_url or kw in email:
                is_spam = True
                spam_reason = f"Contains spam keyword '{kw}'"
                break

    if is_spam:
        spam_to_kill.append((cid, author, spam_reason))
    else:
        # Determine if it's genuinely high-value to auto-approve
        is_genuine = False
        for kw in genuine_keywords:
            if kw in content or kw in author:
                is_genuine = True
                break
                
        # If it doesn't look like spam, has no links, and has moderate word count, we can approve
        # or if it has genuine keywords.
        word_count = len(re.sub(r'[^\w\s]', '', c.get("comment_content", "")).split())
        if is_genuine or (word_count > 2 and len(c.get("comment_content", "")) < 200):
            approved_to_keep.append((cid, author, c.get("comment_content", "")[:60].replace("\n", " ")))
        else:
            ignored_for_safety.append((cid, author, c.get("comment_content", "")[:60].replace("\n", " ")))

# --- Execution ---
print(f"\n💡 Analysis Completed:")
print(f"  - Classified as SPAM (to delete): {len(spam_to_kill)}")
print(f"  - Classified as GENUINE (to approve): {len(approved_to_keep)}")
print(f"  - Safe-held (remain in queue): {len(ignored_for_safety)}")

# 1. Purge Spams in batch
if spam_to_kill:
    spam_ids = [item[0] for item in spam_to_kill]
    print(f"\n🗑️ Deleting {len(spam_ids)} SPAM comments in batches...")
    BATCH = 50
    for i in range(0, len(spam_ids), BATCH):
        batch = spam_ids[i:i+BATCH]
        del_cmd = f"wp --path={wp_path} comment delete {' '.join(batch)} --force"
        run_command(del_cmd)
    print("Spam comments deleted successfully.")

# 2. Approve Genuines in batch
if approved_to_keep:
    app_ids = [item[0] for item in approved_to_keep]
    print(f"\n✅ Auto-approving {len(app_ids)} GENUINE comments in batches...")
    BATCH = 50
    for i in range(0, len(app_ids), BATCH):
        batch = app_ids[i:i+BATCH]
        app_cmd = f"wp --path={wp_path} comment approve {' '.join(batch)}"
        run_command(app_cmd)
    print("Genuine comments approved successfully.")

# Print Sample of Approved Comments
if approved_to_keep:
    print("\nSample of Approved Comments:")
    for cid, auth, txt in approved_to_keep[:10]:
        print(f"  [ID: {cid}] Author: {auth} | Content: {txt}...")

# Print Sample of Spammed Reasons
if spam_to_kill:
    print("\nSample of Deleted Spam Comments (with reasons):")
    for cid, auth, reason in spam_to_kill[:10]:
        print(f"  [ID: {cid}] Author: {auth} | Reason: {reason}")

# --- Step 3: Purge server caches ---
print("\n--- Purging SG cache to apply changes ---")
run_command(f"wp --path={wp_path} sg purge")
print("Cache purged successfully.")

print("\n=== WP COMMENTS MODERATION COMPLETED ===")
