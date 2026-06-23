# skill结构性升级 `现实结晶` / `思考沉淀` 外部对标与 Batch 2 初步结果

> 状态：进行中
> 作用：记录围绕 `现实结晶`、`思考沉淀` 与 `maglev_archival_check` 的第一轮外部对标，并形成 `skill-squadron` Batch 2 的初步巡逻结论。

## 1. 本轮对标目标

本轮只回答三个问题：

1. 行业里如何区分“会话记忆 / 复盘沉淀”和“系统事实更新”
2. 后段闭环更像单点 skill，还是更像 workflow 编排
3. 这些做法是否支持我们当前对 `现实结晶` 与 `思考沉淀` 的拆分

## 2. 参考来源

### A. OpenAI Agents SDK: Session Memory

来源：

- [Memory | OpenAI Agents SDK](https://openai.github.io/openai-agents-python/ref/memory/)

关键信号：

- `Session stores conversation history for a specific session`
- `add_items / get_items / pop_item / clear_session` 这类接口都围绕会话历史展开

当前启发：

- Memory / Session 更像“保存会话上下文”
- 它服务的是上下文连续性
- 它不等于更新系统现状

### B. Atlassian Incident Postmortem

来源：

- [Incident Postmortem Template | Atlassian](https://www.atlassian.com/incident-management/postmortem/templates)

关键信号：

- Postmortem 模板会记录：
  - incident summary
  - leadup
  - impact
  - response
  - recovery
  - timeline
  - root cause
  - lessons learned
- 其中 `Recovery` 和 `incident deemed over` 先定义事件已经恢复
- `postmortem` 再负责记录原因、教训与改进线索

当前启发：

- “事件结束 / 状态恢复” 和 “复盘沉淀” 是相邻但不同的动作
- 复盘文档是经验资产，不是运行现状本身

### C. Anthropic: Prompt Chaining With Gates

来源：

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

关键信号：

- prompt chaining 适合固定步骤
- 中间可加入 `gate`
- workflow 适合结构清晰、步骤可预测的任务

当前启发：

- 后段闭环若能拆成稳定步骤，更适合 workflow
- 不需要为了“有闭环”而立刻新建一个大而全 skill

## 3. 外部模式的共同结论

把这几类外部模式放在一起看，有三个稳定结论：

1. 会话记忆、复盘记录、经验沉淀，与系统事实更新不是同一类对象
2. 先结束状态，再做复盘沉淀，是更常见也更稳定的结构
3. 当后段动作可以被固定拆步时，更适合 workflow + gate，而不是单点大 skill

## 4. 对 Maglev 当前判断的支持

这轮对标整体支持我们之前的两个关键判断：

### A. `思考沉淀` 应独立于 `现实结晶`

支持理由：

- OpenAI 的 session / memory 是上下文连续性对象，不承担现实状态更新
- Atlassian 的 postmortem 负责 lessons learned、root cause、timeline 等沉淀，不等于运行状态本身

因此在 Maglev 里：

- `思考沉淀`
  - 更接近会话资产保全
  - 更接近知识沉淀与复盘
- `现实结晶`
  - 更接近事实状态变更
  - 更接近将新事实写回 `10_reality`

### B. `现实结晶` 更像 workflow 编排

支持理由：

- Anthropic 明确表明，固定子步骤 + gate 更适合 workflow
- 我们当前定义的 `现实结晶` 已经可以被稳定拆成：
  1. 结晶条件确认
  2. 现实回写判定
  3. active 状态收口
  4. 索引与可发现性回填

因此当前不宜急着把它产品化成一个新 skill。

## 5. 对 `maglev_archival_check` 的进一步修正

这轮对标也进一步支持：

`maglev_archival_check` 的核心价值仍然存在，但它更偏：

- 会话资产保全
- 思考沉淀质量门
- 复盘前的知识完整性检查

而不是：

- Reality 回写器
- active 收口器
- 需求生命周期结束器

这意味着：

- 它更像 `思考归档触发链` 上的检查对象
- 而不应继续默认占据“需求归档”语义入口

## 6. Batch 2 初步巡逻结果

基于当前内外部材料，`skill-squadron` 的 `Batch 2: 生命周期后段闭环批次` 可以先给出这版结果：

### 结论 1

`思考沉淀` 与 `现实结晶` 必须继续保持拆分，不能重新合并成一个“归档”大词。

### 结论 2

`maglev_archival_check` 继续保留能力，但只应被理解为：

- `思考归档触发链` 上的知识沉淀检查对象

### 结论 3

`现实结晶` 当前仍应保持 `Workflow-first`。

### 结论 4

`现实结晶` 的稳定接口不在“归档”这个词，而在：

1. 新事实是否成立
2. 是否应写回 `10_reality`
3. active 是否应结束或拆分
4. 是否需要可发现性回填

### 结论 5

后续如果进入第二轮专项外部对标，优先级应转向：

1. `质量层收口`
2. `整体接入`
3. `现状表达`

## 7. 当前结论

这轮对标对当前主线最重要的帮助，不是提供了某个现成同名对象，而是进一步确认了：

- `思考沉淀` 是知识资产链
- `现实结晶` 是事实状态链
- 两者生命周期不同
- 后段闭环更适合 workflow + gate，而不是单点大 skill
