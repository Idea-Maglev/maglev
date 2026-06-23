# Maglev OS Reality Map (Revised)

> **Core Insight**: Maglev 本身就是一个完整的软件项目。`solutions/starter-kit` 不是仅仅是"交付物"，它**就是 Maglev 的源代码** (Source Code)。我们不需要寻找外部仓库，Maglev 项目是自包含的。

## 1. 现状 (10_reality)
Maglev 项目作为一个 "Operating System"，其物理结构应直接映射到其逻辑功能。

| 逻辑层级 | 物理路径 | 对应传统软件概念 | 描述 |
| :--- | :--- | :--- | :--- |
| **Kernel (内核)** | `.agents/skills/` | **Backend Services** | 提供核心能力 (如 `bootstrapper`, `create-spec`) 的微服务集合。 |
| **Interface (接口)** | `.agents/workflows/` | **API Gateway** | 用户交互层 (Slash Commands)。 |
| **Product (产品)** | `solutions/starter-kit/` | **Distributable** | 编译/打包后的输出物 (Starter Kit)。 |
| **Source (源码)** | *(当前分散)* | **Source Code** | **关键修正**: 现有 Skill 的代码 (`.agents/skills/*`) 就是 Maglev 的源码。 |

## 2. 演进 (20_evolution)
我们需要消除 "Maglev 管理外部代码" 的错觉，转而建立 "Maglev 管理自身代码" 的架构。

### 2.1 目录结构修正
*   ❌ 删除 `specs/maglev_system/` (这是对外部系统的模拟，不符合自举)。
*   ✅ 建立 `specs/20_evolution/structure_unification/`。
*   **目标架构**:
    *   `src/skills/`: 将 `solutions/starter-kit/.agents/skills` 视为 `src`。
    *   `src/workflows/`: 将 `solutions/starter-kit/.agents/workflows` 视为 `src`。
    *   `dist/`: `solutions/starter-kit` 是构建产物。

## 3. 四层内容提炼 (The 4 Layers of Maglev)

根据用户指引，Maglev OS 自身的四层定义如下：

### Layer 1: Goal (目标)
*   **Vision**: 消除 Intent 与 Software 之间的熵增。
*   **Metric**: 100% Spec Coverage for all Skills.

### Layer 2: Status (现状)
*   **Legacy**: 20+ 个 "野生" Skill (Prompt-heavy, Code-light)，缺乏统一架构。
*   **Tech Stack**: Python (Runtime), Markdown (Protocol).
*   **Codebase**: `solutions/starter-kit/.agents/skills/` (这是我们的 Monorepo)。

### Layer 3: Needs (需求)
*   **Self-Management**: 能够用 Maglev 的指令 (`/update`) 更新 Maglev 自己的 Skill。
*   **Standardization**: 所有 Skill 必须遵循统一的目录结构 (`src`, `specs`, `tests`).

### Layer 4: Tech/Legacy (遗留与债务)
*   **Current Debt**: `.agents/` 和 `solutions/starter-kit/.agents/` 存在双份拷贝 (开发态 vs 发布态)。
*   **Resolution**: 明确 "开发态" (当前 Repo) 与 "发布态" (Starter Kit) 的流水线关系。

---
*Revised by Maglev Architect based on User Feedback*
