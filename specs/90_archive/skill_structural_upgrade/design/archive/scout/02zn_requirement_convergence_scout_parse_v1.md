# `需求收敛` Scout 需求解析 v1

> 状态：已确认
> 作用：补齐 `requirement-convergence` 在 `skill-scout` 中的 `parse` 产物，使其生成链可追溯为标准 Scout 执行。

## SearchIntent

```yaml
search_intent:
  capability_type: 前段收敛 / 需求澄清
  target_scenario: 在方案设计前完成入口分流、需求定义、Ready Gate 与最小交接
  constraints:
    - 必须服务 Maglev 主流程前段
    - 必须和现状同步、方案设计形成清晰接口
    - 不能重新扩成大而全访谈器
    - 生成对象需符合 Maglev skill 结构
  raw_description: 为 Maglev 补齐前段缺位能力，让模糊任务不再直接滑入方案设计。
  confirmed: true
```

## 当前结论

- 本对象的 Scout 链从这里开始成立。
- 后续正式基线、评估与改造规格见：
  - [02y_requirement_convergence_scout_search_v1.md](02y_requirement_convergence_scout_search_v1.md)
  - [02z_requirement_convergence_scout_evaluation_v1.md](02z_requirement_convergence_scout_evaluation_v1.md)
  - [02za_requirement_convergence_scout_adaptation_spec_v1.md](02za_requirement_convergence_scout_adaptation_spec_v1.md)
