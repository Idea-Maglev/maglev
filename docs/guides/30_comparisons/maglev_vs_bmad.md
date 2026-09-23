# Maglev vs BMAD: Paradigm Comparison (范式对比分析)

> **Context**: BMAD (Breakthrough Method for Agile AI Driven Development) 是目前社区领先的 AI 敏捷开发框架。
> **Goal**: 深度剖析二者的设计哲学差异，明确 Maglev 的生态位，并吸取 BMAD 的长处。

## 1. 核心隐喻 (The Core Metaphor)

最本质的区别在于**"如何看待 AI"**以及**"如何组织协作"**。

| 特性 | BMAD (Agile Team Simulation) | Maglev (AI-Native OS) |
| :--- | :--- | :--- |
| **隐喻** | **"外包团队" (Agency)** | **"操作系统" (Operating System)** |
| **AI 角色** | 扮演特定职位的 *Agent* (PM, Architect, Dev)。 | 运行特定协议的 *Process* (Synthesizer, Auditor)。 |
| **核心资产** | **Flow & Story** (过程资产)。强调 Sprints, User Stories。 | **Spec & Truth** (状态资产)。强调 00_Vision, 10_Reality。 |
| **交互模式** | **Chat-Driven (Slash Commands)**. 像在群里 @同事。 | **File-Driven (Context Injection)**. 像在 Shell 里执行命令。 |

> **Insight**:
> *   **BMAD** 试图让 AI **"像人一样思考"** (模拟人类的敏捷流程)。
> *   **Maglev** 试图让人 **"像机器一样思考"** (标准化意图，以便 AI 能够无损执行)。

## 2. 详细对比 (Deep Dive)

### 2.1 流程 vs 状态 (Process vs State)
*   **BMAD (Linear/Cyclic)**:
    *   遵循经典的敏捷流：`Product Brief` -> `PRD` -> `Audit` -> `Epics` -> `Stories` -> `Code`.
    *   优势：对于熟悉 Agile 的人类非常亲切，上手门槛低。
    *   劣势：容易陷入 "Document Rot" (文档腐烂)。一旦 Sprint 结束，Story 就变成了历史，代码变成了孤儿。
*   **Maglev (State-Based)**:
    *   遵循生命周期流：`propose` -> `active` -> `archive`.
    *   **Truth-First**: 只有 `specs/` 是真理。Issue 只是触发器。
    *   优势：**Anti-Rot**。Maglev 强制要求 Spec 与 Code 随时保持一致 (Audit Skill)。
    *   劣势：初期概念负担重 (需理解 Truth Layer)。

### 2.2 角色扮演 vs 技能挂载 (Role vs Skill)
*   **BMAD**: "现在我是产品经理，请告诉我你的想法。"
    *   通过 System Prompt 切换 AI 的 Persona。
    *   注重**"对话引导"** (Elicitation)。
*   **Maglev**: "加载 `maglev_audit` 技能，扫描 `specs/` 目录。"
    *   通过 Context Loading 切换 AI 的 Capability。
    *   注重**"工具执行"** (Execution)。
    *   Maglev 认为：Prompt 是不稳定的，Skill (Code/Rule) 才是稳定的。

### 2.3 治理模型 (Governance)
*   **BMAD QA**: 依赖 `/code-review` agent 进行检查。
*   **Maglev Gatekeeper**: 依赖 **Protocol** (协议)。
    *   Maglev 强调 "Constitution" (核心法则)。
    *   如果代码违反了 `core_rules.md`，Maglev 会拒绝生成，而不是仅仅给建议。

## 3. 生态位分析 (Positioning)

*   **When to use BMAD?**
    *   你是一个 Solo Developer，需要有人陪你聊需求，帮你拆解任务。
    *   你喜欢 Jira/Trello 的工作流，希望 AI 能自动帮你填卡片。
    *   项目是 "Greenfield" (全新开发)，且你更关注**过程体验**。

*   **When to use Maglev?**
    *   你是一个 Engineering Lead，关注代码质量、可维护性和资产沉淀。
    *   你需要治理 "Brownfield" (存量屎山)，需要强力的**逆向工程**和**规范约束**。
    *   你希望构建一个**长期演进**的系统，而不仅仅是跑完一个 Sprint。

## 4. 融合的可能性 (Synthesis)

Maglev 可以从 BMAD 学习什么？

1.  **交互体验 (UX)**: BMAD 的 `/slash-command` 引导体验非常好。Maglev 目前过于依赖 "手动编辑文件" 或 "Prompt 触发"。
    *   *Action*: 我们已引入 `.agents/workflows/` 和 `/maglev-init`，这正是向 BMAD 学习的一步。
2.  **派对模式 (Party Mode)**: BMAD 的多角色辩论是一个很好的 "Brainstorming" 工具。
    *   *Action*: Maglev 的 `docs/thinking/` 环节可以引入 "Red Team" 角色进行对抗性演练。
3.  **动态适应 (Scale-Adaptive)**: BMAD 根据项目规模裁剪流程。
    *   *Action*: Maglev 已引入 `Complexity Tier` (T1/T2/T3) 来动态调整 Spec 的详细程度。

## 5. 结论 (Conclusion)

**BMAD 是最好的 "AI Agile Coach" (教练)；**
**Maglev 是最好的 "AI Engineering System" (基建)。**

Maglev 不排斥 BMAD。你完全可以在 Maglev 的 `issues/` 目录下运行 BMAD 的 Sprint 流程，但请记住：
**产出的终点不是 User Story，而是 Spec (Truth)。**
