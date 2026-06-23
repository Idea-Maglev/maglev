# `maglev-create-spec` Scout 私域化改造规格 v1

> 状态：已确认
> 作用：记录 `maglev-create-spec` 当前阶段的私域化改造规格。

## AdaptationSpec

```yaml
adaptation_spec:
  baseline_skill: OpenSpec
  baseline_source: https://github.com/Fission-AI/OpenSpec
  object_kind: skill
  customizations:
    feature_trim:
      - 不引入完整 OpenSpec CLI 与命令体系
      - 不把需求收敛职责混入本对象
      - 不把上下文实施与综合验证职责混入本对象
    feature_extend:
      - 显式补齐方案设计的结构定义
      - 显式补齐设计前提追问与设计边界收束
      - 显式强调“先达可设计状态，再起草与落盘”
    naming_convention:
      formal_action_name: 方案设计
      canonical_skill_name: pending
      current_runtime_name: maglev-create-spec
    interaction_style: 严格、少修辞、设计导向、强调边界
    integrations:
      - skill_name: requirement-convergence
        relation: 上游
      - skill_name: maglev-quick-dev
        relation: 下游
      - skill_name: maglev-cross-validate
        relation: 下游
  created_at: 2026-03-30
```

## 当前结论

- 本轮 Scout 允许继续保留 `maglev-create-spec` 作为运行面名称
- 同时正式把它的结构动作收口为 `方案设计`
- 后续如果要推进物理改名，应在新的 Scout/rename 回合中单独完成，不应把本轮口径收口误当成已完成重命名
