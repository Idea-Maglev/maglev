---
name: evolution-observatory
description: 持续进化观测 skill：通过 registry 驱动的 6 Phase 竞品观测循环，持续研究行业框架、维护 insight 生命周期，并为 Maglev 提供可追溯的改进养分。
metadata:
  formal_action_name: 持续进化观测
  top_level_capability: 能力进化
  system_layer: Evolution & Governance Layer
  lifecycle_chain: observatory_loop
  runtime_name_status: canonical_name_active
  distribution_scope: private_only
  author: Maglev contributors
  version: 1.0.0
  last_updated: 2026-06-04
  state_source: specs/10_reality/competitive_registry.yaml
  commit_prefix: research(observatory)
---

# Evolution Observatory (持续进化观测)

> 结构动作名：`持续进化观测`
> 运行面名称：`evolution-observatory`

## 概览 (Overview)

这是一个**持续竞争情报与自我进化驱动工具**。通过系统化地观察、分析、学习行业框架，为 Maglev 提供可追溯的改进养分。

## 元信息

- **状态源**: `specs/10_reality/competitive_registry.yaml`
- **归档约定**: `research(observatory): {description}`
- **默认输入**: Registry 驱动的竞品/框架研究对象
- **定位锚点**: 每轮研究前先读 `specs/10_reality/positioning.md`

底层采用"通用持续情报净化循环"模式，当前 instance 配置为：**观测 AI 协作框架领域**。

核心能力：

- **竞品注册表管理**：维护结构化的观察对象清单（横向竞品 + 垂域参考）
- **结构化研究执行**：按 mandatory + exploratory 维度深度对比
- **Insight 生命周期追踪**：open → proposed → absorbed / superseded
- **新竞品自动发现**：每轮研究探索行业新动态
- **执行自检闭环**：checklist 确保每轮研究完整性

## 何时使用 (When to use)

- 想要深入分析某个行业框架/竞品与 Maglev 的对比时
- 想要系统性巡检已有竞品的最新动态时
- 想要发现新的值得关注的框架/产品时
- 想要了解哪些研究洞察还未被 Maglev 消化时
- 距上次研究已过较长时间，需要更新 Registry 时

## 触发条件 (Triggers)

- `"启动进化观测"`
- `"研究一下 {框架名}"`
- `"对比 Maglev 和 {竞品}"`
- `"检查竞品动态"`
- `"看看有什么新的框架值得关注"`
- `"哪些 insight 还没消化"`

## 交互模式 (Interaction)

- **Role**: 你是 **Observatory Analyst (观测分析师)**。
- **Protocol**: 行动前必须阅读完整步骤文件（`references/workflow.md`），严格遵循 Phase 0 + 6 Phase 顺序。
- **Phase 0 (Self-Knowledge Anchor)**: 每轮研究**开始前**必须先读 `specs/10_reality/positioning.md`，确保对 Maglev 定位、边界和与外部工具关系的理解是正确的。没有这一步的锚定，所有对比都可能方向错误。
- **State Source**: `specs/10_reality/competitive_registry.yaml` 是唯一状态源（竞品清单 + insight 状态）。每次启动时必须先读取。
- **Trigger**: 由人（Creator）主动触发，AI 不自动启动研究。
- **Insight Review**: 每轮 Phase 2 对所有 open insights 做有效性重评估。
- **Superseded Gate**: 建议标记 superseded 时必须等待 Creator 确认，不可自动执行。
- **Hard Gate**: 自检 checklist 未全部通过时，不可标记本轮完成。

## 必需的参考资料 (References)

- 工作流入口: `references/workflow.md`
- Insight 生命周期: `references/insight-lifecycle.md`
- 对标维度: `references/dimensions.md`
- 报告模板: `references/output-template.md`
- 自检清单: `references/self-check.md`
- 状态文件: `specs/10_reality/competitive_registry.yaml`
- 报告归档: `docs/thinking/10_critique/`

## 快速参考

- **Pattern**: Entry → Phase 0 (Self-Knowledge) → 6 Phase Workflow（Scope → Review → Research → Discovery → Output → Check）
- **分层**: 通用层（workflow / insight-lifecycle / self-check）+ 配置层（dimensions / output-template）
- **输出**: 研究报告（Markdown）+ Registry 更新（YAML）+ Insight 记录
- **Commit 约定**: `research(observatory): {description}`

## 编组关系

| 关系 | 目标 | 说明 |
|------|------|------|
| → feeds | `spec-designer` | insight(proposed) 可作为 spec 设计输入 |
| → complements | `knowledge-check` | 研究报告沉淀到 docs/thinking/ |
| → triggers | `crystallization` | insight(absorbed) 触发 reality 更新 |
| ↔ complements | `skill-scout` | 发现优化方向可触发 scout 寻找外部实现 |
| ← called_by | `skill-squadron` | 编队巡逻可纳入本 skill |

## 示例

User: "研究一下 Superpowers 最新版本"
AI: "收到。读取 Registry... Superpowers 上次研究 2026-05-25 (v5.1.0)。开始 Phase 1: Scope & Plan。本轮研究计划：对象=Superpowers latest，维度=M1~M6 + 可能的 E 维度。确认后开始深度研究。"

User: "检查竞品动态"
AI: "收到。读取 Registry... 当前观察 7 个对象。按'距上次研究最久 + 活跃度最高'排序推荐：1. BMAD (last: 2026-02-23, activity: medium)  2. OpenSpec (last: 2026-02-23, activity: medium)。请选择本轮研究对象。"

User: "哪些 insight 还没消化"
AI: "读取 Registry... 当前 open insights: SP-001 (Subagent 模式, medium), SP-002 (Visual Companion, low)... 共 N 条。是否需要逐条 review 有效性？"
