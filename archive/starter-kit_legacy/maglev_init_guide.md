# Maglev 智能研发协议 (Intelligent Development Protocol)

> **核心提示**: 本文档包含两部分：
> 1.  **[由浅] 3分钟快速入门**: 适合初次使用者，快速上手。
> 2.  **[入深] 协议核心定义**: 适合高级用户与 AI，查阅架构细节。

---

## Part 1: 3分钟快速入门 (Quick Start)

> **目标**: 让你在 3 分钟内拥有一个 AI 原生的研发环境。

### 1. 什么是 Maglev?
Maglev 不是一个普通的脚手架，它是你的 **AI 研发队友**。
它会帮你管理需求文档、审查代码质量、甚至自动生成测试用例。你只需要专注于最核心的业务逻辑。

### 2. 如何开始? (How to Start)

#### 步骤一：初始化 (Init)
直接对 AI 说：
> **"初始化 Maglev"** (或者输入 `/maglev-init`)

AI 会自动为你创建好所有必要的目录结构（我们称之为“基地”）。

#### 步骤二：开始工作 (Work)
初始化完成后，你只需要记住一个指令来唤醒 **智能罗盘**：
> **"我该做什么？"** (或者输入 `/start`)

AI 会自动检查你的项目状态，并建议下一步行动：
*   如果没文档 -> 它会帮你写 Spec。
*   如果有文档 -> 它会帮你写代码。
*   如果有代码 -> 它会帮你写测试。

#### 步骤三：查看地图 (Map)
当你想知道项目全景或进度时：
> **"生成项目地图"** (或者输入 `/map`)

AI 会为你生成 `docs/ATLAS.md`，展示当前项目的业务全景与开发进度。

### 3. 核心目录速查 (Cheat Sheet)
初始化后，你会看到这些目录：
*   📂 **`specs/`**: **这是真理**。所有的需求文档、技术方案都放在这里。
*   📂 **`code_storages/`**: **这是肉体**。你的业务代码放在这里。
*   📂 **`docs/`**: **这是记忆**。项目日志、架构决策记录在这里。
*   📂 **`issues/`**: **这是任务**。待办事项放在这里。

---

## Part 2: 协议核心定义 (Deep Dive)

> **To AI Assistant**: 以下内容定义了 Maglev 的核心协作要素与物理架构。在执行初始化时，请严格遵循 **Section 3: Directives**。
> **Critical Update**: 所有业务代码必须存放在 `code_storages/{repo_name}/` 下，严禁散落在根目录。

### 1. 核心要素 (Definitions)

Maglev 是由以下三个核心要素构成的 **AI 协作操作系统**：

#### 🏛️ 法则 (Rules / Context)
项目的“宪法”。它不直接运行，而是作为 **Context** 注入到 AI 的上下文中，约束 AI 的行为。
-   **Core Rules**: 定义了“铁三角”架构 (Truth/Physics/Math)、单一事实来源 (SSOT) 原则及沟通协议。
-   **Location**: 最终应存在于 `.maglev/config/core_rules.md`。

#### ⚡️ 技能 (Skills / Capabilities)
赋予 AI 的特定能力。
- 允许 AI 执行特定的高级任务，如 `maglev_audit` (审计 Spec 一致性) 或 `maglev_reverse_eng` (代码逆向)。
- **Location**: 存放于 `.agents/skills/` (或根据具体 IDE 规范存放)。
- **Inventory (Built-in)**:
    - **Creation (构建)**: `maglev-create-prd` (帮我写PRD), `maglev-quick-dev` (帮我写代码), `maglev-create-spec` (帮我写方案), `maglev-create-test-cases` (帮我生成测试).
    - **Conversion (转化)**: `atomizer` (智能助手), `maglev-reverse-spec` (读懂代码), `maglev-legacy-adopter` (接入旧项目).
    - **Governance (治理)**: `manage_asset_lifecycle` (归档旧文件), `maglev-librarian` (整理项目), `maglev-audit-prd` (检查PRD), `maglev-audit-spec` (检查方案).
    - **Utility (工具)**: `maglev-skill-forge` (创建新技能), `mermaid_expert` (画图).

#### 🌊 工作流 (Workflows / Procedures)
标准化的协作动作。
-   定义了从“意图”到“落地”的标准路径。
-   **Location**: 存放于 `.agents/workflows/`。

---

### 2. 目标状态 (Target State)

一个初始化完成的 Maglev 项目，**必须**具备以下物理结构：

