---
name: review-validation-surface
description: 对实现结果做统一 review 与 validation
output_folder: .agents/skills/review-validation-surface
---

# Review Validation Surface Workflow

**Goal**: 在结果层统一做 review 与 validation，而不是让前后端 review skill 碎片化平铺。

## 流程 (Process)

1. 识别普通实现结果或 Reality 结果分支
2. 加载 review 上下文
3. 检查实现合规性
4. 检查质量与风险
5. Reality 结果额外分别汇总 structure、content、confidence
6. 汇总 findings

## 进入条件 (Entry Conditions)

- 当前已有代码、变更或结果产物可审
- 需要在结果层统一 review，而不是直接跳到综合验证
- Reality 分支还必须有 Work Contract、Module Map、Gate A/B 和目标 Reality 结果

## 退出条件 (Exit Conditions)

1. 已输出统一 findings
2. 已明确下一步是修正、继续还是转交
3. Reality 结果已保留三层状态，未被健康度评分或普通实现结论覆盖

## 最小产物 (Minimum Deliverables)

- 上下文加载结果
- 合规性检查结果
- 质量风险检查结果
- findings 汇总
