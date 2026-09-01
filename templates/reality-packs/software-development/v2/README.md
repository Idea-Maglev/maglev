---
title: "软件研发 Reality Template Pack v2"
type: production_template_pack
status: production
---

# 软件研发 Reality Template Pack v2

这是受 `pack.yaml` 注册的生产模板资产。它定义人读页面契约、方法论、正向示例和审阅项；这些资产只
由通用 Consumer 解析和绑定，不读取项目事实、不生成页面正文、不生成 candidate。`composer_eligible`
仅为历史兼容元数据，不代表当前存在可执行 Composer。

`root-pages/` 和 `page-contracts/` 是 Pack 内的模板资产目录，不是目标项目的输出目录。实际目标路径
只能从 `pack.yaml` 的 `materialization.pages` 解析，不能复制 Pack 目录或根据页面 ID 拼接路径。

## 审阅顺序

1. 先读[方法论与采纳边界](./methodology-catalog.md)，确认每类页面为什么采用该结构。
2. 先读项目级 `root-pages/`，确认项目入口、术语、跨模块架构、系统依赖和相关方关系如何各自展开。
3. 按模块页阅读 `page-contracts/`：每页都包含读者问题、静态来源角色、实际落地结构、完整正向示例和
   模板审阅项。
4. 判断模板是否足以让事实生产者写出有用内容，而不是检查文件是否齐全。

## 项目级根页面

| 页面 | 回答的问题 |
| --- | --- |
| [README](./root-pages/README.md) | Reality 覆盖范围、阅读路径和静态边界 |
| [glossary](./root-pages/glossary.md) | 术语、别名、冲突和状态词 |
| [product-architecture](./root-pages/product-architecture.md) | 能力域、模块关系和系统边界 |
| [system-dependencies](./root-pages/system-dependencies.md) | 上下游系统、集成方向和静态限制 |
| [stakeholders](./root-pages/stakeholders.md) | 人、团队、外部系统与能力关系 |

物化时，五个根页必须一对一落到目标 Reality 根目录：

| Pack 资产 | 目标 Reality 路径 |
| --- | --- |
| `root-pages/README.md` | `README.md` |
| `root-pages/glossary.md` | `glossary.md` |
| `root-pages/product-architecture.md` | `product-architecture.md` |
| `root-pages/system-dependencies.md` | `system-dependencies.md` |
| `root-pages/stakeholders.md` | `stakeholders.md` |

目标目录不得出现 `10_reality/root-pages/`；模板正向示例也不得被当作项目事实。

## 模块级页面

| Slot | 页面 |
| --- | --- |
| capability | [overview](./page-contracts/capability/overview.md)、[use-cases](./page-contracts/capability/use-cases.md)、[workflows](./page-contracts/capability/workflows.md)、[business-rules](./page-contracts/capability/business-rules.md) |
| implementation | [architecture](./page-contracts/implementation/architecture.md)、[components](./page-contracts/implementation/components.md)、[visual](./page-contracts/implementation/visual.md)、[data](./page-contracts/implementation/data.md)、[dependencies](./page-contracts/implementation/dependencies.md) |
| interfaces | [api](./page-contracts/interfaces/api.md)、[events](./page-contracts/interfaces/events.md)、[cli](./page-contracts/interfaces/cli.md) |
| operations | [state-model](./page-contracts/operations/state-model.md)、[permissions](./page-contracts/operations/permissions.md)、[errors](./page-contracts/operations/errors.md)、[configuration](./page-contracts/operations/configuration.md)、[delivery-topology](./page-contracts/operations/delivery-topology.md) |
| verification | [test-matrix](./page-contracts/verification/test-matrix.md)、[static-coverage](./page-contracts/verification/static-coverage.md)、[known-gaps](./page-contracts/verification/known-gaps.md) |
| evidence | [source-map](./page-contracts/evidence/source-map.md)、[requirement-traceability](./page-contracts/evidence/requirement-traceability.md)、[claim-register](./page-contracts/evidence/claim-register.md) |

所有页面仅供模板质量审阅；它们不具备任何执行或逆向授权。

## 本轮审阅问题

- 每个页面是否有不能与其他页面互换的读者问题和内容形状？
- 每个表、图和 unknown/blocked 是否有具体目的，而非通用提示语？
- 方法论是否只采纳适用于该页的结构要素，没有装饰性堆砌？
- 完整示例是否足以让作者理解如何展开，又不会诱导复制业务事实？

任何问题均应以页面、区块和具体原因记录为 `rework_required` 或 `blocked`；本草案不会因目录或
文字量自动被视为合格。

## 生产消费入口

消费者必须从 [Pack manifest](./pack.yaml) 解析公开资产、digest 与页面的正向示例和审阅项关系；不得将
`v2-draft` 作为生产路径或自行枚举本目录。
