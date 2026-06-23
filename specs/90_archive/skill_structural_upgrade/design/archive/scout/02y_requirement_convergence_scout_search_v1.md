# skill结构性升级 `需求收敛` Scout 搜索结果 v1

> 状态：进行中
> 作用：记录 `需求收敛` 进入 `skill-scout` 机制后的第一轮正式搜索结果。

## 1. SearchIntent

基于当前准备包，本轮确认后的 SearchIntent 为：

```yaml
search_intent:
  capability_type: 前段需求收敛 / requirements clarification workflow
  target_scenario: 在方案设计前，对任务入口做分流、需求定义与 ready gate 判断
  constraints:
    - 不做成大而全前段总 skill
    - 需要保留入口分流
    - 需要保留需求定义
    - 需要保留 Ready Gate
    - 不能继续被 create-spec 吞并
  raw_description: 为 Maglev 补齐需求收敛这一显性能力缺口，寻找更成熟的前段 workflow / skill 组织方式
  confirmed: true
```

## 2. Effective Sources

本轮按 `skill-scout` 机制，优先走私有资源池：

### 来源层级

- 内置层：`.agents/skills/skill-scout/references/source-registry.yaml`
- 用户层：`skill-sources.yaml`
- 偏好层：`.agents/skills/skill-scout/references/user-source-preferences.yaml`

### 场景映射

当前主题映射到：

- `spec_driven_development`

### 第一优先级 Effective Sources

1. `GitHub Spec Kit`
2. `OpenSpec`
3. `cc-sdd`

## 3. 候选列表

### #1 OpenSpec

- 来源：<https://github.com/Fission-AI/OpenSpec>
- 能力摘要：
  - 明确把当前真相与变更提案分开
  - 用 proposal / tasks / spec updates 承接从意图到实施的中段链路
  - 强调先对 change 达成一致，再进入实现
- 匹配度：`0.90`
- 适配难度：`medium`
- 标签：
  - `spec-driven`
  - `change-proposal`
  - `brownfield-friendly`
  - `pre-implementation-alignment`

判断：

- 对 `需求收敛` 的直接价值最高
- 尤其适合作为：
  - “先把变更说清”
  - “再进入方案设计”
  的前置参考

### #2 cc-sdd

- 来源：<https://github.com/gotalab/cc-sdd>
- 能力摘要：
  - 强化 `requirements -> design -> tasks -> implementation`
  - 提供 steering 与 validation 机制
  - 明确把 requirements 阶段固定出来
- 匹配度：`0.86`
- 适配难度：`medium`
- 标签：
  - `requirements-first`
  - `design-gate`
  - `task-breakdown`
  - `project-memory`

判断：

- 对 `Ready Gate` 和阶段切分有直接参考价值
- 更像完整方法链中的前段标准化器

### #3 GitHub Spec Kit

- 来源：<https://github.com/github/spec-kit>
- 能力摘要：
  - 强调 Spec-Driven Development
  - 关注 product scenarios 与 predictable outcomes
  - 对前段需求收束和 guardrails 有启发
- 匹配度：`0.82`
- 适配难度：`low`
- 标签：
  - `spec-driven`
  - `guardrails`
  - `predictable-outcomes`
  - `greenfield-friendly`

判断：

- 适合作为结构理念与 guardrail 的补充参照
- 但对“前段缺口对象化”本身的直接支持略弱于 OpenSpec 和 cc-sdd

## 4. 当前排序结论

本轮候选当前排序为：

1. `OpenSpec`
2. `cc-sdd`
3. `GitHub Spec Kit`

## 5. 对 `需求收敛` 的直接启发

本轮正式 Scout 搜索进一步支持：

1. `需求收敛` 不应继续被 `create-spec` 吞并
2. 它更像“进入方案设计前的显式前段能力”
3. 它当前继续 `Workflow-first` 是合理的
4. 它后续若 skill 化，也应更偏：
   - 分流
   - 定义
   - gate
   而不是大而全对话器

## 6. 当前结论

这次搜索已经满足：

- 有明确 SearchIntent
- 有私有资源池优先的 Effective Sources
- 有结构化候选列表

因此从当前阶段起，`需求收敛` 已经不再只是“内部讨论对象”，而是正式进入了 `skill-scout` 的可继续评估阶段。
