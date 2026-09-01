---
name: multica-squad-design-method
description: Use when designing or revising a Multica squad that needs explicit coordination, handoff, quality, and adapter boundaries without assuming a specific project or external carrier.
metadata:
  formal_action_name: Multica 小队设计方法
  top_level_capability: 能力进化
  system_layer: Evolution & Governance Layer
  lifecycle_chain: squad_design_lifecycle
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-08-06
---

# Multica Squad Design Method（通用 Multica 小队设计方法）

这是通用的 Multica 小队设计方法。它关注“如何稳定组织多智能体协作”，不预设目标项目已经使用 Maglev，也不预设存在 `entry-router`、Work Graph、lease、特定文件结构或特定命令行工具。

## 负责

- 将业务、运营、治理或技术目标拆成清晰的小队意图、受众、边界和成功信号。
- 设计协调/路由责任角色与成员角色拓扑，明确职责、权限、并发边界和退出条件；具体角色名称由小队配置决定。
- 定义 Multica 原生协作契约：精确 mention、新评论触发、单一下一责任人、标准 Handoff、禁止横向委派和失败排查。
- 定义 Adapter Contract，让具体项目或第三方承载把通用方法落到自己的文件、命令、权限和验证体系中。
- 通过质量分级、场景化测试矩阵和 Runtime Proof Gate 限制小队能力声明，避免“角色清单”被误称为“可运行小队”。

## 不负责

- 不替代具体项目的实现适配器；模板文件、CLI、仓库结构和发布流程由 Adapter 负责。
- 不默认调用 Maglev skill、`entry-router`、`maglev-multica` 或任何私域能力。
- 不直接创建或更新第三方承载中的对象；它只定义设计与验收方法。
- 不替代业务 Agent 的专业能力设计；业务能力仍需要对应领域的任务说明或工具链支撑。

## 何时使用

- 需要从零设计一支 Multica 小队。
- 现有小队只有角色列表，缺少稳定协同协议、Handoff 或质量门禁。
- 希望把小队方法分享给不使用 Maglev 的团队。
- 需要判断某支小队能声明到 L0/L1/L2/L3 哪个质量等级。

## 何时不用

- 已经选定 Maglev Squad Kit 并要落地到 `packages/maglev-multica-kit/`：使用 `multica-squad-architect` 作为 Maglev Adapter。
- 只是安装或更新已有小队模板：使用对应 Adapter 的安装/同步工具。
- 只是修改某个 Agent 的一句提示词：按实际承载方式的普通配置流程处理。

## 工作流

1. **意图定界**：确认小队用途、受众、非目标、输入边界和成功信号。
2. **角色拓扑**：设计协调/路由责任角色、成员角色、权限、并发和终止条件。
3. **协同契约**：固定 Multica 原生接力、标准 Handoff、横向委派边界和失败排查。
4. **Adapter Contract**：要求落地适配器声明文件面、命令面、权限面、写入门禁和验证证据。
5. **质量门禁**：按 L0-L3 输出 `squad_quality`，限制可对外声明的能力级别。

## 输出契约

一次完整设计至少输出：

- 小队意图与非目标。
- 角色拓扑表。
- 协同契约清单。
- Adapter Contract 填写结果。
- 场景化测试矩阵。
- `squad_quality` 质量声明。
- Runtime Proof 是否完成的结论。

## 质量分级

| 等级 | 含义 | 允许声明 |
|---|---|---|
| L0 | 只有角色清单或初稿意图 | `draft` |
| L1 | 协同契约完整，包含协调/路由责任角色、Handoff、mention、禁止横向委派和失败排查 | `collaboration_designed` |
| L2 | Adapter 已落地模板资产、测试和静态验证 | `template_verified` |
| L3 | 在真实第三方承载或等价运行环境中完成端到端任务触发、接力和终态 Handoff 验证 | `runtime_verified` |

## 通用协同规则

### 共享上下文准入

