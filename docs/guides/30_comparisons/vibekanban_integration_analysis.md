# VibeKanban 与 Maglev 方法论深度匹配分析

> **Strategic Positioning**: VibeKanban 是 Maglev 的 **"Phase 3: North Star"** (终极形态) 方案。
> 对于初期团队，请将其作为 **"反思样板" (Reflective Template)** 来理解 Maglev 的理想运作流，但**不必在 Day 1 强制引入**。
> 初期建议使用 "Issue (Repo) + Git Branching (Manual)" 的轻量级组合。

## 1. 核心理念对比 (Philosophy Alignment)

| Dimension | Maglev Methodology | VibeKanban Philosophy | Status |
| :--- | :--- | :--- | :--- |
| **Execution Model** | **Ring Iteration** (环形迭代)<br>多角色并发，快速试错。 | **Parallel Worktrees** (并发工作树)<br>通过 Git Worktree 实现物理隔离的并发执行。 | ✅ **Perfect Match**<br>VK 是 Maglev "Build" 环节的最佳容器。 |
| **Input Driver** | **Spec-First** (规格驱动)<br>先有定义，再有代码。 | **Task-First** (任务驱动)<br>看板上的 Card 驱动 Agent 行动。 | ⚠️ **Potential Conflict**<br>如果 Card 描述太随意，会退化为 "Prompt & Pray"。 |
| **Governance** | **Rule-Based** (规则治理)<br>靠 Lint/Test/Review 守门。 | **Review-Centric** (评审中心)<br>强调 Human Review 后的 Merge。 | ✅ **Strong Alignment**<br>VK 的 Diff View 是实施 Maglev "Check" 环节的杀手级功能。 |
| **Context** | **Unified Assets** (全量资产)<br>所有上下文都在 Repo 里。 | **Context Layers** (分层上下文)<br>Repo/Org/User 三层配置。 | 🔄 **Needs Adaption**<br>需要将 Maglev 的 `core_rules.md` 注入到 VK 的 Context 中。 |

---

## 2. 深度冲突与化解 (Conflicts & Resolutions)

### Conflict 1: 随意性 vs 严谨性
- **Problem**: VibeKanban 的 Card 往往是简短的 Prompt (e.g., "Fix login bug")。而 Maglev 要求 "No Code without Spec"。如果直接把 Prompt 喂给 Agent，Agent 就会瞎写。
- **Resolution: "Spec Injection" (规格注入)**
    - **不做**: 强迫 VO 在 Card 里写长篇大论。
    - **做**: 在 Card 的 Prompt 里引用 Spec 文件路径。
    - **Pattern**:
        > **Task**: Implement Login Feature
        > **Prompt**: "请仔细阅读 `specs/stories/login_flow.md`。严格按照定义的行为实现 `LoginComponent`。不要随意发挥。"
    - **Tooling**: 在 VibeKanban 的 "Agent Profile" 系统提示词中，强制加上 *"Always ask for the spec file path before verification"* 的指令。

### Conflict 2: 上下文割裂
- **Problem**: Maglev 的规则写在 `solutions/governance/core_rules.md`，VibeKanban 的 Agent 并不天然知道去读这个文件。
- **Resolution: "Context Symlink" (上下文软链)**
    - 利用 VibeKanban 的 **Project Context** 功能。
    - 在 VibeKanban 设置中，将 `solutions/governance/core_rules.md` 的内容配置为所有 Agent 的 **System Prompt 前置指令**。
    - 这样，Agent 在每一次执行 Task 时，都会“脑子里装着 Maglev 的家规”。

---

## 3. 适配改造清单 (Adaptation Action Items)

为了让 VibeKanban 完美运行 Maglev，我们需要做以下适配：

### 3.1 预设 Agent Profile (Profile Tuning)
在 VibeKanban 中创建一个名为 **"Maglev Engineer"** 的 Profile：
```yaml
name: Maglev Engineer
system_prompt: |
  你是一位遵循 Maglev 规范的 AI 工程师。
  1. **Spec-First**: 你的首要动作必须是阅读提示中提供的 Spec 文件。如果没有提供 Spec，请向用户索要。
  2. **Rule-Compliance**: 你必须严格遵守 `solutions/governance/core_rules.md` 中定义的规则。
  3. **Issue-Linking**: 你的所有 Commit Message 最好都能引用 Issue ID (例如 #123)。
```

### 3.2 流程规范 (Process Norms)
- **Card Creation**: Card 的标题必须包含 `#IssueID`。
- **Review Standard**: Reviewer 在 VibeKanban 界面 Review 时，不仅看代码，还要看“是否符合 Spec”。违反 Spec 的代码一律打回 (Reject)。

### 3.3 深度集成：Maglev Bridge (The "Hard" Integration)
为了彻底规避 "Prompt & Pray" 的随意性，我们可以通过脚本将 Maglev 的 `issues/` 目录与 VibeKanban 的 Task 列表进行**硬连接**。

**架构设计**:
`Maglev Repo (issues/*.md)` --[Sync Script]--> `VibeKanban API (MCP)`

**工作流**:
1.  **Write Issue**: VO 在 `issues/` 目录下创建 `issue_001_login.md`，写清楚 Spec。
2.  **Run Sync**: 运行 `python ops/sync_bridge.py`。
3.  **Auto Create**: 脚本调用 VibeKanban 的 MCP 接口，自动创建一个 Task Card：
    - **Title**: `[#001] Implement Login`
    - **Description**: 自动填充 Spec 的核心内容和链接。
    - **Prompt**: 自动注入 "Read spec at `issues/issue_001_login.md` and implement..."
4.  **Execute**: 人类在 VibeKanban 上看到这张卡，点击 "Start"，Agent 自动领命干活，**完全不需要人类手写 Prompt**。

**收益**:
- **强制合规**: 只有写了 Issue 才能进看板。
- **零Prompt**: 开发者的工作从 "写 Prompt" 变成了 "Review Spec & Code"。

### 3.4 类型化驱动 (Typed Issue Mapping)
针对您提到的 "Feature/Bug 是否需要细化"，答案是**必须细化**。
因为不同的 Issue 类型，对应着完全不同的 **Agent Profile** 和 **Execution Strategy**。

| Issue Type | File Prefix | VibeKanban Profile | System Prompt Focus |
| :--- | :--- | :--- | :--- |
| **Feature** | `feat-*.md` | **Builder** | "Read Spec -> Implement -> Verify Acceptance Criteria" |
| **Bug** | `fix-*.md` | **Detective** | "Read Reproduction Steps -> Write Failing Test -> Fix -> Verify Pass" |
| **Refactor** | `refactor-*.md` | **Architect** | "Analyze Dependencies -> Restructure -> Ensure No Regression" |
| **Question** | `rfc-*.md` | **Researcher** | "Search Codebase -> Summarize -> Output Report" |

**Maglev Bridge** 会解析文件名或 Frontmatter 中的类型，自动为 VibeKanban 选择正确的 Agent Profile。这就是为什么我们需要在 `issues/templates/` 下维护不同模版的原因。

---

## 4. 结论
VibeKanban 不仅仅是一个工具，它是 Maglev **"Build -> Check"** 闭环的**唯一真神 (The Chosen One)**。
它用 **Git Worktree** 解决了并发干扰，用 **Visual Diff** 解决了人工评审的惰性。
只要我们通过 **Profile Tuning** 解决了 "Spec 注入" 的问题，或者更进一步通过 **Maglev Bridge** 实现“类型化任务自动同步”，它就是 Maglev 的完美肉身。
