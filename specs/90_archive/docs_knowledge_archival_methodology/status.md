# Status

> 由 project-board 维护。

## 决策修订记录

- **2026-04-28**: K2 librarian 演进决策的范围已被 `runtime_distribute_project_index_protocol` 主题修订——本决策仅覆盖 Track B（docs/），Track A/C 替代与 maglev-librarian 真正退役由该主题完成。详见本主题 `02_design.md` K2 段落顶部修订标注。
- **2026-05-18**: index-librarian skill 在 `feat/docs-knowledge-index-finalize` 分支上完成索引完整性回填：
  - `index_update --module thinking --full` 修正 SS-3 机械漂移（70_retrospective + root INDEX 计数/updated）
  - 新建 4 个 collection INDEX.md（00_meta / 10_critique / 20_architecture / 90_archive），解 P2-L1 + AC-F6-4 90_archive X02 兼容
  - 实测：`index_verify --module thinking --level local` 100% / `--all` 100%，70 项检查全绿，exit 0
  - SS-3"机器可校验"由 🔴 → ✅ 全绿
  - L1"4 个 collection INDEX 缺"由 ⬜ → ✅ 已补齐

## 顶部诚实摘要（2026-04-27, F1 修订后）

⚠️ **主题真实状态：F6 + F1 + F8 骨架全部落地，F1 已 3 态修订（撤回 draft 状态）**

- 35 条 AC：**全做 25 / 部分 7 / 未做 3**，全做率 71%（含部分 91%）
- 5 项 Success Signal：**全绿率 1/5**
- F8（认知地图）：✅ **骨架落地 3/4 AC**（F8-1/F8-2/F8-4；F8-3 librarian navigate 留作 P1）
  - cognitive_map.py：节点=位段，边=跨段引用（markdown + linked_to）
  - knowledge_graph.json + INDEX.md 注入
- F1（生命周期）：✅ **骨架落地**，**已 3 态修订（2026-04-27）**
  - 4 态 → 3 态：撤回 `draft` 状态与 `_drafts/` 目录
  - 撤回理由：真实使用模式是"会话末快照式总结"，不是撰稿流程，draft 中间态从未被消费
  - 详见 `docs/thinking/00_meta/2026-04-27-lifecycle_abstraction_overdesign.md`
  - 当前 lifecycle: `active → crystallized → archived`（3 态）
  - L08 status 字段枚举（已收紧到 3 态） + 位置不变量警告
  - archive_triggers LPM 保护（status=crystallized 跳过 apply，除非作者写 superseded_by）
  - 未做：crystallization_triggers.py（active→crystallized 自动检测）
- F6（归档触发器）：**已实现 3/4**（commit 时间同决策日；AC-F6-4 verify 兼容性留作 P2）

如果你看完这条仍想继续推进，下会话主线为 Phase 4-6 + 真实修复链（schema 计数语义 → update.py bug → 叶子 frontmatter 补全）。

## 当前阶段（事实层）

- ✅ 00_intent / 01_requirements / 02_design 完成（2026-04-24）
- ✅ Phase 1 协议层搬运（`876ccdd`）
- ✅ Phase 2 index-librarian skill + maglev-librarian deprecate（`ddcadf4`）
- ✅ Phase 3 docs/thinking/ 9 位段化结构归位（`7dc2e49 → 1735f43 → 0846198 → 1f295dd`）
  - 30+18 对象 100% `git mv` 保历史
  - 5 个 collection INDEX.md（30/40/50/60/70），4 个仍缺（00/10/20/90 = L1）
  - `index_verify.py --module thinking --level local` exit 0（**浅绿**：仅 root；S2 缺陷）
- ✅ S1+L3 修复（`4ceff3f`）：schema §6 + status 文档化
- ✅ Knowledge-check 补盘（`e25b7f9`）：A7/A8/A10 三篇 retrospective
- ✅ 全域审查（`120d635`）：AC 矩阵 + 5 项 D 缺陷
- ✅ P0 D1+D5 修复（`7dc4e52`）：手编 stats=105 + contribution_log 补登
- ✅ R2 审查的审查（`a55af75`）：revert stats → 0
- ✅ R3 修 stats=47 + R3 报告（`a6561fb`）
- ✅ 旧引用清理 + status 重写 + R2 NEW-1 撤回（本 commit）

## 未完成事项（按优先级）

### P0（阻塞主题真正完成）

