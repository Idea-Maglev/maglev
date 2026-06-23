# Spec: project_board_skill

## 意图

为所有 Maglev 化项目提供标准的项目看板能力，以动态、可持久化的方式展示正在推进的需求、流程阶段和角色状态。

## 问题陈述

当前 Maglev 缺少项目级的需求观测机制：

1. `docs/DASHBOARD.md` 仅是 Maglev 自身的静态快照，不可复用、无时效性
2. 团队成员无法快速了解"当前有哪些需求在跑、各自到哪了、谁在主导"
3. 没有稳定的更新机制和文件结构，无法形成使用习惯

## 目标

- 新建标准 Skill `project-board`，可部署到所有 Maglev 化项目
- 基于 spec 文件 + 代码变更 + 测试覆盖的交叉证据，动态判断每个需求所处的主流程阶段
- 映射铁三角角色（VO/TP/XG）在每个需求上的参与状态
- 提供两级看板（总看板 + 需求子看板），持久化到仓库固定路径
- 通过生命周期事件驱动更新，让团队养成使用习惯

## 状态

- [x] 意图确认
- [x] 需求定义
- [x] 方案设计
- [ ] 实施计划
- [ ] 实施
- [ ] 验证

## 审批记录

- checkpoint: requirement_handoff
- result: approved
- artifacts_reviewed: functional_requirements (01_requirements.md)
- summary: "7 FR / 18 AC，InScope/OutScope 确认，进入方案设计"
- timestamp: 2026-04-14

- checkpoint: spec_final
- result: approved
- artifacts_reviewed: 00_index.md, 01_requirements.md, 02_design.md, 03_plan.md
- summary: "4 模块架构 + Mermaid 看板 + 7 设计决策，进入实施"
- timestamp: 2026-04-15
