---
page_id: evidence.claim-register
slot: evidence
template_kind: page_contract
status: pending_human_quality_review
---

# 事实账本模板

## 读者问题

当前有哪些 canonical claim、每条 claim 的状态和证据相容性是什么、冲突或未知由谁拥有和如何深挖？

## 静态来源角色

Claim Registry 是机器 canonical record，本页是中文账本视图。不得复制每个 owner page 的长正文，
也不得把 claim id 当作事实句。

## 落地结构

### 1. 账本阅读边界

说明 `established`、`unknown`、`not_established`、`not_applicable` 各表示什么，并单独说明
`supported`、`partial`、`missing`、`blocked` 的证据充分度；强调状态来自来源角色与证据，而不是
语言流畅度。

### 2. 中文事实账本

| 中文事实 | 知识状态 | 证据充分度 | 直接证据 | context 来源 | owner page |
| --- | --- | --- | --- | --- | --- |

### 3. 证据相容性与未知项

| claim | 相容/冲突说明 | 缺少的直接证据 | 处理方式 | 深挖 |
| --- | --- | --- | --- | --- |

### 4. 相关页面与深挖

按 owner page 聚合链接；不把账本扩展为模块全部来源地图。

## 完整正向示例

### 账本阅读边界

`established` 表示存在相容的直接静态来源；`not_established` 表示只有需求或设计背景，当前不能
成立实现事实；`unknown` 表示范围内尚未定位足够来源；`not_applicable` 表示有依据地不适用。
证据充分度另记为 `supported`、`partial`、`missing` 或 `blocked`，不能与知识状态混用。

### 中文事实账本

| 中文事实 | 知识状态 | 证据充分度 | 直接证据 | context 来源 | owner page |
| --- | --- | --- | --- | --- | --- |
| 空标题会在验证器中被拒绝 | established | supported | `src/validation/title.ts#rejectEmpty` | `docs/prd/release-notes.md#标题` | `capability/business-rules.md` |
| 草稿保存需要人工审批 | not_established | missing | 未定位 | `docs/prd/release-notes.md#待审阅` | `operations/permissions.md` |

### 证据相容性与未知项

| claim | 相容/冲突说明 | 缺少的直接证据 | 处理方式 | 深挖 |
| --- | --- | --- | --- | --- |
| 人工审批 | 需求有意图，未有策略实现 | Guard、配置或测试 | 保持 unknown | `operations/permissions.md` |

### 4. 状态与证据审阅

| 检查项 | 要求 |
| --- | --- |
| 知识状态 | 只使用 Reality Contract 的 canonical 值，不新增 `context_only` 等别名 |
| 证据充分度 | 单独记录直接来源是否充分，不能用 `high/low` 或文字流畅度替代 |
| context 来源 | 只能说明意图或背景，不得升级为实现、授权或验证事实 |
| 未知与阻断 | 必须绑定 owner page、缺失原因和下一处静态深挖入口 |

## 模板审阅项

- 中文事实是否先于 claim 标识出现？
- context 来源是否没有被当成直接实现证据？
- 知识状态与证据充分度是否分开记录？
- unknown/blocked 是否能回到 owner page 和下一证据入口？
