# skill结构性升级 `体系级能力簇` 外部对标与 Batch 6 初步结果

> 状态：进行中
> 作用：记录围绕 `整体接入`、`现状表达`、`能力进化` 的第一轮外部对标，并形成 `skill-squadron` Batch 6 的初步巡逻结论。

## 1. 本轮对标目标

本轮只回答三个问题：

1. 行业里体系级能力更常被做成单点对象，还是能力簇
2. `整体接入`、`现状表达`、`能力进化` 这三类能力是否适合继续采用协作承接
3. 这些做法是否支持我们当前“不急着硬收成单 skill”的判断

## 2. 参考来源

### A. Anthropic: Building Effective Agents

来源：

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

关键信号：

- 最成功的实现更偏“简单、可组合的模式”
- routing、prompt chaining、orchestrator-workers 都是组合式结构
- 复杂任务更适合由多个角色协同，而不是一个单对象包办

当前启发：

- 体系级能力天然跨边界
- 更适合协作承接，而不是单点总 skill

### B. OpenAI Agents SDK: Sessions

来源：

- [Sessions | OpenAI Agents SDK](https://openai.github.io/openai-agents-js/guides/sessions/)

关键信号：

- session 提供的是持久记忆层
- runner 自动取回历史、追加新输入输出、维持后续可继续运行

当前启发：

- 长期上下文通常被做成底层持续能力
- 它更像基础能力层，而不是用户显性主技能

### C. OpenAI Agents SDK: Context Management

来源：

- [Context management | OpenAI Agents SDK](https://openai.github.io/openai-agents-js/guides/context)

关键信号：

- context 被明确拆成：
  - local context
  - agent/LLM context
- 不同类型的上下文属于不同层次的结构对象

当前启发：

- `现状表达` 不应继续和 `现状同步` 混写
- 长期 Reality / Context 更像底层支撑层

## 3. 外部模式的共同结论

把这些外部模式放在一起看，当前有三个稳定结论：

1. 体系级能力往往天然跨多个结构对象，不适合轻易压成单点 skill
2. 长期上下文、持久记忆、共享状态，更适合底层持续能力，而不是用户显性主流程对象
3. 能力进化与整体接入这类问题，更接近“协作编排”而不是“单对象包办”

## 4. 对 Maglev 当前判断的支持

这轮对标整体支持我们之前的三个关键判断：

### A. `整体接入` 继续保持能力簇理解

支持理由：

- 体系接入天然涉及初始化、存量识别、逆向补齐、索引回填等多个动作
- 这类问题与 orchestrator-workers / routing 的协作模式更一致

因此当前更适合保持：

- `maglev-bootstrapper`
- `maglev-legacy-adopter`
- `maglev-reverse-spec`

作为接入能力簇的协作承接对象。

### B. `现状表达` 继续保持底层长期能力理解

支持理由：

- OpenAI 的 sessions / context management 都强调长期上下文与运行时上下文的区分
- 这和我们对：
  - `现状同步`
  - `现状表达`
  的拆分方向一致

因此当前更适合保持：

- `10_reality`
- `maglev-map-maker`
- `maglev-librarian`

作为 `现状表达` 的协作承接簇。

### C. `能力进化` 继续保持治理能力簇理解

支持理由：

- 能力发现、批量分析、技能孵化，本身就是不同阶段的治理动作
- 更像协作闭环，而不是单一技能角色

因此当前更适合保持：

- `skill-scout`
- `skill-squadron`
- `skill-scout`
- `skill-squadron`

作为 `能力进化` 的协作承接簇。

## 5. 对当前结构的进一步修正

这轮对标后，当前更明确不建议：

1. 把 `整体接入` 强行收成一个“总接入 skill”
2. 把 `现状表达` 误理解成用户主流程入口
3. 把 `能力进化` 收成一个包办发现、孵化、治理的单 skill

当前更推荐：

1. 继续保留体系级能力显性存在
2. 对象层继续采用协作承接
3. 重点治理这些能力簇内部的接口和协调性，而不是先做单点收口

## 6. Batch 6 初步巡逻结果

基于当前内外部材料，`skill-squadron` 的 `Batch 6: 体系级能力簇稳定性批次` 可以先给出这版结果：

### 结论 1

`整体接入`、`现状表达`、`能力进化` 当前继续保持“能力层显性、对象层协作承接”的结构最稳。

### 结论 2

`Keep` 判断当前成立，不建议为了“简洁”而过早把这些簇压成单点对象。

### 结论 3

`Batch 6` 后续重点不应是改名或裁撤，而应是：

1. 检查能力簇内部边界
2. 检查对象之间 handoff 是否清楚
3. 检查修辞表达是否继续压过结构职责

## 7. 当前结论

这轮对标进一步确认了：

- 体系级能力簇更适合协作承接
- `现状表达` 应保持底层长期能力定位
- `整体接入` 与 `能力进化` 都不宜急于总 skill 化
- 当前 `Batch 6` 的主任务是稳边界、稳接口、稳协作，而不是强行收口
