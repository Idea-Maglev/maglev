# Intent: 归档机制重设计

## 目标

让 crystallization skill 在 active close 时自动执行结构化归档，确保：
- 结论写入 10_reality（结晶）
- 过程经验记入 90_archive（归档）
- 两个动作不可跳过、不可混淆

## 触发事件

2026-04-11 归档 `lifecycle_closure_disambiguation` 时，即使已有归档反模式规则，仍然跳过了经验记录直接执行文件搬迁。已 revert。

证明：文字规则不足以防止错误，需要流程内置的门禁步骤。

## 核心语义

| 动作 | 表达什么 | 落点 |
|------|---------|------|
| 结晶 | 现状（WHAT is true now） | `10_reality` |
| 归档 | 操作方式和经验（HOW it was done） | `90_archive` |

结晶和归档是一个流程中的两件事。结晶是归档的前置条件。

## 范围

**包含**：
- crystallization skill Step 5 新增
- 归档日志模板
- 归档前门禁
- 存量归档条目回填策略

**不包含**：
- 10_reality 内容标准（已有定义）
- 扩展点架构（独立 issue）
- 三文件重叠整理（独立 issue）
