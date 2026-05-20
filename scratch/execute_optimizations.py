import paramiko
import time

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

print("Starting speed optimizations...")

# 1. Truncate TranslatePress log table
print("\n--- 1. Truncating TranslatePress Translation Log Table ---")
out, err = run_command(f'wp --path={wp_path} db query "TRUNCATE TABLE zfa_trp_machine_translation_log;"')
print("Output:", out)
if err:
    print("Error:", err)

# 2. Delete all transients
print("\n--- 2. Deleting All Transients ---")
out, err = run_command(f'wp --path={wp_path} transient delete --all')
print("Output:", out)
if err:
    print("Error:", err)

# 3. Deactivate wp-super-cache
print("\n--- 3. Deactivating wp-super-cache ---")
out, err = run_command(f'wp --path={wp_path} plugin deactivate wp-super-cache')
print("Output:", out)
if err:
    print("Error:", err)

# 4. Uninstall wp-super-cache
print("\n--- 4. Uninstalling wp-super-cache ---")
out, err = run_command(f'wp --path={wp_path} plugin uninstall wp-super-cache')
print("Output:", out)
if err:
    print("Error:", err)

# 5. Install and activate sg-cachepress (Speed Optimizer)
print("\n--- 5. Installing and Activating Speed Optimizer (sg-cachepress) ---")
out, err = run_command(f'wp --path={wp_path} plugin install sg-cachepress --activate')
print("Output:", out)
if err:
    print("Error:", err)

# 6. Verify changes
print("\n--- 6. Verifying Caching Curls ---")
time.sleep(3) # Wait a bit for cache plugin initialization
# Check if curl to home page now shows NGINX cache header
out, err = run_command('curl -s -I https://blog.dwgfastview.com | grep -E -i "x-proxy-cache-info|cache-control"')
print("Curl Headers:")
print(out)

# Check active plugins again
out, err = run_command(f'wp --path={wp_path} plugin list --status=active')
print("\nActive Plugins:")
print(out)
