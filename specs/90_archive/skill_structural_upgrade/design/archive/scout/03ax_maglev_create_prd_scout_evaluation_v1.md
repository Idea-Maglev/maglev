# `maglev-create-prd` Scout 评估报告 v1

> 状态：已确认
> 作用：在 `skill-scout` 的 `evaluate` 步骤中，对 `maglev-create-prd` 的保留必要性、吸收方向与边界收口方案给出正式评估结论。

## 1. 输入

- [03av_maglev_create_prd_scout_parse_v1.md](03av_maglev_create_prd_scout_parse_v1.md)
- [03aw_maglev_create_prd_scout_search_v1.md](03aw_maglev_create_prd_scout_search_v1.md)
- [03au_maglev_create_prd_transition_plan_v1.md](../../03au_maglev_create_prd_transition_plan_v1.md)

## 2. 评估目标

本轮评估不直接进入对象生成或物理合并，而是正式回答：

1. `maglev-create-prd` 当前是否仍应保留
2. 它保留的理由是“流程兼容”，还是“目标节点仍需要稳定需求产物”
3. 它后续更适合并入 `requirement-convergence` 还是 `maglev-create-spec`

## 3. 评估约束

本轮沿用的核心约束是：

- 吸收目标必须围绕“抑制前段产物漂移、提升下游可消费性”
- 不能继续让 `maglev-create-prd` 与 `requirement-convergence` 并列成为两个前段一级入口
- 不能并入 `maglev-create-spec`，避免把需求收敛与方案设计重新混在一起
- 不能只因为“团队里有产品经理”就判定保留

## 4. 候选评估

### 4.1 GitHub Spec Kit

来源：

- <https://github.com/github/spec-kit>
- <https://github.github.com/spec-kit/index.html>

#### 能力边界

核心能力：

- 在 implementation 前显式固定 requirements / specification
- 通过多阶段 refinement 让前段产物逐步稳定
- 强调可被后续阶段持续消费的结构化输入

能力上限：

- 很适合作为“为什么前段需要稳定需求产物”的主参考
- 能支持 requirements 与 specification 明确分段

能力局限：

- 它不是 PRD 文档生成对象
- 更偏全流程分阶段方法，而不是单独的需求文档生成节点

#### 当前判断

它最支持的不是“必须保留一个叫 PRD 的 skill”，而是：

- 前段需要稳定 requirements 输入
- 该输入应能被 specification / implementation 持续消费

这支持 `maglev-create-prd` 被吸收到 `requirement-convergence`，作为稳定需求产物输出模式存在。

### 4.2 OpenSpec

来源：

- <https://github.com/Fission-AI/OpenSpec>

#### 能力边界

核心能力：

- 把 proposal、tasks、spec updates 分层维护
- 强调 proposal / change 的显性对齐价值
- 让前段产物不直接滑入设计或实现

能力上限：

- 很适合作为“为什么前段需求产物不应并入 create-spec”的主边界参考

能力局限：

- 它强调的是 proposal/change 对齐，不是 PRD 模板本身
- 不直接提供一个可原样迁移的 PRD skill

#### 当前判断

OpenSpec 最强的支持点是：

- 前段显性产物有必要
- 但这种产物属于前段治理与对齐对象，而不是方案设计对象

这直接支持：

- `maglev-create-prd` 不应并入 `maglev-create-spec`
- 它更应并入 `requirement-convergence`

### 4.3 cc-sdd

来源：

- <https://github.com/gotalab/cc-sdd>

#### 能力边界

核心能力：

- 把 `Requirements -> Design -> Tasks -> Implementation` 明确切开
- 让 requirements 成为后续设计与实施的稳定输入
- 支持评审、审批、团队记忆与可追溯性

能力上限：

- 对“为什么 requirements 不能只停留在松散总结”有很强现实支撑
- 对“需求产物需要可被团队充分消费”有直接帮助

能力局限：

- 同样不是一个 PRD skill 的一比一替代品
- 更像 requirements 阶段的团队实践基线

#### 当前判断

cc-sdd 支持的核心不是“保留 PRD 流程传统”，而是：

- requirements 必须足够稳定
- 否则 design / tasks / implementation 会持续失真

这进一步强化了本轮真正的保留理由：

- 目标节点需要稳定需求产物
- 不是单纯为了兼容产品经理协作

## 5. 综合结论

### 5.1 是否保留

```yaml
retention_decision:
  keep: true
  reason: `maglev-create-prd` 当前仍承接前段“稳定需求产物输出”的真实问题。若直接移除，该问题不会消失，只会重新以口头补充、松散摘要或下游反复追问的形式回流。
```

### 5.2 保留理由是否成立

```yaml
retention_rationale:
  compatibility_only: false
  anti_drift_and_consumability: true
  reason: 保留的核心理由不是“兼容产品经理流程”，而是为了抑制前段产物漂移，并确保下游对象能充分消费需求产物。
```

### 5.3 吸收方向

```yaml
merge_decision:
  target: requirement-convergence
  merge_into_create_spec: false
  reason: `maglev-create-prd` 服务的是前段需求产物稳定化，而不是方案设计本身。并入 `requirement-convergence` 能保持前段边界清晰；并入 `maglev-create-spec` 会重新把需求收敛与方案设计混在一起。
```

### 5.4 对象形态

```yaml
object_shape:
  current_shape: specialized_support_skill
  future_shape: requirement_convergence_output_mode
  immediate_delete: false
```

## 6. 当前结论

- `maglev-create-prd` 现在仍应保留
- 但保留理由已经从“流程兼容”收束为“前段稳定需求产物输出”
- 它后续应并入 `requirement-convergence`
- 不应并入 `maglev-create-spec`
- 当前评估已经足以进入后续 `adapt`
