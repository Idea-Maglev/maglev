# `test-design-surface` Scout 私域化改造规格 v1

> 状态：已确认
> 作用：记录 `Test Design Surface` 的第一版私域化改造规格。

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
      - 不把 spec 审计和结果 review 混入本对象
    feature_extend:
      - 显式补齐测试对象识别
      - 显式补齐覆盖策略设计
      - 显式补齐测试层次建议
      - 显式补齐验证支撑产物建议
      - 与综合验证保持汇聚点边界
    naming_convention: test-design-surface
    interaction_style: 严格、结构化、测试设计导向、少叙事
    integrations:
      - skill_name: maglev-plan-unit-tests-backend
        relation: 互补
      - skill_name: maglev-plan-unit-tests-frontend
        relation: 互补
      - skill_name: maglev-create-test-cases
        relation: 互补
      - skill_name: maglev-cross-validate
        relation: 互补
  created_at: 2026-03-30
```

## 当前结论

- 当前对象适合直接生成独立 skill。
- 它是质量层三面结构中的第三面正式对象。
