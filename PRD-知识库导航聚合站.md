# GstarCAD Academy 全球官方学习与赋能平台 PRD（V2.0 — 回归浩辰海外业务）

> **战略更新（V2.0）**：根据公司海外业务战略调整，本项目全面结束“去浩辰化/第三方泛 CAD 中立聚合”过渡定位，正式回归 **苏州浩辰软件股份有限公司（Suzhou Gstarsoft Co., Ltd.，上交所科创板 688657）海外核心业务**，将 `gstarcademy.com` 升级打造为浩辰出海的官方旗舰级学习、认证与客户成功平台（GstarCAD Global Academy & Migration Hub）。

---

## 1. 产品概述

- **产品定位**：
  **GstarCAD 官方海外学习与赋能学院 (Official GstarCAD Global Academy)**
  集 **AutoCAD 零成本平滑迁移中心** + **官方体系化课程与教程** + **GstarCAD 官方技能认证与考核** + **DWG FastView 云与移动协同** + **GRX/LISP 开发者中心** + **全球商业转化与试用枢纽** 于一体的海外业务阵地。
- **产品目标**：
  1. **商机与线索转化**：为海外各区域（欧洲、日韩、东南亚、美洲、中东）工程设计企业提供从 AutoCAD 转向 GstarCAD 的低门槛验证、30 天试用下载与商业询价通路。
  2. **用户赋能与品牌粘性**：通过 289+ 题考核认证体系、模块化视频/图文课程，让全球工程师与企业快速熟练使用 GstarCAD 及其机械/建筑专版。
  3. **生态与技术壁垒**：支撑海外 ISV 软件厂商将 ObjectARX 插件极低成本移植到 GstarCAD GRX / .NET 平台。

---

## 2. 核心支柱与功能矩阵

| 业务板块 | 核心职责 | 支撑功能与页面 |
|---|---|---|
| **AutoCAD 迁移中心** (`/migration`) | 解决海外企业应对 Autodesk 高昂订阅与授权审查痛点 | 100% 原生 DWG/DXF 互通验证、99% 相同快捷命令速查、直接运行 AutoLISP、5 年 TCO 成本节省 75% 计算器、企业迁移 5 步清单 |
| **官方课程与教程** (`/tutorials`) | 提供官方入门与进阶教程 | GstarCAD 2025/2026 新特性、2D 绘图效率工具、GstarCAD Mechanical 机械标准件/BOM、GstarCAD Architecture 智能建筑对象、DWG FastView 现场协同 |
| **官方技能认证与基准** (`/quiz`) | 标准化 CAD 制图能力评测 | 6 大工程赛道（BIM, MCAD, Civil, 2D Drafting, CAE, Viz）、289+ 道专业题库、错题本复习、GstarCAD 官方能力认证证书与数字徽章 |
| **DWG FastView 协同生态** | 链接 5000 万+ 全球移动/云端用户 | 移动端现场测量看图、云端图纸批注与版本对比、团队跨端协同 |
| **开发者与二次开发中心** (`/developers`) | 吸引海外 ISV 伙伴移植行业插件 | GRX (C++ ObjectARX 高度兼容) SDK、.NET API 指南、AutoLISP / Visual LISP 自动化范例、VBA 办公室集成 |
| **商业漏斗与试用下载** (`/download`) | 引导海外商机转化 | GstarCAD Professional / Mechanical / Architecture 30 天全功能免费试用安装包指引、软硬件环境需求、全球代理商联络 |
| **工程知识库基石** (`/knowledge-base`) | 沉淀高价值工程概念与 SEO 权重 | 交互式 D3 拓扑图谱、ISO/ASME/GB 工程图纸规范、专业术语词典、技术排障 FAQ |

---

## 3. 目标用户画像与出海转化路径

### 3.1 目标用户
1. **海外工程企业采购决策者 / CAD 经理**：
   - 痛点：每年向 Autodesk 支付数万乃至数十万美元的高昂订阅费，面临合规审查压力，寻找真正 100% 兼容且支持永久授权（Perpetual License）的替代方案。
   - 转化路径：`Home` &rarr; `Migration Hub` (查看兼容矩阵与 TCO 计算器) &rarr; `Download Free Trial` (安装试用验证) &rarr; `Contact Global Sales / Find Local Partner` (批量商业采购)。
2. **一线制图工程师 / 设计师**：
   - 痛点：担心更换软件后需要重新学习快捷键、已有图纸打不开或排版混乱、习惯的 AutoLISP 插件跑不起来。
   - 转化路径：`Migration Hub` (验证快捷键与 LISP 原生支持) &rarr; `Learn & Courses` (掌握 GstarCAD 高阶技巧) &rarr; `Certification` (考核拿认证证书)。
3. **第三方行业插件开发者 (ISVs)**：
   - 痛点：想拓展 GstarCAD 的全球庞大用户群，但不希望重写几万行 C++ ObjectARX 代码。
   - 转化路径：`Developers` (阅读 GRX 移植指南) &rarr; 下载 GRX SDK &rarr; 编译插件并上架推荐。

---

## 4. 技术与合规准则

1. **统一品牌与企业归属**：所有对外文案、Footer、Schema.org 结构化数据统一明确标注为 **Gstarsoft Co., Ltd. (苏州浩辰软件股份有限公司, SSE: 688657)**。
2. **性能与体验保障**：保持纯静态 HTML/CSS/JS 极速加载优势（Lighthouse 95+），Cloudflare Pages / Vercel 全球边缘 CDN 分发。
3. **持续自动化回归**：任何针对 Quiz 测验系统的修改，必须严格通过 `node tests/engine-harness.js` 自动化回归测试。
4. **构建规范**：前端修改必须执行 `npx esbuild` 重新生成 `*.min.js` 和 `*.min.css`，并递增版本号防缓存。
