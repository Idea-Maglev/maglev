---
name: human-readable-output
description: Maglev 人类可读输出契约与确定性完整性检查。
metadata:
  formal_action_name: 人类可读输出
  top_level_capability: 治理强制
  system_layer: Foundation Layer
  lifecycle_chain: governance_loop
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-09-08
  version: "1.0.0"
---

# 人类可读输出

本内部能力提供 Maglev 跨技能共享的人类可读输出契约。

## 职责

- 规定人类可见沟通和非代码审阅产物的最低不变量；
- 将机器来源与 Markdown 人类审阅面绑定；
- 对确定性完整性问题输出阻断或建议；
- 明确检查器不判断语义质量、不生成正文、不改写产物。

## 不负责

- 不判断读者目标是否达成；
- 不判断事实是否充分或是否过度推断；
- 不规定标题、章节、篇幅、页面数量或操作双路径；
- 不替代产物洁净度守护的会话痕迹检查；
- 不自动修复人类文档。

## 规则与工具

- 规则单一权威：`contract.md`；
- 检查器：`scripts/check_human_output.py`；
- 机器来源需要人类判断时，使用 `.maglev/temp/human-review/<run-id>/` 下的 Markdown 人审面；
- `status: pass` 只表示机械完整性通过，不表示语义通过或人类接受。