```text
/
├── specs/                  # [Truth] 事实来源
│   ├── 00_vision/          # 愿景与长青文档
│   ├── 10_reality/         # 物理世界的映射 (Map)
│   │   └── repository_map.md # 🆕 仓库映射配置 (必需)
│   ├── 20_evolution/       # 正在进行的变更 (Active Iteration)
│   ├── 90_archive/         # 历史档
│   └── 99_debt/            # 已知技术债
├── {code_repo}/            # [Physics] 代码仓库 (路径灵活，由 repository_map.md 定义)
│   └── .git/               # 独立的 Git 仓库
├── tests/                  # [Guard] 质量门禁 (Black Box)
│   ├── acceptance/         # 业务验收 (Cucumber/Excel)
│   └── e2e/                # 链路测试 (Playwright)
├── issues/                 # [Task] 任务追踪 (Why & When)
│   ├── active/
│   └── closed/
├── docs/                   # [Memory] 知识库
│   ├── thinking/           # 决策过程 (Why)
│   └── guides/             # 操作手册 (How)
├── .maglev/                # [System] 系统配置
│   ├── config/
│   │   └── core_rules.md   # [Rule] 核心法则
│   ├── rules/              # [Source] 规则源
│   └── protocols/          # [Source] 协议源
└── .agents/                 # [Methodology] AI 协作层
    ├── skills/             # [Skill] AI 技能 (Audit, Reverse)
    └── workflows/          # [Workflow] 标准作业流 (Init, Sync)
```

---

### 3. 给 AI 助手的行动指令 (Directives)

作为智能协作伙伴，请执行以下逻辑，将当前文件夹 (Source) 的内容“安装”到项目根目录 (Target)：

#### Phase 1: 物理构建 (Structure)
1.  **Understand**: 扫描当前目录结构。
2.  **Migrate (迁移)**:
    -   将 `.agents/` 和 `.maglev/` 完整复制到项目根目录。
    -   确保 `specs/`, `docs/`, `issues/` 等业务目录结构在根目录创建。
    -   **Critical**: 在 `docs/` 下创建标准的 Johnny Decimal 结构 (thinking, guides等)。
3.  **Activate (激活)**:
    -   复制 `issues/README.md` 到项目对应的位置。
    -   配置 `.maglev/user.yaml`。

#### Phase 2: 核心法则注入 (Brain Injection)
1.  **Deploy**: 部署 `core_rules.md` 到 `.maglev/config/`。
2.  **Adapt (适配)**: 修正文件中的 Context 占位符。

#### Phase 3: 技能与工作流装载 (Methodology Loading)
1.  **Check**: 确保 `.agents/skills/` 和 `.agents/workflows/` 内容完整且路径正确。

---

### Appendix: 能力清单 (Capabilities Inventory)

> Maglev Starter Kit 内置了以下开箱即用的能力：

#### 🛠️ Skills (智能技能)
存放于 `.agents/skills/`，通过自然语言触发。

| 技能名称 | 类别 | 描述 | 典型指令 |
| :--- | :--- | :--- | :--- |
| **maglev-create-prd** | Creation | 帮我把想法变成产品文档 | "帮我写一个 PRD..." |
| **maglev-quick-dev** | Creation | 直接生成代码 | "实现这个功能..." |
| **maglev-create-spec** | Creation | 帮我设计技术方案 | "写一个 Tech Spec..." |
| **maglev-create-test-cases** | Creation | 帮我补充测试用例 | "生成测试用例..." |
| **atomizer** | Conversion | 智能助手 (有问题直接问我) | "下一步该做什么？" |
| **maglev-reverse-spec** | Conversion | 读懂现有代码并补全文档 | "逆向这个模块..." |
| **maglev-audit-prd** | Governance | 帮我检查产品文档写得对不对 | "审计 PRD..." |
| **maglev-audit-spec** | Governance | 帮我检查技术方案写得好不好 | "审计 Tech Spec..." |
| **manage_asset_lifecycle** | Governance | 归档旧文件 | "归档这个 Spec..." |
| **maglev-librarian** | Governance | 帮我整理项目文件 | "整理一下索引..." |
| **maglev-bootstrapper** | Utility | 初始化项目环境 | "初始化 Maglev..." |
| **maglev-tutor** | Utility | 我是新来的，请教教我 | "我是新来的..." |
| **maglev-standup** | Utility | 同步项目最新状态 | "Standup" |
| **maglev-skill-forge** | Utility | 我想创建新技能 | "创建一个新技能..." |
| **mermaid_expert** | Utility | 帮我画图/修图 | "修复这个图表..." |

### 🌊 Workflows (工作流)
存放于 `.agents/workflows/`，定义标准作业程序。

**推荐优先使用 `/` 指令 (Slash Commands) 与 AI 交互。**

| 工作流名称 | 对应指令 | 描述 |
| :--- | :--- | :--- |
| 工作流名称 | 对应指令 | 描述 |
| :--- | :--- | :--- |
| **maglev-init** | `/maglev-init` | 项目初始化 (仓库注册) |
| **map** | `/map` | 生成/更新项目地图 |
| **standup** | `/standup` | 每日站会 |
| **create-prd** | `/create-prd` | 生成 PRD |
| **create-spec** | `/create-spec` | 生成技术方案 (Spec) |
| **quick-dev** | `/quick-dev` | 快速开发功能 |
| **create-tests** | `/create-tests` | 生成测试用例 |
| **legacy-adopter** | `/legacy-adopter` | 存量项目接入 |
| **code-review** | `/code-review-backend` | 后端代码审查 |
| ... | ... | (更多指令请参考 README) |
