# Repository Map (仓库映射)

> 本文件记录当前 Maglev 治理范围内的所有代码仓库。
> **Last Updated**: {YYYY-MM-DD}
> **Maintainer**: AI / Human (在初始化时由 Bootstrapper 生成，后续可手动更新)

## 目的 (Purpose)
此文件是 Maglev 系统了解代码仓库位置的**唯一配置来源**。
- `Atomizer` (智能助手) 会读取此文件来判断项目是否有代码。
- `maglev-map-maker` (制图师) 会读取此文件来绘制项目地图。

---

## 代码仓库列表

| 仓库名称 | 路径 | 类型 | 状态 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| example-frontend | `./example-frontend` | Frontend | Active | Vue 3 SPA 示例前端 |
| example-backend | `./example-backend` | Backend | Active | Spring Boot 示例后端 |

> **Note**: 这是模板示例，请在初始化时替换为您的实际仓库信息。

---

## 目录结构参考 (Starter Kit)

- `.agents/` - Maglev AI Agent 技能与工作流
- `.maglev/` - 配置
- `docs/` - 文档与思考
    - `thinking/` - 决策日志
- `specs/` - Maglev 规格说明书
    - `10_reality/` - 现状 (Current State)
    - `20_evolution/` - 演进 (Evolution)
        - `intake/` - 原始素材仓库 (PRD/Design Docs/Raw Assets)
        - `active/` - 进行中的 Spec
    - `templates/` - 标准 Spec 模板

---

## 类型说明 (Type Legend)

| 类型 | 说明 |
| :--- | :--- |
| **Frontend** | 前端应用 (Vue, React, Angular, etc.) |
| **Backend** | 后端服务 (Spring, Node, Go, Python, etc.) |
| **Library** | 共享库/工具类 |
| **Monorepo** | 单体仓库 (包含多个子项目) |
| **Other** | 其他类型 |

## 状态说明 (Status Legend)

| 状态 | 说明 |
| :--- | :--- |
| **Active** | 正在积极开发 |
| **Stable** | 已稳定，仅维护 |
| **Deprecated** | 已废弃，计划移除 |

---

## 关键入口
- 规格索引: `specs/README.md`
- 文档首页: `README.md`

## 如何更新 (How to Update)
1. 手动编辑此文件，添加/修改 "代码仓库列表" 表格行。
2. 或者运行 `/maglev-init` 重新触发交互式注册。
