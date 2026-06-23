# lifecycle_closure_disambiguation

> 生命周期闭环消歧

## 状态

**Archived**

## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality/01_requirements.md §2.10](../../10_reality/01_requirements.md)
- **关键结论**：crystallization 与 knowledge-check 路由消歧完成；归档操作升级为 close 必选步骤（含门禁）；生命周期三层边界形式化
- **执行经验**：本需求的归档操作本身复现了归档反模式（AI 跳过结晶直接搬迁），反向验证了门禁机制的必要性；该事件直接催生了 archive_mechanism_redesign
- **时间线**：2026-04-10 启动 → 2026-04-11 归档

## 概述

解决两个相关问题：

1. **归档反模式**：AI 助手将 `20_evolution` 内容直接搬到 `90_archive`，结论从未进入 `10_reality`
2. **后段技能混淆**：AI 不能区分 `knowledge-check`（检查知识是否已保存）和 `crystallization`（把成果写回现实）

## 文件索引

| 文件 | 内容 |
|------|------|
| [00_intent.md](./00_intent.md) | 目标与边界 |
| [01_requirements.md](./01_requirements.md) | 需求（路由、边界、防护、关系图） |
| [02_design.md](./02_design.md) | 7 处变更的详细设计 |
