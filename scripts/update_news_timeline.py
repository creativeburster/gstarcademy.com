with open("data/news.json", "r", encoding="utf-8") as f:
    c = f.read()

# 1. IFC 4.3 standard year
c = c.replace("ISO 16739-1:2026", "ISO 16739-1:2024")

# 2. GstarCAD 2027 update
c = c.replace(
    '"title": "Gstarsoft releases GstarCAD 2026 Beta with enhanced multi-core CPU optimization",',
    '"title": "Gstarsoft releases GstarCAD 2027 Service Pack Preview with enhanced multi-core CPU optimization",'
)
c = c.replace(
    "Gstarsoft announces the beta release of GstarCAD 2026",
    "Gstarsoft previews the high-performance 2027 Service Pack update"
)

# 3. BricsCAD V25 -> V27 for 2026 previews
c = c.replace(
    '"title": "Bricsys previews BricsCAD V25: modern BLADE LISP environment adds remote debug protocols",',
    '"title": "Bricsys previews BricsCAD V27: modern BLADE LISP environment adds remote debug protocols",'
)
c = c.replace(
    "BricsCAD V25 introduces a re-engineered BLADE IDE",
    "BricsCAD V27 introduces a re-engineered BLADE IDE"
)

# 4. URLs
c = c.replace("https://www.gstarcad.net/cad-solution/architecture/", "https://www.gstarcad.net/application/")
c = c.replace("https://www.gstarcad.net/cad-solution/point-cloud/", "https://www.gstarcad.net/gstarcad2027")

with open("data/news.json", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated data/news.json timeline and URLs successfully")
