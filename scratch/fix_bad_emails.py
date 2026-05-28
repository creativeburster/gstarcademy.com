import paramiko
import os
import json
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

print("=== FIXING MALFORMED EMAIL LINKS IN WORDPRESS POSTS ===")

# IDs we found earlier that have bad links
target_ids = [2343, 9959]

for post_id in target_ids:
    print(f"\nProcessing Post ID: {post_id}...")
    
    # 1. Fetch current post_content
    cmd_fetch = f"wp post get {post_id} --field=post_content --path={wp_path}"
    content, err = run_ssh_command(cmd_fetch)
    
    if err and "Error" in err:
        print(f"Error fetching post {post_id}: {err}")
        continue
        
    if not content.strip():
        print(f"Warning: Empty content for post {post_id}.")
        continue
        
    # 2. Use regex to replace href="email@domain.com" with href="mailto:email@domain.com"
    # Matches href="anything" where the email doesn't start with mailto:
    pattern = r'href="(?!(mailto:))([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"'
    
    matches = re.findall(pattern, content)
    if not matches:
        print(f"No malformed email links found in Post {post_id}.")
        continue
        
    print(f"Found malformed links: {matches}")
    
    # Replace the matches
    new_content = re.sub(pattern, r'href="mailto:\2"', content)
    
    # 3. Write new content to a temporary file on the remote server to safely update
    # This avoids bash argument escaping issues with huge HTML strings.
    temp_remote_file = f"/home/customer/temp_post_{post_id}.txt"
    
    # We will upload the content using sftp or a simple python wrapper, 
    # but a simple EOF block is also very safe if we escape single quotes properly.
    # To be extremely safe, we will write it via SFTP since we have SSH credentials!
    try:
        passphrase = get_passphrase()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
        ssh.connect(hostname, port=port, username=username, pkey=key)
        
        sftp = ssh.open_sftp()
        with sftp.file(temp_remote_file, 'w') as f:
            f.write(new_content)
        sftp.close()
        ssh.close()
        
        print(f"Uploaded cleaned content to remote temporary file: {temp_remote_file}")
        
        # 4. Perform WordPress post update from the remote file
        cmd_update = f"wp post update {post_id} {temp_remote_file} --path={wp_path}"
        out, err = run_ssh_command(cmd_update)
        
        if err and "Error" in err:
            print(f"Error updating post via wp post update: {err}")
        else:
            print(f"Successfully updated Post {post_id}!")
            print(out.strip())
            
        # 5. Clean up temporary remote file
        run_ssh_command(f"rm {temp_remote_file}")
        
    except Exception as e:
        print(f"SFTP or SSH error during update: {e}")

print("\n=== EMAIL LINK CLEANUP COMPLETED ===")
