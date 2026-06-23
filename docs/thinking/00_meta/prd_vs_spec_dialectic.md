# PRD vs Spec: A Red Team Analysis (红队辩证)

> **Context**: User 提出 "PRD 给人读，Spec 给 AI 读" 及 "真实的 PRD 是对抗共创的产物"。
> **Action**: AI 进行反思与挑战 (Red Teaming)。

## 1. User Hypothesis (用户假设)
1.  **PRD 不一定是人写的，也不可信**。
2.  **True PRD = Plan** (对抗产生的共识)。
3.  **Audience Separation**: PRD -> Human, Spec -> AI/Expert.

## 2. Red Team Challenge (AI 挑战)

### Challenge A: The "Black Box Spec" Trap (黑盒 Spec 陷阱)
*   **User View**: "Spec 更多是给专家和 AI 读的。"
*   **AI Challenge**: 如果 Spec 只有 AI 能读懂（e.g., 纯 JSON Schema, 复杂的伪代码），那么**人类将失去"验收权" (Loss of Adjudication)**。
    *   当 AI 说 "代码写好了"，人类怎么知道它是否符合 Spec？人类看不懂 Spec。
    *   **Conclusion**: **Spec 必须是 "Human-Readable Protocol"**。它是 AI 和 Human 唯一的通用语言（英语/中文 + 伪代码）。它不能堕落为机器码。

### Challenge B: The "Ephemeral Truth" Risk (真理的挥发性)
*   **User View**: "对抗产生的那个计划，才是实际的 PRD。"
*   **AI Challenge**: 聊天记录里的"计划"是挥发性的。
    *   如果我们不把这个 "Debate Outcome" (辩论结果) **固化 (Crystallize)** 下来，两天后我们就会忘记"为什么当时决定这么做"。
    *   **Conclusion**: 那个"对抗产生的计划"，必须被回写到一个文件里。它可以叫 `PRD_v2_Synthesized.md`，或者直接作为 Spec 的 `## Context` 章节。**不能只停留在对话框里。**

## 3. Synthesis (辩证统一)

### 3.1 定义修正 (Refined Definition)

| 资产 | 真正的受众 | 本质 |
| :--- | :--- | :--- |
| **Raw PRD (Input)** | **AI** (它是被 AI "吃" 的原料) | 噪音与意图的混合体。 |
| **Synthesized Spec (Output)** | **Human & AI** (Bridge) | **法律条文 (Legalese)**。它是对齐共识的唯一界面。 |
| **Code** | **Machine** | 执行结果。 |

### 3.2 真正的 "PRD" 是什么？
用户说得对，初始文档不是 PRD。
**真正的 PRD (The Truth)** 是 **Spec 里的 "Context" 章节 + "Logic" 章节**。
Spec 不仅仅是给 AI 执行的，它更是**Human 用来约束 AI 的法律文书**。

## 4. Action Item
在生成 Spec 时，必须保证其**可读性**。
Spec = **Business Context (Human Readable)** + **Technical Constraints (Machine Enforceable)**。

## 5. Final Consensus (最终共识)
通过对抗与反思，达成以下核心对齐：
1.  **Input Diversity**: PRD 只是多模态输入 (Meeting, Interview, Raw) 的一种形式，且初始版本往往不可信。
2.  **Synthesis**: 真正的 "PRD" 是经过 AI-Human 对抗辩论后产生的 **Consensus Plan (共识计划)**。
3.  **The Bridge**: **Spec** 是承载这一共识的唯一容器。它既不是纯自然语言 (Too Vague for AI)，也不是纯代码 (Too Hard for Human)。
4.  **Traceability**: 即使跳过 Input 文档 (Spec-First)，Spec 内部也必须内嵌 "Why" (Context) 以保证长期可维护性。
