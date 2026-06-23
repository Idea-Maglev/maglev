# `knowledge-check` Scout 搜索结果 v1

> 状态：进行中
> 作用：记录 `knowledge-check` 进入 `skill-scout` 机制后的第一轮正式搜索结果。

## 1. SearchIntent

基于当前准备包，本轮确认后的 SearchIntent 为：

```yaml
search_intent:
  capability_type: knowledge capture / session closeout / reflection archive skill
  target_scenario: 在高价值探索、会话切换或任务收尾时，检查思考、方案、参考资料和贡献记录是否已经沉淀
  constraints:
    - 不占用需求归档语义入口
    - 不承担 reality writeback
    - 不承担 active closeout
    - 必须保留 thinking 检查
    - 必须保留 solution 检查
    - 必须保留 references / archive 检查
    - 必须保留 contribution log 检查
  raw_description: 为 knowledge-check 寻找更准确的知识沉淀检查对象模型，对齐更稳定的知识沉淀检查结构
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

1. `OpenAI Agents SDK: Session Memory`
2. `Atlassian Incident Postmortem`
3. `Anthropic: Building Effective Agents`

## 3. 候选列表

### #1 Atlassian Incident Postmortem

- 来源：<https://www.atlassian.com/incident-management/postmortem/templates>
- 能力摘要：
  - 在事件恢复后，整理 timeline、root cause、lessons learned、follow-up actions
  - 复盘文档承担经验沉淀，不承担状态恢复本身
- 匹配度：`0.89`
- 适配难度：`medium`
- 标签：
  - `postmortem`
  - `knowledge-capture`
  - `lessons-learned`
  - `closeout-after-state`

判断：

- 对“知识沉淀检查”最有启发
- 尤其支持把“状态结束”和“经验沉淀”明确分开

### #2 OpenAI Agents SDK: Session Memory

- 来源：<https://openai.github.io/openai-agents-python/ref/memory/>
- 能力摘要：
  - session 保存会话历史
  - 关注上下文连续性和会话资产保留
- 匹配度：`0.82`
- 适配难度：`low`
- 标签：
  - `session-memory`
  - `context-preservation`
  - `conversation-history`

判断：

- 对“思考资产保全”有直接帮助
- 但它更像存储模型，不是审查 skill 本体

### #3 Anthropic: Prompt Chaining With Gates

- 来源：<https://www.anthropic.com/engineering/building-effective-agents>
- 能力摘要：
  - 适合把固定检查动作做成 workflow + gate
- 匹配度：`0.76`
- 适配难度：`low`
- 标签：
  - `workflow-gate`
  - `predictable-checks`

判断：

- 支持把知识沉淀检查做成明确 gate
- 适合作为结构原则辅证

## 4. 私有资源池结论

本轮先走私有资源池后，得到的结论是：

1. 私有资源池更适合提供泛化 skill / infra 视野
2. 对 `knowledge-check` 这种“知识沉淀检查”对象，最强结构基线仍然来自第二层官方/成熟方法来源

因此本轮允许：

- 私有资源池先完成范围校正
- 官方来源作为主结构基线

## 5. 当前排序结论

本轮候选当前排序为：

1. `Atlassian Incident Postmortem`
2. `OpenAI Agents SDK: Session Memory`
3. `Anthropic: Prompt Chaining With Gates`

## 6. 对改写对象的直接启发

本轮正式 Scout 搜索进一步支持：

1. `knowledge-check` 应围绕知识沉淀检查
2. 它应发生在：
   - 高价值探索后
   - 会话切换前
   - 任务收尾前
3. 它不应再默认代表：
   - 需求归档
   - reality writeback
   - active 收口

## 7. 当前结论

这次搜索已经满足：

- 有明确 SearchIntent
- 有私有资源池优先的 Effective Sources
- 有结构化候选列表

因此从当前阶段起，`knowledge-check` 已正式进入 `skill-scout` 的可继续评估阶段。
