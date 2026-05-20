import paramiko

hostname = "c1100271.sgvps.net"
username = "u2-74dmvatthvme"
port = 18765
key_path = r"C:\Users\willp\Desktop\26年5月\siteground_key"
passphrase_file = r"C:\Users\willp\Desktop\26年5月\key_passphrase.txt"

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

print("=== SEARCHING ALL OCCURRENCES OF IMAGE SUBSTRING ===")
script = """python3 -c "
import urllib.request
url = 'https://blog.dwgfastview.com/how-to-change-the-size-of-the-dimensioning-arrow'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    start_search = 0
    count = 0
    while True:
        idx = html.find('dimension_arrow_too_big', start_search)
        if idx == -1:
            break
        count += 1
        print(f'Occur #{count} at index {idx}:')
        print(html[max(0, idx - 100):min(len(html), idx + 200)])
        print('-'*50)
        start_search = idx + 1
    if count == 0:
        print('Not found at all!')
except Exception as e:
    print('Error:', e)
" """

out, err = run_command(script)
print(out)
if err:
    print("Error:", err)
