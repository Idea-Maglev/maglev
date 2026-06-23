# archive_mechanism_redesign

> 归档机制重设计 — 结晶与归档分离

## 状态

**Archived**

## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality/01_requirements.md §2.10](../../10_reality/01_requirements.md)（归档为 close 必选步骤的事实已在 lifecycle_closure 结晶时一并写入）
- **关键结论**：crystallization workflow 从 4 步扩展为 5 步；Step 5 含触发条件（仅 close）+ 4 项门禁 + 结构化日志模板；90_archive/README.md 升级为索引表
- **执行经验**：设计中变更 B 的 diff 最初是空操作（frontmatter 未真正修改），风险审查时发现并修复；R5 存量策略选择了最轻量方案（A：只标记历史条目）
- **时间线**：2026-04-11 启动 → 2026-04-11 归档

## 概述

将 crystallization skill 的归档操作从"可选附带"升级为"结构化必选步骤"，解决：
1. 结晶（写现状）和归档（记经验）语义混淆
2. 90_archive 缺少入口门禁和日志结构
3. 归档反模式在实践中反复发生

## 文件索引

| 文件 | 内容 |
|------|------|
| [00_intent.md](./00_intent.md) | 目标与边界 |
| [01_requirements.md](./01_requirements.md) | 需求定义 |
| [02_design.md](./02_design.md) | 变更设计 |

## 关联

- Issue: `issues/active/task_archive_mechanism_redesign.md`
- 讨论记录: `docs/thinking/20_architecture/extension_point_architecture_2026_04_11.md` §6
