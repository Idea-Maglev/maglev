---
name: step-05-quality-gate
description: 根据证据输出质量等级和可声明能力
next_step: null
---

# Step 5: Quality Gate

## 目标

让每支小队的能力声明与证据一致，避免后续使用者误以为“设计过”就等于“运行稳定”。

## 动作

1. 对照 `collaboration-quality-rubric.md` 判定 L0-L3。
2. 对照 `scenario-test-matrix.md` 检查关键场景是否有设计或测试。
3. 对照 `runtime-proof-gate.md` 判断是否完成真实 Runtime Proof。
4. 检查共享产物准入、有限调度、人类角色路由和非侵入式审查的场景证据。
5. 输出 `squad_quality`，并限制 `allowed_claim`。

## 输出

```yaml
squad_quality:
  design_level: L0 | L1 | L2 | L3
  adapter: maglev | custom | none
  routing_responsibility: configured | missing
  collaboration_contract: pass | fail
  adapter_contract: pass | fail | not_applicable
  template_validation: pass | fail | not_applicable
  runtime_proof: pass | pending | not_run
  allowed_claim:
    - draft
    - collaboration_designed
    - template_verified
    - runtime_verified
  evidence:
    - ...
  remaining_risks:
    - ...
```

Review 质量门还必须记录：

- 生产者 skill 是否被只读追溯，以及来源是 `verified`、`partial`、`unverified` 还是 `conflict`。
- Review Packet 是否包含事实证据、影响、修复责任角色、阻塞条件和复审要求。
- 反馈是否只路由一个主修复角色，且修复后由独立角色复审；复审前不能标记 `resolved`。

## 判定规则

- `collaboration_contract: fail` 时最高只能是 L0。
- `adapter: none` 时最高只能是 L1。
- `adapter_contract` 为 `fail` 或 `not_applicable` 时最高只能是 L1。
- `template_validation` 为 `fail` 或 `not_applicable` 时最高只能是 L1。
- `routing_responsibility: missing` 时不能声明协同契约通过。
- L3 必须同时满足 L2 全部证据为 `pass`，且 `runtime_proof: pass`。
- `runtime_proof` 不是 `pass` 时不得包含 `runtime_verified`。
