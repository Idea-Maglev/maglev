# gstack 深度研究报告

> **日期**: 2026-05-25
> **目标版本**: latest (2026-05, 70+ skills, 23K+ stars)
> **Maglev 版本**: v0.4.3
> **研究范围**: gstack 从 "Garry Tan 个人工具" 演进为完整的 AI 工程流水线框架
> **性质**: 客观对比分析，不预设立场

## 一、概览

gstack 是 Y Combinator 总裁 Garry Tan 开源的 AI 编码工作流系统。核心理念是将软件开发过程分解为**角色驱动的 SKILL.md 文件**，每个 skill 代表一个专家角色（CEO/Eng/QA/Designer/Security/Release），通过 slash commands 触发。

特征数据：
- 23K+ GitHub Stars
- 70+ 技能目录（远超最初报道的 23 个）
- 持久化 headless Chromium 浏览器守护进程（QA 核心）
- 跨平台：Claude Code, Codex, Gemini CLI, Cursor
- Bun runtime, TypeScript 技术栈
- SKILL.md 由 `.tmpl` 模板自动生成

## 二、对标分析

### M-1: 定位与目标

| 维度 | gstack | Maglev v0.4.3 |
|------|--------|---------------|
| 一句话定位 | "Garry Tan 的 Claude Code 配置 — 角色驱动的 AI 工程流水线" | "AI-Native 工程协议，Spec 即 IR" |
| 核心目标 | 让一个人+AI 产出 20 人团队的成果（"Golden Age"） | 产物驱动的全生命周期人机协作 |
| 目标受众 | Solo maker / 小团队创始人（YC 创始人群体） | 个人 → 小团队 |
| 设计哲学 | "Boil the Lake + Search Before Building + User Sovereignty" | "需求→方案→实施→验证" + 对抗纪律 |
| 开源状态 | MIT, 个人维护(Garry Tan), Bun/TypeScript | MIT, 个人维护, 纯 Markdown |
| 覆盖范围 | Plan → Build → Review → QA → Ship → Deploy → Monitor → Retro | 需求 → 方案 → 编码 → 验证 |

**关键差异**: gstack 覆盖了**运维全链路**（部署、监控、iOS QA），Maglev 聚焦**规格/协议层**（spec quality, traceability）。

### M-2: 架构模式

| 维度 | gstack | Maglev v0.4.3 |
|------|--------|---------------|
| 整体架构 | SKILL.md.tmpl → 生成 SKILL.md → 安装到 ~/.claude/skills/ | AGENTS.md + .agents/skills/ 协议层 |
| 技术栈 | Bun, TypeScript, Playwright/Chromium | 纯 Markdown + YAML |
| 分发方式 | `git clone` + `./setup` (symlink) | `git clone` + maglev-cli |
| 扩展机制 | 70+ 内置 skill 目录 + contrib/ | .agents/skills/ + private-catalog.yaml |
| 模板系统 | `.tmpl` → `bun run gen:skill-docs` | 无（SKILL.md 手写） |
| 浏览器能力 | ✅ 持久化 Chromium daemon (~100ms/命令) | ❌ 无 |
| iOS 能力 | ✅ 真机 QA (USB + Tailscale) | ❌ 无 |

**SKILL.md.tmpl 模板机制亮点**：
- Skill 文件由模板生成，不手动编辑输出
- 可针对不同 host (claude/codex) 生成不同版本
- Preamble 自动注入（ETHOS 三原则）
- `{{BROWSE_SETUP}}`, `{{COMMAND_REFERENCE}}` 等占位符统一管理

### M-3: 需求→实施流水线

| 维度 | gstack | Maglev v0.4.3 |
|------|--------|---------------|
| 需求收敛 | `/office-hours` + `/spec` (五阶段 spec → GitHub issue) | requirement-convergence (4-step 对抗) |
| 方案设计 | `/plan-ceo-review` + `/plan-eng-review` + `/plan-design-review` | spec-designer (Socratic Interview) |
| 编码执行 | 直接实施（无专门的 implementation skill） | context-implementer |
| 验证闭环 | `/review` + `/qa`(真浏览器) + `/qa-only` | integrated-validator |
| 部署发布 | `/ship` + `/land-and-deploy` + `/canary` | ❌ 无 |
| 回顾改进 | `/retro` (周报 + shipping streaks) | ❌ 无 |

