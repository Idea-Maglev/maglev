# `spec-audit-surface` Scout 私域化改造规格 v1

> 状态：已确认
> 作用：记录 `Spec Audit Surface` 的第一版私域化改造规格。

## AdaptationSpec

```yaml
adaptation_spec:
  baseline_skill: OpenSpec
  baseline_source: https://github.com/Fission-AI/OpenSpec
  object_kind: skill
  customizations:
    feature_trim:
      - 不复制完整 change lifecycle
      - 不引入 CLI 和固定目录约束
      - 不把 code review 和 test design 混入本对象
    feature_extend:
      - 显式补齐 requirements 审计
      - 显式补齐 spec cluster 审计
      - 显式补齐输入结构检查
      - 显式补齐统一 findings 汇总
      - 与综合验证保持边界
    naming_convention: spec-audit-surface
    interaction_style: 严格、结构化、审查导向、少叙事
    integrations:
      - skill_name: maglev-audit-prd
        relation: 互补
      - skill_name: maglev-audit-spec
        relation: 互补
      - skill_name: maglev-cross-validate
        relation: 互补
  created_at: 2026-03-30
```

## 当前结论

- 当前对象适合直接生成独立 skill。
- 它是质量层三面结构中的第一面正式对象。
