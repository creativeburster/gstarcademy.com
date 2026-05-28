import paramiko
import os

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

print("Searching for articles with relative email links...")
# We will escape double quotes properly for the bash environment
sql = 'SELECT ID, post_title, post_name FROM zfa_posts WHERE post_status=\\"publish\\" AND (post_content LIKE \\"%href=\\\\\\"will@%\\" OR post_content LIKE \\"%href=\\\\\\"support@%\\" OR post_content LIKE \\"%href=\\\\\\"info@%\\")'
cmd = f'wp db query "{sql}" --path={wp_path}'

out, err = run_ssh_command(cmd)

if err:
    print(f"Error: {err}")
if out:
    print("Found matching posts in DB:")
    print(out)
else:
    print("No matching posts found in database using direct LIKE query.")
