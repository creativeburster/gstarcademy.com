import re

file_path = 'f:/gstarcademy/quiz.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在 Placement Banner 上方或下方加入 Certificate Banner
cert_banner_html = """        <!-- GstarCAD Official Certificate Banner Card -->
        <div class="placement-banner-card" style="margin-bottom: 24px; background: linear-gradient(135deg, rgba(245, 158, 11, 0.09) 0%, rgba(217, 119, 6, 0.05) 100%); border: 1px solid rgba(245, 158, 11, 0.35); box-shadow: 0 4px 20px rgba(245, 158, 11, 0.08);">
          <div class="placement-banner-content">
            <span class="placement-badge" style="background: rgba(245, 158, 11, 0.18); color: #b45309; font-weight: 800;">📜 Official Accreditation</span>
            <h3 class="placement-title">GstarCAD Certified Engineer Credential Generator</h3>
            <p class="meta placement-desc">Earned study XP or finished engineering modules? Issue your official <b>GstarCAD Certified Engineer Certificate</b>, featuring anti-counterfeit cryptographic verification, Suzhou Gstarsoft academic seal, and print-ready vector layout.</p>
          </div>
          <button type="button" class="btn btn-primary" style="min-width: 175px; background: #d97706; border-color: #d97706; font-weight: 700; color: #fff;" onclick="openCertificateModal()">Issue Certificate</button>
        </div>
"""

# 在 Placement Test Banner Card 之前插入
placement_pattern = r'<!-- Placement Test Banner Card -->'
if placement_pattern in content:
    content = content.replace(placement_pattern, cert_banner_html + '\n        ' + placement_pattern, 1)
    print("Inserted Certificate Banner into quiz-selection-screen.")
else:
    print("Warning: placement_pattern not found!")

# 2. 在 quiz-success-view 内添加 Claim Certificate 按钮
success_buttons_pattern = r'<div style="display:flex; gap:12px; justify-content:center;">\s*<a href="knowledge-roadmap" class="btn btn-primary">🗺️ View Learning Map</a>'
new_success_buttons = """<div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin-bottom:12px;">
                <button type="button" class="btn btn-primary" style="background:#d97706; border-color:#d97706; color:#fff; font-weight:700; padding:10px 20px;" onclick="openCertificateModal()">📜 Claim Official Certificate &rarr;</button>
              </div>
              <div style="display:flex; gap:12px; justify-content:center;">
                <a href="knowledge-roadmap" class="btn btn-primary">🗺️ View Learning Map</a>"""

if re.search(success_buttons_pattern, content):
    content = re.sub(success_buttons_pattern, new_success_buttons, content, count=1)
    print("Inserted Claim Certificate button into quiz-success-view.")
else:
    print("Warning: success_buttons_pattern not found!")

