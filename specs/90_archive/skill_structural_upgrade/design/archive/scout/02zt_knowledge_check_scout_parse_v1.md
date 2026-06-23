# `knowledge-check` Scout 需求解析 v1

> 状态：已确认
> 作用：补齐 `knowledge-check` 在 `skill-scout` 中的 `parse` 产物，使其生成链可追溯为标准 Scout 执行。

## SearchIntent

```yaml
search_intent:
  capability_type: 知识沉淀检查 / thinking archive guardrail
  target_scenario: 在高价值探索、会话切换或任务收尾前，检查思考、方案、参考资料与贡献记录是否已沉淀
  constraints:
    - 必须退出“归档需求”语义入口
    - 必须与现实结晶链分离
    - 必须保留检查器而非归档器定位
    - 生成对象需符合 Maglev skill 结构
  raw_description: 为 Maglev 建立正式的知识沉淀检查对象，接管旧归档检查对象在思考沉淀链上的合理部分。
  confirmed: true
```

## 当前结论

- 本对象的 Scout 链从这里开始成立。
- 后续正式基线、评估与改造规格见：
  - [02zh_knowledge_check_scout_search_v1.md](02zh_knowledge_check_scout_search_v1.md)
  - [02zi_knowledge_check_scout_evaluation_v1.md](02zi_knowledge_check_scout_evaluation_v1.md)
  - [02zj_knowledge_check_scout_adaptation_spec_v1.md](02zj_knowledge_check_scout_adaptation_spec_v1.md)
