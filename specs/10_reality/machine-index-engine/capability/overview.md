---
reality_id: machine-index-engine.capability.overview
title: 机器索引与导航收据能力
owner_domain: machine-index-engine
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 能力对象定义：机器索引、导航收据、新鲜度门禁
  excludes:
    - 业务规则（属 index-business-rules.md）
    - 使用场景（属 index-use-cases.md）
    - 工作流（属 index-workflows.md）
---

# 机器索引与导航收据能力

## 1. 能力定位与受益者

能力回答一个稳定问题：**在一个多产物仓库（技能、specs、docs、代码、测试都是一等产物）
里，如何用最低成本定位权威文件，并证明这次定位是可信的。** 能力由三部分构成：登记驱动的
确定性索引（让"找文件"不依赖会话记忆）、任务导航收据（把"我怎么找到的"变成可验证记录）、
新鲜度门禁（索引与登记的一致性校验以 exit code 暴露，可被启动流程当作 preflight）。

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 人类开发者 | 在多产物仓库中定位权威文件，不靠记忆或逐目录翻找 | 登记驱动的三类索引产物：目录树 `INDEX.md` 网络、仓库入口锚点 YAML、summary YAML | registry.yaml `tracks:` 段；SKILL.md 概览表 |
| AI Agent / 技能流程 | 任务开始前拿到可解释的上下文入口，而不是全域搜索或凭记忆猜路径 | 任务导航收据 JSON（status + 有限候选 + 匹配依据） | SKILL.md 概览"任务导航先遍历这些相邻 INDEX 记录"段 |
| 会话启动流程（reality-sync preflight） | 在会话起点机器判定"索引是否可信" | `track_verify` 的 exit code 与逐 track 状态报告 | SKILL.md "验证闭环"条；消费链见 `index-use-cases.md` |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 用户说 "检查索引" / "索引巡检" / "verify index" / "索引状态" | 仓库就绪；目标 track 已在 registry 登记 | `track_verify` 逐 track 打印 `ok` 或失败原因，进程 exit code 暴露门禁结论 | `../machine-index-engine/capability/workflows.md` | established（契约文本） | 契约级 |
| 用户说 "扫描模块" / "scan track" / "修复/刷新索引" | 同上 | `track_scan` 写回/刷新 `INDEX.md` 网络与 summary YAML | `../machine-index-engine/capability/workflows.md` | established（契约文本） | 契约级 |
| reality-sync 发现索引异常 / integrated-validator 编排调用 | 消费方处于受控阶段 | 按 track 选择 scan 或 verify，结果回传消费方 | `../machine-index-engine/capability/use-cases.md` | established（契约文本） | 契约级 |
| 任务需要上下文入口（实施/设计等受控阶段） | 相邻 `INDEX.md` 存在知识记录 | `task_navigate` 产出导航收据 JSON（`queried`/`not_needed`/`insufficient` 起步） | `../machine-index-engine/interfaces/cli.md` | established（契约文本） | 契约级 |
| 新模块接入索引协议 | 用户在 registry.yaml 新增 track | 新 track 纳入后续 scan/verify | `../machine-index-engine/capability/use-cases.md` 场景 4 | established（契约文本） | 契约级 |
| 用户说 "仓库入口索引" / "repo entry index" / "代码索引" / "code index" | 对应 track 已登记（code-tree 需显式启用） | repo-entry 锚点 YAML 或 code-tree 锚点 + radar 摘要产物 | `../machine-index-engine/implementation/data.md` 产物形态 | established（契约文本） | 契约级 |
| 每次实际触发 | — | 触发频率、输出被采纳率 | 无运行记录机制 | unknown | 无运行遥测 |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 能力外（分工裁决） | 仓库代码依赖分析（impact/cycles/unused/hotspot/路径/函数）不属本能力，走独立 `radar` skill；`code-tree` 的 `radar_summary` 只是统计摘要 | SKILL.md "委派 radar 的边界"段 | crosscutting radar（域外能力） |
| 能力外（分工裁决） | 人读项目地图 `docs/ATLAS.md` 由 `maglev-map-maker` 生成，本能力不维护独立 Markdown 地图 | SKILL.md 概览段 | `../project-map/implementation/architecture.md` |
| 能力外（Gate A 裁决） | 活跃需求扫描与看板（project-board）不属本能力，归 collaboration-lifecycle 域 | 本域边界裁决记录 | crosscutting collaboration-lifecycle（域外） |
| 不承诺 | 收据不证明任务成功：候选 `confidence` 限定为 `navigation_confidence`，只表示导航候选与意图的匹配强度 | SKILL.md 概览收据边界段 | `../machine-index-engine/interfaces/cli.md` |
| 不承诺 | 三类产物不自动等同于业务事实（如 `repo-entry.yaml` 是机器导航产物） | SKILL.md 概览实例配置段 | `../machine-index-engine/implementation/data.md` |
| 不承诺 | 索引的两层密度分工：`knowledge_records` 面向机器（有限 topic），人读知识导航表只展示前 4 个 topic 并以 `(+N)` 折叠——索引不承担正文摘抄 | SKILL.md 概览两层密度段 | `../machine-index-engine/implementation/data.md` 字段字典 |
| unknown | `track_verify` 被哪些启动哨兵以何种频率调用、verify 失败后的真实处置 | 仅确认 reality-sync preflight 引用存在（intent 层） | `../machine-index-engine/verification/known-gaps.md` |

## 4. 事实与深挖

约束本能力行为的规则（写权隔离、导航门禁、Reality 边界）见
`../machine-index-engine/capability/business-rules.md`；谁在什么场景消费能力见 `../machine-index-engine/capability/use-cases.md`；
标准工作流分解见 `../machine-index-engine/capability/workflows.md`。引擎实现（registry/scan/verify/navigate
四构件）见 `../machine-index-engine/implementation/architecture.md`，产物数据结构见 `../machine-index-engine/implementation/data.md`；
命令行与收据契约见 `../machine-index-engine/interfaces/cli.md`；配置面、失败语义与状态模型见
`../machine-index-engine/operations/configuration.md`、`../machine-index-engine/operations/errors.md`、
`../machine-index-engine/operations/state-model.md`；测试证明力、覆盖分母与已知缺口见
`../machine-index-engine/verification/test-matrix.md`、`../machine-index-engine/verification/static-coverage.md`、
`../machine-index-engine/verification/known-gaps.md`。本页不复制以上页面的实现与验证细节。
