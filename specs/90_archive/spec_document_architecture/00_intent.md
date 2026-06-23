---
maglev_status: accepted
---

# Intent

## 归档日志

- **结晶状态**：✅ 已完成 → 8 个文件写回运行时能力 + glossary.md 写入 10_reality
- **关键结论**：spec-designer 支持交互文档生成（6 文件 crystallize）、术语表机制（需求内嵌+项目级汇总）、文档互联互验（关系头部+跨系 AC 检查+同步提醒）
- **执行经验**：交互模板设计受益于 context/ 的完整预览，先做预览再实施效率更高
- **时间线**：2026-04-14 启动 → 2026-04-14 归档

## 1. 当前目标

扩展 Maglev 文档体系，使 spec-designer 能为含 UI 的项目生成完整的交互需求和交互设计文档，并建立文档间的互联互验机制。

1. **F-1 交互需求文档结构**：定义 `01_requirements_interaction.md` 模板和生成逻辑
2. **F-2 术语表机制**：需求级 + 项目级术语文件
3. **F-3 文档互联互验**：文档关系声明 + 跨系 AC 审计 + 变更同步提醒

## 2. 这个主题只回答什么

1. 交互需求文档和交互设计文档的模板结构
2. 何时生成、何时不生成交互文档
3. 术语表的放置位置和维护方式
4. 文档关系头部的格式和验证规则
5. spec-designer 和 integrated-validator 需要哪些改动

## 3. 这个主题不回答什么

1. 审批门禁机制 → `main_flow_quality_gates` F-1
2. 结构化 AC 格式 → `main_flow_quality_gates` F-2
3. AC 编号追溯链 → `main_flow_quality_gates` F-3
4. maglev-design-ux 的内部实现 → 只定位其与 spec-designer 的接口
