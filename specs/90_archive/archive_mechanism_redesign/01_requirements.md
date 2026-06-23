# Requirements: 归档机制重设计

## R1: 结晶与归档流程内置

crystallization skill 在判定 `active_decision: close` 时，必须执行结构化归档步骤，而不是将归档标记为"可选"。

验收标准：
- crystallization workflow 包含 Step 5（归档步骤）
- Step 3 的 `close` 路径显式指向 Step 5
- SKILL.md 的归档说明从"可选"升级为"close 时必选"

## R2: 归档日志模板

每个归档到 90_archive 的 spec 的 README 必须包含结构化归档日志。

模板：

```markdown
## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality 落点链接]
- **关键结论**：[1-3 句写入 reality 的核心内容]
- **执行经验**：[实际执行中的经验/教训]
- **时间线**：YYYY-MM-DD 启动 → YYYY-MM-DD 归档
```

验收标准：
- Step 5 包含上述模板
- 模板字段不可省略（可以填"无特殊经验"但不能留空）

## R3: 归档前门禁

在执行文件搬迁（mv 到 90_archive）前，必须通过以下检查：

1. ✅ 10_reality 有对应更新（结晶已完成）
2. ✅ spec README 已标记 Archived + 已填写归档日志
3. ✅ **90_archive/README.md 索引表已更新**（含结晶状态和关键结论）— 强卡点
4. ✅ 20_evolution/active/README.md 已准备移除条目

验收标准：
- Step 5 中有明确的 4 项检查清单
- 未通过任意一项时，禁止执行搬迁并报告缺失项

## R6: 90_archive/README.md 模板升级

归档索引从纯链接列表升级为结构化表格，包含：结晶状态、关键结论、归档时间。

验收标准：
- 90_archive/README.md 使用新模板
- 每次新归档必须同步更新索引表（作为门禁卡点）
- 存量历史条目标记为"⚠️ 历史条目"（无需回填完整日志）

## R4: active 索引同步

归档完成后，20_evolution/active/README.md 必须同步移除已归档条目。

验收标准：
- Step 5 的最终动作包含 active 索引更新

## R5: 存量归档策略（决策项）

对 90_archive 中已有的 11 个无日志条目的处理方式。

待决定：
- 选项 A：只对新归档生效，存量不回填
- 选项 B：存量条目补填最小日志（结晶状态 + 时间线）
- 选项 C：存量条目补填完整日志
