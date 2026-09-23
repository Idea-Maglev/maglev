---
reality_id: operations-docs-system.capability.overview
title: 运营文档知识能力
owner_domain: operations-docs-system
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 能力对象：面向使用者的运营知识（guides/发布说明）生产与同步
    - 能力对象：对外 wiki 投影层（docs/wiki/，维度可配置、人与 agent 双读者）
  excludes:
    - docs/thinking 方法论层（属 M4 knowledge-sedimentation）
    - 发行流程本身（属 delivery-runtime 域）
---

# 运营文档知识能力

## 1. 能力定位与受益者

运营文档知识回答一个稳定问题：**使用者（非仓库维护者）如何获得与当前版本一致的运营知识，写作者如何在不跑偏的前提下生产这些知识。**

能力由三个知识面构成：**运营手册**（`source operation guides/`：00_start / 10_concepts / 20_operations /
30_comparisons / 90_advanced 五段结构 + INDEX 导航）、**版本发布知识**（`docs/releases/`，
属 M8 release-knowledge）与**对外 Wiki 投影**（`docs/wiki/`）。Wiki 能力由 `.agents/skills/maglev-wiki/` 携带：`.maglev/wiki.yaml` 只声明项目与来源边界；确定性 Source Universe 登记可访问证据；生产 Agent 推导 Wiki Plan，隔离挑战 Agent 在不可见 Plan 与现有 Wiki 的上下文中重建读者问题、风险和深度信号。
Plan 与 Challenge 经 Divergence Ledger 逐项处置后，`.maglev/wiki/wiki-plan.md` 向人同时展示结构、遗漏、替代方案和剩余风险；未批准、隔离输入污染或摘要不一致时，导航与正文生成阻断。批准后 `wiki_generate.py` 只生成 `WIKI.md`、维度入口和 `FRAMEWORK.md`，正文由 Agent 按证据写作。
最终审查合并 Plan、Challenge、风险、变更和独立业务问答，并要求反证轨迹。没有外部问题或隔离无法证明时，充分性只能是 `provisional`。模板仍只提供约束、建议和示例，不决定页面数量或内容深度。
Wiki 生成状态资产与项目输入分离：`.maglev/wiki.yaml` 保留标题、语言、来源边界和受众提示；Source Universe、Challenge、Plan、Divergence、审批收据与 review 资产统一位于 `.maglev/wiki/`。该目录布局是当前 Wiki 能力契约，不影响 `docs/wiki/` 正文投影路径。

