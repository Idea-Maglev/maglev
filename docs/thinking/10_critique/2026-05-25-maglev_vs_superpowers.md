# Maglev vs Superpowers：客观深度对比

> **日期**: 2026-05-25
> **Superpowers 版本**: v5.1.0 (2026-05)
> **Maglev 版本**: v0.4.3 (2026-05-25)
> **性质**: 客观对比分析，不预设立场

## 一、定位与目标

| 维度 | Superpowers | Maglev |
|------|-------------|--------|
| **一句话定位** | 通用 AI 编码代理的工程纪律框架 | 面向特定团队的 AI 协作全生命周期操作系统 |
| **核心目标** | 让 AI Agent 像专业工程师一样"正确地写代码" | 让 AI Agent 在项目全生命周期中"正确地做事" |
| **受众** | 任何使用 AI 编码工具的开发者 | 特定组织/团队的 AI 辅助工程实践 |
| **哲学** | "纪律即超能力" — 流程强制 | "磁悬浮" — 零摩擦但有导轨 |
| **开源状态** | MIT, 200k+ ⭐, 社区驱动 | 私有/内部, npm 私域发布 |

## 二、架构对比

### Superpowers 架构

```
Session Hook (session-start)
  └── 注入 using-superpowers bootstrap
        └── 技能自动触发机制
              ├── brainstorming (门禁：设计前不许编码)
              ├── writing-plans (精确到文件/行号的计划)
              ├── subagent-driven-development (每任务新 agent + 双阶段 review)
              ├── test-driven-development (铁律：先测试后实现)
              ├── systematic-debugging (假设驱动调试)
              ├── verification-before-completion (完成前验证)
              └── finishing-a-development-branch (分支收尾)
```

**关键特征**: 线性流水线，每个 skill 是管道中的一个阶段。

### Maglev 架构

```
Installer (init/update lifecycle)
  └── 注入 AGENTS.md + llms.txt + discipline
        ├── entry-router (入口分流)
        ├── 主流程 skills
        │     ├── reality-sync (会话同步)
        │     ├── spec-designer (方案设计)
        │     ├── context-implementer (受控编码)
        │     └── integrated-validator (综合验证)
        ├── 治理 skills
        │     ├── maglev-discipline (红线纪律)
        │     ├── knowledge-check (知识沉淀)
        │     ├── crystallization (现实结晶)
        │     └── index-librarian (索引管理)
        ├── 工具 skills
        │     ├── feishu-companion (飞书集成)
        │     ├── lark-integration-** (飞书 API 桥接)
        │     └── radar (依赖分析)
        └── specs/ + docs/thinking/ (知识体系)
```

**关键特征**: 网状结构，有路由层、有生命周期管理、有知识沉淀。

## 三、核心能力逐项对比

### 3.1 工作流强制

| 能力 | Superpowers | Maglev |
|------|-------------|--------|
| **Bootstrap 机制** | Session Hook 注入 using-superpowers 全文 | Installer 注入 AGENTS.md discipline block |
| **触发方式** | "1% 可能性就必须调用" — 纯靠提示词约束 | entry-router 分流 + skill triggers 字段 |
| **硬门禁** | brainstorming 阻止编码；TDD 阻止无测试代码 | discipline 红线；spec-designer 阻止无方案实施 |
| **执行验证** | verification-before-completion 要求实际运行输出 | integrated-validator 多维度交叉验证 |
| **强度评估** | ⭐⭐⭐⭐⭐ (极度强制，语气激烈) | ⭐⭐⭐⭐ (有约束但更信任 AI 判断) |

### 3.2 设计与规划

| 能力 | Superpowers | Maglev |
|------|-------------|--------|
| **需求收敛** | brainstorming: 一次一问，苏格拉底式 | requirement-convergence: 入口分流 + Ready Gate |
| **方案设计** | brainstorming → 2-3 方案 → 用户审批 → spec 文件 | spec-designer: 受控对话 → 结构化 spec → 审计面 |
| **计划粒度** | writing-plans: 2-5 分钟微任务，含完整代码 | context-implementer: 按 spec 受控编码 |
| **Spec 存储** | `docs/superpowers/specs/` (扁平) | `specs/10_reality/`, `specs/20_evolution/`, `specs/90_archive/` (三层生命周期) |
| **Spec 自审** | 占位符扫描 + 一致性检查 + 范围检查 | spec-audit-surface: 独立验证面 |

### 3.3 实施与编码

