import paramiko
import time

hostname = "c1100271.sgvps.net"
username = "u2-74dmvatthvme"
port = 18765
key_path = r"C:\Users\willp\Desktop\26年5月\siteground_key"
passphrase_file = r"C:\Users\willp\Desktop\26年5月\key_passphrase.txt"
wp_path = "www/blog.dwgfastview.com/public_html"
backup_path = "www/db_backup_current.sql"

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

print("=== Creating Database Backup ===")
# Run WP-CLI db export
out, err = run_command(f"wp --path={wp_path} db export {backup_path}")
print("Export Output:", out)
if err:
    print("Export Error:", err)

# Verify backup file size
out, err = run_command(f"ls -lh {backup_path}")
print("Backup File Status:", out)

print("\n=== Creating .htaccess Backup ===")
out, err = run_command(f"cp {wp_path}/.htaccess www/htaccess_backup.txt")
out, err = run_command(f"ls -lh www/htaccess_backup.txt")
print("Htaccess Backup Status:", out)