当前验证边界为静态能力：Wiki 专项测试和目录冒烟已通过；CBU 独立消费者审查仍保持 `provisional/pass_with_findings`，不能升级为运行态或用户充分性验证。
写作侧现在由 Wiki authoring workflow 和人类可读输出契约约束：先构建来源全集、独立挑战和结构审批，再按批准页面写作并审查，不保留独立内容运营层。

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 使用者/读者（第一次接触 Maglev 的人） | 知道从哪篇文档开始上手，而不是在目录里迷路 | `source operation guides/README.md`"如果你只想知道先看什么"按角色分流到五段具体篇目 | `source operation guides/README.md` 起步段 |
| 对外读者（业务/技术评估/接入开发者）与 Agent | 从项目 Wiki 获取按真实任务组织且经过遗漏挑战的知识 | `docs/wiki/WIKI.md` 阅读入口 + 经 Plan/Challenge 差异裁决的页面树；页面标注受众和来源 | `.maglev/wiki/wiki-plan.yaml` + `.maglev/wiki/wiki-challenge.yaml` + `docs/wiki/WIKI.md` |
| 使用者/读者（日常操作者、维护者） | 查安装、初始化、更新、发版、排障的操作口径 | `20_operations` 段的推荐操作链路（7 篇）+ 其他操作文档清单 | `source operation guides/README.md` 20_operations 段 |
| 内容作者（人类或 AI Agent） | 基于当前事实生产用户解释，并保留来源、边界和未知 | Wiki Source Universe、Plan、Challenge、审批收据和页面 review 资产 | `.agents/skills/maglev-wiki/` 与 `.maglev/wiki/` |
| 评估与对外沟通者 | 从 Wiki 和 Reality 获取可复核的定位、比较和风险边界 | 按受众组织的 Wiki 页面与对应 source bindings | `docs/wiki/WIKI.md` + `internal Reality/positioning.md` |
| AI Agent（会话执行方） | 在受控阶段定位 docs 内的权威文件，而不依赖目录猜测 | docs 的 entity-index 导航节点与知识导航块（M1 能力的消费面） | `../machine-index-engine/capability/overview.md` 能力对象定义 |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 生成或更新 Wiki | 项目配置、事实来源和读者任务已确定 | 构建 Source Universe、Producer Plan 和 Blind Challenge，形成待审结构 | `.agents/skills/maglev-wiki/` + `.maglev/wiki/` | established（流程契约） | 契约级 |
| Wiki 结构获得人类批准 | Plan、Challenge 和 Divergence 已完成差异处置 | 生成审批收据、证据包和批准页面 | `wiki-plan-approval.yaml` + `wiki_content.py` | established（流程契约） | 契约级 |
| Wiki 来源或正文发生变化 | 变更影响已定位 | 重跑 frontmatter、结构、漂移、可读性和开放世界检查 | `.agents/skills/maglev-wiki/scripts/` | established（机械门禁） | 机械级 |
| docs/ 目录发生实质变化 | M1 索引引擎被运行 | INDEX 网络与 `docs/_meta/index.yaml` 写回刷新 | `../operations-docs-system/implementation/data.md` | established（M1 引擎行为） | 引擎级 |
| 受控阶段需要定位 docs 权威文件 | 导航查询被发起 | INDEX 知识导航块命中候选；无充分候选时升级（M1 收据语义） | `../machine-index-engine/operations/state-model.md` 收据三态 | established（M1 能力定义） | 引擎级 |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 不拥有事实层 | Wiki 与 guides 是用户解释或操作入口，不取代 `internal Reality` 作为当前事实来源 | `.maglev/wiki/` Plan/Approval 规则 + Reality 定位 | `../../../internal Reality/README.md` |
| 不负责正文自动生成 | `wiki_generate.py` 只生成导航和框架，批准正文仍需按证据写作与审查 | `maglev-wiki` 工作流 | `../../../.agents/skills/maglev-wiki/SKILL.md` |
| 不覆盖发布流程 | 版本发布说明和发行流程分别归 release-knowledge 与 delivery-runtime | frontmatter excludes | `../release-knowledge/capability/overview.md` |
| 不覆盖方法论层 | `docs/thinking/` 属 M4 knowledge-sedimentation，本能力不登记其内容 | frontmatter excludes + `docs/INDEX.md` thinking 记录 | `../knowledge-sedimentation/capability/overview.md` |
| unknown：私域文档内容边界 | `docs/private/` 存在且被 docs track 扫描，但其内容未盘点 | 目录名 + `docs/_meta/index.yaml` 条目 | `../operations-docs-system/verification/known-gaps.md` |
| 不承诺用户充分性统计 | Wiki 机械检查只证明可复算完整性；没有独立用户问答或可信隔离时，充分性保持 provisional | Wiki review workflow | `../../../.agents/skills/maglev-wiki/references/step-07-present-and-record.md` |

## 4. 事实与深挖

两个知识面的机制事实分布如下，本页不复制其内容：

- 约束用户文档行为的规则（受众视角、入口页三问、来源边界和相对链接）：
  `../operations-docs-system/capability/business-rules.md`。
- 消费与生产场景（读者分流、Wiki 结构审批、操作指南阅读）：`../operations-docs-system/capability/use-cases.md`。
- Wiki 结构、审批、证据和正文审查流程：`../operations-docs-system/capability/workflows.md`。
- `docs/` 运营侧目录形态与索引覆盖：`../operations-docs-system/implementation/architecture.md`。
- INDEX 节点与知识记录的数据契约：`../operations-docs-system/implementation/data.md`。
- 门禁与缺口（索引新鲜 ≠ 内容不过期）：`../operations-docs-system/verification/test-matrix.md`、
  `../operations-docs-system/verification/known-gaps.md`。
