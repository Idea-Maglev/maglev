---
page_id: implementation.components
slot: implementation
template_kind: page_contract
status: pending_human_quality_review
---

# 组件模板

## 读者问题

哪些组件承担关键职责、怎样协作、实现锚点在哪里、哪些候选组件尚不能确认其作用？

## 静态来源角色

代码、依赖注入/注册、配置和测试是组件事实来源；架构设计只能说明预期职责。

## 落地结构

### 1. 组件目录

| 组件 | 类型 | 职责摘要 | 代码锚点 | 状态 |
| --- | --- | --- | --- | --- |

### 2. 职责与协作

| 组件 | 接收什么 | 产生什么 | 协作对象 | 不能承担的责任 |
| --- | --- | --- | --- | --- |

### 3. 实现锚点与边界

| 组件 | 关键入口 | 读取/写入边界 | 测试/验证锚点 | 关联页 |
| --- | --- | --- | --- | --- |

### 4. 未解析组件

| 名称/位置 | 为什么尚未归类 | 已查依据 | 下一步 |
| --- | --- | --- | --- |

## 完整正向示例

### 组件目录

| 组件 | 类型 | 职责摘要 | 代码锚点 | 状态 |
| --- | --- | --- | --- | --- |
| `DraftService` | 服务 | 根据已选变更生成草稿 | `src/service/draft.ts#DraftService` | established |
| `EntryStore` | 存储适配器 | 查询已选变更 | `src/store/entries.ts#listSelected` | established |

### 职责与协作

| 组件 | 接收什么 | 产生什么 | 协作对象 | 不能承担的责任 |
| --- | --- | --- | --- | --- |
| `DraftService` | 发布周期与变更集合 | 草稿对象 | `EntryStore`、`DraftWriter` | 不负责发布到外部渠道 |
| `EntryStore` | 查询条件 | 已选变更集合 | 本地记录 | 不决定草稿格式 |

### 实现锚点与边界

| 组件 | 关键入口 | 读取/写入边界 | 测试/验证锚点 | 关联页 |
| --- | --- | --- | --- | --- |
| `DraftService` | `create` | 读取 entries，写入 draft | `tests/draft.test.ts#creates-draft` | `verification/test-matrix.md` |

### 未解析组件

| 名称/位置 | 为什么尚未归类 | 已查依据 | 下一步 |
| --- | --- | --- | --- |
| `formatters/legacy.ts` | 仅发现导入，未定位调用职责 | `src/service/draft.ts#imports` | `implementation/dependencies.md` |

## 模板审阅项

- 组件是否按责任和边界列出，而非按所有文件罗列？
- 协作是否说明输入、输出和不负责什么？
- 未解析项是否保留位置与下一步，而不猜测用途？
