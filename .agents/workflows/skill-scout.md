---
description: 发现、引入、改造与巡逻优化能力对象 (Use skill-scout skill)
metadata:
  formal_action_name: 技能侦察
  top_level_capability: 能力进化
  object_kind: workflow
  lifecycle_chain: governance_loop
  author: Maglev contributors
  last_updated: 2026-03-30
---
# Skill Scout Workflow

在以下场景中，优先进入 `skill-scout`：

- 需要一个当前仓库还没有的能力对象
- 需要参考外部高相似度对象来生成或改写现有对象
- 需要对已登记到项目级治理对象清单中的对象做 Patrol 优化
- 需要把新对象注册到 `.agents/private-catalog.yaml`

当前边界：

- `skill-scout` 不只处理 `skill`
- `skill-scout` 现在同时包含侦察、改造、生成与登记能力
- 当目标对象适合独立 skill 化时：
  - 走 `Scout -> Adapt -> Generate Skill -> Register`
- 当目标对象应保持 `workflow-first` 时：
  - 走 `Scout -> Adapt -> Workflow -> Register`

关键输入：

- `.agents/private-catalog.yaml`
- `skill-sources.yaml`
- `references/source-registry.yaml`

推荐触发方式：

1. 新对象发现与改造
   > "请启动 `skill-scout`，我要引入一个新的能力对象。"
2. 已有对象巡逻优化
   > "请启动 `skill-scout` 的 patrol 模式，检查当前对象是否有更成熟做法。"

当前注意事项：

- 进入真正的 skill 撰写或重写时，优先通过 `skill-scout`
- 不需要再额外寻找独立 Forge 对象；生成能力已经内并到 `skill-scout`
- 若对象当前被判定为 `workflow-first`，不要强行生成独立 skill
