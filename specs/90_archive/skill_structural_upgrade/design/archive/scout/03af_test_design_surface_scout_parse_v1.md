# `test-design-surface` Scout 需求解析 v1

> 状态：已确认
> 作用：为 `Test Design Surface` 补齐标准 `skill-scout` 的 `parse` 产物。

## SearchIntent

```yaml
search_intent:
  capability_type: 质量层 / 测试设计能力面
  target_scenario: 对 requirements、spec 与实现结果形成统一测试设计、覆盖策略与验证支撑
  constraints:
    - 不能继续以测试规划与测试用例 skill 碎片平铺暴露
    - 必须保留测试对象识别、覆盖策略与产物建议三类职责
    - 必须与 spec 审计、review 与验证保持边界
    - 生成对象需符合 Maglev skill 结构
  raw_description: 为 Maglev 质量层补一个统一的 Test Design Surface，收口单测规划与测试用例生成的碎片入口。
  confirmed: true
```
