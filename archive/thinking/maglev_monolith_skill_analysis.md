---
type: thinking
status: done
author: AI Agent
topic: maglev_monolith_skill_analysis
---

# Analysis: Should we encapsulate Maglev into a single "God Skill"?

## 1. Context
用户提问：*"有必要将当前整个 Maglev 项目封装成一个 Skill 么？"*
这代表了一种对 **"极致易用性"** 的追求——用户希望有一个 "Maglev Agent"，只要安装了它，就拥有了 Maglev 的一切智慧和能力。

## 2. Dialectic (辩证思考)

### Thesis (正方：应该封装)
- **Unified Interface**: 用户不需要知道有 `reverse_engineer` 还是 `structure_thinking`。只有一个入口 `All in One`。
- **Portability**: 只要复制一个 `SKILL.md`，整个 Maglev 方法论就带走了。
- **Context Awareness**: 可以在同一个 Session 里既做逆向，又做架构设计，上下文连贯。

### Antithesis (反方：绝对不行)
- **Token Explosion (上下文爆炸)**: Maglev 目前包含几十个文档 (.md)，如果把这些全部塞进 Skill 的 System Prompt，Context Window 会瞬间耗尽（即使是 200k/1m 模型，也会导致注意力分散）。
- **Maintenance Nightmare (维护地狱)**: 文档在 `solutions/` 下更新了，Skill 里还要再 copy 一遍？这是 "Single Source of Truth" 的死敌。
- **Hallucination Risk (幻觉风险)**: "God Skill" 往往指令模糊。给 AI 太多且杂的指令（既要懂流程，又要懂架构，又要懂代码），AI 容易在执行时混淆优先级。
- **Separation of Concerns**: 知识 (Data) 和 能力 (Logic) 应该分离。Skill 是 Logic，Docs 是 Data。

## 3. Synthesis (综合结论)

**结论：不要做 "God Skill" (全知全能的大单体)，要做 "Gateway Skill" (路由网关)。**

我们目前的架构其实已经是一个 **"Router + Plugins"** 的微服务架构：

1.  **The Librarian (Router)**: `.agents/skills/consult_maglev_guide`
    - 它不记背所有文档。
    - 它只知道“什么问题该去查哪个文档”。
    - **这就是“封装”的最佳形态**：它封装了索引，而不是封装内容。

2.  **The Workers (Plugins)**: `solutions/skills/*`
    - `reverse_engineer`: 专精逆向。
    - `contribute_methodology`: 专精文档构建。
    - 它们是原子化的工具，按需加载。

## 4. Recommendation

不要试图物理上把所有 Markdown 合并到一个 Prompt 里。
相反，应该强化 **`consult_maglev_guide`** 的路由能力，把它变成 **"Maglev OS"** 的 Kernel。

当用户问 "Maglev 怎么帮我重构？" 时：
1.  Kernel 识别意图。
2.  Kernel 建议："这需要用到 `reverse_engineer` 技能，建议你加载它。" (或者如果 IDE 支持，自动 invoke sub-agent)。

**Action Item**:
- 保持现状。文档 (Data) 留在 `solutions/`，技能 (Logic) 留在 `skills/`。
- 通过 `consult_maglev_guide` 作为统一入口来索引它们。
