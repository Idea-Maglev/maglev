# `现实结晶` Scout 搜索结果 v1

> 状态：进行中
> 作用：记录 `现实结晶` 进入 `skill-scout` 机制后的第一轮正式搜索结果。

## 1. SearchIntent

基于当前准备包，本轮确认后的 SearchIntent 为：

```yaml
search_intent:
  capability_type: 后段闭环 / crystallization workflow
  target_scenario: 在综合验证之后，对已成立变化执行 reality writeback、active 收口与可发现性回填
  constraints:
    - 不与思考沉淀混成一个归档大词
    - 不被 maglev_archival_check 吞并
    - 不直接做成单点大 skill
    - 必须保留 reality writeback
    - 必须保留 active closeout
    - 必须保留 discoverability backfill
  raw_description: 为 Maglev 补齐综合验证后的后段闭环，寻找更成熟的 crystallization / closeout workflow 组织方式
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

1. `OpenSpec`
2. `cc-sdd`
3. `GitHub Spec Kit`

### 第二层校正来源

1. `Atlassian Incident Postmortem`
2. `Anthropic Building Effective Agents`

## 3. 候选列表

### #1 OpenSpec

- 来源：<https://github.com/Fission-AI/OpenSpec>
- 能力摘要：
  - 明确区分当前事实与变更提案
  - 通过 `archive` 把已完成 change 合并回 source-of-truth specs
  - 强调“先完成实现，再 archive completed change”
- 匹配度：`0.92`
- 适配难度：`medium`
- 标签：
  - `spec-driven`
  - `archive-and-update-specs`
  - `state-finalization`
  - `brownfield-friendly`

判断：

- 对 `现实结晶` 的直接参考价值最高
- 尤其适合作为：
  - “已完成变化如何回写长期事实”
  - “后段闭环如何作为固定 workflow”
  的主基线

### #2 GitHub Spec Kit

- 来源：<https://github.com/github/spec-kit>
- 能力摘要：
  - 强调 `requirements -> plan -> tasks -> implement`
  - 强调规范化与可预测结果
  - 对后段 closeout 本身支持较弱，但对前后段 guardrails 有帮助
- 匹配度：`0.74`
- 适配难度：`low`
- 标签：
  - `spec-driven`
  - `guardrails`
  - `predictable-outcomes`
  - `implementation-closure`

判断：

- 更适合作为流程规范化和 gate 设计的补充参照
- 对 `现实结晶` 本身的直接启发弱于 OpenSpec

### #3 cc-sdd

- 来源：<https://github.com/gotalab/cc-sdd>
- 能力摘要：
  - 强调 `requirements -> design -> tasks -> implementation`
  - 有 steering 和 project memory
  - 更擅长前中段，不直接覆盖 reality writeback
- 匹配度：`0.68`
- 适配难度：`medium`
- 标签：
  - `requirements-first`
  - `project-memory`
  - `phase-structure`
  - `team-alignment`

判断：

- 可作为“阶段收口纪律”辅助参照
- 但不是 `现实结晶` 的主参照来源

## 4. 第二层校正来源启发

### A. Atlassian Incident Postmortem

- 来源：<https://www.atlassian.com/incident-management/postmortem/templates>
- 启发：
  - 先有 `Recovery`
  - 再有 `Lessons learned / Corrective actions`

支持结论：

- 状态恢复与经验沉淀是相邻但不同动作
- 支持 `现实结晶` 与 `思考沉淀` 继续保持拆分

### B. Anthropic: Prompt Chaining With Gates

- 来源：<https://www.anthropic.com/engineering/building-effective-agents>
- 启发：
  - 固定可拆步骤更适合 workflow
  - 中间可设置 gate

支持结论：

- `现实结晶` 更适合固定 steps + gate 的 workflow 形态

## 5. 当前排序结论

本轮候选当前排序为：

1. `OpenSpec`
2. `GitHub Spec Kit`
3. `cc-sdd`

## 6. 对 `现实结晶` 的直接启发

本轮正式 Scout 搜索进一步支持：

1. `现实结晶` 更像后段固定 workflow，而不是单点大 skill
2. 它必须显式包含“已成立变化写回长期事实”的动作
3. 它必须与 `思考沉淀` 继续保持拆分
4. 它需要 gate，而不只是“做完后顺手归档”

## 7. 当前结论

这次搜索已经满足：

- 有明确 SearchIntent
- 有私有资源池优先的 Effective Sources
- 有结构化候选列表

因此从当前阶段起，`现实结晶` 已正式进入 `skill-scout` 的可继续评估阶段。
