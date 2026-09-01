---
name: confirm-readiness
description: 判断当前是否已具备进入现实结晶阶段的条件
next_step: references/step-02-judge-writeback.md
---

# Step 1: Confirm Readiness

## 目标

确认当前主题的变化是否已经成立到足以进入现实结晶。

## 动作

1. 检查当前主题是否已通过实现层综合验证，具备形成 Reality Projection 的依据。
   `integrated-validator` 的旧报告只证明 requirements/spec/code/tests，不替代完整
   Reality 投影验证。
2. 如果结果来自逆向链，检查 `reverse_work_contract`、`reverse_module_map`、Gate A/B、
   逐模块 `semantic_review_package` 和三层 `reverse_review_result` 是否绑定同一 baseline、
   candidate commit、Template Pack 和 Reality digest。
3. 判断哪些变化已经成立，哪些仍只是过程草稿。
4. 若尚未成立，明确指出阻塞项。
5. 输出唯一判断：
   - `ready_to_crystallize`
   - `not_ready_to_crystallize`

## 通过标准

至少同时满足：

1. 当前主题的关键结果已经成立
2. 主要阻塞已被验证或显式解除
3. 当前已能区分“新事实”与“过程草稿”
4. 当前分支能够明确记录 Reality 修改前的 base commit
5. 若经过逆向链，Gate A、Gate B 和 structure/content/confidence 三层结果均已通过
6. 已确认项目级入口页和模块页面的目标路径，且所有路径均由 Profile 或模板包声明

## 输出格式

- `crystallization_gate`
- `established_changes`
- `blockers`

## 输出

- 一份结晶条件判断
- 一组 blocker 或已成立结果
