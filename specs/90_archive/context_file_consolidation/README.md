# context_file_consolidation

> AI 上下文文件整合 + 项目治理原则定位

## 状态

**Archived**

## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality/01_requirements.md §2.11](../../10_reality/01_requirements.md)
- **关键结论**：AI 上下文从三文件整合为两文件（AGENTS.md + llms.txt）；core_rules.md 12 条规则经逐条核查后退役；不需要单独的"项目宪法"文件
- **执行经验**：原始设计假设"8 条独有规则可原样搬运"，现状核查发现全部过时或已被覆盖，最终只提炼出 3 条新原则；V1 断链检查发现 30+ 残余引用分布在 docs/guides 和 legacy workflow 中，属于更大范围的清理
- **时间线**：2026-04-11 启动 → 2026-04-11 归档

## 概述

整理 AGENTS.md / llms.txt / core_rules.md 三文件约 40% 内容重叠问题，将 core_rules.md 独有的 8 条规则归位，并确定"项目治理原则"（类似 SpecKit constitution）的正式位置。

## 文件索引

| 文件 | 内容 |
|------|------|
| [00_intent.md](./00_intent.md) | 目标与边界 |
| [01_requirements.md](./01_requirements.md) | 需求定义 |

## 关联

- Issue: `issues/active/task_extension_point_architecture.md`（关联发现章节）
- 讨论记录: `docs/thinking/20_architecture/extension_point_architecture_2026_04_11.md` §5
