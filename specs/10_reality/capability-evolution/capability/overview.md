---
reality_id: capability-evolution.capability.overview
title: 能力进化能力
owner_domain: capability-evolution
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 能力对象能力面：持续进化观测（evolution-observatory）、技能侦察（skill-scout 双模式）、编队巡逻（skill-squadron）、扩展迭代（extension-evolver）
    - 对象清单与生命周期状态的登记口径（public capability catalog，单一权威）
    - 域边界注册（internal Reality/00_profile.yaml 的 capability-evolution 条目）
  excludes:
    - 三条演进循环的机制与状态机细节（属 implementation/evolution-cycle）
    - extension-manager 消费侧命令面与 code-execution-slot（r1 Gate A 裁决归 skill-runtime 域）
    - 执行记录缺口与页面归属分歧（登记于 verification/known-gaps）
---

# 能力进化能力

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| Creator（框架维护者） | 让能力清单跟上外部框架演进，知道哪些洞察还未消化 | 结构化竞品研究报告 + 竞品注册表 + insight 生命周期记录 | `.agents/skills/evolution-observatory/SKILL.md` 概览与核心能力段 |
| Creator | 在不从头设计的前提下获得新能力 | 外部 skill/workflow 经私域化改造后生成并登记为私域能力对象 | `.agents/skills/skill-scout/SKILL.md` 概览 Scout 模式 |
| Creator | 持续优化已登记的治理对象 | Patrol 差异分析与按价值排序的巡逻报告 | `.agents/skills/skill-scout/SKILL.md` 概览 Patrol 模式 |
| 扩展作者 / Registry 维护者 | 对已发布的 Extension Pack 做受控迭代 | `maintenance/` 决策与验证记录 + Registry 发布交接信息 | `.agents/skills/extension-evolver/SKILL.md` 首段与记录约定 |

域边界依据：`internal Reality/00_profile.yaml` 中 capability-evolution 条目声明
"竞品观测、扩展演进和能力注册共同定义能力进化边界"（boundary_basis:
`product_outcome` + `workflow`）。对象清单以 `public capability catalog`
为单一权威：`top_level_capability: '能力进化'` 的登记对象共 7 个——
skill-scout、skill-squadron、extension-manager、extension-evolver、
multica-squad-design-method、multica-squad-architect、evolution-observatory，
全部 `status: active`。

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| "启动进化观测" / "研究一下 {框架名}" / "检查竞品动态" 等 | Creator 主动触发（AI 不自动启动研究）；每轮开始前先读 positioning.md 锚定 | 研究报告归档至 `docs/thinking/10_critique/`，competitive-registry.yaml 更新（last_researched、version_tracked、新增 open insights），commit 前缀 `research(observatory)` | 演进循环机制 | established（契约文本） | 契约级 |
| "启动 Skill Scout，我需要一个…" 等 Scout 触发词 | 实际联网检索并留下显式证据（Hard Gate：无联网证据不得进入 evaluate/adapt/register） | 私域能力对象生成并登记进 private-catalog | 演进循环机制 | established（契约文本） | 契约级 |
| "启动巡逻模式" / "巡逻一下现有技能" 等 Patrol 触发词 | 治理对象已登记 catalog | PatrolReport（优化机会按 value_score 降序；无机会时 `all_current` 结束） | 演进循环机制 | established（契约文本） | 契约级 |
| 编队巡逻（skill-squadron） | 治理对象已登记 catalog | 基于治理对象关系图的分组、巡逻、命名状态检查与跨对象影响分析；单对象扫描委托 skill-scout 的 Patrol 模式 | `public capability catalog` skill-squadron 条目 relations | established（catalog 登记） | 契约级 |
| 已发布 Extension Pack 的变更意图 | extension.yaml、Registry entry、lock 可定位基线 | `maintenance/records/YYYY-MM-DD-<topic>.md`（意图、兼容性、验证证据、交接），兼容性不能确认时必须标为阻塞 | 演进循环机制 | established（契约文本） | 契约级 |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 不自动触发 | 观测研究由人主动触发，AI 不自动启动；superseded 标记必须等 Creator 确认，不可自动执行 | `.agents/skills/evolution-observatory/SKILL.md` 交互模式段 Trigger 与 Superseded Gate | — |
| catalog 不是完备清单 | catalog 自述"不是 `.agents/skills/` 的机械镜像，也不是历史日志"；本轮目录对比抽查到 9 个 private document integration 对象未登记且无逐对象免登记裁决记录 | `public capability catalog` 头注释；本轮 `.agents/skills/` 目录与 catalog 清单 diff | [已知缺口](../verification/known-gaps.md) |
| 对象知识页跨域 | r1 Gate A 裁决将 skill-scout / skill-squadron / extension-manager / extension-evolver 的知识资产页归 skill-runtime 域，本页只写能力面与登记状态，不复制其实现细节 | `specs/90_archive/reality-knowledge-reverse-r1/gate-a-record.md` 跨域排除段 | `../skill-runtime/capability/overview.md` |
| 页面归属待裁决 | multica-squad-design-method 与 multica-squad-architect 登记于能力进化顶层能力，但未出现在 r1 Gate A 归属裁决清单中，其 10_reality 事实页归属未裁决；本页只引用 catalog 登记字段 | gate-a-record.md 跨域排除清单（无此二对象） | [已知缺口](../verification/known-gaps.md) |
| 不承诺洞察已被消化 | registry 中 25 条 insight 全部 `status: open`，"观测养分回流 spec/reality"只有机制契约，无执行实例 | competitive-registry.yaml status 字段统计（本轮） | [已知缺口](../verification/known-gaps.md) |

## 4. 事实与深挖

三条演进循环（观测 6 Phase、侦察双模式、扩展迭代六步）的机制事实、insight
状态机与 registry 结构见
`../capability-evolution/implementation/evolution-cycle.md`；执行记录缺口与
归属分歧账本见 `../capability-evolution/verification/known-gaps.md`。本页不复制其内容。
