---
reality_id: knowledge-sedimentation.capability.overview
title: 知识沉淀能力
owner_domain: knowledge-sedimentation
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 能力对象：高价值思考的沉淀检查与 9 段记忆归类
  excludes:
    - specs 分层（属 M6）
    - 运营文档（属 M7）
---

# 知识沉淀能力

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 人类开发者（会话主导者） | 高价值探索结束后确认"这一轮的为什么不会随会话消失" | 资产清单、缺口清单与最小补齐动作 | `.agents/skills/knowledge-check/SKILL.md` 职责与交付物定义 |
| AI Agent | 会话切换/任务收尾前核对思考、方案、参考资料、贡献记录是否已落盘 | 同上，外加 9 段位段归类判断 | 同上，description 与"概览"段 |
| crystallization（相邻能力） | 接收被明确切出的生命周期后段动作 | 边界判断 + 转交建议（reroute_target） | SKILL.md"与 crystallization 的边界" |
| 后续会话/新贡献者 | 找回历史"为什么"作为推理上下文 | `docs/thinking/` 9 段记忆宫殿 + 段内 INDEX 导航 | `docs/thinking/INDEX.md` 9 段目录知识记录 |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 一段高价值探索结束后 | 本轮产生了值得长期保留的思考/方案/治理判断 | 资产清单 + 未沉淀项 + 最小补齐动作 | `../knowledge-sedimentation/capability/workflows.md` 步骤表 | established（契约文本） | 契约级 |
| 会话准备切换前 | 会话即将切换，可能存在未落盘资产 | 补沉淀缺口判断，防止思考停留在对话中 | 同上 | established（契约文本） | 契约级 |
| 任务收尾前 | 进入收尾阶段 | 贡献记录核对 + 9 段归类结论 | 同上 | established（契约文本） | 契约级 |
| 怀疑本轮有价值思考可能流失时 | 用户主动提出 | 同探索收尾的检查输出 | SKILL.md"何时使用"第 4 条 | established（契约文本） | 契约级 |
| 问题命中归类关键词（位段/segments/9 段记忆宫殿/thinking 归类/资产是否落盘） | 问题匹配 SKILL.md"快速识别"清单 | 以 knowledge-check 为 canonical 入口的归类判断 | `../knowledge-sedimentation/capability/business-rules.md` 规则目录 | established（契约文本） | 契约级 |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 范围外（生命周期后段） | 需求归档、reality writeback、active 状态收口 | SKILL.md"它不负责"段 | crosscutting crystallization |
| 范围外（内容重写） | 不替代沉淀对象本身重写内容，只判断"是否已沉淀" | SKILL.md 判定纪律 | — |
| 范围外（段内容生成） | 各段内容由会话沉淀产生，本能力不代写"为什么" | 同上 | `../knowledge-sedimentation/capability/workflows.md` 落盘行 |
| 范围外（位段 schema 规约） | segments 字段的 schema 格式由 index-librarian 规约，本能力不定义 schema | SKILL.md"与 index-librarian 的边界" | `.agents/skills/index-librarian/` |
| 范围外（specs 事实层生产） | thinking→specs 反哺由 spec-pipeline draft 工作流执行，本能力只提供已沉淀的"为什么" | `../spec-knowledge-layering/capability/workflows.md` 流转图（M6） | crosscutting spec-pipeline |
| unknown | 检查与归类的实际执行率（会话是否真的触发） | 全仓无会话级运行记录 | `../knowledge-sedimentation/verification/known-gaps.md` |

## 4. 事实与深挖

- 约束与决策：`../knowledge-sedimentation/capability/business-rules.md`（canonical 入口、边界铁律、blocker 隔离、冲突边界）。
- 流程分解：`../knowledge-sedimentation/capability/workflows.md`（四步检查 + 位段归类 + 落盘交接）。
- 场景视角：`../knowledge-sedimentation/capability/use-cases.md`（三类触发场景与跨域反哺交接）。
- 验证面：`../knowledge-sedimentation/verification/test-matrix.md`、`../knowledge-sedimentation/verification/static-coverage.md`、`../knowledge-sedimentation/verification/known-gaps.md`。

本页不复制上述页面的机制细节；9 段位段语义本体由
`.agents/skills/knowledge-check/references/segments-canonical.yaml`（机器读）与
`segments-canonical.md`（人读）持有，`docs/thinking/` 的目录结构是它的物理载体。

### 附：9 段记忆宫殿一览（语义来源 segments-canonical.yaml）

| 位段 | 房间名 | 一句话用途 |
| --- | --- | --- |
| 00_meta | 元厅 | 模块元信息、入口与导航 |
| 10_critique | 批判间 | 反思、对抗与质疑性分析 |
| 20_architecture | 架构间 | 系统结构、分层与边界设计 |
| 30_philosophy | 哲学殿 | 范式根基、第一性原理与方程式表达 |
| 40_paper | 论文阁 | 学术对位、方法借鉴与理论引用 |
| 50_alignment | 对标厅 | 跨范式对比、生态对位与差异化定位 |
| 60_case | 案例馆 | 落地实例、试点与具体场景产出 |
| 70_retrospective | 复盘室 | 迭代闭环、决策回顾与经验提炼 |
| 90_archive | 归档库 | 已被结晶/上位重写/退役的历史文档 |

9 段在 `docs/thinking/INDEX.md` 中 9/9 有 indexed 知识记录；scope_in/scope_out 互斥定义与
状态语义（active/draft/archived）以 canonical 文件为准，本页不复制。
