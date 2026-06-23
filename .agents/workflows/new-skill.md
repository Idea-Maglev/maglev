---
description: 创建新能力对象 (Use skill-scout skill)
metadata:
  formal_action_name: 新能力对象创建入口
  top_level_capability: 能力进化
  object_kind: workflow
  lifecycle_chain: governance_loop
  author: Maglev contributors
  last_updated: 2026-03-30
---
# New Skill Workflow

1. 呼叫技能:
   > "请启动 `skill-scout`，我要生成一个新的能力对象。"
2. 生成约束:
   - `SKILL.md` 顶层 frontmatter 仅使用标准字段：`name`、`description`
   - 自定义治理字段统一写入 `metadata`
   - 默认补充：
     - `metadata.author`（优先取当前 git 账号）
     - `metadata.last_updated`（当前日期）