| 能力 | Superpowers | Maglev |
|------|-------------|--------|
| **执行模式** | Subagent-driven: 每任务新 agent + spec review + quality review | context-implementer: 单 agent 按 spec 逐步实施 |
| **TDD** | 铁律，违反则删除代码重来 | 未内建强制 TDD（由项目自身测试策略决定） |
| **Code Review** | 双阶段：spec 合规 → 代码质量 | review-validation-surface: 统一 review |
| **模型选择** | 按任务复杂度选模型（cheap/standard/capable） | 未内建模型选择指导 |
| **并行执行** | dispatching-parallel-agents (多 worktree) | 无对应机制（单会话单线程） |
| **Git 工作流** | using-git-worktrees (强制隔离工作区) | Git 分支约定 + 新需求必须新分支 |

### 3.4 知识管理

| 能力 | Superpowers | Maglev |
|------|-------------|--------|
| **知识沉淀** | ❌ 无 | knowledge-check: 4 步检查 + docs/thinking/ 体系 |
| **知识体系** | 仅 specs + plans (实施文档) | thinking/ 7 个分类 + specs 三层生命周期 |
| **结晶机制** | ❌ 无 | crystallization: 演进主题 → 现实归档 |
| **索引管理** | ❌ 无 | index-librarian: 多类索引扫描/验证/归档 |
| **项目记忆** | ❌ (每次 session 独立) | reality-sync: 会话启动同步主线/风险/下一步 |

### 3.5 治理与纪律

| 能力 | Superpowers | Maglev |
|------|-------------|--------|
| **红线定义** | 散布在各 skill 中（TDD iron law, brainstorming hard gate） | maglev-discipline: 集中 3 条红线 + 8 类惰性模式 |
| **纪律强度** | 语气极强，大写加粗 "EXTREMELY IMPORTANT" | 结构化定义，L0-L4 压力升级 |
| **纪律分发** | Session hook 每次注入 | Installer 自动注入 + drift 检测 |
| **纪律更新** | 用户手动更新 plugin | Installer update 自动升级 discipline block |
| **合规检查** | ❌ 无独立检查机制 | ai-context-check: 5 维 drift 检测 |

### 3.6 分发与集成

| 能力 | Superpowers | Maglev |
|------|-------------|--------|
| **安装方式** | Marketplace 插件 (1-click) | `npx @idea-maglev/maglev-cli init` |
| **支持平台** | Claude Code, Codex, Cursor, OpenCode, Gemini, Copilot CLI | 理论上任何读 AGENTS.md 的 AI 工具 |
| **更新方式** | Plugin 自动更新 (marketplace) | `maglev update` (手动触发) |
| **零依赖** | ✅ 纯 Markdown + Bash hook | ❌ Python 运行时, npm 包 |
| **隔离性** | Plugin 不修改项目文件 | 修改项目 AGENTS.md, llms.txt, 写入 .agents/ |

### 3.7 工具集成

| 能力 | Superpowers | Maglev |
|------|-------------|--------|
| **企业通讯** | ❌ 无 | feishu-companion + lark-integration-** (飞书全功能) |
| **代码分析** | ❌ (靠 agent 原生能力) | radar (optional external dependency analysis integration) |
| **可视化** | Visual Companion (浏览器 mockup) | Mermaid (模型原生能力) + whiteboard |
| **项目管理** | ❌ 无 | project-board (看板), lark-task |
| **日历/会议** | ❌ 无 | lark-calendar, lark-vc, meeting-summary |

## 四、设计哲学差异

### Superpowers 的哲学："纪律铸就超能力"

1. **极度不信任 AI 的自由裁量** — 用激烈语气和硬门禁强制流程
2. **每个任务都是独立的** — Subagent 模式确保无上下文污染
3. **代码质量至上** — TDD 铁律、双阶段 review、不妥协
4. **通用性优先** — 拒绝领域特定 skill，追求"对所有项目有用"
5. **零状态** — 不维护项目记忆，每次 session 从零开始

### Maglev 的哲学："有导轨的磁悬浮"

1. **信任 AI 但设置边界** — 红线明确但不强迫微观流程
2. **连续性优先** — reality-sync 保持跨 session 连续记忆
3. **全生命周期关注** — 不只是"写代码"，还有知识、治理、运营
4. **组织特异性** — 深度集成飞书等企业工具，面向特定团队
5. **演进感知** — specs 有生命周期（活跃→结晶→归档），不是写完就完

## 五、强项与弱项

### Superpowers 的优势