**gstack `/spec` 流程**: vague intent → five phases → GitHub issue → optional agent spawn in fresh worktree → `/ship` closes issue on merge。这是一个**完整的 spec-to-ship 自动化链路**。

**gstack `/autoplan`**: 一键运行 CEO → Design → Eng → DX 四个 review（并行审视同一个计划）。

### M-4: 治理与纪律

| 维度 | gstack | Maglev v0.4.3 |
|------|--------|---------------|
| 核心纪律 | 3 原则 (Boil the Lake / Search / User Sovereignty) | 3 不可灰度红线 + 8 惰性模式 |
| 安全门禁 | `/careful` + `/freeze` + `/guard` + `/cso` (OWASP) | maglev-discipline L0-L4 |
| 路由机制 | PROACTIVE 模式：意图模式匹配 → 自动触发 skill | entry-router |
| 防跳步 | 角色分离（CEO review ≠ Eng review ≠ QA） | Activation sequence |
| 代码质量 | `/health` (type checker, linter, tests, dead code) | integrated-validator |

**PROACTIVE routing 亮点**：
gstack 在 SKILL.md.tmpl 中定义了约 40 条**意图→skill 路由规则**，当用户表达匹配意图时自动调用对应 skill。这比 Maglev 的 entry-router 更**声明式**和**细粒度**。

### M-5: 知识管理

| 维度 | gstack | Maglev v0.4.3 |
|------|--------|---------------|
| 跨会话记忆 | `/context-save` + `/context-restore` + gbrain (跨机器同步) | session-store + knowledge-check |
| 学习系统 | `/learn` (管理 gstack 跨会话学习内容) | knowledge-check |
| 文档生成 | `/document-generate` (Diataxis: tutorial/how-to/reference/explanation) | ❌ 无自动文档生成 |
| 知识分层 | 无（平面 skills/ 目录） | docs/thinking/ (5 层) + specs/ (3 层) |
| 结晶/归档 | ❌ 无 | ✅ crystallization |

### M-6: 对 Maglev 的启示

#### 1. 可借鉴的模式

**① PROACTIVE routing 声明式意图映射（优先级：高）**

gstack 的 40+ 条 "pattern → skill" 路由规则非常精巧：
```
User describes a new idea → /office-hours
User asks about strategy → /plan-ceo-review
User reports a bug → /investigate
User asks to ship → /ship
```

Maglev 的 entry-router 做类似的事，但规则是隐含在 SKILL.md 的描述中的，不如 gstack 的**显式声明式路由表**清晰。可以考虑在 entry-router 中增加类似的结构化路由声明。

**② Skill 模板生成机制（优先级：中）**

`SKILL.md.tmpl` → `bun run gen:skill-docs` 的模式解决了一个痛点：skill 中有大量共享内容（preamble, 工具列表, 安全规则），手动维护容易不一致。Maglev 可以考虑：
- 将 ETHOS 注入 → 等价于将 maglev-discipline 自动注入每个 skill
- 将平台差异（claude/codex/cursor）通过模板变量处理

**③ "Boil the Lake" 完整性哲学（优先级：低-中）**

"When the complete implementation costs minutes more than the shortcut — do the complete thing. Every time." 这个哲学可以被吸收为 Maglev 的编码纪律补充。

#### 2. Maglev 差异化优势

- **Spec 质量深度**: gstack 的 `/spec` 是五阶段自动生成 spec → issue；Maglev 的 spec-designer 是**对话式** Socratic Interview + 结构化质量规则。Maglev 产出的 spec 质量更高。
- **需求对抗**: gstack 无 requirement-convergence 对等物——直接从"想法"跳到 spec。
- **追踪性**: gstack 无 requirements↔spec↔code↔test 四层交叉验证。
- **知识分层**: gstack 是平面 skills/，Maglev 有 5 层 thinking/ + 3 层 specs/。
- **结晶闭环**: gstack 的 spec 没有生命周期管理。
- **纪律深度**: gstack 的 3 原则是"好的建议"，Maglev 的 8 类惰性模式 + L0-L4 是**可检测可升级的系统**。

#### 3. gstack 做了 Maglev 没做的事