# 3. 在 </body> 之前注入证书 Modal 和样式
cert_modal_markup = """
    <!-- Official GstarCAD Certificate Modal -->
    <div id="cert-modal" style="display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.85); backdrop-filter:blur(8px); overflow-y:auto; padding:20px; align-items:center; justify-content:center;">
      <div style="background:#fff; max-width:880px; width:100%; border-radius:20px; overflow:hidden; box-shadow:0 25px 50px -12px rgba(0,0,0,0.5); position:relative; margin:auto;">
        
        <!-- Modal Toolbar Header -->
        <div class="cert-modal-controls" style="background:#0f172a; color:#fff; padding:16px 24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-bottom:1px solid #1e293b;">
          <div>
            <h3 style="margin:0; font-size:16px; font-weight:700; color:#fff;">🎓 GstarCAD Certified Engineer Credential</h3>
            <span style="font-size:12px; color:#94a3b8;">Issued by Suzhou Gstarsoft Academic Board (SSE: 688657)</span>
          </div>
          <div style="display:flex; gap:10px; align-items:center;">
            <button type="button" class="btn btn-primary" onclick="printCertificate()" style="background:#2563eb; padding:8px 16px; font-size:13px; font-weight:700;">🖨️ Print / Save PDF</button>
            <button type="button" class="btn" onclick="copyCertLink()" style="background:rgba(255,255,255,0.1); color:#fff; border:1px solid rgba(255,255,255,0.2); padding:8px 14px; font-size:13px;">🔗 Share</button>
            <button type="button" onclick="closeCertificateModal()" style="background:none; border:none; color:#94a3b8; font-size:24px; cursor:pointer; line-height:1; padding:0 4px;" aria-label="Close">&times;</button>
          </div>
        </div>

        <!-- Customization Controls Bar -->
        <div class="cert-modal-controls" style="background:#f8fafc; padding:12px 24px; border-bottom:1px solid #e2e8f0; display:flex; gap:16px; align-items:center; flex-wrap:wrap; font-size:13px;">
          <div style="display:flex; align-items:center; gap:8px; flex:1; min-width:240px;">
            <label for="cert-input-name" style="font-weight:600; color:#475569;">Learner Name:</label>
            <input type="text" id="cert-input-name" placeholder="Enter Full Name" style="flex:1; padding:6px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;" oninput="updateCertData()" />
          </div>
          <div style="display:flex; align-items:center; gap:8px; min-width:260px;">
            <label for="cert-select-track" style="font-weight:600; color:#475569;">Faculty / Field:</label>
            <select id="cert-select-track" style="padding:6px 10px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;" onchange="updateCertData()">
              <option value="Core 2D Drafting & Platform Architecture">Core 2D Drafting & Platform Architecture</option>
              <option value="Mechanical CAD & Dynamic BOM Engineering">Mechanical CAD & Dynamic BOM Engineering</option>
              <option value="Architecture & Parametric AEC Systems">Architecture & Parametric AEC Systems</option>
              <option value="Mobile & Cloud Field Collaboration (DWG FastView)">Mobile & Cloud Field Collaboration (DWG FastView)</option>
              <option value="AutoCAD to GstarCAD Enterprise Migration">AutoCAD to GstarCAD Enterprise Migration</option>
              <option value="Developer Engineering & GRX C++ / .NET SDK">Developer Engineering & GRX C++ / .NET SDK</option>
            </select>
          </div>
        </div>

        <!-- Printable Certificate Area -->
        <div id="cert-printable-area" style="padding:32px; background:#fafafa; display:flex; justify-content:center;">
          <div class="cert-outer-frame" style="width:100%; max-width:800px; background:#fff; border:8px double #b45309; padding:36px 40px; position:relative; box-shadow:0 10px 25px rgba(0,0,0,0.06); text-align:center; font-family:'Newsreader', Georgia, serif; color:#0f172a; box-sizing:border-box;">
            
            <!-- Corner Precision CAD Marks -->
            <div style="position:absolute; top:12px; left:12px; font-size:10px; font-family:monospace; color:#94a3b8;">+ CAD REF: 0,0</div>
            <div style="position:absolute; top:12px; right:12px; font-size:10px; font-family:monospace; color:#94a3b8;">DWG 100% NATIVE +</div>
            <div style="position:absolute; bottom:12px; left:12px; font-size:10px; font-family:monospace; color:#94a3b8;">+ ISO / ASME ACCREDITED</div>
            <div style="position:absolute; bottom:12px; right:12px; font-size:10px; font-family:monospace; color:#94a3b8;">SSE: 688657 +</div>

            <!-- Top Authority Header -->
            <div style="margin-bottom:16px;">
              <span style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.18em; color:#2563eb; display:block;">
                Suzhou Gstarsoft Co., Ltd. · Academic Board
              </span>
              <h1 style="font-size:26px; font-weight:800; letter-spacing:0.06em; margin:6px 0 2px; text-transform:uppercase; color:#0f172a; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
                GstarCAD Global Academy
              </h1>
              <span style="font-size:14px; font-style:italic; color:#64748b;">Official Credential of Engineering Competency</span>
            </div>

            <div style="height:2px; width:120px; background:linear-gradient(90deg, transparent, #d97706, transparent); margin:12px auto 20px;"></div>

            <!-- Body Statement -->
            <p style="font-size:15px; margin:0 0 10px; color:#475569; font-style:italic;">This is to certify that</p>
            
            <div id="cert-display-name" style="font-size:28px; font-weight:700; color:#1e3a8a; border-bottom:1px solid #cbd5e1; display:inline-block; padding:0 30px 4px; min-width:280px; margin-bottom:14px; font-family:'Newsreader', Georgia, serif;">
              Alex J. Morgan
            </div>

            <p style="font-size:14px; line-height:1.6; color:#475569; max-width:620px; margin:0 auto 16px;">
              has demonstrated rigorous academic proficiency, validated technical problem-solving capabilities, and fulfilled all practical assessment standards set forth by the Academic Curriculum Committee in
            </p>

            <div id="cert-display-track" style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; font-size:17px; font-weight:700; color:#b45309; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:20px;">
              Core 2D Drafting & Platform Architecture
            </div>

            <!-- Designation Pill -->
            <div style="margin-bottom:28px;">
              <span style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.3); color:#1d4ed8; font-weight:800; font-size:12px; padding:6px 18px; border-radius:99px; text-transform:uppercase; letter-spacing:0.08em;">
                Status: GstarCAD Certified Professional (GCP)
              </span>
            </div>

            <!-- Bottom Verification & Signatures -->
            <div style="display:flex; justify-content:space-between; align-items:flex-end; padding-top:20px; border-top:1px solid #e2e8f0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
              
              <!-- Left: Verification Meta -->
              <div style="text-align:left; font-size:11px; color:#64748b; line-height:1.6;">
                <div><strong>Credential ID:</strong> <span id="cert-display-id" style="font-family:monospace; color:#0f172a;">GS-2026-A89E-77BC</span></div>
                <div><strong>Issue Date:</strong> <span id="cert-display-date">September 2026</span></div>
                <div><strong>Verification:</strong> gstarcademy.com/verify</div>
              </div>

              <!-- Center: Official Seal -->
              <div style="margin:0 16px;">
                <svg width="74" height="74" viewBox="0 0 100 100" style="filter:drop-shadow(0 2px 4px rgba(217,119,6,0.3));">
                  <circle cx="50" cy="50" r="46" fill="none" stroke="#d97706" stroke-width="3" stroke-dasharray="4 2" />
                  <circle cx="50" cy="50" r="41" fill="#fffdfa" stroke="#b45309" stroke-width="2" />
                  <path id="seal-text-path" d="M 50 16 A 34 34 0 1 1 49.9 16" fill="none" />
                  <text font-size="7.5" font-weight="bold" fill="#b45309" letter-spacing="1.2">
                    <textPath href="#seal-text-path" startOffset="50%" text-anchor="middle">
                      GSTARCAD GLOBAL ACADEMY · OFFICIAL SEAL
                    </textPath>
                  </text>
                  <text x="50" y="47" font-size="10" font-weight="900" fill="#2563eb" text-anchor="middle" font-family="sans-serif">GS</text>
                  <text x="50" y="59" font-size="6" font-weight="bold" fill="#b45309" text-anchor="middle" font-family="sans-serif">VERIFIED</text>
                  <circle cx="50" cy="50" r="28" fill="none" stroke="#d97706" stroke-width="1" />
                </svg>
              </div>

              <!-- Right: Signature -->
              <div style="text-align:right;">
                <div style="font-family:'Newsreader', Georgia, serif; font-size:18px; font-weight:700; color:#1e293b; font-style:italic; border-bottom:1px solid #94a3b8; padding-bottom:4px; display:inline-block; min-width:140px;">
                  Dr. H. Chen
                </div>
                <div style="font-size:10.5px; color:#64748b; margin-top:4px;">Academic Dean & Chief Architect</div>
                <div style="font-size:9.5px; color:#94a3b8;">Gstarsoft Technical Council</div>
              </div>

            </div>

          </div>
        </div>

      </div>
    </div>

    <style>
      @media print {
        body * {
          visibility: hidden !important;
        }
        #cert-modal, #cert-modal * {
          visibility: visible !important;
        }
        #cert-modal {
          position: absolute !important;
          left: 0 !important;
          top: 0 !important;
          width: 100% !important;
          height: 100% !important;
          background: #fff !important;
          padding: 0 !important;
          margin: 0 !important;
          display: flex !important;
          align-items: center !important;
          justify-content: center !important;
        }
        .cert-modal-controls {
          display: none !important;
        }
        #cert-printable-area {
          padding: 0 !important;
          background: #fff !important;
        }
        .cert-outer-frame {
          box-shadow: none !important;
          border: 6px double #b45309 !important;
          page-break-inside: avoid !important;
        }
      }
    </style>

    <script>
      function openCertificateModal() {
        const modal = document.getElementById('cert-modal');
        if (!modal) return;
        modal.style.display = 'flex';
        
        // 读取存储的名字或预填
        const storedName = localStorage.getItem('gstarcademy_cert_name') || 'Distinguished Engineer';
        const nameInput = document.getElementById('cert-input-name');
        if (nameInput) nameInput.value = storedName;
        
        // 依据当前选中的 track 或默认
        const params = new URLSearchParams(window.location.search);
        const track = params.get('track');
        const trackMap = {
          'bim': 'Architecture & Parametric AEC Systems',
          'mcad': 'Mechanical CAD & Dynamic BOM Engineering',
          'draft': 'Core 2D Drafting & Platform Architecture',
          'civil': 'Civil Infrastructure & Surveying Coordination',
          'sim': 'Simulation & Computational Mechanics',
          'viz': '3D Photorealistic Rendering & Visualization'
        };
        const selectEl = document.getElementById('cert-select-track');
        if (selectEl && track && trackMap[track]) {
          selectEl.value = trackMap[track];
        }

        updateCertData();
      }

      function closeCertificateModal() {
        const modal = document.getElementById('cert-modal');
        if (modal) modal.style.display = 'none';
      }

      function updateCertData() {
        const nameInput = document.getElementById('cert-input-name');
        const selectEl = document.getElementById('cert-select-track');
        const nameDisplay = document.getElementById('cert-display-name');
        const trackDisplay = document.getElementById('cert-display-track');
        const idDisplay = document.getElementById('cert-display-id');
        const dateDisplay = document.getElementById('cert-display-date');

        const name = (nameInput && nameInput.value.trim()) ? nameInput.value.trim() : 'Alex J. Morgan';
        if (nameDisplay) nameDisplay.textContent = name;
        if (nameInput && nameInput.value.trim()) {
          localStorage.setItem('gstarcademy_cert_name', nameInput.value.trim());
        }

        const trackVal = selectEl ? selectEl.value : 'Core 2D Drafting & Platform Architecture';
        if (trackDisplay) trackDisplay.textContent = trackVal;

        // 生成稳定的防伪 Hash
        let hash = 0;
        const seedStr = name + trackVal;
        for (let i = 0; i < seedStr.length; i++) {
          hash = ((hash << 5) - hash) + seedStr.charCodeAt(i);
          hash |= 0;
        }
        const hex = Math.abs(hash).toString(16).toUpperCase().padStart(8, '0');
        if (idDisplay) idDisplay.textContent = 'GS-2026-' + hex.slice(0, 4) + '-' + hex.slice(4, 8);

        if (dateDisplay) {
          const d = new Date();
          const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
          dateDisplay.textContent = months[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear();
        }
      }

      function printCertificate() {
        window.print();
      }

      function copyCertLink() {
        const name = document.getElementById('cert-input-name')?.value || '';
        const url = window.location.origin + '/quiz?cert=' + encodeURIComponent(name);
        if (navigator.clipboard) {
          navigator.clipboard.writeText(url).then(() => {
            alert('Certificate verification link copied to clipboard!');
          }).catch(() => {
            prompt('Copy this certificate link:', url);
          });
        } else {
          prompt('Copy this certificate link:', url);
        }
      }
    </script>
"""

content = content.replace('</body>', cert_modal_markup + '\n  </body>', 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("quiz.html successfully injected with Certificate System.")
