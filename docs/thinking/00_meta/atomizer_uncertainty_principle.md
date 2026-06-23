# 意图雾化与不确定性原理 (Atomizer & The Uncertainty Principle)

> **Context**: 如何处理 50 页的 Mega-PRD？如何避免 "Idea -> Code" 过程中的幻觉与偏差？

## 1. 核心争论: 为什么不能直接执行 Issue？

### The Uncertainty Principle (不确定性原理)
*   **前提**: Maglev 拒绝假定 "Human 的想法一开始就是清晰的" 或 "AI 的理解一开始就是对的"。
*   **双盲陷阱**:
    *   Human 以为自己写清楚了 Requirement。
    *   AI 以为自己看懂了 Context。
    *   **结果**: 双方在错误的假设上狂奔，产出无用的代码。

### 解决方案: 对抗式共创 (Adversarial Co-Creation)
我们必须引入一个 **"Clarification (质询)"** 和 **"Reflection (反思)"** 环节。意图不是被"记录"的，而是被"审问"出来的。

## 2. 意图雾化器 ( The Atomizer)

### 2.1 为什么要雾化？
*   **Token 瓶颈**: 一个 Issue 无法承载 50 页的上下文。
*   **关注点分离**: 开发 UI 时不应被 Stripe 的支付协议干扰。

### 2.2 工作流
1.  **Ingest**: 把 PRD 扔进 `specs/20_evolution/intake/` (Raw Material)。
2.  **Clarify**: AI 提出拆解计划，Human 挑战计划 (The Three-Beat Rhythm)。
3.  **Atomize**: 生成 N 个 `issues/active/` (Atomic Intents)。
4.  **Link**: 建立 `Issue -> PRD#Section` 的引用。

## 3. 设计辩证 (Dialectics)

### Q: PRD 为什么不放在 `00_vision`？
*   **Vision (00)** 是北极星 (两年后的愿景)。
*   **PRD** 是行军图 (两周内的迭代)。
*   **结论**: PRD 是 `20_evolution` 的一部分，作为 **"Intake Input"** 存在。

### Q: 为什么需要缓释交付 (Buffered Delivery)？
*   如果在迭代过程中实时合并 `10_reality`，会导致 Truth 被"半成品"污染。
*   **策略**: 所有变更在 `20_evolution` (Sandbox) 中闭环，直到验收通过，才通过 **Batch Merge** 跃迁进 `10_reality`。

## 4. 结论
通过 **Uncertainty Principle** (反思) 和 **Atomizer** (降维)，我们实现了从 "模糊宏大" 到 "精准原子" 的安全着陆。