- **Browser QA**: 持久化 Chromium + 真实浏览器测试。这是 Maglev 完全没覆盖的维度。
- **Deploy/Ship/Monitor**: `/ship` → `/land-and-deploy` → `/canary` 完整 CD 链路。
- **iOS 真机测试**: USB + Tailscale 远程驱动真实 iPhone。
- **Retro/回顾**: 结构化的 weekly retro 和 shipping streak 追踪。
- **自动文档生成**: Diataxis 四象限文档生成。

但这些差异**不是 Maglev 需要追赶的**——它们属于"运维/操作层"，而 Maglev 的定位是"协议/规格层"。这是定位差异，不是能力差距。

#### 4. 风险/警示

- **gstack 在 combo stack 中的角色**: 用户可能把 gstack 用作"组织/角色/QA 层"，搭配其他工具做 spec。Maglev 需要意识到 gstack 用户已经有了角色分离和阶段门控——如果要吸引这些用户，需要展示 Maglev 在 spec 质量和追踪性上的独特价值。
- **PROACTIVE 模式的启示**: gstack 证明了"不需要用户记住 40 个命令"——意图自动路由就够了。Maglev 的 20+ skills 也面临同样的发现性问题。

## 三、Actionable Insights

| ID | 标题 | 建议目标 | 优先级 | 简述 |
|----|------|----------|--------|------|
| GST-001 | 声明式意图路由表 | entry-router | high | 参考 PROACTIVE 模式将路由规则从隐式→显式声明 |
| GST-002 | Skill 模板生成机制 | skill 体系 | medium | 考虑 .tmpl → SKILL.md 生成，解决共享内容一致性 |
| GST-003 | "Boil the Lake" 完整性原则 | maglev-discipline | low | 作为编码纪律的补充（AI 时代完整实现的边际成本为零） |

### GST-001: 声明式意图路由表

| 层次 | 分析 |
|------|------|
| **What** | gstack 在模板中定义 40+ 条显式 pattern→skill 映射，如 "user reports a bug → /investigate" |
| **Why** | 用户不可能记住所有 skill 名称；框架需要"自动发现最合适的 skill" |
| **Demand Signal** | high — 所有多 skill 框架用户都面临"不知道该用哪个 skill"的问题 |
| **Maglev Applicability** | high — Maglev 20+ skills 同样有发现性问题，entry-router 是隐式的 |
| **Response Strategy** | absorb — 在 entry-router 或 AGENTS.md 中增加显式意图路由声明表 |

### GST-002: Skill 模板生成机制

| 层次 | 分析 |
|------|------|
| **What** | SKILL.md.tmpl → `bun run gen:skill-docs` 自动生成最终 skill 文件，注入共享 preamble |
| **Why** | 多 skill 框架有大量共享内容（纪律规则、工具列表），手动维护不一致 |
| **Demand Signal** | medium — 当 skill 数量超过 10-15 个时出现的维护痛点 |
| **Maglev Applicability** | medium — Maglev 目前 20+ skills，已有一致性问题但可通过 AGENTS.md 部分解决 |
| **Response Strategy** | watch → absorb when pain grows — 当前 AGENTS.md 注入足够，但如果 skill 数量继续增长，值得考虑模板机制 |

### GST-003: "Boil the Lake" 完整性原则

| 层次 | 分析 |
|------|------|
| **What** | "AI 时代完整实现的边际成本接近零，永远选择完整方案而非捷径" |
| **Why** | 开发者习惯性选择"够用"而非"完整"，AI 改变了成本结构 |
| **Demand Signal** | low — 这是哲学/文化层面，不是功能需求 |
| **Maglev Applicability** | low — maglev-discipline 已有类似精神，但未如此直白表述 |
| **Response Strategy** | watch — 作为文化参考，不需要机制改动 |

## 四、新竞品发现（本轮）

本轮未发现新竞品。但确认了 combo stack 中的第三个成员 GSD (Get Shit Done) 框架值得后续关注。

## 五、研究元数据

- **信息来源**: GitHub (garrytan/gstack) 仓库根目录 + AGENTS.md + ETHOS.md + SKILL.md.tmpl; Web search (TechTimes, Pulumi blog, MarketPost, BuildThisNow, DeepWiki)
- **研究耗时**: ~10 min
- **Registry 变化**:
  - 升级 gstack: research_type batch_scan→deep, 更新 insights (GST-001 升级 + 新增 GST-002, GST-003)
  - 可能新增 GSD 为候选观察对象
- **维度说明**: Mandatory M1-M6 全覆盖, 未触发新 Exploratory 维度
