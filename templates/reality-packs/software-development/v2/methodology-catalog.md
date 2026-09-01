---
title: "v2 模板方法论与采纳边界"
type: methodology_catalog
status: pending_human_quality_review
---

# v2 模板方法论与采纳边界

模板只借鉴能帮助读者理解静态事实的结构，不宣称符合或替代任何外部标准。

| 来源 | 用于哪些页面 | 只采纳什么 | 明确不采纳什么 |
| --- | --- | --- | --- |
| [GB/T 9385-2008](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=3892B755FDE15A9AE05397BE0A0AE71E)（状态待官方复核） | capability、需求追踪 | 需求范围、约束、可验收预期与追溯关切 | 需求不作为当前实现证明，Reality 不成为 PRD 镜像 |
| [GB/T 8567-2006](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=0B9CF4979A769353E05397BE0A0AB25E)（状态待官方复核） | 全部页面 | 需求、设计、测试、支持关切是否遗漏 | 传统交付物目录和文档格式不决定模块路径或 Slot |
| [GB/T 9386-2008](https://openstd.samr.gov.cn/bzgk/std/index)（状态待官方复核） | verification | 测试对象、测试行为、结果与缺口的表达关切 | 测试存在不等于覆盖完整或生产行为被证明 |
| [GB/T 25000.51-2016](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=BCA1ACCA0D5C4140E05397BE0A0A03BB)（状态待官方复核） | verification、known-gaps | 质量要求、验证与质量缺口的讨论维度 | 不转成质量总分或自动内容评分 |
| [arc42](https://docs.arc42.org/home/) 与 [C4](https://c4model.com/) | architecture、components、dependencies、delivery-topology | 关切、边界、构件关系和有静态依据时的图 | 不强制完整章节或图集，不替代产品/验证页面 |
| [OpenAPI](https://spec.openapis.org/oas/latest.html) 与 [AsyncAPI](https://www.asyncapi.com/docs/reference/specification/v3.1.0) | api、events | 操作、消息、输入输出、错误、发送接收和兼容边界 | 不将描述文件或设计稿提升为已实现事实 |
| [Home Office documentation guidance](https://engineering.homeoffice.gov.uk/patterns/write-effective-documentation/) | 全部页面 | 从读者任务组织内容、区分概念/参考信息、收集读者反馈 | 不作为事实置信度或软件架构规范 |
| [DeepWiki-Open](https://github.com/AsyncFuncAI/deepwiki-open) | implementation 辅助导航 | 代码地图、代码引用、关系图和分层导航 | 不作为模块、产品、权限、验证或证据结构的权威 |

## 页面模型比较与选择

v2 草案采用混合 Reality 作为页面骨架：能力、实现、接口/运行、验证和证据页面共同回答模块现状，
但每一项只由相应来源角色支持。它不是“覆盖越多越好”的目录集合；下表保留了结构取舍，供审阅者
检查每个 Slot 是否仍服务其读者问题。

| 候选模型 | 擅长解决的问题 | 作为主结构的缺口 | v2 的处置 |
| --- | --- | --- | --- |
| 纯代码 Wiki | 代码地图、调用关系、实现定位 | 无法可靠说明用户价值、产品范围、授权或验证边界 | 仅采纳实现导航和关系图的表达方式 |
| PRD/需求镜像 | 用户、场景、范围、预期 | 不能证明当前实现、数据、接口或测试 | 仅采纳 capability 和追踪页的意图来源角色 |
| arc42/C4 多视图 | 架构关切、构件关系、静态图 | 不覆盖产品能力、协议细节、证据账本与测试缺口 | 仅采纳 implementation/operations 的关系和约束表达 |
| 混合 Reality | 跨能力、实现、接口、验证与证据的深挖导航 | 多视图可能重复，模板维护成本较高 | 作为本草案主结构；用 owner page、来源角色、专属页面结构和人工审阅控制重复 |

因此，页面目录不照搬任何外部标准：每页必须先回答专属读者问题，再选择适用的方法要素；不能把代码
目录、PRD 章节或架构图层级直接变成模块路径。完整的来源权威性评估、候选比较与不可迁移边界见
[参考依据评估](../../../../specs/90_archive/abandoned/2026-08-26-reality-software-template-convergence/context/reference-authority-assessment.md)。

## 共同事实纪律

| 来源角色 | 可以说明 | 不可以说明 |
| --- | --- | --- |
| 产品需求、PRD | 用户、场景、范围、预期和约束 | 当前实现、权限、数据或接口已成立 |
| API 契约、技术设计 | 协议/设计意图、字段和约束 | 代码当前行为或运行时效果 |
| 代码、配置、数据库定义 | 当前可定位的静态实现 | 用户价值、动态行为或完整测试覆盖 |
| 测试 | 已编码的验证行为和覆盖边界 | 所有需求或生产行为已完成 |

每个页面只在相应区块中表达 unknown/blocked：必须说明缺少什么、已检查什么、下一处静态深挖入口
在哪里，不能使用“暂无资料”或通用证据提示取代事实结构。

## 共同落地规则

### 最小事实摘要

每个适用页面至少要让读者知道当前结论、适用范围、直接来源和下一处深挖入口。摘要不能只列
技术名词、目录或页面标题；删除一条事实后如果读者对功能用法、实现位置或验证边界不会产生
误解，这条内容就不应为了凑篇幅写入。

### Provenance 与状态

每条关键事实至少绑定 `source_unit`、来源角色、静态 `baseline`、项目相对路径或锚点、事实状态
和定位质量。需求/设计只能支持意图，代码/配置支持静态实现，Guard/策略和测试分别记录授权与
验证；任何来源角色都不能替代另一角色。知识状态使用 Reality Contract 的 canonical 值，证据
充分度单独记录，不用流畅度、文件数量或页面数量推断置信度。

### 适用性与缺口

适用页面即使缺少直接证据也要保留，并明确 `unknown` 或 `blocked`、已查范围和下一静态入口。
只有能说明范围依据的页面才能记为 `not_applicable`；不得用空表、通用句子或模板示例伪装完成。

### 读者与审阅

页面要围绕自己的读者问题组织，能力层与实现层互相链接但不互相代写。图表只表达已有静态证据
支持的关系；没有锚点时使用账本或未知项。结构完整不等于内容通过，内容丰富度和事实/来源置信度
必须单独审阅。
