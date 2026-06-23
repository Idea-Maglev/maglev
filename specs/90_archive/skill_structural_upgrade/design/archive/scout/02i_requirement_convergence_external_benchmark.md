# skill结构性升级 `需求收敛` 外部对标与 Batch 1 巡逻结果

> 状态：进行中
> 作用：记录围绕 `需求收敛` 的第一轮外部对标，并将结论回收为 `skill-squadron` 的 Batch 1 巡逻结果。

## 1. 本轮对标目标

本轮不是泛搜“有没有相似 skill”，而是只回答三个问题：

1. 行业内更成熟的做法，如何承接前段 `需求收敛`
2. 这类能力更像单点 skill，还是更像 workflow / routing / gate
3. 这些做法是否修正当前 Maglev 的骨架判断

## 2. 参考来源

### A. Anthropic: Building Effective Agents

来源：

- [Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents/)

关键信号：

- 优先使用简单、可组合的模式，而不是一开始就上复杂框架
- `Routing` 用于先分类输入，再导向更合适的后续处理
- `Prompt chaining` 适合固定子步骤，中间可加入 `gate`
- workflow 更适合可预测、结构清晰的任务；agent 更适合开放任务

### B. OpenAI Agents SDK

来源：

- [Quickstart | OpenAI Agents SDK](https://openai.github.io/openai-agents-js/guides/quickstart/)
- [InputGuardrail | OpenAI Agents SDK](https://openai.github.io/openai-agents-js/openai/agents/interfaces/inputguardrail/)

关键信号：

- `handoffs` 用于在多个 agent 之间进行编排与转交
- `input guardrail` 是正式结构对象，用于在入口处先检查输入
- guardrail 可以并行执行，也可以阻塞后续 agent

### C. LangChain / LangGraph Router Pattern

来源：

- [Build a multi-source knowledge base with routing](https://docs.langchain.com/oss/javascript/langchain/multi-agent/router-knowledge-base)

关键信号：

- router pattern 的核心是：先分类输入，再把请求导向专门对象
- 当需要显式路由逻辑、专门预处理、或显式控制并行时，router 比“让大 agent 自己决定”更合适
- router 的结果不是最终能力本体，而是把请求送入更合适的下游结构

### D. Atlassian Definition of Ready

来源：

- [What is Definition of Ready | Atlassian](https://www.atlassian.com/agile/project-management/definition-of-ready)

关键信号：

- 在真正开始工作前，需要一套 ready criteria
- 重点不是写更多文档，而是确保工作已经“可执行、清晰、可行”
- `Independent / Negotiable / Valuable / Estimable / Small / Testable` 这组标准，本质上是一种进入实施前的质量门

## 3. 外部模式的共同结论

把这几类成熟做法放在一起看，当前有三个稳定共识：

1. 前段能力通常不会被做成一个“大而全的 spec skill”
2. 更常见的结构是：
   - 入口分流 / 路由
   - 前置澄清或预处理
   - ready gate
   - 再进入下游主能力
3. 越靠近前段，越需要显式判断“能不能进入下一阶段”，而不是默认一路滑进设计或实施

## 4. 对 `需求收敛` 的直接修正

基于本轮对标，当前对 `需求收敛` 的结构理解进一步收敛为：

`需求收敛` 不是一个新的“大前段总 skill”，而更像一个前段能力簇，内部至少包含两类稳定结构：

1. `入口分流`
   - 判断输入到底是什么类型的问题
   - 判断应该进入哪条下游主线
   - 必要时做最小预处理

2. `Ready Gate`
   - 判断当前输入是否已经足够进入 `方案设计`
   - 如果不够，明确缺的不是“更多 spec”，而是哪些前置信息

这比我们之前的表达更进一步。

之前我们写的是：

- `入口收敛`
- `需求定义`

现在外部对标给出的修正是：

- `入口收敛` 更接近 `入口分流`
- `需求定义` 之后还应明确存在一个 `Ready Gate`

也就是说，`需求收敛` 更合理的最小结构应变成：

1. `入口分流`
2. `需求定义`
3. `Ready Gate`

## 5. 对当前主流程的影响

当前主流程更适合写成：

`现状同步 -> 需求收敛 -> 方案设计 -> 上下文实施 -> 综合验证`

但其中 `需求收敛` 现在不应再被理解成一个黑箱步骤，而应明确为：

- 先判断请求是什么
- 再把它定义清楚
- 再判断是否已经 ready

也就是：

`现状同步 -> 入口分流 -> 需求定义 -> Ready Gate -> 方案设计`

## 6. 对 skill 形态的结论

本轮外部对标后，当前更明确不建议：

1. 立刻新建一个大而全的 `需求收敛` skill
2. 继续让 `maglev-create-spec` 前置访谈隐式吞掉这段能力
3. 只做“入口聊天”，但没有进入 `方案设计` 前的 ready 判断

当前更推荐：

1. 保持 `需求收敛` 为显性顶层能力
2. 短期继续 `Workflow-first`
3. workflow 内部显式拆成：
   - `入口分流`
   - `需求定义`
   - `Ready Gate`
4. 等输入输出长期稳定后，再评估是否产品化成独立显性对象

## 7. Batch 1 巡逻结果

基于当前内外部材料，`skill-squadron` 的 `Batch 1: 前段缺口批次` 可以先给出这版结果：

### 结论 1

`需求收敛` 仍然是当前最关键的显性能力缺口，这个判断不变。

### 结论 2

`需求收敛` 暂不宜直接 skill 化，继续采用 `Workflow-first`。

### 结论 3

`需求收敛` 的最小结构应升级为：

1. `入口分流`
2. `需求定义`
3. `Ready Gate`

### 结论 4

`需求收敛` 和 `方案设计` 的接口应由 `Ready Gate` 固定，而不是靠会话感觉决定。

### 结论 5

如果后续要做第二轮外部对标，优先级应转向：

1. `现实结晶`
2. `思考沉淀`
3. `质量层收口`

## 8. 当前结论

这轮对标对当前主线的帮助，不在于“找到了现成同名 skill”，而在于确认了：

- `需求收敛` 的方向是对的
- 但它更像前段 workflow 能力簇
- 其内部应显式加入 `Ready Gate`
- 当前不应急于把它产品化成一个新 skill 名称
