import glob

patterns = ["kb/**/*.html"]
count = 0

for pattern in patterns:
    for fn in glob.glob(pattern, recursive=True):
        with open(fn, "r", encoding="utf-8") as f:
            c = f.read()
        orig = c
        c = c.replace('<p>© Gstarcademy.</p>', '<p>© <span id="year">2026</span> Suzhou Gstarsoft Co., Ltd. (SSE: 688657). All rights reserved.</p>')
        c = c.replace('<p>© <span id="footer-year"></span> Gstarcademy.</p>', '<p>© <span id="year">2026</span> Suzhou Gstarsoft Co., Ltd. (SSE: 688657). All rights reserved.</p>')
        c = c.replace('© Gstarcademy.', '© Suzhou Gstarsoft Co., Ltd. (SSE: 688657).')
        if c != orig:
            with open(fn, "w", encoding="utf-8") as f:
                f.write(c)
            count += 1

print(f"Updated {count} remaining kb files.")
