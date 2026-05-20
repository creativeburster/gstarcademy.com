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

print("=== SAFE DB QUERY: Counting Missing Image Alts ===")

# Query total images
total_images, _ = run_command(f"wp --path={wp_path} db query 'SELECT COUNT(*) FROM zfa_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%\"'")
print("Total images in Media Library:", total_images.strip())

# Query images with ALT text
with_alt, _ = run_command(f"wp --path={wp_path} db query 'SELECT COUNT(DISTINCT post_id) FROM zfa_postmeta WHERE meta_key=\"_wp_attachment_image_alt\" AND meta_value != \"\"'")
print("Images WITH Alt text:", with_alt.strip())

# Calculate missing
try:
    total = int(total_images.strip()) if total_images.strip().isdigit() else 0
    have_alt = int(with_alt.strip()) if with_alt.strip().isdigit() else 0
    missing = total - have_alt
    print(f"Images MISSING Alt text: {missing} ({(missing/total)*100:.1f}%)" if total > 0 else "No images found.")
except Exception as e:
    print("Error calculating:", e)
