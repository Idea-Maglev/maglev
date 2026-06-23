# `entry-router` Scout 需求解析 v1

> 状态：已确认
> 作用：补齐 `entry-router` 在 `skill-scout` 中的 `parse` 产物，使其生成链可追溯为标准 Scout 执行。

## SearchIntent

```yaml
search_intent:
  capability_type: 入口路由 / handoff
  target_scenario: 在会话入口识别请求类型、判断下游路径并交接给最合适的 Maglev 能力
  constraints:
    - 必须退出旧入口对象的抽象比喻语义
    - 必须低人格化、结构优先
    - 必须与主流程对象形成清晰 handoff
    - 生成对象需符合 Maglev skill 结构
  raw_description: 为 Maglev 建立新的正式入口路由对象，替代旧入口对象造成的语义混乱。
  confirmed: true
```

## 当前结论

- 本对象的 Scout 链从这里开始成立。
- 后续正式基线、评估与改造规格见：
  - [02ze_entry_router_scout_search_v1.md](02ze_entry_router_scout_search_v1.md)
  - [02zf_entry_router_scout_evaluation_v1.md](02zf_entry_router_scout_evaluation_v1.md)
  - [02zg_entry_router_scout_adaptation_spec_v1.md](02zg_entry_router_scout_adaptation_spec_v1.md)
