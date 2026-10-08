---
reality_id: collaboration-lifecycle.capability.multica-squad-kit
title: Multica Squad Kit 能力
owner_domain: collaboration-lifecycle
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - Squad Kit 的五套小队模板、角色拓扑、质量分级上限与 Maglev/Multica 责任边界
  excludes:
    - 包内模块与命令的实现结构（属 implementation/multica-squad-kit.md）
    - 测试证明力与 Runtime 证据状态（属 verification/multica-squad-kit.md）
---

# Multica Squad Kit 能力

## 1. 能力定位与受益者

`packages/maglev-multica-kit/`（包名 `@idea-maglev/maglev-multica-kit`，版本 `0.2.4`）把 Maglev 的多角色协作适配为可安装、可校验、可升级的 Multica 小队模板工具包。Multica 是第三方运行承载；需求、方案、仓库产物、验证证据和 Reality 等项目质量事实保留在 Maglev 侧。

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 已初始化 Maglev 的目标仓库 | 获得覆盖主流程的小队模板 | `maglev-complete@0.4.0`（`default: true`，9 角色） | `assets/squad-templates/catalog.yaml`；`maglev-complete/manifest.yaml` |
| 未完成初始化的存量仓库 | 获得只读接入与 Reality 建模小队 | `maglev-legacy-onboarding@0.2.1`（7 角色） | `catalog.yaml`；`maglev-legacy-onboarding/manifest.yaml` |
| 低配置成本的使用者 | 用少量 Agent 覆盖流程 | `maglev-complete-lite@0.1.1`、`maglev-legacy-onboarding-lite@0.1.2`（各 3 角色：Coordinator/Generalist/Validator） | `catalog.yaml`；两套 lite `manifest.yaml` |
| 平台操作场景 | 在完整主流程上显式接入平台操作域 | `maglev-platform-operations@0.1.0`（`base_template: maglev-complete`，3 平台角色，非默认模板） | `maglev-platform-operations/manifest.yaml` |

## 2. 模板目录与角色拓扑

角色名取自各模板 `manifest.yaml` 的 `roles:` 列表；`maglev-complete` 的 9 角色为 `coordinator`、`requirement`、`design`、`scheduler`、`builder`、`challenger`、`validator`、`process_auditor`、`closure_steward`。`maglev-legacy-onboarding` 的 7 角色为 `coordinator`、`project_diagnostician`、`bootstrap_steward`、`reverse_archaeologist`、`reality_modeler`、`index_librarian`、`process_auditor`。

| 模板 | 版本 | 角色 | 定位 | 依据 |
| --- | --- | --- | --- | --- |
| `maglev-complete` | 0.4.0 | 9 | 默认完整小队：以 Coordinator 串联需求、方案、实施、审查、验证、审计与收口 | `catalog.yaml`；`maglev-complete/manifest.yaml` |
| `maglev-legacy-onboarding` | 0.2.1 | 7 | 存量项目接入：Context Clean、阶段回执、接收方准入 | `catalog.yaml`；`maglev-legacy-onboarding/manifest.yaml` |
| `maglev-complete-lite` | 0.1.1 | 3 | 三角色串联完整生命周期 | `catalog.yaml`；`maglev-complete-lite/manifest.yaml` |
| `maglev-legacy-onboarding-lite` | 0.1.2 | 3 | 三角色覆盖存量接入阶段 | `catalog.yaml`；`maglev-legacy-onboarding-lite/manifest.yaml` |
| `maglev-platform-operations` | 0.1.0 | 3（平台域） | 继承完整小队并显式接入平台操作域 | `maglev-platform-operations/manifest.yaml` |

通用小队方法由 `multica-squad-design-method` 承载，不固定角色名称；Maglev Adapter（`multica-squad-architect`）把通用方法的协调/路由责任在模板中映射为唯一的 `coordinator`，该映射是样本实现，不回写为通用方法的固定角色名。

## 3. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 通用小队设计已稳定，需要落地 Maglev | 设计包含意图、角色拓扑、协同契约 | Squad Kit 模板资产 + catalog + 测试 + `squad_quality` 声明 | `../implementation/multica-squad-kit.md` | established（Adapter 契约文本） | 契约级 |
| 目标仓库安装/升级模板 | `maglev-multica` CLI 可用 | 受管对象 plan/apply、drift 回查、self-check receipt | `../implementation/multica-squad-kit.md` | established（契约文本） | 契约级 |
| 小队运行需要质量声明 | 模板通过 self-check | 最高声明到 L2/`template_verified`；L3/`runtime_verified` 需真实第三方承载验证 | `../verification/multica-squad-kit.md` | established（分级契约） | 契约级 |

## 4. 质量分级上限（能力承诺边界）

| 等级 | 含义 | 对 Squad Kit 的当前含义 | 依据 |
| --- | --- | --- | --- |
| L0 | 只有角色清单 | 不适用：模板均含协同契约 | `.agents/skills/multica-squad-design-method/SKILL.md` 质量分级表 |
| L1 | 协同契约完整 | 模板 `squad.yaml` 的 `shared_contract` 达成 | 同上 |
| L2 | Adapter 已落地模板资产、测试和静态验证 | Maglev 侧静态验证的可声明上限 | 同上；`.agents/skills/multica-squad-architect/SKILL.md` 判定纪律 |
| L3 | 真实第三方承载端到端验证 | 当前未声明：需要真实 Runtime Proof，本仓库未用本地验证替代 | 同上；`../verification/known-gaps.md` |

## 5. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 责任边界 | 成员身份、通知、Task、状态与 Runtime 由 Multica 等第三方承载，以外部回执为准；Maglev 侧状态转移只记录意图 | `.agents/skills/multica-squad-architect/SKILL.md` 通用契约映射段 | `../verification/known-gaps.md` |
| 责任边界 | 主链路技能不感知 multica 等载体（回执等载体契约只存在于 kit 与适配层技能）；发行流水线以载体中立检查拦截窄化复发 | `scripts/check_carrier_neutrality.py`（发版 Hash & Manifest 阶段强制执行）；白名单仅 `multica-squad-architect`、`multica-squad-design-method` | `../implementation/multica-squad-kit.md` |
| 不承诺 | Lite 模板不声明与母模板相同的专业角色深度或 Agent 身份隔离 | `catalog.yaml` 中 lite 为独立模板、角色仅 3 个 | `../implementation/multica-squad-kit.md` |
| 不承诺 | `maglev-platform-operations` 不改变 Maglev 主流程、不隐式继承其他小队 skills | `.agents/skills/multica-squad-architect/SKILL.md`；其 `manifest.yaml` 仅声明平台角色 | `../verification/known-gaps.md` |
| 不承诺 | 写入任务必须具备 Work Graph、lease、基线提交、允许文件范围和项目负责人批准，模板本身不放宽 | `.agents/skills/multica-squad-architect/SKILL.md` 判定纪律 | `../verification/multica-squad-kit.md` |
| unknown | `runtime_verified` 所需的真实第三方接力证据当前不存在 | 无 Runtime Proof 记录可绑定 | `../verification/known-gaps.md` |
