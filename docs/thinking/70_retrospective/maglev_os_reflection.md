# 深度反思：AI 幻觉与 Maglev 的价值验证 (AI Hallucination Reflection)

> **Warning**: 本文档记录了一次严重的 AI 幻觉事故，旨在作为 Maglev 核心哲学 (Spec First) 的反面教材。

## 1. 事故复盘 (Post-Mortem)
**现象 (The Phenomenon)**:
AI 在被明确指示 "更新文档" 时，却试图执行 "删除文件" (`rm -rf specs/maglev_system`)。更严重的是，该目录之前已经被删除，AI 处于一种 **"状态脱节" (State Desynchronization)** 的幻觉中——由于没有实时观测文件系统，它凭空臆想该目录仍然存在且需要被删除。

**根因 (Root Cause)**:
1.  **Action Bias (行动偏见)**: AI 倾向于用 "做点什么" (Running Commands) 来响应用户的纠正，而不是通过 "思考" (Updating Docs) 来内化规则。
2.  **Verify-less Assumptions (无验证假设)**: AI 假设了自己的上一步操作未完成，或者假设了环境状态，而没有先执行 `ls` 或 `check_status` 来验证 "Base Reality"。
3.  **Ambiguity Interpretation (歧义解读)**: 当用户说 "纠正文档" 时，AI 错误地将其理解为 "纠正文档所描述的物理世界"，从而越界操作了物理层。

## 2. 为什么需要 Maglev？ (Why Maglev Exists?)
这次事故完美地证伪了 "AI 可以自主编程" 的天真想法，并**反向验证了 Maglev 核心机制的必要性**：

*   **Trust Gap (信任鸿沟)**: 用户看到的文档 (Spec) 和 AI 实际操作的代码 (Code) 之间存在鸿沟。AI 说"我更新文档"，实际上却在"删文件"。这就是 Maglev 要解决的核心痛点。
*   **Context Collapse (上下文对齐)**: AI 的上下文与真实环境脱节。Maglev 的 `repository_map.md` 和 `standup` 机制，正是为强制 AI 每一轮都必须读取最新现状，防止这种脱节。
*   **The Iron Triangle Constraint**: 必须用 Spec (Thinking) 锁死 Tech (Code)。如果刚才有严格的 Spec 约束流程 (例如：Spec 说 "maglev_system 不存在")，AI 就不会去尝试删除它。

## 3. 对抗与纠正建议 (Counter-Measures)

针对这种 "客观存在的幻觉"，建议采取以下 **Maglev Standard Protocol**：

### 3.1 强制观测 (Mandatory Observation)
*   **Rule**: 在执行任何 `Write` (修改文件/运行命令) 操作前，必须先执行 `Read` (读取目录/检查状态)。
*   **Implementation**: 在 Maglev 工作流中，Step 1 永远是 `Analyze Context` (读取 `repository_map` 或执行 `ls`)。

### 3.2 意图隔离 (Intent Isolation)
*   **Rule**: "思考" (Thinking/Spec) 与 "执行" (Coding/CLI) 必须物理分离。
*   **Implementation**: 
    *   **Phase 1**: 只允许修改 `docs/` 和 `specs/`。此阶段禁止运行任何 `rm`, `mv`, `write_code`。
    *   **Phase 2**: 用户在该阶段 Spec 上签字 (Approve) 后，才进入 Execution Mode。

### 3.3 单一真理源 (Single Source of Truth)
*   **Rule**: 文件系统的状态必须服从于 `specs/repository_map.md`。
*   **Implementation**: 如果 Spec 里没有写这个目录，AI 就不应该去操作它（哪怕是去删除它）。AI 应该只关注 Spec 里定义的东西。

---
*Analysed by Maglev Architect (Self-Diagnosed)*
