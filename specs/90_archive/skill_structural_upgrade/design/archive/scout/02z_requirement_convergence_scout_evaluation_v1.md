# `需求收敛` Scout 评估报告 v1

> 状态：进行中
> 作用：在 `skill-scout` 的 `evaluate` 步骤中，对 `需求收敛` 的高相似度候选进行结构化评估，确认当前最适合作为改造基线的外部参照。

## 1. 评估范围

本轮评估基于上一轮搜索结果：

- [02y_requirement_convergence_scout_search_v1.md](02y_requirement_convergence_scout_search_v1.md)

当前评估对象：

1. `OpenSpec`
2. `cc-sdd`
3. `GitHub Spec Kit`

本轮不直接进入 skill 撰写，也不进入 `adapt`。  
目标只是回答：

- 谁最适合作为 `需求收敛` 的外部改造基线
- 哪些结构值得吸收
- 哪些结构不能直接照搬到 Maglev

## 2. 评估约束

当前 `需求收敛` 的稳定约束来自：

- [02w_scout_readiness_packets_v1.md](02w_scout_readiness_packets_v1.md)
- [03e_requirement_convergence_workflow.md](../plan/03e_requirement_convergence_workflow.md)

本轮沿用的核心约束是：

- 必须保留 `入口分流`
- 必须保留 `需求定义`
- 必须保留 `Ready Gate`
- 必须和 `方案设计` 保持清晰接口
- 不得继续被 `create-spec` 吞并
- 不得做成大而全前段总 skill

## 3. 候选评估

### 3.1 OpenSpec

来源：

- <https://github.com/Fission-AI/OpenSpec>

关键证据：

- 明确区分 `openspec/specs/` 与 `openspec/changes/`
- 强调在写代码前先对 change 达成一致
- 变更目录中显式维护 `proposal.md`、`tasks.md`、`spec` 更新
- 工作流显式包含：
  - Draft Change Proposal
  - Review & Align
  - Implement Tasks
  - Archive & Update Specs

#### 能力边界

核心能力：

- 把“当前事实”和“提议中的变更”分开
- 在实现前先形成 change proposal
- 通过 review/alignment 固定变更边界
- 通过 archive 把批准后的变化回写到长期规范

能力上限：

- 非常适合“已有系统上的变更收敛”
- 对 brownfield 和跨 spec 变更尤其友好

能力局限：

- 它更像完整变更工作流，不是单独的前段需求收敛器
- 对“入口分流”的强调不强
- `Ready Gate` 不是被单独显式命名的对象

扩展潜力：

- 高
- 两层状态模型与 proposal-first 结构可以很容易迁移到 Maglev 前段

#### 依赖项

外部依赖：

- `openspec` CLI
- 约定式目录结构与 agent 指令集

环境依赖：

- 偏 Node/CLI 驱动

数据依赖：

- proposal、tasks、spec deltas 等结构化变更文件

依赖风险：

- `medium`
- 有工具与目录约束，但方法本身不依赖特定闭源服务

#### 兼容性评估

架构契合度：

- `medium`
- 它不是 `SKILL.md + workflow + step` 结构，但工作流边界非常清晰

交互模式兼容性：

- `high`
- 非常适合作为 Maglev 的前段 workflow 参考

数据格式兼容性：

- `medium`
- 需要映射到 Maglev 的 `intent / requirements / spec` 文件簇

与现有对象的关系：

- 对 `需求收敛` 和 `现实结晶` 都有直接启发
- 能帮助 `create-spec` 退出前段吞并位置

#### 改造工作量

改造难度：

- `medium`

预估步骤数：

- 2 到 3 个 workflow 步骤

主要改造点：

1. 把 proposal / review-and-align 映射到 `入口分流 + 需求定义`
2. 把“达成一致后再进入实现”收成 Maglev 的 `Ready Gate`
3. 避免把 OpenSpec 的完整 change workflow 整体复制进来

预估耗时：

- 约 2 到 3 轮对话

#### 当前判断

`OpenSpec` 是当前最适合作为 `需求收敛` 改造基线的候选。  
原因不是它直接提供了一个同名 skill，而是它最清楚地回答了：

- 为什么前段必须先锁定 change
- 为什么设计前必须先完成对齐
- 为什么这件事不应再被实现对象吞并

### 3.2 cc-sdd

来源：

- <https://github.com/gotalab/cc-sdd>

关键证据：

- 显式强调 `Requirements -> Design -> Tasks -> Implementation`
- 强调 steering、project memory、统一 workflow
- 目标是把 AI coding agent 拉入可审批的 spec-driven 路径

#### 能力边界

核心能力：

- 把 requirements 阶段单独固定出来
- 把 design、tasks、implementation 链路清楚分开
- 通过 steering 和 memory 维持项目一致性

能力上限：

- 对“阶段切分”和“前段显性化”有直接帮助
- 对 team-level approval 和 task decomposition 特别有价值

能力局限：

- 更偏完整 AI-DLC 方法链
- 对“入口分流”支持弱于 OpenSpec
- Ready Gate 的表达更多是过程氛围，不是独立对象

扩展潜力：

- 高
- 可作为 `需求定义` 与后续 `方案设计` 接口约束的重要参照

#### 依赖项

外部依赖：

- 一组 agent/workflow 命令模板

