# Maglev vs BMM: 体系对比与对抗性反思 (Adversarial Critique)

> **Date**: 2026-02-02
> **Topic**: Skill System Architecture Comparison
> **Status**: Crystallized

## 1. 核心哲学差异 (Philosophy Divergence)

| 维度 | BMM (BMAD) | Maglev (Current) |
| :--- | :--- | :--- |
| **隐喻** | **重装步兵 (Heavy Infantry)** | **特种部队 (Special Ops)** |
| **核心逻辑** | **Workflow-Driven (流程驱动)** | **Outcome-Driven (产物驱动)** |
| **信任假设** | **Zero Trust**: 假设人不靠谱，强制 Checkpoint。 | **High Trust**: 假设 AI 很强，强制 Spec 结构。 |
| **颗粒度** | **Monolithic**: 一个 Skill 干完整个生命周期 (e.g., `create-ux`, 14 steps)。 | **Atomic**: 技能拆碎，由 Atomizer 动态路由 (e.g., `quick-spec` + `design-ux`)。 |
| **绘图语言** | **Excalidraw (JSON)**: 人类手绘，不可 Diff，非结构化。 | **Mermaid (Code)**: 代码生成，可 Diff，结构化。 |
| **产物形态** | **Documents**: 也就是 "文档"。 | **Protocol**: 也就是 "Spec/Rule/Code"。 |

---

## 2. 你的设计亮点 (Highlights) ✨

### A. 真正的 AI-Native (Mermaid vs Excalidraw)
*   **BMM 的败笔**: 强行让 AI 生成/修改 Excalidraw JSON 是反直觉的。JSON 极其脆弱，且无法进行 Code Review。
*   **Maglev 的胜利**: 坚持 **infrastructure-as-code**。User Journey, State Diagram 全用 Mermaid。这使得 Design 像 Code 一样可以被 Version Control、被 Diff、被 AI 完美理解和修改。

### B. 动态路由 (The Atomizer)
*   **BMM 的僵化**: 用户想改个字体，得跑完 `create-ux` 的 14 步流程？或者不知道该调哪个 workflow。
*   **Maglev 的灵动**: `atomizer` (v2.0) 充当了一个 "Intent Layer"。用户只需说 "我觉得登录体验不好"，Atomizer 自动识别是去 `quick-dev` 修 Bug，还是去 `design-ux` 重做设计。这种 **"意图雾化"** 是 BMM 不具备的。

### C. 闭环的生命周期 (Lifecycle)
*   **BMM 的断裂**: BMM 往往止步于 "生成了文档"。然后呢？Issue 关了吗？看板动了吗？
*   **Maglev 的闭环**: `maglev-spec-crystallize` (Step 99) 和 `maglev-spec-ingest` 实现了对 Issue 的 **自动吞吐**。Issue 既是 Trigger 也是终点。

---

## 3. 对抗性反思：你的不足 (Shortcomings & Risks) ⚠️

### A. "空心化" 风险 (The Hollow Senior Risk)
*   **攻击点**: BMM 的 `bmm-01-product-brief` 或 `bmm-06-architecture` 强迫用户回答大量 "Why" 的问题。这种繁琐的流程反而逼迫人类思考。
*   **Maglev 弱点**: `maglev-quick-spec` 太快了。AI 往往为了填满 Spec 模板而生成 "正确的废话"。
*   **风险**: 产生大量 *看起来完美但缺乏灵魂* 的功能。Maglev 缺乏一个强制人类 "慢下来" 的机制（除了新加的 Research）。

### B. 利益相关者缺失 (The Stakeholder Gap)
*   **攻击点**: BMM 包含 `sprint-planning`, `retrospective` 等技能，显式处理 "人与人" 的协作。
*   **Maglev 弱点**: 假设是 "Solo Maker" 或 "小团队"。缺乏对审批流、跨部门撕逼、汇报进度的支持。
*   **风险**: 在大公司落地时，Maglev 会被认为 "太极客"，缺乏 "管理抓手"。

### C. 技能膨胀陷阱 (Complexity Trap)
*   **攻击点**: BMM 虽然重，但技能少而全。
*   **Maglev 弱点**: 我们不知不觉已经搞了 **26 个** 技能了！`code-review-frontend`, `code-review-backend`, `plan-test-frontend`...
*   **风险**: `atomizer` 的路由逻辑会越来越复杂。如果不加治理，Maglev 会变成一个 "技能迷宫"。

---

## 4. 结论与修正策略

**Verdict**: Maglev 目前明显优于 BMM，因为它适应了 "AI 编程" 的现实（速度为王、代码即真理）。但在 "深度思考" 和 "管理维度" 上做了妥协。

**修正策略**:
1.  **Keep Research Hard**: 保持 `maglev-research` 的高门槛（必须引用），作为对抗 "空心化" 的盾牌。
2.  **Atomizer as Interface**: 用户不需要知道 26 个技能。必须强化 `atomizer` 的自然语言理解能力，让它成为唯一的 "One Interface"。
3.  **Ignore Management**: 暂时不要学 BMM 做管理类技能。Maglev 的定位应是 **"Execution Engine"**，而不是 Jira。
