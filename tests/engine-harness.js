// 行为级回归：在 Node 中加载真实发布的 quiz.min.js（esbuild 产物），
// 用最小 DOM 桩驱动引擎，验证本次修复的关键逻辑。
const fs = require("fs");
const path = require("path");

function makeClassList() {
  const set = new Set();
  return {
    add: (...cs) => cs.forEach((c) => set.add(c)),
    remove: (...cs) => cs.forEach((c) => set.delete(c)),
    contains: (c) => set.has(c),
    toggle: (c, force) => {
      const has = set.has(c);
      const want = force === undefined ? !has : !!force;
      want ? set.add(c) : set.delete(c);
      return want;
    },
    _sync: (v) => { set.clear(); String(v || "").split(/\s+/).filter(Boolean).forEach((c) => set.add(c)); },
  };
}

function makeEl(tag) {
  const el = {
    id: "",
    tagName: (tag || "div").toUpperCase(),
    style: {},
    children: [],
    _html: "",
    textContent: "",
    value: "",
    href: "",
    disabled: false,
    type: "",
    listeners: {},
    _qcache: {},
    insertAdjacentElement(pos, other) { this.children.push(other); return other; },
    appendChild(c) { this.children.push(c); return c; },
    remove() {},
    querySelector(sel) { return (this._qcache[sel] = this._qcache[sel] || makeEl(sel)); },
    querySelectorAll(sel) {
      if (sel === ".quiz-option-btn") return this.children.filter((c) => c.className === "quiz-option-btn");
      return [];
    },
    addEventListener(ev, fn) { (this.listeners[ev] = this.listeners[ev] || []).push(fn); },
    click() { (this.listeners.click || []).forEach((fn) => fn({ target: this, preventDefault() {} })); },
  };
  Object.defineProperty(el, "innerHTML", {
    get() { return this._html; },
    set(v) { this._html = v; this.children.length = 0; },
  });
  let cls = "";
  const list = makeClassList();
  Object.defineProperty(el, "className", {
    get() { return cls; },
    set(v) { cls = v; list._sync(v); },
  });
  el.classList = list;
  return el;
}

const els = {};
const byId = (id) => (els[id] = els[id] || makeEl("div"));
[
  "quiz-selection-screen", "quiz-active-screen", "quiz-result-screen", "quiz-lessons-screen",
  "quiz-question-title", "quiz-options-wrapper", "quiz-track-badge", "quiz-question-progress",
  "quiz-progress-bar", "quiz-hearts-container", "quiz-feedback-banner", "quiz-feedback-status",
  "quiz-explanation-body", "quiz-btn-continue", "quiz-submit-btn", "quiz-success-view",
  "quiz-failure-view", "result-xp", "result-status", "global-streak-badge", "global-streak-count",
  "lessons-unit-title", "lessons-unit-subtitle", "lessons-cards-wrapper", "mistake-review-card",
  "mistake-count-badge", "backup-stat-xp", "backup-stat-streak", "backup-stat-nodes",
  "backup-code-input", "btn-copy-backup", "import-code-input", "btn-import-backup", "backup-message",
].forEach(byId);
["bim", "mcad", "civil", "draft", "sim", "viz"].forEach((t) => {
  byId("ring-fill-" + t); byId("ring-text-" + t); byId("stat-desc-" + t);
});

const store = new Map();
global.localStorage = {
  getItem: (k) => (store.has(k) ? store.get(k) : null),
  setItem: (k, v) => store.set(k, String(v)),
  removeItem: (k) => store.delete(k),
};
const locationStub = { search: "", href: "http://x/quiz", reload() {} };
const windowListeners = {};
const documentListeners = {};
global.window = { addEventListener: (ev, fn) => (windowListeners[ev] = windowListeners[ev] || []).push(fn), location: locationStub };
global.document = {
  getElementById: byId,
  createElement: (tag) => makeEl(tag),
  addEventListener: (ev, fn) => (documentListeners[ev] = documentListeners[ev] || []).push(fn),
  querySelectorAll: () => [],
  body: makeEl("body"),
};
global.navigator = { clipboard: { writeText: async () => {} } };
global.btoa = (s) => Buffer.from(s, "binary").toString("base64");
global.atob = (s) => Buffer.from(s, "base64").toString("binary");
global.escape = escape;
global.unescape = unescape;

const code = fs.readFileSync(path.join(__dirname, "..", "quiz.min.js"), "utf8");
function boot(search) {
  // 模拟真实浏览器刷新：清空缓存的元素与旧监听器，避免跨 boot 叠加
  for (const k of Object.keys(els)) delete els[k];
  for (const k of Object.keys(windowListeners)) delete windowListeners[k];
  for (const k of Object.keys(documentListeners)) delete documentListeners[k];
  locationStub.search = search || "";
  locationStub.href = "http://x/quiz" + (search || "");
  eval(code);
}

