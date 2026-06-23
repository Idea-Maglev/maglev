# `entry-router` Scout 注册部署 v1

> 状态：已完成
> 作用：补齐 `entry-router` 在 `skill-scout` 中的 `register` 产物，记录其正式部署与治理登记结果。

## Registration Input

```yaml
registration_input:
  object_name: entry-router
  object_kind: skill
  object_path: .agents/skills/entry-router/
  capability_summary: 在会话入口完成 triage、route 与 handoff，避免入口对象继续吞并主流程能力
  adaptation_spec_ref: design/02zg_entry_router_scout_adaptation_spec_v1.md
```

## 文件结构校验

已确认以下文件存在并形成完整 step 链：

- `.agents/skills/entry-router/SKILL.md`
- `.agents/skills/entry-router/references/entry-router.workflow.md`
- `.agents/skills/entry-router/references/step-01-scan-entry.md`
- `.agents/skills/entry-router/references/step-02-assess-context.md`
- `.agents/skills/entry-router/references/step-03-select-route.md`
- `.agents/skills/entry-router/references/step-04-handoff.md`

## Catalog 登记结果

```yaml
private_catalog_entry:
  name: entry-router
  path: .agents/skills/entry-router/
  formal_action_name: 入口路由
  top_level_capability: 需求收敛
  object_kind: skill
  source_url: https://openai.github.io/openai-agents-python/handoffs/
  adaptation_date: "2026-03-30"
  version: "1.0.0"
  status: active
```

## 当前结论

- `entry-router` 已完成标准 Scout 链中的 `register`。
- 它是当前运行面的正式入口 skill，不再只是概念替代物。
