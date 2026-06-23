# `现实结晶` Scout 评估报告 v1

> 状态：进行中
> 作用：在 `skill-scout` 的 `evaluate` 步骤中，对 `现实结晶` 的高相似度候选进行结构化评估，确认当前最适合作为改造基线的外部参照。

## 1. 评估范围

本轮评估基于上一轮搜索结果：

- [02zb_crystallization_scout_search_v1.md](02zb_crystallization_scout_search_v1.md)

当前评估对象：

1. `OpenSpec`
2. `GitHub Spec Kit`
3. `cc-sdd`

第二层校正来源：

1. `Atlassian Incident Postmortem`
2. `Anthropic Building Effective Agents`

## 2. 评估约束

当前 `现实结晶` 的稳定约束来自：

- [02w_scout_readiness_packets_v1.md](02w_scout_readiness_packets_v1.md)
- [03c_crystallization_workflow.md](../plan/03c_crystallization_workflow.md)

本轮沿用的核心约束是：

- 必须保留 `结晶条件确认`
- 必须保留 `现实回写判定`
- 必须保留 `active 状态收口`
- 必须保留 `索引与可发现性回填`
- 不得与 `思考沉淀` 混成一个归档大词
- 不得被 `maglev_archival_check` 吞并
- 不得直接做成单点大 skill

## 3. 候选评估

### 3.1 OpenSpec

来源：

- <https://github.com/Fission-AI/OpenSpec>

关键证据：

- 明确区分 source-of-truth specs 与 changes
- 工作流显式包含 `Archive & Update Specs`
- 明确要求在完成实现后再 archive completed change
- archive 后将批准变化回写到长期 specs

#### 能力边界

核心能力：

- 把已完成变更合并回长期事实
- 让活动 change 在后段完成收口
- 明确“当前变化”和“长期真相”之间的转换动作

能力上限：

- 非常适合“已完成变化的事实回写”
- 对 brownfield 和持续演进场景尤其友好

能力局限：

- 它的 archive 同时带有 specs 更新语义，不等于 Maglev 的完整 reality 体系
- 不直接处理 `思考沉淀`
- 不直接覆盖 `map-maker / librarian` 式的可发现性回填

扩展潜力：

- 高
- 可直接映射到 `现实回写判定 + active 收口`

#### 依赖项

外部依赖：

- `openspec` CLI
- 约定式 change / specs 目录结构

环境依赖：

- 偏 CLI 与目录驱动

数据依赖：

- proposal、tasks、spec deltas、archive 命令

依赖风险：

- `medium`

#### 兼容性评估

架构契合度：

- `medium`

交互模式兼容性：

- `high`

数据格式兼容性：

- `medium`
- 需要映射到 Maglev 的 `10_reality` / `20_evolution/active`

与现有对象的关系：

- 对 `现实结晶` 直接有帮助
- 同时支持我们把它继续保持为 `workflow-first`

#### 改造工作量

改造难度：

- `medium`

预估步骤数：

- 3 到 4 个 workflow 步骤

主要改造点：

1. 把 archive 语义拆成 Maglev 的 `现实回写判定 + active 收口`
2. 明确把 `思考沉淀` 排除在该对象外
3. 补齐 `索引与可发现性回填`

预估耗时：

- 约 2 到 3 轮对话

#### 当前判断

`OpenSpec` 是当前最适合作为 `现实结晶` 改造基线的候选。

### 3.2 GitHub Spec Kit

来源：

- <https://github.com/github/spec-kit>

关键证据：

- 强调可预测结果与规范化 phases
- 强调 plan/tasks/implement 的清晰阶段分离

#### 能力边界

核心能力：

- 为 spec-driven 提供统一过程纪律
- 对 gate 与阶段完整性有补充作用

能力上限：

- 适合做 guardrail 和流程完整性补充

能力局限：

- 不直接提供 reality writeback 模型
- 不直接回答 active closeout 与 discoverability backfill

