---
page_id: implementation.visual
slot: implementation
template_kind: page_contract
status: pending_human_quality_review
---

# 视觉与交互实现模板

## 读者问题

模块是否有可定位的界面、路由、组件和静态交互关系；若无界面，边界是“不适用”还是“尚未发现”？

## 静态来源角色

产品需求说明用户交互意图；路由、组件、样式和前端测试证实界面实现。后端模块不能因未发现前端目录
自动判定无界面。

## 落地结构

### 1. 界面范围

| 视图/区域 | 面向用户任务 | 需求依据 | 路由/入口 | 状态 |
| --- | --- | --- | --- | --- |

### 2. 路由与组件目录

| 路由/入口 | 组件 | 主要交互 | 实现锚点 | 关联 API/状态 |
| --- | --- | --- | --- | --- |

### 3. 静态交互关系

只有组件、动作和调用关系均可定位时才作图；否则使用交互表并保留 unknown。

| 入口/组件 | 前置状态 | 用户动作 | 结果/失败状态 | 实现锚点 | API/数据连接 |
| --- | --- | --- | --- | --- | --- |

### 4. 无界面或未知边界

| 判断 | 范围与依据 | 不能说明什么 | 深挖入口 |
| --- | --- | --- | --- |

### 5. 前端实现边界

| 维度 | 当前事实 | 直接来源 | 未证实边界 |
| --- | --- | --- | --- |
| 用户任务与页面入口 |  |  |  |
| 视图/组件与状态 |  |  |  |
| 前端源文件与样式 |  |  |  |
| API、Store 或数据连接 |  |  |  |

## 完整正向示例

### 界面范围

| 视图/区域 | 面向用户任务 | 需求依据 | 路由/入口 | 状态 |
| --- | --- | --- | --- | --- |
| 发布说明草稿面板 | 发布者查看并编辑草稿 | `docs/prd/release-notes.md#草稿编辑` | `/release-notes/draft` | established |

### 路由与组件目录

| 路由/入口 | 组件 | 主要交互 | 实现锚点 | 关联 API/状态 |
| --- | --- | --- | --- | --- |
| `/release-notes/draft` | `DraftEditor` | 加载、编辑、保存草稿 | `web/routes/draft.tsx#DraftEditor` | `interfaces/api.md#保存草稿` |

### 静态交互关系

```mermaid
flowchart LR
    Route[草稿路由] --> Editor[编辑器组件]
    Editor --> Save[保存动作]
    Save --> Api[保存接口]
```

### 前端实现边界

| 维度 | 当前事实 | 直接来源 | 未证实边界 |
| --- | --- | --- | --- |
| 用户任务与页面入口 | 发布者在草稿路由编辑内容 | `docs/prd/release-notes.md#草稿编辑`；`web/routes/draft.tsx#DraftEditor` | 移动端入口 unknown |
| 视图/组件与状态 | `DraftEditor` 处理加载、编辑和保存 | `web/routes/draft.tsx#DraftEditor`；`web/components/DraftEditor.tsx#state` | 离线恢复 unknown |
| 前端源文件与样式 | 路由和编辑器组件位于 Web 前端 | `web/routes/draft.tsx`；`web/components/DraftEditor.tsx` | 视觉设计稿 unknown |
| API、Store 或数据连接 | 保存动作调用草稿保存接口 | `interfaces/api.md#保存草稿` | 错误重试策略 unknown |

### 无界面或未知边界

| 判断 | 范围与依据 | 不能说明什么 | 深挖入口 |
| --- | --- | --- | --- |
| unknown | 仅冻结范围未发现移动端入口 | 不证明不存在其他客户端 | `implementation/dependencies.md` |

## 模板审阅项

- 是否区分“没有界面证据”和“经完整范围证明不适用”？
- 每个可见区域是否有用户任务、入口、组件、状态和实现锚点？
- 是否能沿前端源文件继续定位 API、Store 或数据连接？
- 是否说明了尚未证实的客户端、状态或体验边界？
- 图是否只描述静态可定位的交互？
