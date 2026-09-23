---
reality_id: release-knowledge.capability.overview
title: 发行知识能力
owner_domain: release-knowledge
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 能力对象：面向用户的版本说明知识生产
  excludes:
    - 发行流程与 npm 渠道（属 delivery-runtime 域）
    - CHANGELOG.md 的 Creator 执行细节（属实现页）
---

# 发行知识能力

## 1. 能力定位与受益者

发行知识回答一个问题：**每个版本"对用户意味着什么"**，与面向维护者的过程记录（发版脚本执行、npm 渠道状态、git tag）分开。能力由一个生成技能和三件知识产物构成：

- `maglev-changelog-generator`：读取 Changelog Draft，结合源码分析，生成面向用户的语义化 CHANGELOG.md（**仅 Creator**——只生成，不执行发版动作）。
- `docs/releases/<version>.md`：版本知识归档，每版一档（Gate A 裁决 C1 纳入本域：流程归 delivery-runtime，知识归本域）。
- `docs/releases/index.md`：版本索引与当前版本指针。
- `.maglev_build/CHANGELOG.md`：构建态镜像，随当次 release 构建分发（与归档的同步关系见 workflows 页）。

技能登记事实（SKILL.md frontmatter）：正式动作名"版本说明生成"，属非核心主流程能力 / Specialized Support Layer，运行名状态 `active_legacy_name`，分发范围 `private_only`，版本 1.0.0（2026-04-23 更新）。

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 下游用户 | 升级前知道这个版本带来什么、是否需要主动适配 | 按版本归档的语义化发行说明（新特性/打磨/缺陷修复/破坏性变更四类） | `docs/releases/0.7.4.md` |
| Maglev 维护者 | 发版时把机械变更清单转化为可发布的版本说明并长期归档 | 三产物：构建态 CHANGELOG + 版本归档 + index 登记 | `.agents/skills/maglev-changelog-generator/SKILL.md` 核心目标 |
| AI Agent（Creator 角色） | 在发版工作流中执行版本说明生成 | SKILL.md 三步执行指导与终态检查 | 同上"执行步骤" |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 发版停点：release compiler Step 4 提示调用 `/generate-changelog` | `.maglev_build/CHANGELOG_DRAFT.md` 已生成 | 三产物落盘 + 中文确认语 | `../release-knowledge/capability/workflows.md` | established（契约文本 + 脚本锚点） | 契约级 + 代码锚点 |
| 用户升级前查阅 | 目标版本已有归档 | 该版本的用户语义说明 | `../release-knowledge/capability/use-cases.md` | established | 归档实例级 |
| 确认当前版本口径 | index.md 维护正常 | 当前版本指针：trunk 已随发版准备撤回复位 0.7.3（用户裁决：0.7.4 迭代未完，revert 77e7626）；0.7.4 待迭代完成后重新归档 | 同上 | established | 一手盘点 + 裁决 |
| 校验失败后的补齐循环 | 三产物任一缺失或未登记 | 脚本报错指路并重新询问确认，不放行 | `../release-knowledge/capability/business-rules.md` 决策表 | established（代码锚点） | 代码级 + 测试 |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 范围外 | 不执行发版动作：npm 发布、git tag、release 分支推送均属 delivery-runtime 域 | SKILL.md"仅 Creator"声明；脚本 step6/7/8 均为发版动作 | `scripts/maglev_release.py`（delivery-runtime 域事实） |
| 范围外 | 无 implementation/operations 页组：Gate B 槽位矩阵裁定 M8 只有 capability 与 verification 槽位 | `specs/90_archive/reality-knowledge-reverse-r1/stage-a-module-map.md` v2.1 槽位矩阵 M8 行 | 本页组 7 页即全部 |
| 范围外 | 不覆盖 0.1.4 之前的版本语义 | `docs/releases/` 序列起点为 0.1.4（2026-03-21），更早版本无归档 | `../release-knowledge/verification/known-gaps.md` |
| 未证实 | 0.7.4 迭代未完，发版准备已按用户裁决自 master 撤回（revert 77e7626，已推送）；正式发版提交 f2a9ef1 保留于 origin/release | 撤回提交一手可核（git show 77e7626）；npm 渠道状态无本域证据；本分支工作树因分叉时序仍含 0.7.4 准备产物，合并后以 trunk 为准 | `../release-knowledge/verification/known-gaps.md` |
| 未证实 | 语义化质量无机器门禁 | SKILL.md 只有 DoD 文本约束，tests/ 无对应断言 | `../release-knowledge/verification/test-matrix.md` |
| 未证实 | 双产物内容一致性（构建态 vs 归档）无自动校验 | 脚本只校验文件存在性与 index 登记，不比对两份内容 | `../release-knowledge/verification/known-gaps.md` |

## 4. 事实与深挖

- 规则与发版确认点决策表：`../release-knowledge/capability/business-rules.md`
- 消费与生产场景：`../release-knowledge/capability/use-cases.md`
- draft → generate → archive → sync 流程：`../release-knowledge/capability/workflows.md`
- 验证依据与缺口：`../release-knowledge/verification/test-matrix.md`、`../release-knowledge/verification/static-coverage.md`、`../release-knowledge/verification/known-gaps.md`
- 发版动作本体（版本号解析、publish、npm 验证、tag）属 delivery-runtime 域：`scripts/maglev_release.py`