扩展潜力：

- `medium`

#### 依赖项

外部依赖：

- `specify` CLI

环境依赖：

- 偏工具链和规范模板

数据依赖：

- requirements、plan、tasks 等规范文档

依赖风险：

- `low`

#### 兼容性评估

架构契合度：

- `medium`

交互模式兼容性：

- `medium`

数据格式兼容性：

- `medium`

与现有对象的关系：

- 更适合作为 workflow gate 和规范纪律补充

#### 改造工作量

改造难度：

- `low`

预估步骤数：

- 1 到 2 个 workflow 步骤

主要改造点：

1. 只吸收其阶段纪律
2. 不把它误用为 `现实结晶` 的主模型

预估耗时：

- 约 1 到 2 轮对话

#### 当前判断

`GitHub Spec Kit` 适合作为辅助参照，不适合作为主改造基线。

### 3.3 cc-sdd

来源：

- <https://github.com/gotalab/cc-sdd>

关键证据：

- 强调完整 phase 结构
- 强调 steering 与 project memory

#### 能力边界

核心能力：

- 对阶段纪律有帮助
- 对 memory 与规范稳定性有帮助

能力上限：

- 适合作为完整方法链中的结构参照

能力局限：

- 对 `现实结晶` 本体帮助弱
- 不直接给出 reality writeback 模型

扩展潜力：

- `medium`

#### 兼容性评估

架构契合度：

- `medium`

交互模式兼容性：

- `medium`

数据格式兼容性：

- `medium`

与现有对象的关系：

- 更像整体方法链的辅证，不是本对象的主基线

#### 当前判断

`cc-sdd` 当前只适合作为低优先级辅助参照。

## 4. 第二层校正结论

### A. Atlassian Incident Postmortem

支持结论：

- 先完成状态恢复，再做 postmortem 沉淀
- 支持 `现实结晶` 与 `思考沉淀` 保持拆分

### B. Anthropic Building Effective Agents

支持结论：

- 固定可预测步骤 + gate 更适合 workflow
- 支持 `现实结晶` 继续保持 `workflow-first`

## 5. 横向比较

| 维度 | OpenSpec | GitHub Spec Kit | cc-sdd |
|---|---|---|---|
| 对 reality writeback 的直接帮助 | 高 | 低 | 低 |
| 对 active closeout 的帮助 | 高 | 低 | 低 |
| 对 workflow gate 的帮助 | 中高 | 中 | 中 |
| 对与思考沉淀分离的支持 | 高 | 中 | 中 |
| 作为主基线的适合度 | 高 | 中低 | 低 |

## 6. 基线选择结论

当前选择：

```yaml
adaptation_baseline:
  skill_name: OpenSpec
  source_url: https://github.com/Fission-AI/OpenSpec
  source_type: github
  evaluation_summary: 适合作为现实结晶的主改造基线，因为它最清楚地表达了“已完成变化如何回写长期事实并结束活动 change”的后段逻辑。
  confirmed: true
```

## 7. 对 Maglev 的直接改造启发

基于当前评估，`现实结晶` 后续若继续推进，最值得吸收的是：

1. 已完成变化与长期事实之间必须有显式转换动作
2. 后段闭环应有稳定 gate，而不是模糊收尾
3. active 对象结束与长期事实更新应成对出现

同时明确不应直接照搬的是：

1. 不把 `OpenSpec archive` 直接等同于 Maglev 全部结晶动作
2. 不把 postmortem / memory 逻辑混入该对象
3. 不把其直接产品化为单点大 skill

## 8. 当前结论

本轮 `skill-scout evaluate` 已得到足够稳定的中间结论：

- `现实结晶` 的主改造基线优先选择 `OpenSpec`
- `GitHub Spec Kit` 作为流程纪律补充
- `cc-sdd` 作为低优先级辅证

因此下一步若继续进入 `skill-scout`，应进入：

- `adapt`

但当前仍应优先将其维持为 `workflow-first`。
