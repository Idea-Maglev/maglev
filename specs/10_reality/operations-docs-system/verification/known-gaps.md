---
reality_id: operations-docs-system.verification.known-gaps
title: 运营文档已知缺口
owner_domain: operations-docs-system
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 静态无法证明的文档体系事实
  excludes:
    - 已证明事实（属 test-matrix / static-coverage）
---

# 运营文档已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 内容漂移 | 本页组全部 capability 页 + guides 读者 | "docs 与当前版本一致"类结论 | open |
| 审查充分性 | business-rules / use-cases / workflows | 机械检查、审批收据和结构通过不等于用户充分性 | open |
| 范围覆盖 | implementation/docs-system | `docs/private/`、`docs/extensions/` 的知识边界 | open |
| 手工正文 | docs-system-data / use-cases | guides/README 人工推荐段的覆盖度 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 文档内容与当前版本的口径漂移（guides/Wiki 是否逐篇同步） | `docs/INDEX.md`、`docs/releases/` 和 Wiki source bindings | track_verify 只证明索引结构一致；页面语义与 release 口径仍需逐篇核对 | 读者可能按旧口径操作 | 发布轮次的 Wiki/guides review |
| 页面审查的实际充分性 | Plan、Challenge、Divergence 和 review contract；仓库无用户级遥测 | 契约和机械检查证明流程存在，不证明每次页面都回答真实用户问题 | 无法把结构通过升级为用户充分性 | 独立业务问答与反证审查 |
| `docs/private/` 知识边界 | 目录名；`docs/_meta/index.yaml` 有 `docs/private`、`private documentation` 两条 has_index 条目；`source operation guides/README.md` 链接其私域入口 | 未盘点（本轮读取契约不含其内容）；"被扫描"不等于"内容已登记" | 涉及私域的运营事实无法登记；docs/ 全量知识地图不完整 | 需授权后单独盘点轮次 |
| guides/README 人工推荐段的覆盖度 | 文件名清单比对：`source operation guides/20_operations/` 实有 19 篇（不含 INDEX），README 提及其中 14 篇，5 篇未提及（agent_hooks_adoption_guide、extension_maintenance、hooks_trace_snapshot_analysis_manual、maglev_hooks_semantic_trace_schema、maglev_rebuild_and_update_e2e_manual） | README 是人工正文，保留正文规则只保证它不被机器覆盖，不负责自动补全 | 新增操作手册可能不在读者推荐路径上 | 发版轮次人工刷新 |
| Challenge 隔离证据 | `wiki-challenge-receipt.yaml` isolation_status 为 unproven | 仓库收据不能认证执行者或会话独立性 | 整体充分性保持 provisional | `.agents/skills/maglev-wiki/references/step-03-review-structure.md` |
| `docs/extensions/` 仅含 INDEX.md（child_count 0） | `docs/INDEX.md` extensions 记录 + 目录清单 | 只能观察"无正文文档"，无法区分"待建专题"与"已废弃占位" | 该专题在读者导航中的角色无法登记 | 观测类主题 |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 无用户级审查记录 | "Wiki 页面已充分回答真实用户问题"类表述 | 没有独立业务问答和反证轨迹时，充分性保持 provisional | ✗"机械检查通过所以内容充分" |
| `docs/private/` 未盘点 | "docs/ 知识地图完整覆盖"类表述 | 非 complete 范围不得称完整 | ✗"目录存在且被扫描，所以已盘点" |
| 索引新鲜 ≠ 内容新鲜 | "guides 内容与 0.7.4 一致" | verify 只证明结构一致，不证明内容口径 | ✗"INDEX freshness 是 current，所以内容不过期" |
| README 覆盖 partial | "README 列出了全部操作手册" | 未列入清单的分母不得视为已映射 | ✗"README 是入口页，所以必然完整" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 内容漂移 | 发版轮次中逐篇对照 release 说明与 guides 的带时间戳核对记录 | 单篇抽查的使用感受 | `../operations-docs-system/verification/static-coverage.md`、`../operations-docs-system/capability/business-rules.md` |
| 页面审查充分性 | 独立业务问答、反证轨迹和受影响页面 review ledger | 仅机械检查、审批收据或作者自评 | `../operations-docs-system/capability/workflows.md` |
| `docs/private/` 边界 | 授权盘点轮次产出的内容清单与边界登记（含 knowledge records 或明确的排除决定） | 仅凭目录名与 has_index 条目推断 | `../operations-docs-system/implementation/architecture.md` |
| README 覆盖度 | README 更新为全量清单，或登记"不做全量"的显式决策记录 | 零散补几条链接 | `../operations-docs-system/capability/use-cases.md` |
| `docs/extensions/` 语义 | 该目录获得说明文档或显式的建立/废弃决定记录 | 保持只有 INDEX.md 不动 | `../operations-docs-system/implementation/architecture.md` |
| Challenge 隔离 | 仓库外可信隔离/身份证明，或明确接受 provisional 边界 | 仓库内执行收据的自我声明 | `.agents/skills/maglev-wiki/references/step-03-review-structure.md` |
