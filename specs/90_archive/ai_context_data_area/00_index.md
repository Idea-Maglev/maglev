# AI 上下文数据区 — Spec 索引

| 字段 | 值 |
|------|-----|
| slug | ai_context_data_area |
| 标题 | AI 上下文数据区（context/ 目录约定扩展） |
| 状态 | ✅ Archived |
| 创建日期 | 2026-04-21 |
| 归档日期 | 2026-04-22 |
| 触发来源 | modelconfig v2.15 归档审查反模式 |

## 文件清单

| 文件 | 说明 |
|------|------|
| `00_intent.md` | 意图与问题陈述 |
| `01_requirements.md` | 4 FR / 10 AC |
| `02_design.md` | 技术设计（5 决策 + 4 变更） |
| `context/input_facts.md` | 输入事实基准 |

## 归档日志

- **结晶状态**：✅ 已完成 → 无需 10_reality 回写（变更直接在 canonical 位置完成：`collaboration.md` §3、`specs_lifecycle.md` §2、`step-01-split-files.md`）
- **关键结论**：标准化 `context/` 为 AI 上下文数据区，与 `ref/`（外部引用）严格区分；`input_facts.md` 必需，其余可选；禁止 backup/ 和个人命名空间
- **执行经验**：方案设计应在第一时间落盘到项目，不应只存在于对话中。对抗性审查发现的路径不一致（连字符 vs 下划线）和遗漏更新（README 计数、thinking 索引）在文档类变更中是高频问题
- **时间线**：2026-04-21 启动 → 2026-04-22 归档
