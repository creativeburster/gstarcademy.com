import re

file_path = 'f:/gstarcademy/tutorials.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替换标题与 meta
content = re.sub(
    r'<title>.*?</title>',
    '<title>GstarCAD Academy Course Catalog – Official Masterclasses & Certification Tracks | Gstarcademy</title>',
    content
)
content = re.sub(
    r'<meta name="description" content=".*?" />',
    '<meta name="description" content="Official learning portal for GstarCAD 2027, GstarCAD Mechanical, Architecture, DWG FastView, and AutoCAD migration. Master professional drafting and GRX SDK with verified academic certificates." />',
    content,
    count=1
)

# 2. 清理侧边栏 Software 过滤芯片，彻底移除无关非浩辰品牌
old_chips_pattern = r'<div class="chips" data-filter-group="software"[^>]*>[\s\S]*?</div>\s*</div>\s*<div class="filter-group"'
new_chips = """<div class="chips" data-filter-group="software" style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span class="chip active" data-filter-value="all">All Academy Tracks</span>
                <span class="chip" data-filter-value="gstarcad" style="background:#2563eb;color:#fff;font-weight:700;">★ GstarCAD 2027 Pro</span>
                <span class="chip" data-filter-value="fastview" style="background:#6366f1;color:#fff;font-weight:700;">★ DWG FastView Mobile/Web</span>
                <span class="chip" data-filter-value="mechanical" style="background:#10b981;color:#fff;font-weight:700;">★ GstarCAD Mechanical</span>
                <span class="chip" data-filter-value="architecture" style="background:#f59e0b;color:#fff;font-weight:700;">★ GstarCAD Architecture</span>
                <span class="chip" data-filter-value="migration" style="background:#8b5cf6;color:#fff;font-weight:700;">★ AutoCAD Migration Camp</span>
                <span class="chip" data-filter-value="developers" style="background:#0284c7;color:#fff;font-weight:700;">★ GRX & LISP Developers</span>
                <span class="chip" data-filter-value="gstarrender" style="background:#0ea5e9;color:#fff;font-weight:700;">★ GstarRender AI</span>
              </div>
            </div>
            <div class="filter-group" """

content = re.sub(old_chips_pattern, new_chips, content, count=1)

# 3. 彻底删除 <!-- Standard Community & Video Index --> 到 <!-- youtube-build:end -->
# 匹配从 <!-- Standard Community & Video Index --> 开始，直到 <!-- youtube-build:end --> 结束
del_pattern = r'<!-- Standard Community & Video Index -->[\s\S]*?<!-- youtube-build:end -->'
match = re.search(del_pattern, content)
if match:
    print(f"Found YouTube section: length {len(match.group(0))} characters")
    content = content[:match.start()] + content[match.end():]
    print("Successfully stripped YouTube section.")
else:
    print("Warning: del_pattern not matched!")

# 4. 替换 Software Deep Dives 为 GstarCAD 官方矩阵
old_deep_dives_pattern = r'<div style="margin-top: 48px; border-top: 1px solid var\(--ink-line, #e2e8f0\); padding-top: 32px;">[\s\S]*?</div>\s*</div>\s*</main>'

new_deep_dives = """<div style="margin-top: 48px; border-top: 1px solid var(--ink-line, #e2e8f0); padding-top: 32px;">
            <h3 style="font-size: 1.15rem; font-weight: 800; color: var(--ink-text); margin-bottom: 8px;">🎓 GstarCAD Academic Faculties & Official Software Suite</h3>
            <p style="font-size: 13.5px; color: var(--ink-text-soft); margin-bottom: 16px;">Direct portal links to official software editions, engineering modules, and certification exams:</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px;">
              <a href="/migration" style="padding: 12px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>🔄</span> <span>AutoCAD Migration Hub</span>
              </a>
              <a href="https://www.gstarcad.net/cad-software/" target="_blank" rel="noopener" style="padding: 12px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>💻</span> <span>GstarCAD 2027 Pro ↗</span>
              </a>
              <a href="https://www.gstarcad.net/mechanical/" target="_blank" rel="noopener" style="padding: 12px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>⚙️</span> <span>GstarCAD Mechanical ↗</span>
              </a>
              <a href="https://www.gstarcad.net/architecture/" target="_blank" rel="noopener" style="padding: 12px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>🏢</span> <span>GstarCAD Architecture ↗</span>
              </a>
              <a href="https://en.dwgfastview.com/" target="_blank" rel="noopener" style="padding: 12px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>📱</span> <span>DWG FastView Mobile ↗</span>
              </a>
              <a href="https://en.dwgfastview.com/cloud/" target="_blank" rel="noopener" style="padding: 12px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>☁️</span> <span>DWG FastView for Web ↗</span>
              </a>
              <a href="/developers" style="padding: 12px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>🛠️</span> <span>GRX C++ / .NET SDK</span>
              </a>
              <a href="/quiz" style="padding: 12px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                <span>📜</span> <span>Academic Certification</span>
              </a>
              <a href="/download" style="padding: 12px 14px; background: rgba(37,99,235,0.08); border: 1px solid rgba(37,99,235,0.3); border-radius: 10px; text-decoration: none; color: #2563eb; font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                <span>⚡</span> <span>Download 30-Day Trial</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>"""

content = re.sub(old_deep_dives_pattern, new_deep_dives, content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("tutorials.html successfully updated and saved.")
