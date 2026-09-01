---
page_id: evidence.source-map
slot: evidence
template_kind: page_contract
status: pending_human_quality_review
---

# 来源地图模板

## 读者问题

本模块消费哪些静态来源、各来源用于说明什么、怎样通过相对路径和锚点深挖、哪些来源定位质量不足？

## 静态来源角色

本页是 Source Ref 的人读地图，不重复 claim 正文；来源类型、范围和锚点必须可回查。

## 落地结构

### 1. 来源图阅读边界

说明 Source Ref 不是实现结论：需求、设计、代码、测试各自能支持什么，不能支持什么。

### 2. 来源定位账本

| source unit | 来源角色 | 静态 baseline | 相对路径与锚点 | owner page | 用于何事实 | 定位质量 | evidence state | evidence sufficiency | 深挖入口 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 3. 定位质量与阻断

| 来源 | 定位问题 | 影响 | 已查范围 | 下一入口 |
| --- | --- | --- | --- | --- |

### 4. 深挖入口

按能力、实现、接口、验证和 claim-register 链接；不把完整来源表复制到所有页面。

## 完整正向示例

### 来源图阅读边界

产品需求说明草稿目标；代码定位当前处理器；测试说明空标题验证。三者不能互相升级。

### 来源定位账本

| source unit | 来源角色 | 静态 baseline | 相对路径与锚点 | owner page | 用于何事实 | 定位质量 | evidence state | evidence sufficiency | 深挖入口 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| release-notes-prd | intent | `abc1234` | `docs/prd/release-notes.md#生成草稿` | `capability/overview.md` | 需求追踪的意图 | exact_anchor | not_established | supported | `evidence/requirement-traceability.md` |
| release-notes-code | implementation | `abc1234` | `src/service/draft.ts#create` | `implementation/architecture.md` | 草稿服务实现事实 | exact_symbol | established | supported | `implementation/components.md` |
| release-notes-tests | verification | `abc1234` | `tests/title.test.ts#rejects-empty-title` | `verification/test-matrix.md` | 空标题验证行为 | exact_test | established | supported | `verification/known-gaps.md` |

### 定位质量与阻断

| 来源 | 定位问题 | 影响 | 已查范围 | 下一入口 |
| --- | --- | --- | --- | --- |
| `docs/design.md` | 仅章节无具体操作锚点 | 只能作为 context | 设计目录 | `evidence/requirement-traceability.md` |

## 模板审阅项

- 是否说明每类来源的支持边界，而非只列路径？
- 每行是否有 source unit、来源角色、baseline、owner page、“用于什么”、定位质量和深挖入口？
- evidence state 与 evidence sufficiency 是否分开，且没有把需求来源升级为实现事实？
- 定位问题是否说明会阻断哪类结论？
