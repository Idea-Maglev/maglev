---
reality_id: spec-knowledge-layering.capability.overview
title: 规格知识分层能力
owner_domain: spec-knowledge-layering
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 能力对象：四层规格知识（愿景/现状/演进/归档）的分层表达与检索
  excludes:
    - 结晶写回的执行与门禁（属 governance-quality 域）
    - 索引网络（属 M1 machine-indexing）
---

# 规格知识分层能力

## 1. 能力定位与受益者

能力对象：四层规格知识（愿景/现状/演进/归档）的分层表达与检索。它回答
**"为什么"（愿景与思考）与"是什么"（当前事实）如何分开存放、各自演进、并可被机器与新人同时检索**。

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 新加入的贡献者 | 快速知道"现在是什么"，并区分"为什么/正在变/历史" | 四层目录与每层入口（README/INDEX/定位锚点） | `specs/README.md` 四层架构标准 |
| AI Agent | 不读全仓即取得当前事实与能力边界作为推理依据 | 分层事实页 + 页面 frontmatter 知识状态 | AGENTS.md"10_reality 定位"节 |
| 维护者 | 判断一段内容放入哪一层、何时收口归档 | 层间分工规则与生命周期边界 | AGENTS.md"Git 工作流纪律"；crystallization SKILL 生命周期边界 |
| 定位敏感场景（竞品分析/战略决策/对外沟通） | 避免"Maglev 是什么"的越界表述 | `internal Reality/positioning.md` 定位锚点 | AGENTS.md"定位锚点"节（强制读取） |
| 索引引擎（index-librarian） | 以稳定对象模型扫描与验证知识树 | 分层目录作为 dir-tree track 的可扫根 | `.agents/skills/index-librarian/protocol/registry.yaml`（M1 页组登记） |

四层结构（`specs/README.md` 标准）：

| 层 | 位置 | 回答的问题 | 生命周期 | 索引形态 |
| --- | --- | --- | --- | --- |
| 愿景 | `specs/00_vision.md` | 我们在构建什么（三层构成、四类漂移、北极星原则；README 将其概括为 Iron Triangle / Anti-Entropy） | 稳定，低频修订 | 根 entity-index 的文件级记录 |
| 现状 | `internal Reality/` | 现在是什么（当前事实层） | 随结晶回写演进 | 域 INDEX 网络 + 域 README |
| 演进 | `specs/20_evolution/` | 正在发生什么变化（进行中主题） | 主题完成即收口 | entity-index（collection）+ active/ 目录索引 |
| 归档 | `specs/90_archive/` | 历史如何走到今天 | 只读 | entity-index（collection） |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 新人/Agent 首次进入 specs | 仓库就绪 | `specs/README.md` 地图 → 各层 INDEX → 具体页 | `../spec-knowledge-layering/implementation/architecture.md` | established | supported |
| 会话需要当前事实边界 | 相关页面已按 profile 登记 | 10_reality 域页（frontmatter 携带 knowledge_status/evidence_refs） | `../session-reality-sync/capability/overview.md`（会话起点消费方） | established | supported |
| 追踪一个进行中主题 | 主题目录存在于 `specs/20_evolution/active/` | 主题 `status.md`：意图/流程进度/当前主阶段/已知阻塞 | `../spec-knowledge-layering/capability/use-cases.md` 场景卡 | established | supported |
| 溯源历史结论 | 主题已归档 | `specs/90_archive/README.md` 编年史条目（结晶状态/关键结论/归档时间） | `../spec-knowledge-layering/capability/use-cases.md` 场景卡 | established | supported |
| 机器检索知识对象 | track_scan 已运行 | entity-index 网络与知识导航块（`specs/INDEX.md` 等） | `../machine-index-engine/capability/overview.md` | established | supported |
| 结晶回写落位判断 | 主题通过综合验证 | 回写目标槽位由分层结构决定（写"当前事实"，不指向归档） | `../spec-knowledge-layering/capability/workflows.md` | established | supported |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 范围外 | 结晶写回的执行与质量门禁（floor/ceiling 卡点、admission 收据） | Gate A 裁决：crystallization 写回执行面属 governance-quality 域 | `../governance-quality/capability/overview.md` |
| 范围外 | 索引引擎实现（scan/verify 脚本与 schema 契约） | 本域 M1 已单独建页 | `../machine-index-engine/capability/overview.md` |
| 范围外 | 知识流转的操作步骤 | 属流程页，本页只定位能力 | `../spec-knowledge-layering/capability/workflows.md` |
| unknown | 愿景层内容的新鲜度与修订触发 | 00_vision.md 为单文件，仅根 entity-index 记录 fingerprint，无独立槽位页 | `../spec-knowledge-layering/verification/known-gaps.md` |
| unknown | "分层清晰"能否推出"内容正确" | 分层只约束存放位置与导航；admission 明示不做语义归属判断 | `../spec-knowledge-layering/verification/test-matrix.md` |
| unknown | 演进主题状态词的统一枚举 | status.md 状态段为实例惯例，无登记的状态词表 | `../spec-knowledge-layering/implementation/data.md` |

## 4. 事实与深挖

四层目录形态与索引覆盖见 `../spec-knowledge-layering/implementation/architecture.md`；entity-index 节点、
status.md 字段与页面 frontmatter 的数据契约见 `../spec-knowledge-layering/implementation/data.md`；
机器验证手段与证明力边界见 `../spec-knowledge-layering/verification/test-matrix.md`；层间流转工作流见
`../spec-knowledge-layering/capability/workflows.md`；静态缺口账本见 `../spec-knowledge-layering/verification/known-gaps.md`。
本页不复制其内容。
