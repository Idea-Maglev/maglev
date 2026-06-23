# Docs Archival 主题全域审查报告

> **Created**: 2026-04-25
> **Status**: active
> **Segment**: 70_retrospective
> **Subject**: `specs/20_evolution/active/docs_knowledge_archival_methodology/`
> **HEAD at review**: `e25b7f9`
> **Reviewer**: AI（应用户"对当前需求重新审查"指令）
> **Trigger**: Phase 1-3 完成 + 红队修复 + knowledge-check 补盘 后的统一回看

---

## 1. 范围

对主题"docs 知识归档方法论"做一轮全域交叉审查（requirements ↔ spec ↔ code ↔ tests ↔ contribution_log），目标：

1. 量化 35 条 AC 的实际兑现率
2. 抓出事实层不一致点
3. 用 01_requirements §B.3 的 Success Signal 反查能否宣告主题完成
4. 给出后续优先级建议（不立即执行）

## 2. AC 追溯矩阵

`01_requirements.md` 共定义 **F1-F8 八个功能领域 / 35 条 AC**。

| 大类 | AC 数 | ✅ 全做 | 🟡 部分 | ❌ 未做 | 关键差距 |
|------|------|------|------|------|------|
| F1 生命周期 | 7 | 0 | 2 | 5 | `_drafts/` 未建；STM/MTM/LPM 未在 design 落字段；态间触发条件未实施 |
| F2 编号位段 | 5 | 4 | 1 | 0 | F2-3 ≥4 触发位段升级无机制承载 |
| F3 主题聚类 | 4 | 1 | 1 | 2 | F3-2 时间挪 frontmatter 未做；F3-4 cross_segments 未实施 |
| F4 索引协议 | 5 | 4 | 1 | 0 | F4-2 stats 字段定义但 total=0（与 child_count=9 不一致） |
| F5 librarian 升级 | 4 | 2 | 2 | 0 | F5-1 触发词未在 SKILL.md 显式列；F5-3 catalog 元数据弱 |
| F6 归档触发 | 4 | 1 | 0 | 3 | F6-1 三条件未实施；F6-2 superseded_by 未补；F6-4 verify 不识归档 |
| F7 现存重组 | 4 | 4 | 0 | 0 | ✅ 唯一 100% 区 |
| F8 认知地图 | 4 | 0 | 1 | 3 | **整块零实现**：无 Mermaid / 无 knowledge_graph.json / 无 navigate |
| **合计** | **35** | **16** | **8** | **11** | 全做率 46%；含部分 = 69% |

## 3. 关键不一致（事实错位）

| 编号 | 不一致 | 影响 |
|---|---|---|
| D1 | `INDEX.md` `child_count: 9` vs `stats.total: 0` | F4-2 数据失真，自相矛盾 |
| D2 | spec 称 30+ md + 18 dir 已重组，但**叶子文档无一带 segment/status frontmatter**（除新增 3 篇） | F1+F2-4 形同虚设 |
| D3 | F3-2 明令"时间不允许在文件名"，实测 `_2026_02_03` `_2026_03_15` 仍大量存在 | 重组只完成位置归位，未完成命名清洗 |
| D4 | `archive/starter-kit_legacy/` + `specs/10_reality/01_requirements.md:31` 仍引用 `maglev-librarian` | M3 残留，会误导新读者 |
| D5 | 整个主题 5 天 14 commits，**contribution_log 一条都没补**（断登 2026-04-23 后） | 知识沉淀链路本身漏档（A 等级） |

## 4. Ready Gate 倒查（B.3 Success Signal）

| 信号 | 现状 | 判定 |
|---|---|---|
| ① 三问可独立回答（这份放哪/编号怎么选/什么时候归档） | "放哪/编号"可答；**"何时归档"无答案** | 🟡 |
| ② 现状归位 git log 可追溯 | rename 100% | ✅ |
| ③ `index_verify.py docs` exit 0 | 仅 root 浅绿（S2 缺陷） | 🟡 |
| ④ 半年后无新一轮堆砌 | 不可现在判定 | ⏸ |
| ⑤ librarian 调用完成 scan/verify/calibrate | scan/verify ✅；**calibrate 未跑过** | 🟡 |

→ **5 项 Success Signal 全绿率 1/5**。可宣告"基础设施落地"，不可宣告"主题已成"。

## 5. 整体诊断

- **结构上**：路径 C 决策（新建 index-protocol + index-librarian）执行得很干净，Phase 1-3 把骨架立起来了。
- **内核上**：本主题真正的精神（F1 生命周期态机 + F8 认知地图）**一行未落**。当前交付物精确印证了 Phase 3 红队的哲学层质问 — 实质只是"目录改了名"。
- **程序上**：knowledge-check 已识别 contribution_log 漏档，但补盘止于 thinking/，未触达治理日志本身。**"知识沉淀方法论"主题本身没把会话沉淀到贡献日志**，是递归讽刺。

## 6. 推荐处理顺序

| 优先级 | 项 | 原因 |
|---|---|---|
| P0 | 补 contribution_log 本会话条目 | D5，元方法论不能自我违反 |
| P0 | 修 D1 stats 矛盾（跑 `index_update.py` 或手对齐） | 数据真值 |
| P1 | **F8 落地** | 哲学层承诺，主题 30% 价值悬空 |
| P1 | **F1 落地**（建 `_drafts/`、定 status 枚举、补老叶子 frontmatter） | 没生命周期态机就是改名运动 |
| P2 | F6 归档触发条件实施 + L1（4 segment 缺 INDEX） | 非紧急但承诺过 |
| P2 | M3 旧引用扫除 | 卫生 |
| P3 | F3-2 文件名时间清洗 | 灵敏度低 |

## 7. 复用价值（这份审查的方法）

本次审查使用的 4 步法（**AC 矩阵 → 事实抽查 → Success Signal 倒查 → 优先级建议**）可以作为任何 active 主题在 Phase 中段做"是否在跑偏"自检的标准动作。

它**比红队反思更结构化**（红队偏对抗、列缺陷；本审查贴 AC、判完成度），适用于：

- 主题自宣 Phase N 完成时
- 用户问"现在到底什么程度"时
- 准备进入 crystallization 前的 Ready Gate 卡口
