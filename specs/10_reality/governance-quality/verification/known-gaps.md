---
reality_id: governance-quality.verification.known-gaps
title: 治理与质量已知缺口
owner_domain: governance-quality
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 治理面当前无法闭环验证的缺口及关闭条件
  excludes:
    - 已建立事实（属各页面）
---
# 治理与质量已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| hooks 观测 | evidence/hooks-observability | 跨项目会话统计不可宣称，只能宣称机制与单测锚点 | open |
| 纪律执行 | capability/overview | 红线执行只能是静态契约级陈述 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| hooks 观测的跨项目会话统计无本轮直接证据 | 本轮未实际运行 exporter 取样；仅有脚本与单测锚点 | 仅有机制证据，无运行输出 | 跨项目统计不可宣称 | `../evidence/hooks-observability.md` |
| maglev-discipline 红线执行是静态契约 | 纪律遵循发生在会话行为中，仓库静态证据无法证明"每次主流程都执行了红线" | 行为不在静态可证范围 | 执行保证只能表述为契约 | `../capability/overview.md` |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| trace 完整性 | "hooks trace 是审计日志" | 竞争丢弃使其只是 best-effort 观测旁路，不是审计级完整日志 | ✗"有记录即完整" |
| 测试覆盖 | "测试体系覆盖了全部协议脚本" | 覆盖范围以 tests/ 实际模块为准，未列即未覆盖 | ✗"有测试体系即全覆盖" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| hooks 跨项目统计 | 在多项目工作区运行 export_hooks_trace_snapshot.py 并留存快照 | 再次阅读脚本 | `../evidence/hooks-observability.md` |
| 红线执行 | hooks trace 长期数据积累后按事件统计 | 单次会话自述遵守 | `../capability/overview.md` |