环境依赖：

- 偏多 agent / 多工具协同场景

数据依赖：

- requirements、design、tasks、project memory 等结构对象

依赖风险：

- `medium`
- 方法兼容性好，但整体链路较重

#### 兼容性评估

架构契合度：

- `medium`

交互模式兼容性：

- `high`

数据格式兼容性：

- `high`
- 和 Maglev 现有 `requirements / design / active spec` 语义接近

与现有对象的关系：

- 对 `需求收敛 -> 方案设计` 的阶段接口价值很高
- 对 `现状表达` 和 `project memory` 的关系也有补充启发

#### 改造工作量

改造难度：

- `medium`

预估步骤数：

- 2 到 3 个 workflow 步骤

主要改造点：

1. 把 requirements-first 的优势提取出来
2. 去掉其完整 AI-DLC 重流程部分
3. 补足 Maglev 特有的 `入口分流` 与 `Ready Gate`

预估耗时：

- 约 2 到 3 轮对话

#### 当前判断

`cc-sdd` 是当前第二优先级参考。  
它不是最佳基线，但非常适合作为 `需求定义` 和阶段切分的辅助约束来源。

### 3.3 GitHub Spec Kit

来源：

- <https://github.com/github/spec-kit>

关键证据：

- 强调 `Spec-Driven Development`
- 强调 `product scenarios` 和 `predictable outcomes`
- 强调 requirements / design / tasks 的规范化

#### 能力边界

核心能力：

- 为 spec-driven 开发提供统一骨架
- 强调规范产物与可预测结果
- 对 guardrails 和标准化流程有帮助

能力上限：

- 对 greenfield / 0→1 和规范化设计很强

能力局限：

- 对 brownfield 变更收敛不如 OpenSpec 直接
- 对 `需求收敛` 的对象化启发较弱
- 不能直接回答 Maglev 的 `入口分流 + Ready Gate` 缺口

扩展潜力：

- `medium`

#### 依赖项

外部依赖：

- `specify` CLI

环境依赖：

- 偏 CLI 初始化与规范工具链

数据依赖：

- 一组标准 spec-driven 文档与模板

依赖风险：

- `low`
- 开放且结构清晰

#### 兼容性评估

架构契合度：

- `medium`

交互模式兼容性：

- `medium`

数据格式兼容性：

- `medium`

与现有对象的关系：

- 更适合作为 `方案设计` 和 guardrail 语义的补充参照
- 对 `需求收敛` 本身帮助次于前两者

#### 改造工作量

改造难度：

- `low`

预估步骤数：

- 1 到 2 个 workflow 步骤

主要改造点：

1. 只吸收其规范化与 guardrail 思路
2. 不把它误当成前段收敛对象模板

预估耗时：

- 约 1 到 2 轮对话

#### 当前判断

`GitHub Spec Kit` 适合作为补充参照，不适合作为 `需求收敛` 的主改造基线。

## 4. 横向比较

| 维度 | OpenSpec | cc-sdd | GitHub Spec Kit |
|---|---|---|---|
| 对前段收敛的直接帮助 | 高 | 中高 | 中 |
| 对 `入口分流` 的帮助 | 中 | 低 | 低 |
| 对 `需求定义` 的帮助 | 高 | 高 | 中 |
| 对 `Ready Gate` 的帮助 | 中高 | 中 | 低 |
| 对 brownfield / 变更场景适配 | 高 | 中 | 中低 |
| 被整体方法链吞没的风险 | 中 | 中高 | 中 |
| 作为主基线的适合度 | 高 | 中高 | 中低 |

## 5. 基线选择结论

当前选择：

```yaml
adaptation_baseline:
  skill_name: OpenSpec
  source_url: https://github.com/Fission-AI/OpenSpec
  source_type: github
  evaluation_summary: 适合作为需求收敛的主改造基线，因为它最清楚地区分了当前事实与变更提案，并把“先对齐再进入实现”的前段逻辑做成了稳定结构。
  confirmed: false
```

这里刻意保持 `confirmed: false`。  
原因不是评估不够，而是当前还停在结构升级主线内，尚未正式切到 `step-04-adapt`。

## 6. 对 Maglev 的直接改造启发

基于当前评估，`需求收敛` 后续若继续推进，最值得吸收的是：

1. 先固定“当前事实 / 当前任务入口 / 本轮变更意图”之间的边界
2. 在 `方案设计` 前显式设置 `Ready Gate`
3. 把前段对象保持为小而清晰的 workflow，而不是大而全对话器

同时明确不应直接照搬的是：

1. 不把 OpenSpec 的整套 change 目录照搬为 Maglev 前段 skill
2. 不把 cc-sdd 的完整 AI-DLC 重流程整体移植
3. 不把 Spec Kit 的规范工具链误用为前段能力本体

## 7. 当前结论

本轮 `skill-scout evaluate` 已经得到一个足够稳定的中间结论：

- `需求收敛` 的主改造基线优先选择 `OpenSpec`
- `cc-sdd` 作为 requirements-first 的辅助参照
- `GitHub Spec Kit` 作为规范化与 guardrail 的补充参照

因此下一步若继续进入 `skill-scout`，应进入：

- `adapt`

但在当前主线里，仍应先把这个结论作为结构资产沉淀，而不是立刻写 skill。