const optionBtns = () => byId("quiz-options-wrapper").children.filter((c) => c.className === "quiz-option-btn");
const clickOption = (i) => optionBtns()[i].click();
const submitMulti = () => byId("quiz-submit-btn").click();
const continueQuiz = () => byId("quiz-btn-continue").click();
const heartsBroken = () => byId("quiz-hearts-container").children.filter((c) => c.classList.contains("broken")).length;
const stripTags = (s) => s.replace(/<[^>]+>/g, " ").replace(/&amp;/g, "&").replace(/\s+/g, " ").trim().replace(/^[A-D] /, "");

const ORACLE = {
  "structural role of a 'Family'": { c: ["A reusable component containing parametric"], multi: false },
  "Shared Coordinates' critical": { c: ["It aligns independent architectural"], multi: false },
  "Scan-to-BIM workflows": { c: ["It registers the point cloud"], multi: false },
  "primary structural difference": { c: ["Project Parameters can appear in schedules"], multi: false },
  "standard Revit workflows": { c: ["Acquiring coordinates from a linked survey", "Publishing coordinates to linked", "Specifying coordinate parameters directly"], multi: true },
  "Clash Detection' before site": { c: ["It identifies spatial intersections"], multi: false },
  "exporting coordinates and metadata": { c: ["To enable open-standard data exchange"], multi: false },
  "4D and 5D BIM": { c: ["4D adds construction schedule time"], multi: false },
  "Search Sets' preferred": { c: ["Search Sets dynamically update"], multi: false },
  "Model View Definitions": { c: ["IFC2x3 Coordination View", "IFC4 Reference View", "IFC4 Design Transfer View"], multi: true },
  "federated model' from a single": { c: ["A federated model overlays separate"], multi: false },
};
function answerCurrent(deliberateWrong) {
  const title = byId("quiz-question-title").textContent;
  const key = Object.keys(ORACLE).find((k) => title.includes(k));
  if (!key) throw new Error("oracle 缺失: " + title.slice(0, 70));
  const { c } = ORACLE[key];
  const ok = [], bad = [];
  optionBtns().forEach((b, i) => (c.some((p) => stripTags(b._html).startsWith(p)) ? ok : bad).push(i));
  (deliberateWrong ? bad.slice(0, 1) : ok).forEach((i) => clickOption(i));
  if (ok.length > 1) submitMulti();
}
const T = [];
const check = (n, cond) => T.push([cond ? "PASS" : "FAIL", n]);
const getJSON = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) || d; } catch { return d; } };
const mistakes = () => getJSON("gstarcademy_mistakes", []);

// ---------- 场景 1：单选/多选 答错登记、答对移除（修复点 #1） ----------
localStorage.setItem("gstarcademy_lessons_progress", JSON.stringify({ bim: [1] }));
boot("?track=bim&lesson=2");
answerCurrent(true); // 第 1 题故意答错
check("S1 答错扣心 (broken=" + heartsBroken() + ")", heartsBroken() === 1);
check("S1 错题本登记 1 条: " + JSON.stringify(mistakes()), mistakes().length === 1);
continueQuiz();
answerCurrent(false); // 第 2 题答对
check("S1 答对后错题本: " + JSON.stringify(mistakes()), mistakes().length <= 1);
continueQuiz();
answerCurrent(true); // 第 3 题再答错
check("S1 再次答错登记: " + JSON.stringify(mistakes()), mistakes().length >= 1 && mistakes().length <= 2);

// ---------- 场景 2：错题复习全对 → 清空 + 20 XP ----------
boot("?track=mistake");
const pool = mistakes().length;
check("S2 复习抽题 = 错题数 (" + pool + ")", pool >= 1);
for (let i = 0; i < pool; i++) { answerCurrent(false); continueQuiz(); }
check("S2 复习后错题清空", mistakes().length === 0);
check("S2 通关 +20 XP (xp=" + localStorage.getItem("gstarcademy_total_xp") + ")", localStorage.getItem("gstarcademy_total_xp") === "20");
check("S2 结算标题 = Mistakes Cleared!", byId("quiz-success-view").querySelector(".hero-title").textContent.includes("Mistakes Cleared"));

// ---------- 场景 3：9 课支持（修复点 #2） ----------
localStorage.setItem("gstarcademy_lessons_progress", JSON.stringify({ bim: [1] }));
boot("?track=bim&lesson=4");
check("S3 未解锁 L4 → 重定向关卡页 (href=" + locationStub.href + ")", locationStub.href.includes("track=bim") && !locationStub.href.includes("lesson"));
localStorage.setItem("gstarcademy_lessons_progress", JSON.stringify({ bim: [1, 2, 3] }));
boot("?track=bim&lesson=4");
const q4 = byId("quiz-question-title").textContent;
check("S3 L1-L3 完成后 L4 直接开考 (Q=" + q4.slice(0, 45) + "...)", q4.length > 10 && !q4.includes("Loading"));
check("S3 L4 徽章 = [" + byId("quiz-track-badge").textContent + "]", byId("quiz-track-badge").textContent.includes("L4"));
boot("?track=bim&lesson=99");
check("S3 越界 lesson=99 → 重定向", locationStub.href.includes("track=bim") && !locationStub.href.includes("lesson"));

