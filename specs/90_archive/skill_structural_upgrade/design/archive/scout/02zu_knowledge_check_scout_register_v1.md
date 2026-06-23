# `knowledge-check` Scout 注册部署 v1

> 状态：已完成
> 作用：补齐 `knowledge-check` 在 `skill-scout` 中的 `register` 产物，记录其正式部署与治理登记结果。

## Registration Input

```yaml
registration_input:
  object_name: knowledge-check
  object_kind: skill
  object_path: .agents/skills/knowledge-check/
  capability_summary: 在高价值探索、会话切换或任务收尾前执行知识沉淀检查，避免思考资产流失
  adaptation_spec_ref: design/02zj_knowledge_check_scout_adaptation_spec_v1.md
```

## 文件结构校验

已确认以下文件存在并形成完整 step 链：

- `.agents/skills/knowledge-check/SKILL.md`
- `.agents/skills/knowledge-check/references/knowledge-check.workflow.md`
- `.agents/skills/knowledge-check/references/step-01-scan-assets.md`
- `.agents/skills/knowledge-check/references/step-02-audit-records.md`
- `.agents/skills/knowledge-check/references/step-03-check-boundaries.md`
- `.agents/skills/knowledge-check/references/step-04-report-gaps.md`

## Catalog 登记结果

```yaml
private_catalog_entry:
  name: knowledge-check
  path: .agents/skills/knowledge-check/
  formal_action_name: 知识沉淀检查
  top_level_capability: 思考沉淀
  object_kind: skill
  source_url: https://www.atlassian.com/incident-management/postmortem/templates
  adaptation_date: "2026-03-30"
  version: "1.0.0"
  status: active
```

## 当前结论

- `knowledge-check` 已完成标准 Scout 链中的 `register`。
- 它是当前运行面的正式知识沉淀检查 skill。
