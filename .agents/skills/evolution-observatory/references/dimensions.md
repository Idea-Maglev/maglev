# 对标维度体系

## Mandatory 维度

每轮研究**必须**覆盖以下维度，不可省略。

| # | 维度 | 说明 | 对比要点 |
|---|------|------|----------|
| M-1 | **定位与目标** | 产品的核心定位 | 一句话定位、核心目标、目标受众、设计哲学、开源状态 |
| M-2 | **架构模式** | 技术架构设计 | 整体架构图、技术栈、部署/分发方式、扩展机制 |
| M-3 | **需求→实施流水线** | 从需求到代码的路径 | 需求收敛方式、方案设计机制、编码执行模式、验证闭环 |
| M-4 | **治理与纪律** | 约束和质量保障 | 红线/门禁定义、drift 检测、纪律执行强度、合规检查 |
| M-5 | **知识管理** | 知识沉淀与连续性 | 知识体系结构、跨会话记忆、结晶/归档机制、索引管理 |
| M-6 | **对 Maglev 的启示** | 具体参考价值 | 可借鉴的模式、差异化优势、互补点、Actionable Insights |
| M-7 | **模块化分发与生态策略** | 如何分发、组合、被集成 | 分发机制（monolith/模块/插件）、用户可组合性、第三方扩展路径、combo stack 兼容性 |

## 垂域工具豁免规则

当目标为垂域工具（如纯 TDD 框架、单一用途 SDK）时：

- M-5（知识管理）可标记为 `N/A`，附简短理由
- M-6（对 Maglev 的启示）**不可省略**，即使只有一条 insight
- M-7（模块化分发与生态策略）可标记为 `N/A`，如目标不涉及分发/生态
- M-1 ~ M-4 正常覆盖

## Exploratory 维度

AI 可根据目标框架的独特特性，自主添加额外对比维度：

- 标记为 `E-{N}: {维度名}`
- 在报告中单独章节展示
- 每次使用记录到 Registry 的 `dimension_upgrades.pending`

## Exploratory → Mandatory 升级规则

当某个 exploratory 维度满足以下条件时，**建议升级为 mandatory**：

1. 连续 3 次研究中都被使用（pending 记录 ≥ 3）
2. AI 评估其对 Maglev 有持续参考价值
3. Creator 确认升级

升级后：
- 从 `pending` 移到 `promoted`，记录升级日期
- 在 dimensions.md 中追加为新的 M-{N+1}
- 后续研究强制覆盖

## 维度来源追溯

当前 mandatory 维度从以下已有对比文档中提炼：

- `2026-05-25-maglev_vs_superpowers.md`：M-1~M-5 全覆盖
- `2026-02-23-maglev_vs_openspec_vs_bmad.md`：M-1~M-3
- `research_industry_validation.md`：M-2, M-3
- `2026-03-16-maglev_vs_harness_engineering.md`：M-4
- `maglev_vs_hermes_agent.md`：M-2, M-5
