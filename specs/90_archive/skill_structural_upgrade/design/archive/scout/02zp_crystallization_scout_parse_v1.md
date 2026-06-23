# `现实结晶` Scout 需求解析 v1

> 状态：已确认
> 作用：补齐 `crystallization` 在 `skill-scout` 中的 `parse` 产物，使其生成链可追溯为标准 Scout 执行。

## SearchIntent

```yaml
search_intent:
  capability_type: 后段闭环 / 现实结晶
  target_scenario: 在综合验证后完成结晶条件确认、Reality 回写判定、active 收口与可发现性回填
  constraints:
    - 必须与知识沉淀检查分离
    - 必须服务 Maglev 主流程后段
    - 必须显式处理 Reality 写回与 active 状态收口
    - 生成对象需符合 Maglev skill 结构
  raw_description: 为 Maglev 补齐综合验证后的状态闭环能力，让已成立结果能稳定沉淀为新的项目现实。
  confirmed: true
```

## 当前结论

- 本对象的 Scout 链从这里开始成立。
- 后续正式基线、评估与改造规格见：
  - [02zb_crystallization_scout_search_v1.md](02zb_crystallization_scout_search_v1.md)
  - [02zc_crystallization_scout_evaluation_v1.md](02zc_crystallization_scout_evaluation_v1.md)
  - [02zd_crystallization_scout_adaptation_spec_v1.md](02zd_crystallization_scout_adaptation_spec_v1.md)
