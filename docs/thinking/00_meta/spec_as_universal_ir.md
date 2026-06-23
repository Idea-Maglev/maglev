# Spec as Universal IR: The End of "The Rewrite"

> **Context**: User Hypothesis. "如果有了完整的 Spec 和现状...是不是就天然具备了用任何技术栈还原现状的能力？"
> **Insight**: Yes. Maglev makes the codebase **"Portable"**.

## 1. The Compiler Metaphor (编译器隐喻)

传统软件工程中，"重构"或"转语言"之所以是灾难，是因为**真理失传了**。
真理散落在老代码的细节、离职员工的脑子、和过期的文档里。
转语言 = 考古 + 猜谜。

在 Maglev 架构下：
*   **Specs (`specs/`)** = **Source Code (High-Level)**.
    *   包含：业务逻辑 (Logic), 数据模型 (Schema), 状态机 (Flow), UI 蓝图.
*   **Tech Stack (Java/Go)** = **Target Architecture (x86/ARM)**.
*   **Atomizer** = **Compiler (Backend)**.
*   **Source Code (`src/`)** = **Assembly/Binary**.

## 2. Capability: "Reality Rendering" (现实渲染)

如果 Spec 是完备的 SSOT (Single Source of Truth)，改变技术栈只是一次 **"Re-compile"** (重新渲染)。

### Scenario: The Migration
*   **Input**: 
    1.  `specs/10_reality/` (完整业务逻辑)
    2.  `repository_map.md` (旧架构)
    3.  **Command**: "Atomizer, switch target to `Golang + Gin`. Render."
*   **Process**:
    1.  Atomizer 读取 Spec (Logic: "满减规则").
    2.  Atomizer 调用 `golang_skill`.
    3.  Atomizer 生成新代码。
*   **Result**: 业务逻辑 100% 保留，实现细节 100% 替换。

## 3. The Tower of Babel Solved (巴别塔的倒塌)

在此视角下，"技术栈不一致" 不再是阻碍，而是 **配置项**。
Fleet 可以容纳 Java 项目和 Go 项目，因为它们在 **Spec 层** 是通用的语言（Markdown/Mermaid）。
Fleet 的 `Observatory` 分析的是 Spec 层的 "Auth Logic"，而不是 Java 层的 "Auth Class"。

> **Conclusion**: Maglev 实现了 **"Logic - Implementation Decoupling" (逻辑与实现的分离)**。这才是解决巴别塔问题的终极答案。
