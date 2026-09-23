---
reality_id: collaboration-lifecycle.capability.overview
title: 协作生命周期能力概览
owner_domain: collaboration-lifecycle
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 本域登记的协作能力对象：需求收敛到结晶的主线技能、项目看板、Multica 小队设计方法与 Maglev Adapter 及 Squad Kit 工具包
  excludes:
    - reality-sync 会话现状同步（属 session-reality-sync 域）
    - code-execution-slot 代码执行插槽（属 skill-runtime 域）
---

# 协作生命周期能力概览

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 人类贡献者 | 把一个模糊请求收敛为需求、方案、实施、验证并结晶回写 | 主线技能链：`entry-router` → `requirement-convergence` → `spec-designer` → `context-implementer` / `code-execution-slot` → `integrated-validator` → `crystallization` | `AGENTS.md` 主链路区块 |
| 维护者 | 知道当前活跃需求各自到哪个阶段、谁在主导 | 项目看板输出总看板与需求子看板，只观测不驱动 | `.agents/skills/project-board/SKILL.md` 概览与不负责段 |
| 需要组织多智能体协作的设计者 | 设计一支协作、交接、质量边界清晰的小队 | 通用 Multica 小队设计方法（意图、角色拓扑、协同契约、质量分级 L0-L3） | `.agents/skills/multica-squad-design-method/SKILL.md` 负责段 |
| Maglev 仓库的小队落地者 | 把通用小队设计落成 Maglev Squad Kit 模板、catalog、测试与质量声明 | Maglev Adapter：Squad Kit 文件面、`maglev-multica` 命令面、写入门禁和验证面 | `.agents/skills/multica-squad-architect/SKILL.md` 负责段 |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 会话请求进入主流程 | 仓库就绪、技能已在 `public capability catalog` 注册为 `active` | `entry-router` 分诊后交接下游能力，直至 `crystallization` 回写 | 各技能 `SKILL.md` 工作流章节 | established（注册与契约文本） | 契约级 |
| 手动调用 `/board` 或 reality-sync 自动展示 | `specs/20_evolution/active/` 存在活跃需求 | `specs/20_evolution/board.md` 总看板 + 需求子看板 `status.md` | `../operations/team-roles.md` | established（契约文本） | 契约级 |
| 小队设计需要落地为 Maglev 模板 | 通用小队设计包已稳定 | Squad Kit 模板资产、catalog 登记、测试与 `squad_quality` 声明 | `multica-squad-kit.md`（本域 capability）；`../implementation/multica-squad-kit.md` | established（契约文本） | 契约级 |
| 仅做通用小队设计、不落 Maglev | 存在小队目标与边界 | 小队意图、角色拓扑、协同契约与质量等级结论，不产生 Maglev 文件 | `multica-squad-design-method/SKILL.md` 何时不用段 | established（契约文本） | 契约级 |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 范围外 | `reality-sync`（会话起点同步）属 `session-reality-sync` 域；本域概览只登记其看板展示消费面 | `AGENTS.md` 主链路与 r1 域划分 | `../session-reality-sync/capability/overview.md` |
| 范围外 | `code-execution-slot` 属 `skill-runtime` 域；本域仅在主链顺序中引用其分支位置 | `AGENTS.md` 主链路；`internal Reality/skill-runtime/capability/overview.md` | `../skill-runtime/capability/overview.md` |
| 范围外 | `project-board` 不执行流程推进、不做工时/绩效/外部集成、不做 commit 级追踪 | `.agents/skills/project-board/SKILL.md` 不负责段 | `../operations/team-roles.md` |
| 边界 | `multica-squad-architect` 不替代通用方法设计、不直接安装远端 Workspace、不替代综合验证 | `.agents/skills/multica-squad-architect/SKILL.md` 不负责段 | `../verification/known-gaps.md` |
| unknown | 主线各技能的会话级行为质量（如收敛耗时、验证通过率）无运行记录机制，本域不声明 | 本域无此类统计来源 | `../verification/known-gaps.md` |

## 4. 事实与深挖

- Multica 小队方法与 Maglev Adapter 的能力对象、模板清单和质量边界：`multica-squad-kit.md`（本域 capability）。
- Squad Kit 包的构件、命令面与阶段契约：`../implementation/multica-squad-kit.md`。
- VO/TP/XG 协作角色映射与项目配置：`../operations/team-roles.md`。
- 测试与 Runtime 证据边界、当前缺口账本：`../verification/multica-squad-kit.md`、`../verification/known-gaps.md`。
- 本页不复制上述页面的技术细节与角色拓扑正文。
