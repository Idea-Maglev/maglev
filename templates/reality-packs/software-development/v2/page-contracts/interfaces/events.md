---
page_id: interfaces.events
slot: interfaces
template_kind: page_contract
status: pending_human_quality_review
---

# 事件与消息契约模板

## 读者问题

哪些消息由谁发送或接收、channel 和 payload 如何定义、顺序、重试和恢复哪些已有证据、哪些不能推断？

## 静态来源角色

AsyncAPI/设计资料说明消息契约意图；生产者、消费者、消息类型、绑定配置和测试证实静态实现。

## 落地结构

### 1. 事件范围与方向

| 事件 | 本模块角色 | 发送方/接收方 | 触发意图 | 状态 |
| --- | --- | --- | --- | --- |

### 2. 消息与 channel 契约

| 事件 | channel/topic | payload/关键字段 | 定义锚点 | 实现锚点 |
| --- | --- | --- | --- | --- |

### 3. 交付、顺序与恢复边界

| 事件 | 已证实语义 | 未证实语义 | 依据 | 深挖 |
| --- | --- | --- | --- | --- |

### 4. 未证实事件

| 候选事件 | 为什么无法成立 | 已查范围 | 下一入口 |
| --- | --- | --- | --- |

## 完整正向示例

### 事件范围与方向

| 事件 | 本模块角色 | 发送方/接收方 | 触发意图 | 状态 |
| --- | --- | --- | --- | --- |
| `draft.created` | 发送者 | 草稿服务 → 通知适配器 | 草稿生成后通知下游 | established |

### 消息与 channel 契约

| 事件 | channel/topic | payload/关键字段 | 定义锚点 | 实现锚点 |
| --- | --- | --- | --- | --- |
| `draft.created` | `release-notes.draft` | `draftId`、`title` | `api/asyncapi.yaml#draftCreated` | `src/events/publish.ts#draftCreated` |

### 交付、顺序与恢复边界

| 事件 | 已证实语义 | 未证实语义 | 依据 | 深挖 |
| --- | --- | --- | --- | --- |
| `draft.created` | 发布调用存在 | 投递至少一次、顺序、重试 unknown | 发布函数与消息定义 | `operations/errors.md` |

### 未证实事件

| 候选事件 | 为什么无法成立 | 已查范围 | 下一入口 |
| --- | --- | --- | --- |
| `draft.deleted` | 未发现消息定义或发布调用 | `api/asyncapi.yaml`、`src/events/` | `implementation/components.md` |

## 模板审阅项

- 是否分别表达发送/接收方向和 channel，而不把事件名当完整契约？
- 是否把投递、顺序、重试列为需证实的边界？
- 无事件是否通过范围与查询依据表达，而非留空？
