# Docs 位段分类启发式（60_case vs 70_retrospective）

> **Created**: 2026-04-25
> **Status**: active
> **Segment**: 70_retrospective
> **Context**: Phase 3 重组 thinking/ 时，需要把 36 个未分类文件/目录按位段语义归位

---

## 1. 问题

`docs/thinking/` 重组到位段时，多数文件文件名只有"主题 + 日期"信息，没有显式语义标签。靠人工逐个判读太慢，需要一组**纯文件名级别**的判定规则，能快速做出 80% 准确的初分类。

## 2. 适用范围

仅适用于"已知该模块的位段语义、需要把无标签文件批量归位"的场景。**不替代内容审阅**——这是一个加速器，不是免责声明。

## 3. 60_case vs 70_retrospective 判定规则

### 3.1 关键词触发表

| 关键词 | 候选位段 | 信号强度 |
|--------|---------|---------|
| `_retrospective`, `_closeout`, `_reflection`, `_antipattern` | **70_retrospective** | 强（直接命中） |
| `_lifecycle_management`, `_dogfooding`, `_on_*`（自指）| 70_retrospective | 中（元反思） |
| `improvement_prioritization`, `_lessons` | 70_retrospective | 中 |
| `_rollout`, `_fix`, `_cleanup`, `_refactor`, `_audit`, `_research` | **60_case** | 强（具体动作） |
| `_plan`, `_strategy`, `_test_plan`, `_mapping` | 60_case | 中（前瞻规划） |
| `_definition`, `_reconstruction`, `_repair_plan` | 60_case | 弱（看具体内容） |

### 3.2 时间标签辅助

- 文件名带日期后缀（`*_YYYY_MM_DD.md` 或 `YYYY-MM-DD-*.md`）→ 倾向 **60_case**（具体迭代场景）
- 不带日期的抽象主题文档 → 倾向 70_retrospective 或 30_philosophy

### 3.3 决策核心问题

> **"这份文档是事后回看，还是事中/事前留痕？"**

- 回看 / 提炼 / 反思 / 经验 → 70
- 留痕 / 计划 / 执行 / 研究 → 60

## 4. 已知歧义点

某些组合会让规则失效，必须人工裁决：

| 文件名 | 歧义 | 本次决定 |
|--------|------|---------|
| `maglev_dogfooding_plan.md` | "plan" 是前瞻信号，但 dogfooding 是元反思 | 70（元反思优先） |
| `maglev_reality_definition.md` | "definition" 偏哲学，但内容是具体定义动作 | 60（动作优先） |
| `consolidation_task.md` | 信息量极少 | 60（默认归动作） |
| `maglev_root_reconstruction.md` | "reconstruction" 是动作但内涵偏范式 | 60（动作优先） |

**经验**：当强信号关键词冲突时，按"反思优先"判（70）。这与"先把案例位段保持纯净"的目标对齐。

## 5. 命中率（本次实测）

- 36 个文件/目录靠规则初分：30 项强匹配 + 6 项弱匹配
- 用户复审后**全部接受**初分类（无回退）
- 弱匹配项后续可能需要内容复审

## 6. 不适用场景

- 跨模块（不同 docs/ 子树有不同位段语义，规则不通用）
- 文件名是 hash / UUID（无语义可提取）
- 文件名是中文长串（关键词匹配失效，需 LLM 推断）

## 7. 后续改进

- 用 frontmatter `segment` 字段固化决定，避免下次重新猜
- 如果某个 segment 经常误归（如 60 vs 70），增加 segment-level README 说明边界
- 可考虑写成 `module_checks/thinking.py` 的 lint 规则：检测带强信号关键词但归错段的文件

## 8. 关联

- `docs/thinking/70_retrospective/docs_archival_phase3_red_team_review.md` — 红队对抗反思
- `specs/20_evolution/active/docs_knowledge_archival_methodology/02_design.md` §2 — 位段语义表（驱动判定的语义源）
