# `maglev-quick-dev` Scout 私域化改造规格 v1

> 状态：已确认
> 作用：记录 `maglev-quick-dev` 当前阶段的私域化改造规格。

## AdaptationSpec

```yaml
adaptation_spec:
  baseline_skill: GitHub Spec Kit
  baseline_source: https://github.com/github/spec-kit
  object_kind: skill
  customizations:
    feature_trim:
      - 不引入完整 Spec Kit CLI 与命令体系
      - 不把 requirements、plan、tasks 阶段混入本对象
      - 不把综合验证职责混入本对象
    feature_extend:
      - 显式补齐上下文实施的结构定义
      - 显式补齐自检与对抗性审查闭环
      - 显式强调“先达可实施状态，再执行改动”
    naming_convention:
      formal_action_name: 上下文实施
      canonical_skill_name: pending
      current_runtime_name: maglev-quick-dev
    interaction_style: 严格、少修辞、实施导向、强调边界
    integrations:
      - skill_name: requirement-convergence
        relation: 上游
      - skill_name: maglev-create-spec
        relation: 上游
      - skill_name: maglev-cross-validate
        relation: 下游
  created_at: 2026-03-30
```

## 当前结论

- 本轮 Scout 允许继续保留 `maglev-quick-dev` 作为运行面名称
- 同时正式把它的结构动作收口为 `上下文实施`
- 后续如果要推进物理改名，应在新的 Scout/rename 回合中单独完成，不应把本轮口径收口误当成已完成重命名
