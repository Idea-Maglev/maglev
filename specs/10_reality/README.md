# 10 Reality

这里记录 Maglev 当前可证实的能力、实现、操作与证据，供新贡献者与 AI Agent 使用：先确认阅读范围，再按问题进入能力域，最后沿深挖路径核对证据。它不是任务总结、历史变更或源码镜像。

## 1. 阅读范围与事实边界

| 项目/受管范围 | 版本或静态基线 | 纳入的事实类型 | 明确排除 |
| --- | --- | --- | --- |
| Maglev 仓库当前事实层：14 个能力域 + 横切事实 | 00_profile.yaml `profile_id: maglev-core-v1`（`layout_version: 1`）；实体索引 `knowledge_schema_version: 1`、updated `2026-08-30`（INDEX.md）；模板覆盖基线 `template-coverage/v2`、Pack `software-development 2.0.0`（template-coverage.yaml） | capability、implementation、interfaces、operations、verification、evidence 六类 slot 的已登记事实（slot 契约见 00_profile.yaml） | 项目管理报告（无排期/里程碑/负责人）、变更日志、需求编号与验收标准表镜像、过程归档（依据 `AGENTS.md:52-55`） |
| 横切事实（crosscutting/） | 只收经证明横跨两个及以上能力域的当前事实 | 仓库地图、跨域接口、证据、风险 | 技能/代码系统入口、active spec、无法归属的临时内容（crosscutting/README.md） |

## 2. 从问题到深挖的导航

| 想了解的问题 | 先读页面 | 再进入的模块或来源 | 为什么从这里开始 |
| --- | --- | --- | --- |
| Maglev 是什么、不是什么 | [定位](./positioning.md) | 定位页的关系类型与不变量章节 | `AGENTS.md` 定位锚点要求在理解"是什么/不是什么"前必读此页 |
| 如何安装、更新或发布 | 交付运行时 | distribution-path、installer | 安装/更新/构建/发布共同定义交付运行边界（00_profile.yaml 域边界） |
| 索引导航与目录盘点如何工作 | 机器索引引擎 | [capability/overview](./machine-index-engine/capability/overview.md) | 机器索引网络、导航收据与目录盘点事实的 owner 域 |
| 人读项目地图如何生成与校验 | 项目地图 | [capability/overview](./project-map/capability/overview.md) | ATLAS 地图的确定性生成与唯一性校验事实在此 |
| 会话起点如何对齐现状 | 会话同步 | [capability/overview](./session-reality-sync/capability/overview.md) | 会话起点对齐、漂移哨兵与四类同步事实在此 |
| 思考如何沉淀为知识 | 知识沉淀 | [capability/overview](./knowledge-sedimentation/capability/overview.md) | 沉淀检查与 9 段位段归类事实在此 |
| AGENTS/llms 上下文面如何维护 | 上下文面 | [capability/overview](./agent-context-surface/capability/overview.md) | 上下文面的注入、检查与漂移判定事实在此 |
| specs 四层知识如何分工流转 | 规格分层 | [capability/overview](./spec-knowledge-layering/capability/overview.md) | specs 四层的分层、流转与回写规则在此 |
| 运营手册知识如何生产、审批与同步 | 运营文档 | [capability/overview](./operations-docs-system/capability/overview.md) | 运营手册的受众规则、Wiki 结构审批与索引覆盖事实在此 |
| 项目依赖与外部集成如何工作 | [系统依赖](./system-dependencies.md) | 交付依赖、[扩展分发](./delivery-runtime/implementation/extension-distribution.md) | 先区分跨系统依赖、同进程关系和未证实的运行边界 |
| 哪些人和外部系统与项目发生关系 | [相关方](./stakeholders.md) | [协作能力](./collaboration-lifecycle/capability/overview.md)、[角色映射](./collaboration-lifecycle/operations/team-roles.md) | 先查看任务关系，再回到 owner page 判断权限 |
| 版本说明知识如何生产归档 | 发行知识 | [capability/overview](./release-knowledge/capability/overview.md) | 面向用户的版本说明知识生产与归档在此 |
| 仓库位置与目录分工 | 仓库地图 | crosscutting | 仓库全景地图是顶层目录分工的唯一导航入口 |

## 3. 根页面与模块地图

