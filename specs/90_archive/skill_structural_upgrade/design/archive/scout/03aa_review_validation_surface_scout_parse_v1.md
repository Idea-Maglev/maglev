# `review-validation-surface` Scout 需求解析 v1

> 状态：已确认
> 作用：为 `Review / Validation Surface` 补齐标准 `skill-scout` 的 `parse` 产物。

## SearchIntent

```yaml
search_intent:
  capability_type: 质量层 / 结果审查与验证能力面
  target_scenario: 对实现结果进行统一 review 与 validation，发现偏差、风险与不一致
  constraints:
    - 不能继续按前后端碎片 skill 平铺暴露
    - 必须保留实现结果审查与验证的统一入口
    - 必须与 spec 审计、测试设计保持边界
    - 生成对象需符合 Maglev skill 结构
  raw_description: 为 Maglev 质量层补一个统一的 Review / Validation Surface，收口前后端 code review 的碎片入口。
  confirmed: true
```
