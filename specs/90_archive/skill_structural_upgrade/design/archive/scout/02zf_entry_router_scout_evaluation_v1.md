# `entry-router` Scout 评估报告 v1

> 状态：进行中
> 作用：在 `skill-scout` 的 `evaluate` 步骤中，对 `entry-router` 的外部参照进行结构化评估，确认当前最适合作为改造基线的来源。

## 1. 评估范围

本轮评估基于：

- [02ze_entry_router_scout_search_v1.md](02ze_entry_router_scout_search_v1.md)

当前评估对象：

1. `OpenAI Agents SDK: Handoffs`
2. `Anthropic: Routing Pattern`
3. `Awesome AI Agents`

## 2. 评估约束

当前替代对象的稳定约束来自：

- [02w_scout_readiness_packets_v1.md](02w_scout_readiness_packets_v1.md)
- 当前已落地对象：[`../../../../../../.agents/skills/entry-router/SKILL.md`](../../../../../../.agents/skills/entry-router/SKILL.md)

本轮沿用的核心约束是：

- 必须保留会话入口
- 必须保留请求识别
- 必须保留路由与 handoff
- 不再使用全能助手语义
- 不再使用强人格化叙事
- 不吞并主流程能力本体

## 3. 候选评估

### 3.1 OpenAI Agents SDK: Handoffs

来源：

- <https://openai.github.io/openai-agents-python/handoffs/>

关键证据：

- 以 `Triage agent` 接住入口请求
- 明确让 specialist 在 handoff 后接管会话
- 支持 `input_filter`
- 强调 handoff 适合不同 agent 专长清晰分离的场景

#### 能力边界

核心能力：

- 在入口识别请求类型
- 选择目标专长对象
- 显式交接会话
- 控制交接上下文

能力上限：

- 非常适合“入口路由器”
- 特别适合已有一组专长能力的体系

能力局限：

- 它是架构模式，不是现成 Maglev skill
- 不直接提供项目内 Reality 读取规则
- 不直接回答 Maglev 的具体下游选择集

扩展潜力：

- 高

#### 依赖项

外部依赖：

- Agents SDK 的 handoff 概念模型

环境依赖：

- 无强依赖，可被方法化吸收

数据依赖：

- 请求分类信息
- specialist 集合
- handoff 说明

依赖风险：

- `low`

#### 兼容性评估

架构契合度：

- `high`
- 和我们当前对 `Entry / Routing Layer` 的判断高度一致

交互模式兼容性：

- `high`

数据格式兼容性：

- `high`
- 可自然映射到 Maglev 的“请求 -> 路径 -> 交接”结构

与现有对象的关系：

- 对 `entry-router` 的结构定义最直接
- 有助于把入口对象稳定收成“入口路由器”

#### 改造工作量

改造难度：

- `low`

预估步骤数：

- 4 个 step 文件

主要改造点：

1. 加入 Maglev 的下游能力集合
2. 增加与 `现状同步 / 需求收敛 / 方案设计 / 上下文实施 / 综合验证` 的路由规则
3. 明确禁止吞并后续专长对象

预估耗时：

- 约 2 轮对话

#### 当前判断

`OpenAI Agents SDK: Handoffs` 是当前最适合作为替代 skill 改造基线的候选。

### 3.2 Anthropic: Routing Pattern

来源：

- <https://www.anthropic.com/engineering/building-effective-agents>

关键证据：

- routing 先分类输入，再送往 specialized followup task
- 不鼓励单个对象包办全部能力

#### 能力边界

核心能力：

- 输入分类
- specialized followup
- 降低单对象复杂度

能力上限：

- 对结构原则帮助很大

能力局限：

- 不是一个完整可改造 skill
- 不包含 handoff 细节与输入过滤机制

扩展潜力：

- 中高

#### 当前判断

`Anthropic Routing Pattern` 适合作为结构原则辅证，不适合作为主基线。

### 3.3 Awesome AI Agents

来源：

- <https://github.com/e2b-dev/awesome-ai-agents>

#### 当前判断

- 适合作为资源池补充
- 不适合作为当前对象的主基线

## 4. 横向比较

| 维度 | OpenAI Handoffs | Anthropic Routing | Awesome AI Agents |
|---|---|---|---|
| 对入口路由的直接帮助 | 高 | 中高 | 低 |
| 对 handoff 的直接帮助 | 高 | 中 | 低 |
| 对去人格化的帮助 | 高 | 高 | 低 |
| 作为主改造基线的适合度 | 高 | 中 | 低 |

## 5. 基线选择结论

当前选择：

```yaml
adaptation_baseline:
  skill_name: OpenAI Agents SDK Handoffs
  source_url: https://openai.github.io/openai-agents-python/handoffs/
  source_type: official_docs
  evaluation_summary: 适合作为 entry-router 主改造基线，因为它最清楚地定义了 triage、handoff 和 specialist takeover 的边界。
  confirmed: true
```

## 6. 对 Maglev 的直接改造启发

基于当前评估，`entry-router` 后续若继续推进，最值得吸收的是：

1. 入口对象应只负责 triage 与 handoff
2. specialist 一旦清晰，就应接管会话
3. 交接上下文应受控，而不是把一切混进单个入口对象

同时明确不应继续保留的是：

1. 全能助手语义
2. 强人格化叙事
3. 地图优先与建议系统被写成入口对象的唯一人格特征

## 7. 当前结论

本轮 `skill-scout evaluate` 已得到足够稳定的结论：

- `entry-router` 的主改造基线优先选择 `OpenAI Agents SDK: Handoffs`
- `Anthropic Routing Pattern` 作为结构原则辅证
- 当前下一步应进入 `adapt`
