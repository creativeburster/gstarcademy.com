import requests

url = "https://blog.dwgfastview.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

print("=== Fetching 3 times locally ===")
for i in range(1, 4):
    print(f"\n--- Request #{i} ---")
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        for k, v in r.headers.items():
            if k.lower() in ["x-proxy-cache-info", "cache-control", "x-cache-enabled", "vary"]:
                print(f"{k}: {v}")
    except Exception as e:
        print("Error:", e)
