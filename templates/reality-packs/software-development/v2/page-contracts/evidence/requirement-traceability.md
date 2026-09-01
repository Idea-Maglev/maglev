---
page_id: evidence.requirement-traceability
slot: evidence
template_kind: page_contract
status: pending_human_quality_review
---

# 需求追踪模板

## 读者问题

哪些需求或设计预期关联哪些 canonical fact、直接实现证据和验证；哪里发生断链，如何复核而不把需求当成
实现事实？

## 静态来源角色

需求/设计是意图或协议 context；代码/配置/数据库是直接实现来源；测试是验证边界。追踪关系必须逐行
表达，不用 Registry 标识串或模块来源表代替。

## 落地结构

<!-- reality:section
id: requirement-baseline
shape: table
required_roles: [intent, design_protocol]
optional_roles: []
binding: source-to-scope-and-exclusion
on_missing: row_specific_unknown
-->
### 1. 需求基线与适用范围

| 需求/设计来源 | 版本/锚点 | 本页用途 | 排除范围 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- |

<!-- reality:section
id: traceability-matrix
shape: matrix
required_roles: [intent, implementation]
optional_roles: [verification, design_protocol]
binding: expected-to-claim-to-implementation-to-verification
on_missing: row_specific_unknown
-->
### 2. 需求—事实—实现—验证矩阵

| 预期/约束 | canonical fact | 直接实现证据 | 测试/验证 | owner page | 状态/边界 |
| --- | --- | --- | --- | --- | --- |

<!-- reality:section
id: gaps-and-conflicts
shape: table
required_roles: [intent]
optional_roles: [design_protocol, implementation, verification]
binding: gap-to-searched-scope-to-impact-to-next-entry
on_missing: blocked
-->
### 3. 断链、冲突与未知

| 需求/事实 | 缺少或冲突的环节 | 已查依据 | 影响 | 下一静态入口 |
| --- | --- | --- | --- | --- |

<!-- reality:section
id: review-path
shape: narrative
required_roles: [intent]
optional_roles: [design_protocol, implementation, verification]
binding: section-bindings-to-relative-review-links
on_missing: blocked
-->
### 4. 深挖与复核

给出复核问题、owner page、来源锚点和测试入口；不复制 claim 说明。

## 完整正向示例

### 需求基线与适用范围

| 需求/设计来源 | 版本/锚点 | 本页用途 | 排除范围 | 状态 |
| --- | --- | --- | --- | --- |
| `docs/prd/release-notes.md#标题` | 当前归档版本 | 标题约束的意图 | 不证明 UI 文案或 exit code | not_established | supported |

### 需求—事实—实现—验证矩阵

| 预期/约束 | canonical fact | 直接实现证据 | 测试/验证 | owner page | 状态/边界 |
| --- | --- | --- | --- | --- | --- |
| 标题不得为空 | 空标题被拒绝 | `src/validation/title.ts#rejectEmpty` | `tests/title.test.ts#rejects-empty-title` | `capability/business-rules.md` | established |

### 断链、冲突与未知

| 需求/事实 | 缺少或冲突的环节 | 已查依据 | 影响 | 下一静态入口 |
| --- | --- | --- | --- | --- |
| 草稿需人工审批 | 未定位策略或实现 | PRD 仅说明待审阅 | 不声明审批已实现 | `operations/permissions.md` |

### 深挖与复核

复核“空标题被拒绝”时，先看业务规则页的事实表，再定位验证器和命名测试；不要仅凭需求锚点或
`CLM-*` 标识认定实现成立。

## 模板审阅项

- 四个区块是否分别回答范围、映射、断链和复核？
- 矩阵是否强制区分意图、直接实现和验证？
- 断链是否说明缺少的具体环节和影响？
