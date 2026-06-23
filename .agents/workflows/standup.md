---
description: 现状同步与会话启动 (Use reality-sync skill)
metadata:
  formal_action_name: 现状同步
  object_kind: workflow
  author: Maglev contributors
  last_updated: 2026-03-30
---
# Standup Workflow

在每次会话开始或感觉上下文失真时，启动 `现状同步（reality-sync）`。

目标：
- 识别当前主线
- 识别当前风险
- 识别下一步动作
- 进入正确工作模式

执行方式：
1. 启动 `现状同步（reality-sync）` 技能。
2. 输出一份包含 `Space / Mind / Risk / Action / Mode` 的会话简报。
3. 基于简报继续进入分析、实现、验证或发版工作。

兼容说明：

- workflow 文件名仍保留为 `standup.md`
- `/standup` 继续作为兼容入口存在