本层 14 个能力域均登记 `reality_id` 与域级 claim 登记册，claim 由脚本从页面 frontmatter 机械枚举、以 digest 绑定证据（机制见 §4）。

| 入口 | 回答的问题 | 深挖路径 | 状态 |
| --- | --- | --- | --- |
| [系统依赖](./system-dependencies.md) | 项目依赖哪些外部系统？ | delivery-runtime/implementation/dependencies.md | established |
| [相关方](./stakeholders.md) | 哪些人、Agent 和外部系统与项目发生关系？ | [collaboration-lifecycle/operations/team-roles.md](./collaboration-lifecycle/operations/team-roles.md) | established |
| 机器索引引擎 | 索引导航与目录盘点如何工作？ | [capability/overview.md](./machine-index-engine/capability/overview.md) | established |
| 项目地图 | 人读项目地图如何生成与校验？ | [capability/overview.md](./project-map/capability/overview.md) | established |
| 会话同步 | 会话起点如何对齐现状？ | [capability/overview.md](./session-reality-sync/capability/overview.md) | established |
| 知识沉淀 | 思考如何沉淀为知识？ | [capability/overview.md](./knowledge-sedimentation/capability/overview.md) | established |
| 上下文面 | AGENTS/llms 上下文面如何维护？ | [capability/overview.md](./agent-context-surface/capability/overview.md) | established |
| 规格分层 | specs 四层知识如何分工流转？ | [capability/overview.md](./spec-knowledge-layering/capability/overview.md) | established |
| 运营文档 | 运营手册知识如何生产同步？ | [capability/overview.md](./operations-docs-system/capability/overview.md) | established |
| 发行知识 | 版本说明知识如何生产归档？ | [capability/overview.md](./release-knowledge/capability/overview.md) | established |
| 协作生命周期 | 请求如何被收敛、设计、实施、验证与结晶？ | [capability/overview.md](./collaboration-lifecycle/capability/overview.md) | established |
| 治理与质量 | 哪些纪律、审计和验证事实正在生效？ | [capability/overview.md](./governance-quality/capability/overview.md) | established |
| 技能运行时 | 代码执行能力和扩展如何被选择？ | [capability/overview.md](./skill-runtime/capability/overview.md) | established |
| 交付运行时 | 安装、更新、发行和协议运行时如何工作？ | [capability/overview.md](./delivery-runtime/capability/overview.md) | established |
| 接入与集成 | 新项目、存量项目和外部 Agent 如何接入？ | [capability/overview.md](./adoption-integration/capability/overview.md) | established |
| 能力进化 | 能力如何发现、观测与演进？ | [capability/overview.md](./capability-evolution/capability/overview.md) | established |
| crosscutting | 哪些事实横跨多个能力域？ | repository-map/overview.md | established |

> 状态词取自各域 `capability/overview.md` 的 `knowledge_status` frontmatter；词表与语义见 §4。

## 4. 读取限制与更新线索

| 限制/变化线索 | 当前能说明 | 不能说明 | 下一静态入口 |
| --- | --- | --- | --- |
| knowledge_status 语义 | established / unknown / not_established / not_applicable 四个状态词的含义与证据充分度口径（direct / missing / partial） | 状态不来自叙述流畅度，也不表示运行时验证通过 | claim-register 状态表；词表见 00_profile.yaml |
| 页面证据绑定（reality_id + digest） | 每页 claim 以 digest 绑定证据，证据文件逐字节可复核 | digest 一致不等于内容真实："结构通过"不能包装成"内容真实" | 各域 evidence/claim-register.md（示例） |
| 域级 claim 登记册复核 | 14 域各有登记册，由脚本从页面 frontmatter 机械枚举、逐页 claim 入账 | 登记册自身为自指条目，不入本表 | 各域 `evidence/claim-register.md` |
| 收口前置回执 | crystallization 只有拿到 `accepted` 或 `no_change` Receipt 后才能 close active | 回执不替代 Validator 对事实丰富度和置信度的判断 | `.agents/skills/crystallization/SKILL.md`（Receipt 前置条件） |
| 静态基线时限 | 上述基线描述索引登记时点（updated `2026-08-30`）的文件关系 | 不说明该基线是否已部署、运行或被使用；运行时能力当前不采集 | INDEX.md（freshness 与 updated 字段） |