- 跨隔离执行环境共享的产物必须有不可变版本标识，以及接收方已同步、可回查或等价的准入证据。
- 对话文本、当前沙箱偶然可见的文件和只有生产方持有的本地版本，不能作为共享完成事实。
- 具体项目或第三方承载如何实现版本、同步和准入由 Adapter Contract 定义，通用方法不指定 Git、目录或命令。

### 有限调度和状态回执

- 协调/路由责任角色只能消费当前状态、Handoff、准入证据和产物证据，使用决策指纹避免重复提问或重复派发。
- 没有新增证据时只能产生一次性 `human_action`、`blocked` 或 `awaiting_external`，并遵守明确的停止条件；满足完成条件时转为 `ready_to_close`，不生成无限下一步。
- 状态转移意图不等于实际外部状态；只有关联任务、触发原因、前后状态和回执引用齐全时，才能声明外部状态已更新。

### 人类责任路由

- 需要人类动作时采用角色优先路由：先选择一个或多个角色，再按角色内成员的描述和顺序选择成员。
- 描述不能唯一匹配时使用第一顺位并记录兜底；支持多角色目标，一个成员可以承担多个角色，一次 Handoff 可以指派多个角色。
- 没有人类动作时 `human_targets: []` 合法；成员身份、责任承载和通知成功必须由实际承载回执证明。

### 非侵入式审查和反馈

- 审查角色只读追溯实际生产者 skill 的既有标准、格式和来源，不要求生产者 skill 增加新接口。
- Review Packet 同时包含生产者标准、共享阶段最低门槛、事实证据、影响和修复条件。
- 协调/路由责任角色只选择一个单一主修复角色；修复产生新产物、Handoff 和验证证据后，必须执行独立复审，复审前不能标记 `resolved`。

### 规则分层和质量声明

- 构建者先区分通用方法规则、Adapter 规则、样本特有约束和第三方能力依赖。
- 单一样本只能支持样本或 Adapter 层证据，不能直接成为跨项目 Accepted 实践。
- 未获得真实第三方回执时使用 `unverified`、`blocked` 或 `awaiting_external`，不得声明 `runtime_verified`。

## 判定纪律

- 小队不是 Agent 名单；没有协同契约的小队最多是 L0。
- 协调/路由责任角色是默认唯一下一责任人决策者；成员默认交回该角色。
- 成员不能把“下一建议责任人”当成已委派任务。
- 写入门禁必须由 Adapter 显式定义；通用方法只要求其存在，不假定具体实现。
- 未完成 Runtime Proof 时，不得声明小队已稳定运行。

## 必需的参考资料

- 工作流：[`references/multica-squad-design-method.workflow.md`](references/multica-squad-design-method.workflow.md)
- 阶段一：[`references/step-01-squad-intent.md`](references/step-01-squad-intent.md)
- 阶段二：[`references/step-02-role-topology.md`](references/step-02-role-topology.md)
- 阶段三：[`references/step-03-collaboration-contract.md`](references/step-03-collaboration-contract.md)
- 阶段四：[`references/step-04-adapter-contract.md`](references/step-04-adapter-contract.md)
- 阶段五：[`references/step-05-quality-gate.md`](references/step-05-quality-gate.md)
- 质量分级：[`references/collaboration-quality-rubric.md`](references/collaboration-quality-rubric.md)
- Adapter Contract：[`references/adapter-contract.md`](references/adapter-contract.md)
- Runtime Proof：[`references/runtime-proof-gate.md`](references/runtime-proof-gate.md)
- 场景测试矩阵：[`references/scenario-test-matrix.md`](references/scenario-test-matrix.md)

## 示例

User: “我要做一支处理客户投诉的 Multica 小队。”

AI: “我会先用通用 Multica 小队设计方法固定小队目标、角色拓扑、协同契约和质量等级；如果后续需要具体项目或第三方承载，再填写对应 Adapter Contract。”