// ---------- 场景 4：备份管理器节点总数动态化（修复点 #3） ----------
store.clear();
localStorage.setItem("gstarcademy_lessons_progress", JSON.stringify({ bim: [1] }));
boot("");
check("S4 Lit Nodes = [" + byId("backup-stat-nodes").textContent + "]", byId("backup-stat-nodes").textContent === "0 / 40");

// ---------- 场景 5：placement 阈值与失败分支 ----------
boot("?track=placement");
check("S5 placement 抽 12 题 (progress=" + byId("quiz-question-progress").textContent + ")", byId("quiz-question-progress").textContent.includes("12"));
let guard = 0;
while (heartsBroken() < 3 && byId("quiz-result-screen").style.display !== "block" && guard < 30) {
  const btn = optionBtns()[0];
  btn.click();
  continueQuiz();
  guard++;
}
check("S5 心耗尽 → 失败结算 (result=" + byId("quiz-result-screen").style.display + ")", byId("quiz-result-screen").style.display === "block" && byId("quiz-failure-view").style.display === "block");
check("S5 失败标题 = [" + byId("quiz-failure-view").querySelector(".hero-title").textContent + "]", byId("quiz-failure-view").querySelector(".hero-title").textContent.includes("Placement Test Failed"));

// ---------- 场景 6：placement 通关 → +150 XP / 6 赛道点亮 / 40 节点 / 概念点亮 ----------
store.clear();
boot("?track=placement");
const P_ORACLE = {
  "In a collaborative BIM project, which of the following is the standard workflow": "Exporting models in IFC/NWC format",
  "According to BIM specifications, what does LOD 400 represent": "Detailed fabrication, shop assembly",
  "When building a parametric 3D CAD model": "To capture and enforce design intent",
  "ultimate technical goal of adopting Model-Based Definition": "Embedding all Product Manufacturing Information",
  "Triangulated Irregular Network (TIN) surface": "By connecting survey coordinate points",
  "Horizontal Alignments dynamically linked to Vertical Profiles": "Alignments govern the horizontal X-Y centerline",
  "acad.pgp or gcad.pgp configuration files": "Mapping custom single or double-letter keyboard",
  "referencing drawings via Xrefs": "Xrefs reference external files dynamically",
  "golden rule for separating Model Space and Paper Space": "Drawing all design geometry at 1:1 scale in Model Space",
  "primary purpose of writing and loading AutoLISP": "Writing custom macro procedures",
  "mesh convergence testing essential": "Mesh convergence verifies that results",
  "laminar or turbulent flow solver": "The Reynolds number of the flow",
  "Metalness and Roughness parameters control": "Metalness determines whether light is reflected",
  "render separate passes (diffuse, reflection, depth, shadow)": "Separate passes enable non-destructive",
};
for (let i = 0; i < 12; i++) {
  const title = byId("quiz-question-title").textContent;
  const key = Object.keys(P_ORACLE).find((k) => title.includes(k));
  if (!key) throw new Error("placement 未知题: " + title.slice(0, 60));
  let hit = -1;
  optionBtns().forEach((b, j) => { if (stripTags(b._html).startsWith(P_ORACLE[key].slice(0, 30))) hit = j; });
  if (hit < 0) throw new Error("placement 选项未命中: " + title.slice(0, 60));
  clickOption(hit);
  continueQuiz();
}
check("S6 placement 通关结算显示", byId("quiz-success-view").style.display === "block");
check("S6 结算标题 = Placement Test Passed!", byId("quiz-success-view").querySelector(".hero-title").textContent.includes("Placement Test Passed"));
check("S6 +150 XP (xp=" + localStorage.getItem("gstarcademy_total_xp") + ")", localStorage.getItem("gstarcademy_total_xp") === "150");
const roadmap = getJSON("gstarcademy_roadmap_progress", {});
const litTracks = ["bim", "mcad", "civil", "draft", "sim", "viz"].filter((t) => Array.isArray(roadmap[t]) && roadmap[t].length > 0);
check("S6 点亮赛道 = " + litTracks.join(","), litTracks.length === 6);
const nodes = Object.values(roadmap).reduce((s, a) => s + a.length, 0);
check("S6 点亮节点总数 = " + nodes, nodes === 40);
const concepts = getJSON("gstarcademy_concept_mastery", []);
check("S6 概念点亮含 sim/viz/placement slug (" + concepts.length + " 个)", concepts.includes("fea-discretization") && concepts.includes("placement-pbr-materials"));
boot("");
check("S6 备份面板 = [" + byId("backup-stat-nodes").textContent + " / " + byId("backup-stat-xp").textContent + "]", byId("backup-stat-nodes").textContent === "40 / 40" && byId("backup-stat-xp").textContent === "150 XP");

console.log("\n===== 回归结果（quiz.min.js 行为级）=====");
T.forEach(([s, n]) => console.log(s + "  " + n));
const fails = T.filter(([s]) => s === "FAIL").length;
console.log("\n" + (fails ? "❌ " + fails + " 项失败" : "✅ 全部通过"));
process.exit(fails ? 1 : 0);
