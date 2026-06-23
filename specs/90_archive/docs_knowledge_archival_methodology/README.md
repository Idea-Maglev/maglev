# docs_knowledge_archival_methodology

> docs/ 知识归档与索引方法论 — 从堆砌治理为有机分层

## 状态

**Archived**

## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality/repository_map.md §1 行 13 + §2 工具层 docs/thinking 条目](../../10_reality/repository_map.md)（"docs/thinking 已按 9 位段组织，每段含 collection INDEX.md，由 index-librarian skill 维护索引一致性" 作为项目事实）
- **关键结论**：
  - **F1 生命周期**：3 态收紧（`active → crystallized → archived`），撤回 4 态中的 `draft` / `_drafts/`
  - **F6 归档触发器**：三类触发器（时间窗 / 上位重写 / 引用断链）+ git mv apply 路径
  - **F8 认知地图**：cognitive_map.py（节点=位段、边=跨段引用）+ knowledge_graph.json 机读图谱 + INDEX.md 注入；仅 status != draft 入图
  - **9 位段结构**：00_meta / 10_critique / 20_architecture / 30_philosophy / 40_paper / 50_alignment / 60_case / 70_retrospective / 90_archive 全部建立 collection INDEX.md（含 frontmatter + body 表）
  - **schema 计数语义**：`stats.total` = 全树叶子递归数（不含 INDEX.md / README.md）；mixed collection 自动检测 child_count
  - **maglev-librarian → index-librarian 接力**：由 #19 `runtime_distribute_project_index_protocol` 主题完成物理废弃
- **执行经验**：
  1. 本主题在 4 月份多轮推进（Phase 1-3 + 红队复盘 + R2/R3 review of review）后，剩余 SS-3 fail 与 4 个 collection INDEX 缺等"机械维护"项被作者降级到 P2 卫生项
  2. 本次结晶前实地复核发现：所谓"全绿率 1/5"其实只剩 SS-3 一项 fail + 该 fail 是 4 月底之后新增文档导致的 stats 漂移，跑一次 `index_update` 即可恢复
  3. 这印证了"verify 类机械检查应该自我修复（updater 接力），不应作为主题完成度的硬阻塞"——是工程化经验，不是方法论失败
  4. AC-F6-4（90_archive X02 兼容）选择"补 INDEX.md"而非"改 verify 协议代码"路径，更小成本解锁
- **测试证据**：未引入 `tests/` 下正式测试文件；验证依赖可重复命令：
  - `python3 .agents/skills/index-librarian/protocol/scripts/index_verify.py --module thinking --level local --format summary` → exit 0 / 100%
  - `python3 .agents/skills/index-librarian/protocol/scripts/index_verify.py --format summary`（all tracks） → exit 0 / 100% (70/70 passed)
- **未做但已显式降级**（数据卫生 / 范围扩展，不再阻塞主题）：
  - L2: `module_checks/thinking.py` 自定义检查器（扩展点，无强需求）
  - D2/D3: 老叶子 frontmatter 补全 / 文件名时间戳清洗（数据卫生）
  - Phase 4: registry 扩展到 guides / releases（范围扩展到新模块，属于 follow-up 主题）
  - Phase 6 contributors 补登（文档收尾）
  - SS-4 可持续性（半年回看，时间维度）
- **时间线**：2026-04-24 启动 → 2026-04-27/28 多轮红队复盘 + R2/R3 → 2026-05-18 索引完整性回填 + 结晶归档

## 概述

为 `docs/` 建立**长期可持续的知识归档与索引机制**，把现状的"知识堆砌"治理为"有机分层"。归纳方法论先行，索引脚本随后。

本主题最终交付：

- 方法论：`docs/thinking/_meta/` + `20_architecture/lifecycle_layer_boundary.md` + 协议层 `index-librarian/protocol/` 文档体系
- 协议骨架：F1（生命周期）+ F6（归档触发器）+ F8（认知地图）
- 9 位段化的 docs/thinking 结构 + 完整 INDEX 网络
- index-librarian skill 接管 maglev-librarian 职责（由 #19 完成 maglev-librarian 物理废弃）

## 文件索引

| 文件 | 内容 |
|------|------|
| [00_intent.md](./00_intent.md) | 目标、边界、上游证据 |
| [01_requirements.md](./01_requirements.md) | FR / AC / Success Signal / Key Unknowns |
| [02_design.md](./02_design.md) | F1-F8 设计 + Phase 1-6 路线 + K1-K7 决策 |
| [status.md](./status.md) | 完整事实层进度 + 决策修订记录 + 反思链跳转 |

## 关联

- **当前事实承载**：[10_reality/repository_map.md](../../10_reality/repository_map.md) §1 行 13 + §2 工具层 docs/thinking 条目
- **协议层**：`.agents/skills/index-librarian/protocol/`（registry / index-schema / index-verify / lifecycle 等）
- **承接主题**：#19 `runtime_distribute_project_index_protocol`（完成 maglev-librarian 物理废弃 + dist catalog 拆分 + multi-track 升级）
- **反思链**（高价值，保留在 `docs/thinking/70_retrospective/` 不入归档）：
  - `docs_archival_phase3_red_team_review.md`（9 项分级缺陷 + 哲学质问）
  - `docs_archival_full_topic_review.md`（AC 矩阵 + Success Signal 倒查）
  - `docs_archival_r2_review_of_review.md` / `docs_archival_r3_review_of_r2.md`（review of review 第 4-5 层元讽刺）
