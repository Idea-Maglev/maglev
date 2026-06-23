# Maglev vs Traditional: A Paradigm Shift Analysis
> **Objective**: 对比 "传统软件工程" 与 "Maglev AI-Native 工程" 的环境与方法论差异。

## 1. 核心范式对比 (Core Paradigm)

| 维度 | 传统开发 (Traditional) | Maglev (AI-Native) | 本质变化 |
| :--- | :--- | :--- | :--- |
| **第一资产** | **Code** (代码是唯一真理) | **Spec & Rules** (文档与规则是真理) | **Shift Up**: 资产重心上移，代码沦为"编译产物"。 |
| **驱动引擎** | **Human Brain** (人脑记忆与逻辑) | **Context** (AI 上下文与检索) | **Context-Driven**: 开发不再靠"记性"，靠"索引"。 |
| **最小单元** | **Function/Class** | **Skill/Workflow** | **Agentic**: 封装的不再是代码块，而是"能力"。 |

## 2. 环境差异 (Environment)

### 2.1 传统环境
*   **IDE**: 是个文本编辑器 + 调试器。
*   **Git**: 是个存储库。
*   **CI/CD**: 是个打包流水线。
*   **痛点**: 上下文割裂。需求在文档里，代码在 IDE 里，Bug 在 Jira 里。

### 2.2 Maglev 环境 (The "Context Engine")
*   **IDE (Cursor/Windsurf)**: 是个 **Conversational Runtime (对话运行时)**。
    *   它不仅编辑代码，还"阅读"规则 (`.maglev/rules`)。
    *   它主动"执行"工作流 (`.agents/workflows`)。
*   **Repo Structure**: 是个 **Knowledge Graph (知识图谱)**。
    *   `specs/` 与 `src/` 通过双向链接 (`metrics.py` <-> `data_schema.md`) 强绑定。
*   **Validation**: 是个 **Real-time Auditor (实时审计)**。
    *   不再等 CI 跑挂了才知道错了，Coding 阶段 AI 就在审计 "Spec Alignment"。

## 3. 工作流差异 (Workflow)

### 3.1 线性 vs 环形
*   **传统**: 需求 -> 设计 -> 编码 -> 测试 -> 发布 (线性，回滚成本高)。
*   **Maglev**:
    1.  **Intent**: 人定义 "我要做什么" (Thinking)。
    2.  **Crystallize**: AI 将其固化为 Spec。
    3.  **Generate**: AI 生成/修改 Code。
    4.  **Audit**: AI/脚本 校验一致性。
    *   *特点*: **原子化闭环**。每一个 Feature 都是一次完整的 PDCA 循环。

### 3.2 守门员机制
*   **传统**: 靠 Code Review (人眼看) 和 Unit Test (覆盖率)。
*   **Maglev**: 靠 **Protocol** (协议)。
    *   提交时强制检查 "Code 变了，Spec 变了吗？"(Bi-directional Sync)。
    *   "降级模式"允许负债，但必须显性化。

## 4. 人的角色变化
*   **Coder -> Architect**: 你不再需要手写 `for` 循环，你需要定义 `Interface` 和 `Constraint`。
*   **Executor -> Reviewer**: 你的主要工作从"写"变成了"审"。
*   **Memory -> Indexer**: 你不需要记住所有代码细节，但需要维护好 `repository_map.md`，让 AI 能找到。

## 5. 结论
Maglev 并不是"让开发变快了"（虽然结果往往如此），而是 **"让开发的抽象层级变高了"**。
我们构建的不是代码，而是一套 **"能自我进化的数字资产"**。
