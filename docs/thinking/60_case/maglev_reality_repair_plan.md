# Maglev Reality Repair Plan (去幻觉与现状重塑)

> **Goal**: 消除 AI 幻觉，基于项目真实的文档、标准和代码库，重建 `specs/10_reality/` 和 `specs/00_vision.md`。绝不臆造不存在的设计。

## 1. 幻觉清除 (Hallucination Purge)

| 幻觉产物 | 现状判定 | 纠正措施 |
| :--- | :--- | :--- |
| `specs/10_reality/02_design.md` | **臆造**。文档描述了一个不存在的 Kernel/Plugin 架构。 | **删除**。 Maglev 目前是 "Methodology + Scripts + Skills"，不存在集中式 Kernel。 |
| `specs/30_solution/` | **早产**。用于构建Starter Kit的配置尚未存在。 | **删除**。保持目录纯净，直到真正需要构建时再创建。 |
| `specs/10_reality/reverse_...` (仅Bootstrapper) | **狭隘**。仅逆向了一个 Skill，忽略了 Maglev 庞大的方法论资产。 | **扩展**。认可 `standards/`, `docs/thinking/`, `.agents/skills/` 均为现状。 |

## 2. 现状重塑 (Reality Calibration)

Maglev 的现状不仅仅是代码 (Code)，更重要的是 **Methodology (方法论)** 和 **Standards (标准)**。

### 2.1 新增: `specs/00_vision.md` (愿景)
*   **Source**: `docs/thinking/README.md` (Iron Triangle), `llms.txt`, `INDEX.md`.
*   **Content**:
    *   **Vision**: 消除软件工程熵增 (Anti-Entropy).
    *   **Mission**: 构建自我进化的 AI 操作系统 (OS).
    *   **Core Values**: Spec First (所想即所得), Code as Spec (代码即设计).

### 2.2 重构: `specs/10_reality/01_requirements.md` (现状需求)
*   **Source**: `standards/` (如 `collaboration_conventions.md`), `TODO.md`.
*   **Content**: Maglev 目前已经满足的需求，而非未来需求。
    *   **Methodology**: 已经定义了 Iron Triangle, Bidirectional Protocol.
    *   **Skills**: 已经拥有了 29 个标准 atomic skills.
    *   **Workflows**: 已经拥有了 `bootstrapper`, `legacy-adopter` 等工作流.

### 2.3 重构: `specs/10_reality/repository_map.md` (真实地图)
*   **Source**: `ls -R .` (Real File System).
*   **Correction**: 必须反映 **Root is Source** 的事实。
    *   `.agents/skills` -> Core Capabilities.
    *   `standards/` -> Protocols.
    *   `docs/thinking/` -> Decision Log.

## 3. 架构设计 (Archive Architecture)

Maglev 目前的架构是 **"Agent-Driven, Skill-Based"** (Agent 驱动，技能为基)。
*   **No Central Kernel**: 目前没有 `manage.py` 这种物理内核。
*   **Distributed Runtime**: 运行时分布在 `.agents/skills/` 的各个脚本中，由 MCP 或 IDE 插件调度。
*   **Action**: 如果要写 `02_design.md`，必须如实描述这种**分散式架构**，而不是虚构一个集中式架构。

## 4. 执行步骤 (Execution Steps)

1.  **Delete**: 删除 `specs/10_reality/02_design.md`, `specs/30_solution/`.
2.  **Create**: 撰写 `specs/00_vision.md`.
3.  **Update**: 重写 `specs/10_reality/repository_map.md` 包含 `standards/` 和 `docs/`.
4.  **Verify**: 确认所有描述均有对应的文件支持。

---
*Planned by Maglev Reality Checker*