- ✅ **F8 认知地图**：骨架落地 3/4 AC（2026-04-27 commit `dbe5209`）。`scripts/cognitive_map.py` 提供 Mermaid 图（节点=位段，边=跨段引用）+ `_meta/knowledge_graph.json` 机读图谱 + INDEX.md 注入。仅 status != draft 入图（AC-F8-4）。当前 9 节点 0 边——空图诚实反映"叶子均为 draft"的事实。AC-F8-3（librarian navigate）留作 P1。
- ✅ **F1 生命周期**：骨架落地 4/7 AC（2026-04-27 commit `2c29549`）。lifecycle.md 方法论文档；`docs/thinking/_drafts/` STM 草稿区；index_update/verify/archive_triggers 三脚本均排除 `_drafts/`；L08 status 字段枚举校验；archive_triggers LPM 保护。未做：crystallization_triggers.py（active→crystallized 自动检测）。
- ✅ **F6 归档触发器**：已实现 3/4 AC（2026-04-27）。`scripts/archive_triggers.py` 提供三种触发器（时间窗 / 上位重写 / 引用断链）+ git mv apply 路径。AC-F6-4（verify 对归档态兼容）留作 P2。

### P1（已知 bug，互锁）

- ✅ **schema 计数语义已定**（2026-04-27）：`stats.total` = 全树叶子递归数（不含 INDEX.md / README.md，不要求 frontmatter 完整性）。详见 schema §6.5。
- ✅ **update.py 计数实现已修**（2026-04-27）：
  - root 层 `stats.total` 47 → **107**（全树叶子，commit `(本)`）
  - `60_case` `stats.total` 28 → **46**
  - `child_count` 在 mixed collection 自动检测（含子目录+叶子时 sum）
  - 纯叶子型 collection（无 child_type 字段）也走全树递归
- **叶子 frontmatter 补全降级 P2**（与计数语义解耦后不再阻塞主线）。
- 📝 ~~`body_table` 仍需 AI 更新 6 个 collection INDEX 的表格~~ ✅ 已核查（2026-04-27）：30/40/50/70 body 与实际叶子完全对齐，60_case body 列直接子节点（语义正确），root INDEX 修复 30_philosophy 缺链接 1 处。脚本"needs_ai_update"仅因 stats 数字变动触发，body 内容本身已对齐。

### P2（卫生）

- **L1**：00_meta / 10_critique / 20_architecture / 90_archive 缺 collection INDEX.md
- **S2**：verify 仅 root 浅绿，需 deep 级别全树校验
- **D3**：文件名时间清洗（如 `_2026_02_03` 仍在文件名上）
- **L2**：`module_checks/thinking.py` 未实现
- **D2**：~60 篇老叶子无 frontmatter（计数语义解耦后从 P1 降到 P2）
- **AC-F6-4**：verify 对 90_archive 子树应放宽 X02 检查（当前仍有 1 处 X02 失败）

## 已撤回的判定

- ❌ R2 NEW-1（复盘文档 frontmatter 不合规）：经 R3 复查为错告，方法论从未要求 active 态叶子带 frontmatter

## 反思链快速跳转

| 文档 | HEAD | 价值 |
|---|---|---|
| [docs_archival_phase3_red_team_review.md](../../../docs/thinking/70_retrospective/docs_archival_phase3_red_team_review.md) | Phase 3 后 | 9 项分级缺陷 + 哲学质问（高价值） |
| [docs_archival_full_topic_review.md](../../../docs/thinking/70_retrospective/docs_archival_full_topic_review.md) | `e25b7f9` | AC 矩阵 + Success Signal 倒查（高价值） |
| [docs_archival_r2_review_of_review.md](../../../docs/thinking/70_retrospective/docs_archival_r2_review_of_review.md) | `7dc4e52` | 审查的审查；NEW-1 已撤回（中等价值） |
| [docs_archival_r3_review_of_r2.md](../../../docs/thinking/70_retrospective/docs_archival_r3_review_of_r2.md) | `a55af75` | 元讽刺第 4-5 层；含递归边际衰减观察（中等价值） |

## 主导角色

XG（Execution Guardian）— Phase 4 待启动。

## 已知元讽刺总账

| 层 | 内容 | 状态 |
|---|---|---|
| 1 | D5 主题不补 contribution_log | ✅ 已修（条目过长，本次已压缩） |
| 2 | 修 D5 手编 INDEX 违 AC-F4-4 | 📝 已记录，未真修（依赖 P1 解锁） |
| 3 | retrospective frontmatter 不合规 | ❌ R3 撤回 NEW-1 |
| 4 | R2 用 0 而非 47 | ✅ R3 修复 |
| 5 | R2 自我宣告"标准卡口" | 📝 R3 不再自我宣告 |
