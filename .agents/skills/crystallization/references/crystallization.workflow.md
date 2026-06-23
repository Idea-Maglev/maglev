---
name: crystallization
description: 在综合验证后完成现实回写、active 收口与可发现性回填
output_folder: .agents/skills/crystallization
---

# Crystallization Workflow

**Goal**: 在主流程后段完成事实状态闭环，把已成立结果沉淀为新的项目现实。

## 流程 (Process)

1. 结晶条件确认
2. 现实回写判定
3. active 状态收口
4. 可发现性回填
5. 结构化归档（仅当 Step 3 判定 close 时）

## 进入条件 (Entry Conditions)

- 当前主题已完成主要实施
- 已具备进入后段闭环的必要依据
- 需要判断 Reality 回写、active 收口或可发现性回填

## 退出条件 (Exit Conditions)

满足以下任一条件即可结束本次结晶：

1. 明确给出 Reality 回写、active 状态和可发现性回填结论
2. 明确给出 `not_ready_to_crystallize` 与阻塞项，停止继续结晶

## 最小产物 (Minimum Deliverables)

- 结晶条件结果
- 写回范围判断
- active 状态结论
- 回填动作清单

## 步骤架构

- **Micro-Steps**: 严格遵循 `step-*.md`
- **Isolation**: 内存中只加载当前步骤

## 初始化

1. 阅读 `references/step-01-confirm-readiness.md`