1. **极低门槛** — 1-click 安装，零配置
2. **通用性** — 任何项目、任何语言、任何 AI 工具
3. **Subagent 架构** — 真正解决了上下文污染和质量门控
4. **强制 TDD** — 显著提升代码可靠性
5. **社区验证** — 200k stars, 大量真实使用反馈
6. **轻量** — 纯 Markdown + Shell，无运行时依赖

### Superpowers 的不足

1. **无项目记忆** — 每次 session 从零开始，无法积累知识
2. **无知识管理** — 没有 thinking docs、知识沉淀、演进跟踪
3. **无企业集成** — 不关心通讯、文档、日历等企业场景
4. **过度强制** — 极端语气可能适得其反（AI 可能死板执行）
5. **无治理机制** — 没有 drift 检测、版本管理、分发闭环
6. **仅限编码** — 不覆盖需求分析、知识管理、项目治理等

### Maglev 的优势

1. **全生命周期** — 从需求到实施到知识沉淀完整覆盖
2. **组织级治理** — Installer + discipline + drift 检测形成闭环
3. **知识系统** — docs/thinking/ 7 分类 + specs 三层 + 结晶机制
4. **深度企业集成** — 飞书全功能（文档/消息/日历/表格/会议）
5. **连续记忆** — reality-sync + index 保持跨 session 上下文
6. **演进感知** — specs 有显式生命周期，不会"写完就忘"

### Maglev 的不足

1. **高门槛** — 需要 Python + npm + 理解概念才能上手
2. **非通用** — 深度绑定 enterprise private ecosystem和飞书工具
3. **无强制 TDD** — 缺少 Superpowers 那种"铁律"级别的编码纪律
4. **无 Subagent 架构** — 不支持多 agent 并行 + 独立 review
5. **社区为零** — 私有项目，无外部验证和反馈
6. **复杂性高** — 30+ skills, 多层 specs, 概念负荷大
7. **平台局限** — 主要在 Copilot CLI 验证，其他 AI 工具未充分适配

## 六、互补性分析

两者并非竞争关系，而是**不同层次的解决方案**：

```
┌─────────────────────────────────────────────────┐
│          Maglev 层 (组织/项目级)                 │
│  知识管理 · 治理 · 企业集成 · 生命周期 · 分发   │
├─────────────────────────────────────────────────┤
│       Superpowers 层 (编码执行级)                │
│  TDD · Subagent · Review · Debug · Plans        │
├─────────────────────────────────────────────────┤
│          AI Agent 层 (基础能力)                   │
│  Claude / GPT / Copilot / Codex                 │
└─────────────────────────────────────────────────┘
```

**理论上可以叠加**：Maglev 管"做什么"和"为什么"，Superpowers 管"怎么写代码"。

### 可借鉴的具体点

| 从 Superpowers → Maglev | 从 Maglev → Superpowers |
|--------------------------|--------------------------|
| Subagent 架构（每任务新 agent + 双阶段 review） | 知识沉淀机制（跨 session 积累） |
| 强制 TDD 铁律 | Spec 生命周期（active → archive） |
| 2-5 分钟微任务粒度 | 纪律分发闭环（installer + drift 检测） |
| 模型选择指导（按复杂度选模型） | 企业工具集成层 |
| Visual Companion（浏览器 mockup） | 入口路由（entry-router 分流） |
| 并行 Worktree 执行 | 治理状态检查（ai-context-check） |

## 七、结论

**Superpowers 是"编码执行层的黄金标准"** — 在"让 AI 正确写代码"这个维度上做到了极致，通过 TDD 铁律、Subagent 隔离、双阶段 Review 形成了业界最严格的质量门控。

**Maglev 是"组织级 AI 协作操作系统"** — 在"让 AI 在组织中正确做事"这个更广泛维度上构建了完整体系，涵盖知识管理、治理分发、企业集成和项目生命周期。

二者解决的是不同层次的问题。Superpowers 的 14 个 skill 全部聚焦于"代码从需求到合入"的流水线；Maglev 的 30+ skills 覆盖了从"启动会话同步上下文"到"知识结晶归档"的全景。

**对团队的建议**：如果团队的痛点是"AI 写的代码质量不够高"，Superpowers 是直接答案。如果痛点是"AI 不理解我们的项目上下文、不知道之前做过什么、不能和企业工具联动"，Maglev 是正确选择。最理想的状态是在 Maglev 的 context-implementer 中吸收 Superpowers 的 Subagent + TDD 机制。
