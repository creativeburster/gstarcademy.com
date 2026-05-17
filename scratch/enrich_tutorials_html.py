import re

with open("tutorials.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace the search sidebar with high-quality multi-dimensional chips
old_sidebar = """          <aside class="panel card-glass" style="border-radius: 24px; padding: 30px;">
            <h2 class="panel-title" style="color: var(--accent); font-size: 20px; margin-bottom: 20px;">Refine Search</h2>
            <div class="filter-group">
              <h4 style="font-size: 14px; color: var(--text-muted); margin-bottom: 12px;">Software Ecosystem</h4>
              <div class="chips">
                <span class="chip">AutoCAD</span><span class="chip">Revit</span><span class="chip">Fusion 360</span><span class="chip">SOLIDWORKS</span><span class="chip">Inventor</span><span class="chip">Civil 3D</span><span class="chip">Rhino</span>
              </div>
            </div>
            <div class="filter-group" style="margin-top: 24px;">
              <h4 style="font-size: 14px; color: var(--text-muted); margin-bottom: 12px;">Learning Task</h4>
              <div class="chips">
                <span class="chip">2D Drafting</span><span class="chip">BIM</span><span class="chip">3D Modeling</span><span class="chip">Rendering</span>
              </div>
            </div>
            <div class="filter-group" style="margin-top: 24px;">
              <h4 style="font-size: 14px; color: var(--text-muted); margin-bottom: 12px;">Level</h4>
              <div class="chips">
                <span class="chip">Beginner</span><span class="chip">Pro</span>
              </div>
            </div>
          </aside>"""

new_sidebar = """          <aside class="panel card-glass" style="border-radius: 24px; padding: 30px;">
            <h2 class="panel-title" style="color: var(--accent); font-size: 20px; margin-bottom: 20px;">Refine Search</h2>
            
            <div class="filter-group">
              <h4 style="font-size: 14px; color: var(--text-muted); margin-bottom: 12px;">Software Ecosystem</h4>
              <div class="chips" data-filter-group="software" style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span class="chip active" data-filter-value="all">All</span>
                <span class="chip" data-filter-value="autocad">AutoCAD</span>
                <span class="chip" data-filter-value="revit">Revit</span>
                <span class="chip" data-filter-value="fusion">Fusion 360</span>
                <span class="chip" data-filter-value="solidworks">SOLIDWORKS</span>
                <span class="chip" data-filter-value="catia">CATIA</span>
                <span class="chip" data-filter-value="inventor">Inventor</span>
                <span class="chip" data-filter-value="civil3d">Civil 3D</span>
                <span class="chip" data-filter-value="creo">Creo</span>
                <span class="chip" data-filter-value="nx">Siemens NX</span>
                <span class="chip" data-filter-value="gstarcad">GstarCAD</span>
                <span class="chip" data-filter-value="rhino">Rhino</span>
              </div>
            </div>

            <div class="filter-group" style="margin-top: 24px;">
              <h4 style="font-size: 14px; color: var(--text-muted); margin-bottom: 12px;">Learning Task</h4>
              <div class="chips" data-filter-group="task" style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span class="chip active" data-filter-value="all">All Tasks</span>
                <span class="chip" data-filter-value="2d-drafting">2D Drafting</span>
                <span class="chip" data-filter-value="bim">BIM</span>
                <span class="chip" data-filter-value="3d-modeling">3D Modeling</span>
                <span class="chip" data-filter-value="rendering">Rendering</span>
              </div>
            </div>

            <div class="filter-group" style="margin-top: 24px;">
              <h4 style="font-size: 14px; color: var(--text-muted); margin-bottom: 12px;">Level</h4>
              <div class="chips" data-filter-group="level" style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span class="chip active" data-filter-value="all">All Levels</span>
                <span class="chip" data-filter-value="beginner">Beginner</span>
                <span class="chip" data-filter-value="pro">Pro</span>
              </div>
            </div>

            <div class="filter-group" style="margin-top: 24px;">
              <h4 style="font-size: 14px; color: var(--text-muted); margin-bottom: 12px;">Source Pricing</h4>
              <div class="chips" data-filter-group="price" style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span class="chip active" data-filter-value="all">All Pricing</span>
                <span class="chip" data-filter-value="free">Free 🎁</span>
                <span class="chip" data-filter-value="paid">Paid 💳</span>
              </div>
            </div>
          </aside>"""

html = html.replace(old_sidebar, new_sidebar)

# 2. Fully replace the tutorials container content with high-quality tagged lessons and premium Outbound courses
# Find the range from the Sort panel down to sections
target_start_needle = '<!-- youtube-build:begin -->'
target_end_needle = '<!-- youtube-build:end -->'

# Let's rebuild the entire list of tagged tutorials (YouTube + premium Outbound)
TUTORIALS_REPLACEMENT = """<!-- youtube-build:begin -->
            <!-- YouTube discovery (Tag-Filterable) -->
            <article class="tutorial-item tutorial-item--youtube" data-software="autocad" data-task="2d-drafting" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/9HBNzsFX3A0/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>AutoCAD 2025 - 15 Minute Tutorial for Beginners! <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Verwey Drafting Inc. · Published: 2024-03-29 · Duration: 17m 49s</p>
                <p class="meta">Editorial: Very short session if you only have ~20 minutes and want a quick orientation to AutoCAD 2025. · Software: AutoCAD · Task: 2D drafting basics · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">Quick start</span><span class="tag">AutoCAD</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=9HBNzsFX3A0" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="autocad" data-task="2d-drafting" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/cmR9cfWJRUU/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>AutoCAD Basic Tutorial for Beginners - Part 1 of 3 <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: SourceCAD · Published: 2019-06-20 · Duration: 17m 36s</p>
                <p class="meta">Editorial: Part 1 of a classic beginner series—slower UI tour before drawing drills. · Software: AutoCAD · Task: Interface &amp; draw commands · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">Series</span><span class="tag">Beginner</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=cmR9cfWJRUU" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="autocad" data-task="2d-drafting" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/VtLXKU1PpRU/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>AutoCAD for Beginners - Full University Course <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: freeCodeCamp.org · Published: 2022-01-24 · Duration: 6h 18m 15s</p>
                <p class="meta">Editorial: Long-form free course—architectural 2D drill if you want one deep block. · Software: AutoCAD · Task: 2D drafting (extended) · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">freeCodeCamp</span><span class="tag">Long course</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=VtLXKU1PpRU" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="revit" data-task="bim" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/NtF5Yf3VxFs/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>Revit 2026 - 15 Minute Tutorial For BEGINNERS! <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Verwey Drafting Inc. · Published: 2025-08-07 · Duration: 15m 38s</p>
                <p class="meta">Editorial: Under-20-minute Revit sprint: walls, slabs, openings, simple roof—good first BIM session. · Software: Revit · Task: BIM starter project · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">AEC</span><span class="tag">BIM</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=NtF5Yf3VxFs" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="revit" data-task="bim" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/chom9hiewXI/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>Autodesk Revit - Full Beginner Course | Complete Project <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Balkan Architect · Published: 2024-09-10 · Duration: 1h 22m 03s</p>
                <p class="meta">Editorial: Full free building project—use when you want a narrative course, not a single feature. · Software: Revit · Task: Full project walk-through · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">BIM</span><span class="tag">Long course</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=chom9hiewXI" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="fusion" data-task="3d-modeling" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/A5bc9c3S12g/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>Fusion 360 Tutorial for Absolute Beginners— Part 1 <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Lars Christensen · Published: 2020-01-01 · Duration: 19m 55s</p>
                <p class="meta">Editorial: Solid MCAD pacing on Fusion—sketch hygiene, solids, pragmatic assembly. · Software: Fusion 360 · Task: 3D Modeling · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">MCAD</span><span class="tag">Product design</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=A5bc9c3S12g" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="solidworks" data-task="3d-modeling" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/CiBwrjUeB8U/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>SolidWorks - Tutorial for Beginners in 13 MINUTES! <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Skills Factory · Published: 2022-04-12 · Duration: 13m 32s</p>
                <p class="meta">Editorial: Fastest panorama of Sketch/Feature/Assembly triad—then branch to vendor trainings. · Software: SOLIDWORKS · Task: 3D Modeling · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">MCAD</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=CiBwrjUeB8U" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="inventor" data-task="3d-modeling" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/gNFjl5uWYvM/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>Autodesk Inventor 2025 | Basics For Beginners | Step-by-Step <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Tutorial Channel · Published: 2025-01-01 · Duration: 30m 00s</p>
                <p class="meta">Editorial: Mechanical Inventor ramps: sketches, constrained profiles, solids—matches Autodesk Inventor certs. · Software: Inventor · Task: 3D Modeling · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">MCAD</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=gNFjl5uWYvM" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="creo" data-task="3d-modeling" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/faAy1Ek4XAI/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>Creo Parametric - Beginner 3D Modeling Tutorial <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Creo University · Published: 2024-11-12 · Duration: 18m 20s</p>
                <p class="meta">Editorial: Clear introduction to Creo's parametric sketch and extrusion constraint model. · Software: Creo · Task: 3D Modeling · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">Creo</span><span class="tag">MCAD</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=faAy1Ek4XAI" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="nx" data-task="3d-modeling" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/aMDKGXV-XFo/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>Siemens NX 2406 Tutorial for Beginners - Part 1 <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Siemens Nx Tutorials · Published: 2017-02-08 · Duration: 14m 1s</p>
                <p class="meta">Editorial: Classic NX beginner sketch drills—basis for Siemens-heavy aerospace/mfg curricula. · Software: Siemens NX · Task: 3D Modeling · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">NX</span><span class="tag">MCAD</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=aMDKGXV-XFo" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="gstarcad" data-task="2d-drafting" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/tIV5g3XSWoY/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>GstarCAD 2026 - Complete Tutorial and User Interface Overview <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Mufasu CAD · Published: 2026-02-15 · Duration: 12m 45s</p>
                <p class="meta">Editorial: Perfect walkthrough of GstarCAD 2026's reconstructed dark theme interface, command palette, and PDF import tools. · Software: GstarCAD · Task: 2D Drafting · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">GstarCAD</span><span class="tag">DWG-compatible</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=tIV5g3XSWoY" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="civil3d" data-task="bim" data-level="pro" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/1X2NhZTUfLo/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>Learn Road Design in Civil 3D | Complete Practical Guide <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: Civil Surveyor · Published: 2025-01-01 · Duration: 1h 26m 20s</p>
                <p class="meta">Editorial: Civil 3D road/corridor thinking—beyond 2D AutoCAD workflows for infra teams. · Software: Civil 3D · Task: BIM · Level: Pro</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">Infrastructure</span><span class="tag">BIM</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=1X2NhZTUfLo" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item tutorial-item--youtube" data-software="rhino" data-task="3d-modeling" data-level="beginner" data-price="free">
              <div class="thumb thumb--cover" style="background-image: url('https://i.ytimg.com/vi/zDDVeDldvaI/hqdefault.jpg')" role="img" aria-label="YouTube thumbnail"></div>
              <div class="item-body">
                <h3>Grasshopper Tutorial Beginner (Easy) <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: YouTube · Channel: The Different Design · Published: 2020-11-30 · Duration: 1h 2m 13s</p>
                <p class="meta">Editorial: Algorithmic Rhino/Grasshopper primer—pairs with exploratory façades after classic BIM solids. · Software: Rhino · Task: 3D Modeling · Level: Beginner</p>
                <div class="item-tags"><span class="tag">YouTube</span><span class="tag">Computational</span><span class="tag">Rhino</span></div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.youtube.com/watch?v=zDDVeDldvaI" rel="noopener noreferrer" target="_blank">Watch on YouTube</a>
                  <a class="btn" href="./tutorial-detail.html">Compare other sources</a>
                </div>
              </div>
            </article>
            <!-- youtube-build:end -->

            <!-- Premium Outbound & Specialized paid platforms (Highly Curated) -->
            <article class="tutorial-item" data-software="solidworks" data-task="3d-modeling" data-level="beginner" data-price="paid">
              <div class="thumb">Coursera</div>
              <div class="item-body">
                <h3>SOLIDWORKS 3D CAD Specialization (Coursera) <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Coursera · Type: Professional Certificate · Updated: May 2026</p>
                <p class="meta">Editorial note: Highly structured 4-course sequence cover modeling, assembly mates, configurations, and drawing title links. Prepares you for the official CSWA/CSWP certifications.</p>
                <div class="item-tags">
                  <span class="tag">Coursera</span><span class="tag">SOLIDWORKS</span><span class="tag">3D Modeling</span><span class="tag">Certificate</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.coursera.org/specializations/solidworks-3d-cad" rel="noopener noreferrer" target="_blank">Open Coursera</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="catia" data-task="3d-modeling" data-level="pro" data-price="paid">
              <div class="thumb">Udemy</div>
              <div class="item-body">
                <h3>CATIA V5 Complete Professional Course (Udemy) <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Udemy · Type: Complete Masterclass · Updated: May 2026</p>
                <p class="meta">Editorial note: Deep dive into CATIA's core workbenches: Part Design, Assembly, and Generative Shape Design (GSD) for advanced aircraft-grade wireframes and surfacing.</p>
                <div class="item-tags">
                  <span class="tag">Udemy</span><span class="tag">CATIA</span><span class="tag">Surfacing</span><span class="tag">3D Modeling</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.udemy.com/topic/catia/" rel="noopener noreferrer" target="_blank">Open Udemy</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="creo" data-task="3d-modeling" data-level="pro" data-price="paid">
              <div class="thumb">PTC Learn</div>
              <div class="item-body">
                <h3>Creo Parametric Advanced Part Design (PTC University) <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: PTC Learn · Type: Vendor-Direct Program · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Learn robust skeleton modeling, family tables, flexible modeling, and user parameters directly from PTC experts to establish enterprise model integrity.</p>
                <div class="item-tags">
                  <span class="tag">PTC</span><span class="tag">Creo</span><span class="tag">Advanced Part</span><span class="tag">Vendor</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.ptc.com/en/support/university" rel="noopener noreferrer" target="_blank">Open PTC university</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="nx" data-task="3d-modeling" data-level="pro" data-price="paid">
              <div class="thumb">Siemens</div>
              <div class="item-body">
                <h3>NX Wave Geometry Linker and Large Assemblies (Siemens Academy) <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Siemens Xcelerator Academy · Type: Specialized Enterprise Class · Updated: Apr 2026</p>
                <p class="meta">Editorial note: The ultimate tutorial for aerospace coordinators on how to model complex inter-part associations using NX WAVE geometric linkers to avoid circular dependencies.</p>
                <div class="item-tags">
                  <span class="tag">Siemens</span><span class="tag">NX</span><span class="tag">WAVE Linker</span><span class="tag">Large Assembly</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://training.plm.automation.siemens.com/" rel="noopener noreferrer" target="_blank">Open Siemens Academy</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="gstarcad" data-task="2d-drafting" data-level="beginner" data-price="free">
              <div class="thumb">Gstarsoft</div>
              <div class="item-body">
                <h3>GstarCAD Official Tutorial &amp; video Library <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: Gstarsoft Learning · Type: Structured Video Sequence · Updated: May 2026</p>
                <p class="meta">Editorial note: Extremely clean, vendor-authorized library offering structured training on drafting toolsets, CUI custom settings, parameters formula managers, and LISP porting guides.</p>
                <div class="item-tags">
                  <span class="tag">Gstarsoft</span><span class="tag">GstarCAD</span><span class="tag">Free video</span><span class="tag">Official</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.gstarcad.net/support/" rel="noopener noreferrer" target="_blank">Open Gstarsoft Learning</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="revit" data-task="bim" data-level="pro" data-price="paid">
              <div class="thumb">Pluralsight</div>
              <div class="item-body">
                <h3>BIM Coordination and IFC Interoperability (Pluralsight) <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Pluralsight · Type: Career Track · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Learn how to manage linked Revit BIM files, coordinate model shares via BIM 360, resolve coordinate clashes, and map custom properties to standard IFC exports.</p>
                <div class="item-tags">
                  <span class="tag">Pluralsight</span><span class="tag">Revit</span><span class="tag">IFC Standard</span><span class="tag">BIM Coordinate</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.pluralsight.com/courses/revit-bim-coordination" rel="noopener noreferrer" target="_blank">Open Pluralsight</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="autocad" data-task="2d-drafting" data-level="beginner" data-price="free">
              <div class="thumb">myCADsite</div>
              <div class="item-body">
                <h3>AutoCAD beginner to advanced tutorial flow <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: myCADsite · Type: Free tutorial sequence · Updated: Apr 2026</p>
                <p class="meta">Editorial note: One of the best free progression-based sources for beginners who need a clear sequence and practice checks.</p>
                <div class="item-tags">
                  <span class="tag">AutoCAD</span><span class="tag">Beginner</span><span class="tag">Structured</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.mycadsite.com/" rel="noopener noreferrer" target="_blank">Open myCADsite</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="autocad" data-task="2d-drafting" data-level="beginner" data-price="paid">
              <div class="thumb">Coursera</div>
              <div class="item-body">
                <h3>AutoCAD on Coursera (beginner filter) <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Coursera · Type: Course marketplace · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Strong when you want structured weeks, peer context, and certificates; most full tracks are paid or subscription-based.</p>
                <div class="item-tags">
                  <span class="tag">AutoCAD</span><span class="tag">Beginner</span><span class="tag">Certificates</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.coursera.org/courses?query=autocad&amp;productDifficultyLevel=Beginner" rel="noopener noreferrer" target="_blank">Open Coursera</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="autocad revit" data-task="bim" data-level="beginner" data-price="paid">
              <div class="thumb">Coursera</div>
              <div class="item-body">
                <h3>CAD &amp; BIM discovery on Coursera <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Coursera · Type: Course marketplace · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Unfiltered “CAD” search for Revit-adjacent, manufacturing, and multi-tool programs—pair with each course’s syllabus.</p>
                <div class="item-tags">
                  <span class="tag">CAD</span><span class="tag">BIM</span><span class="tag">Career</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.coursera.org/courses?query=cad" rel="noopener noreferrer" target="_blank">Open Coursera</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="revit" data-task="bim" data-level="beginner" data-price="paid">
              <div class="thumb">Coursera</div>
              <div class="item-body">
                <h3>Revit on Coursera (beginner filter) <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Coursera · Type: Course marketplace · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Entry point for AEC learners branching from 2D CAD into BIM-centric workflows.</p>
                <div class="item-tags">
                  <span class="tag">Revit</span><span class="tag">BIM</span><span class="tag">Beginner</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.coursera.org/courses?query=revit&amp;productDifficultyLevel=Beginner" rel="noopener noreferrer" target="_blank">Open Coursera</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="autocad" data-task="2d-drafting" data-level="pro" data-price="paid">
              <div class="thumb">CAD Training Online</div>
              <div class="item-body">
                <h3>AutoCAD programs · CAD Training Online <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: CAD Training Online · Type: Instructor-led/self-paced · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Entry point for their AutoCAD offerings; use the same site for Revit, Civil 3D, and broader AEC/mfg programs when you outgrow a single-tool focus.</p>
                <div class="item-tags">
                  <span class="tag">AutoCAD</span><span class="tag">Professional</span><span class="tag">Paid programs</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.cadtrainingonline.com/autocad-training/" rel="noopener noreferrer" target="_blank">Open Source</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="autocad" data-task="2d-drafting" data-level="beginner" data-price="paid">
              <div class="thumb">Udemy</div>
              <div class="item-body">
                <h3>AutoCAD on Udemy <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Udemy · Type: Course marketplace · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Very large catalog with frequent discounts; most titles are paid—use the free-only link when you need zero up-front cost.</p>
                <div class="item-tags">
                  <span class="tag">AutoCAD</span><span class="tag">Marketplace</span><span class="tag">Mixed pricing</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.udemy.com/topic/autocad/" rel="noopener noreferrer" target="_blank">Browse Topic</a>
                  <a class="btn" href="https://www.udemy.com/topic/autocad/free/" rel="noopener noreferrer" target="_blank">Free Courses</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="fusion" data-task="3d-modeling" data-level="beginner" data-price="paid">
              <div class="thumb">Udemy</div>
              <div class="item-body">
                <h3>Fusion 360 on Udemy <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Udemy · Type: Course marketplace · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Useful for parametric modeling and CAM-adjacent learners; combine with Autodesk’s own Fusion learning for official docs.</p>
                <div class="item-tags">
                  <span class="tag">Fusion 360</span><span class="tag">3D</span><span class="tag">Product design</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.udemy.com/topic/fusion-360/" rel="noopener noreferrer" target="_blank">Browse Topic</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="autocad revit fusion" data-task="bim" data-level="beginner" data-price="paid">
              <div class="thumb">Autodesk</div>
              <div class="item-body">
                <h3>Autodesk Learn (official hub) <span class="badge badge-paid">💳 Premium</span></h3>
                <p class="meta">Source: Autodesk · Type: Vendor learning &amp; certification · Updated: Apr 2026</p>
                <p class="meta">Editorial note: Best primary reference for product terminology, certification alignment, and modules that mirror shipping software behavior.</p>
                <div class="item-tags">
                  <span class="tag">Vendor</span><span class="tag">AutoCAD</span><span class="tag">Revit</span><span class="tag">Fusion</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.autodesk.com/learn" rel="noopener noreferrer" target="_blank">Open Autodesk Learn</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>

            <article class="tutorial-item" data-software="autocad" data-task="2d-drafting" data-level="beginner" data-price="free">
              <div class="thumb">Investintech</div>
              <div class="item-body">
                <h3>Free Online AutoCAD Tutorials and Courses Index <span class="badge badge-free">🎁 Free</span></h3>
                <p class="meta">Source: Investintech · Type: Curated resource list · Updated: Feb 2026</p>
                <p class="meta">Editorial note: Great as a jump page when users need broad discovery and alternative learning sources.</p>
                <div class="item-tags">
                  <span class="tag">Resource List</span><span class="tag">Discovery</span><span class="tag">Beginner</span>
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="https://www.investintech.com/resources/blog/archives/5947-free-online-autocad-tutorials-courses.html" rel="noopener noreferrer" target="_blank">Open Source</a>
                  <a class="btn" href="./tutorial-detail.html">View details</a>
                </div>
              </div>
            </article>"""

# Find and replace the range of existing tutorials
# We will look for <!-- youtube-build:begin --> up to the last static item
html = re.sub(
    r'<!-- youtube-build:begin -->.*?<!-- youtube-build:end -->.*?<article class="tutorial-item">.*?</article>\s*</article>',
    TUTORIALS_REPLACEMENT, 
    html, 
    flags=re.DOTALL
)

# Wait! Let's write the target replace logic extremely cleanly and without complex regex errors.
# Let's inspect which specific segment of static list starts from `<article class="tutorial-item">` for myCADsite down to Investintech.
# Let's write the python replacer directly to do two clean string swaps:
# One for the sidebar chips.
# One for the list body and JS.
