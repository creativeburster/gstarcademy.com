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

print("=== SAFE DB QUERY: Finding 5 specific missing ALT images and posts ===")

sql = """
SELECT a.ID, a.guid, p.post_name, p.post_title 
FROM zfa_posts a 
INNER JOIN zfa_posts p ON a.post_parent = p.ID 
WHERE a.post_type = 'attachment' 
  AND a.post_mime_type LIKE 'image/%' 
  AND a.ID NOT IN (
    SELECT post_id FROM zfa_postmeta WHERE meta_key = '_wp_attachment_image_alt' AND meta_value != ''
  )
LIMIT 5;
"""

out, err = run_command(f'wp --path={wp_path} db query "{sql}"')
if err:
    print("Error:", err)
    exit()

print(out)
