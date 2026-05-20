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

print("Enabling SiteGround Speed Optimizer configurations...")

# 1. Enable Dynamic Caching
print("\n--- 1. Enabling Dynamic Caching ---")
out, err = run_command(f"wp --path={wp_path} sg optimize dynamic-cache enable")
print("Output:", out)
if err:
    print("Error:", err)

# 2. Enable Memcached
print("\n--- 2. Enabling Memcached ---")
out, err = run_command(f"wp --path={wp_path} sg memcached enable")
print("Output:", out)
if err:
    print("Error:", err)

# 3. Enable WebP Conversion
print("\n--- 3. Enabling WebP Conversion ---")
out, err = run_command(f"wp --path={wp_path} sg optimize webp enable")
print("Output:", out)
if err:
    print("Error:", err)

# 4. Enable Lazy Load
print("\n--- 4. Enabling Lazy Load ---")
out, err = run_command(f"wp --path={wp_path} sg optimize lazyload enable")
print("Output:", out)
if err:
    print("Error:", err)

# 5. Enable Frontend Optimizations (CSS, JS Minification & Combination)
print("\n--- 5. Enabling Frontend CSS/JS Optimizations ---")
commands = [
    f"wp --path={wp_path} sg optimize css enable",
    f"wp --path={wp_path} sg optimize js enable",
    f"wp --path={wp_path} sg optimize html enable",
    f"wp --path={wp_path} sg optimize js-async enable", # Defer render-blocking JS
]
for cmd in commands:
    print(f"Running: {cmd}")
    out, err = run_command(cmd)
    print("Output:", out)
    if err:
        print("Error:", err)

# 6. Verify NGINX dynamic cache status via curl
print("\n--- 6. Verifying NGINX Dynamic Caching Response Headers ---")
time.sleep(2)
out, err = run_command('curl -s -I https://blog.dwgfastview.com | grep -E -i "x-proxy-cache-info|cache-control"')
print("Curl Response Headers (1st Request):")
print(out)

# 2nd request to test cache Hit
time.sleep(1)
out, err = run_command('curl -s -I https://blog.dwgfastview.com | grep -E -i "x-proxy-cache-info|cache-control"')
print("Curl Response Headers (2nd Request):")
print(out)
