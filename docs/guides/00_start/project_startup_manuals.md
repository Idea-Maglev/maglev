# Maglev 项目启动实操手册 (Project Startup Manuals)

本文档为不同阶段的项目提供分流式落地指引。请根据项目现状选择 **Track A (新项目)** 或 **Track B (老项目)**。

---

## 🚦 Track A: 绿地开荒 (Greenfield)
**适用场景**: 全新项目，从零开始。
**核心逻辑**: **AI-Driven Bootstrap** (Zero Code).

> **推荐**: 直接按当前维护中的初始化路径执行，优先参考 [Maglev 快速开始](../20_operations/maglev_distribution_quickstart.md) 和 [Maglev 初始化使用手册](../20_operations/maglev_init_manual.md)。

### 0. 准备工作 (Prerequisite)
1.  准备一个目标项目目录。
2.  按当前文档路径使用 `npm / npx` 或维护者初始化流程完成接入。

### 1. 为什么不再需要手动 mkdir？
Maglev 已经进化为 Prompt-Driven 的操作系统。
只需按当前初始化流程接入 Maglev，AI 会替你完成：
1.  构建完整的 `specs/` 体系。
2.  配置 `core_rules`。
3.  初始化 Dashboard 和 User Profile。

---

## 🚧 Track B: 存量接管 (Brownfield)
**适用场景**: 已有大量存量代码，文档缺失，希望逐步引入 AI 协作。
**核心逻辑**: **Workstation Mode** (Establish HQ -> Mount Legacy -> Reverse Spec).

### Step 0: 建立指挥部 (Setup The Workstation)
1.  **初始化工作站**:
    创建一个新的目录作为全团队的统一工作台。
    ```bash
    mkdir maglev-workspace && cd maglev-workspace
    # 使用与新项目相同的初始化流程
    # 参见 Track A 的 maglev_init_guide.md
    ```
2.  **挂载业务仓库 (Mount Legacy Repos)**:
    将你现有的业务代码 Clone 到 `source/` 目录下。
    ```bash
    mkdir source
    echo "source/" >> .gitignore
    git clone <your-legacy-repo-url> source/backend-legacy
    ```

### Step 1: 物理隔离，逻辑统一
- **Repo A (Outer)**: Maglev 仓库（包含 specs, docs, rules）。
- **Repo B (Inner)**: 业务代码仓库（在 source/ 下）。

### Step 2: 逆向工程 (Reverse Engineering)
不要试图一次性清洗整个项目。
1.  **划定特区**: 确定本次 Sprint 要动的模块（例如 `auth`）。
2.  **考古 (Reverse)**:
    - 选中代码 -> 询问 AI。
    - **Prompt**: "分析这段代码，在 `specs/20_evolution/active/reverse_auth/` 生成 Spec。"
3.  **夺权 (Establish Truth)**: 人工确认 Spec 无误后，它就成了新的 Truth。

---

## 🛠 通用工具箱 (Shared Toolkit)

| 工具 | 用法 |
| :--- | :--- |
| **项目看板** | 使用 [`project-board`](../../../.agents/skills/project-board/SKILL.md) 生成和维护当前看板 |
| **Context** | 每个人都应配置 `.maglev/user.yaml` |
