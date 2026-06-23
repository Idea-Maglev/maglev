# `entry-router` Scout 搜索结果 v1

> 状态：进行中
> 作用：记录 `entry-router` 进入 `skill-scout` 机制后的第一轮正式搜索结果。

## 1. SearchIntent

基于当前准备包，本轮确认后的 SearchIntent 为：

```yaml
search_intent:
  capability_type: entry routing / triage / handoff skill
  target_scenario: 在会话入口识别请求类型、判断下游路径，并把请求交接给最合适的 Maglev 能力
  constraints:
    - 不再使用全能助手语义
    - 不再使用强人格化叙事
    - 不吞并主流程能力本体
    - 必须保留请求识别
    - 必须保留路由与 handoff
    - 必须能与现状同步、需求收敛、方案设计等对象形成清晰接口
  raw_description: 为 entry-router 寻找更成熟的入口路由技能模型，对齐更稳定的 triage、route 与 handoff 结构
  confirmed: true
```

## 2. Effective Sources

本轮按 `skill-scout` 机制，优先走私有资源池。

### 来源层级

- 内置层：`.agents/skills/skill-scout/references/source-registry.yaml`
- 用户层：`skill-sources.yaml`
- 偏好层：`.agents/skills/skill-scout/references/user-source-preferences.yaml`

### 场景映射

当前主题更接近：

- `general_agent_infrastructure`

### 第一优先级 Effective Sources

1. `SkillHub`
2. `ClawHub`
3. `Awesome AI Agents`

### 第二层校正来源

1. `OpenAI Agents SDK: Handoffs`
2. `Anthropic: Building Effective Agents`

## 3. 候选列表

### #1 OpenAI Agents SDK: Handoffs

- 来源：<https://openai.github.io/openai-agents-python/handoffs/>
- 能力摘要：
  - 明确用 `Triage agent` 接住入口请求
  - 通过 `handoffs` 将会话交给后续专长对象
  - 支持 `input_filter` 调整交接上下文
- 匹配度：`0.93`
- 适配难度：`low`
- 标签：
  - `triage-agent`
  - `handoff`
  - `entry-routing`
  - `conversation-takeover`

判断：

- 对 `entry-router` 的直接参考价值最高
- 尤其适合作为：
  - “入口识别”
  - “明确交接”
  - “不吞并后续专长能力”
  的主基线

### #2 Anthropic: Routing Pattern

- 来源：<https://www.anthropic.com/engineering/building-effective-agents>
- 能力摘要：
  - 把 routing 定义为“先分类，再交给专长后续任务”
  - 强调 specialized tasks
  - 不鼓励单对象大包大揽
- 匹配度：`0.87`
- 适配难度：`low`
- 标签：
  - `routing`
  - `specialized-followup`
  - `modular-agents`
  - `workflow-gate`

判断：

- 对 `entry-router` 的结构边界很有帮助
- 更像架构原则辅证，而不是可直接改造的完整 skill

### #3 Awesome AI Agents

- 来源：<https://github.com/e2b-dev/awesome-ai-agents>
- 能力摘要：
  - 提供多种 agent / router / orchestration 资源索引
  - 更适合作为横向视野补充
- 匹配度：`0.62`
- 适配难度：`medium`
- 标签：
  - `catalog`
  - `agent-infra`
  - `router-patterns`

判断：

- 更适合作为资源池，不适合作为本对象主基线

## 4. 私有资源池结论

本轮先走私有资源池后，得到两个结论：

1. 私有资源池里有足够强的“路由 / agent infra”方向来源
2. 但对 `entry-router` 这种“入口路由 skill 本体”而言，最直接、最可执行的结构参照仍来自第二层官方来源

因此本轮允许：

- 私有资源池先完成范围校正
- 官方来源作为主结构基线

## 5. 当前排序结论

本轮候选当前排序为：

1. `OpenAI Agents SDK: Handoffs`
2. `Anthropic: Routing Pattern`
3. `Awesome AI Agents`

## 6. 对替代对象的直接启发

本轮正式 Scout 搜索进一步支持：

1. `entry-router` 应该是明确的入口路由器
2. 它的核心职责是：
   - 请求识别
   - 路径选择
   - handoff
3. 它不应再承担：
   - 全能助手人格
   - 主流程能力本体
   - 大而全解释器

## 7. 当前结论

这次搜索已经满足：

- 有明确 SearchIntent
- 有私有资源池优先的 Effective Sources
- 有结构化候选列表

因此从当前阶段起，`entry-router` 已正式进入 `skill-scout` 的可继续评估阶段。
