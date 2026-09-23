---
reality_id: governance-quality.capability.overview
title: 治理与质量能力
owner_domain: governance-quality
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 纪律、需求来源治理、文档源治理、Hooks 观测与仓库测试体系的当前事实
  excludes:
    - 各主链路技能的业务语义（属 collaboration-lifecycle 域）
    - 代码执行插槽选择（属 skill-runtime 域）
---
# 治理与质量能力

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 会话内 agent | 在主流程中受红线与升级纪律约束 | maglev-discipline 会话级背景纪律 | `.agents/skills/maglev-discipline/SKILL.md` |
| 需求/方案作者 | 输入质量与来源完整性被审计 | spec-audit-surface 审计面（来源缺失即 blocker） | `.agents/skills/spec-audit-surface/references/step-02-audit-requirements.md` |
| 文档维护者 | 受管表面不被手工漂移 | 治理注册表驱动的生成与漂移检查 | `specs/_meta/documentation-governance.json` |
| 验证者 | 行为回归有统一入口 | unittest 测试体系（30 个测试模块） | `tests/INDEX.md` |
| 平台运营 | hooks 行为可观测 | trace 快照导出与策略独立保护 | `scripts/export_hooks_trace_snapshot.py` |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 主流程进入 | AGENTS.md 纪律区块在上下文 | 红线与升级纪律作为背景约束生效 | [已知缺口](../verification/known-gaps.md)（静态契约） | established（契约文本） | supported |
| 实施前审计 | requirements 与 spec 已成文 | 来源完整性 blocker 判定 | 需求来源治理 | established | supported |
| 主链路/发布源修改 | 治理注册表先行更新 | 受管表面重新渲染；漂移检查报 code/path/message | 文档源治理 | established | supported |
| hooks 事件发生 | trace root 可用 | 事件追加（best-effort）；deny/allow 决策不受 trace 可用性影响 | Hooks 观测 | established | supported |
| `unittest` 运行 | `.maglev/runtime/python` 就绪 | 行为回归结果；部分用例需已构建 `dist/` | 测试体系 | established | supported |
| 发版流水线 Hash & Manifest 阶段 | 发行集技能文件就绪 | 载体 token 命中即拦截发行；适配层技能（`multica-squad-architect`、`multica-squad-design-method`）在白名单内 | `scripts/check_carrier_neutrality.py`（由 `scripts/maglev_release.py` 调用） | established | supported |
| Reality 投影提交 | 投影 diff 已提交（base→candidate） | 准入只验客观可追溯性（frontmatter 身份、证据 digest、Profile 一致性、投影摘要一致），不判页面结构与措辞；占位符残留为非阻断 WARN，指引回模板包修复 | `.agents/skills/_internal/reality-admission/scripts/reality_admission.py`；同目录 `protocol/reality_contract.yaml` 角色边界声明 | established | supported |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 未证实 | 红线在每次主流程中被真实执行 | 纪律遵循发生在会话行为中，静态证据不可证 | [已知缺口](../verification/known-gaps.md) |
| 不承诺 | hooks trace 是审计级完整日志 | 竞争丢弃设计使其只是观测旁路 | Hooks 观测 |
| 不承诺 | 测试体系覆盖全部协议脚本 | 覆盖以 `tests/` 实际模块为准 | 测试体系 |
| 范围外 | 代码执行插槽选择语义 | 属 skill-runtime 域 | `../../skill-runtime/capability/overview.md` |

## 4. 事实与深挖

- 文档源治理、需求来源治理
- Hooks 观测、测试体系、[已知缺口](../verification/known-gaps.md)、Claim 登记册
