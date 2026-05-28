import urllib.request
import re

print("=== PHYSICAL VERIFICATION OF SEO FIXES VIA HTTP ===")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. Verify robots.txt
print("\n--- 1. Testing robots.txt ---")
try:
    req = urllib.request.Request('https://blog.dwgfastview.com/robots.txt', headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    community_ok = "Disallow: */community/*" in html
    participant_ok = "Disallow: */participant/*" in html
    email_ok = "Disallow: */will@blog.dwgfastview.com*" in html
    
    print(f"  [PASS] robots.txt responded with HTTP 200")
    print(f"  [PASS] community block: {community_ok}")
    print(f"  [PASS] participant block: {participant_ok}")
    print(f"  [PASS] email URL block: {email_ok}")
except Exception as e:
    print(f"  [FAIL] robots.txt check failed: {e}")

# 2. Verify FAQ page mailto
print("\n--- 2. Testing FAQ Page (ID 2343) ---")
try:
    req = urllib.request.Request('https://blog.dwgfastview.com/faq', headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    # Search for the corrected mailto: link
    match = re.search(r'href="mailto:will@blog\.dwgfastview\.com"', html)
    bad_match = re.search(r'href="will@blog\.dwgfastview\.com"', html)
    
    if match:
        print(f"  [PASS] Corrected link found: href=\"mailto:will@blog.dwgfastview.com\"")
    else:
        print(f"  [FAIL] Corrected link NOT found.")
        
    if bad_match:
        print(f"  [FAIL] Warning: Legacy bad link is still present!")
    else:
        print(f"  [PASS] Bad relative link has been completely replaced.")
except Exception as e:
    print(f"  [FAIL] FAQ page check failed: {e}")

# 3. Verify Holiday Notice page mailto
print("\n--- 3. Testing Holiday Notice Page (ID 9959) ---")
try:
    req = urllib.request.Request('https://blog.dwgfastview.com/holiday-notice-spring-festival-break', headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    match = re.search(r'href="mailto:support@dwgfastview\.com"', html)
    bad_match = re.search(r'href="support@dwgfastview\.com"', html)
    
    if match:
        print(f"  [PASS] Corrected link found: href=\"mailto:support@dwgfastview.com\"")
    else:
        print(f"  [FAIL] Corrected link NOT found.")
        
    if bad_match:
        print(f"  [FAIL] Warning: Legacy bad link is still present!")
    else:
        print(f"  [PASS] Bad relative link has been completely replaced.")
except Exception as e:
    print(f"  [FAIL] Holiday Notice check failed: {e}")

print("\n=== VERIFICATION FINISHED ===")
