# Critique: Tech Solution Generation (技术方案生成反思)

> **Trigger**: User requested reflection on the "9-Point Robustness Checklist".
> **Status**: Red Teaming via Self-Reflection.

## 1. 风险：过度设计 (Over-Engineering)
*   **Problem**: 如果为了修一个简单的 Bug (e.g., 文案错误) 也要走完 "9点检查" 和 "架构分层分析"，这是巨大的 Token 浪费和效率倒退。
*   **Correction**: 需要引入 **"Complexity Tier" (复杂度分级)**。
    *   **Tier 1 (Atomic)**: 直接 Diff。
    *   **Tier 2 (Feature)**: 走标准流程。
    *   **Tier 3 (Architecture)**: 走完整 9 点检查 + 独立设计文档。

## 2. 悖论：范围锁定的先有鸡还是先有蛋 (The Scope Paradox)
*   **Problem**: 检查点 7 要求 **"直接规划代码模块结构...严禁全库扫描"**。
    *   但在没看代码之前，AI 怎么知道要改哪些文件？
    *   如果 AI 凭空（基于文件名）猜测 Scope，很可能漏掉隐蔽的依赖（e.g., 一个全局的 EventBus Listener）。
    *   结果：AI 被锁死在错误的 Scope 里，改不动 bug，产生幻觉。
*   **Correction**: **"Two-Stage Search" (两段式搜索)**。
    *   **Stage 1 (Survey)**: 允许基于 `repository_map` 和关键字进行广度检索 (High-Level)。
    *   **Stage 2 (Lock-in)**: 检索确任后，再锁定具体的 Scope 列表，供 Coding Agent 执行。

## 3. 风险：元能力爆炸 (Meta Explosion)
*   **Problem**: 检查点 9 鼓励生成 Rule/Skill。如果不加节制，`skills/` 目录会迅速膨胀成垃圾堆。
*   **Correction**: **"Candidate Pattern" (候选人模式)**。
    *   AI 生成的 Skill 只能放在 `.agents/skills/candidates/`。
    *   必须经过 Review 和多次复用验证，才能晋升为正式 Skill。

## 4. 结论
现在的方案偏"重"，在处理轻量级任务时不仅繁琐，而且容易因为 Scope 锁得太死而导致失败。必须增加 **"弹性" (Elasticity)**。
