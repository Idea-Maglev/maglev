---
reality_id: adoption-integration.capability.overview
title: 接入与集成能力
owner_domain: adoption-integration
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 四个接入/教学能力对象（maglev-bootstrapper、maglev-legacy-adopter、maglev-reverse-spec、maglev-tutor）的定位、触发与边界
  excludes:
    - Claude Code 适配层的生成机制与命令契约（属 implementation/claude-code-adapter.md 与 interfaces/cli.md）
    - 主链路能力对象（reality-sync、spec-designer 等，属各自域）
---

# 接入与集成能力

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 新仓库发起人 | 把空目录或新环境变成可进入 Maglev 主流程的项目 | Greenfield/Adoption 判定、骨架注入、仓库登记与初始化自检 | `.agents/skills/maglev-bootstrapper/SKILL.md` Phase 1-4 |
| 存量项目接手者 | 把已有代码仓库纳入 Maglev 且不破坏现有逻辑 | 六阶段接入：诊断、注入、逆向准备、Projection 验证准入、索引登记、首次项目地图 | `.agents/skills/maglev-legacy-adopter/SKILL.md` 核心规则与 Phase 1-6 |
| 存量事实重建执行者 | 为缺少现状文档的项目重建可独立核对的现实资料 | 模块地图、语义审阅包、经 Gate A/B 人工裁决的现实资料投影与准入记录 | `.agents/skills/maglev-reverse-spec/SKILL.md` 输出段 |
| 新成员/贡献者 | 理解 Maglev 范式并找到自己的协作入口 | User/Maker 分层课程与 `specs/`、`.agents/skills/` 交互式导览 | `.agents/skills/maglev-tutor/SKILL.md` 核心能力段 |

四个对象的分层口径来自各 SKILL.md frontmatter metadata：前三者 `top_level_capability: 整体接入`、`system_layer: Infrastructure Layer`、`lifecycle_chain: system_enablement`；maglev-tutor 为 `非核心主流程能力`、`Specialized Support Layer`、`specialized_support`（`rk.ad.cap.four-objects`）。

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 用户输入 `/maglev-init` 或 "Initialize Maglev" | 当前目录可扫描 | 骨架目录（`.agents/`、`.maglev/`、空 `specs/`、`docs/`、`issues/`）、受管仓库清单、AI 上下文自检结论 | `../adoption-integration/implementation/claude-code-adapter.md`（适配产物消费面） | established（契约文本） | 契约级 |
| 需要把已有仓库纳入 Maglev 结构 | 项目已有代码与运行现实 | Validator worktree 验证结果与 Admission Receipt；仅 `accepted`/`no_change` 后更新索引并生成 `docs/ATLAS.md`（`--check` 通过才允许完成态） | `.agents/skills/maglev-legacy-adopter/references/legacy-adopter.workflow.md` 时序图 | established（契约文本） | 契约级 |
| 用户提出逆向请求 | entry-router 交接；准备检查通过（目标项目与基线锁定、读取契约、模板包选定、目录隔离、静态读取授权） | 阶段 A 产出模块地图与语义审阅包；阶段 B 在 Gate A/B 通过后写出现实资料并独立验证准入 | `.agents/skills/maglev-reverse-spec/SKILL.md` 触发条件与唯一工作顺序段 | established（契约文本） | 契约级 |
| 逆向模板包选定 | `templates/reality-packs/registry.yaml` 登记的 pack（当前唯一入口：`software-development` v2，status production） | Template Pack 是可替换扩展：Pack 内资产目录由 `pack.yaml` 自定义并映射到目标 Reality 根；active 逆向/验证/结晶/契约链不感知特殊根页目录；页面结构与措辞以所选 Pack 页面契约为准 | `templates/reality-packs/registry.yaml`；`templates/reality-packs/software-development/v2/pack.yaml` | established | supported |
| 新成员需要理解 Maglev | 用户发起教学会话 | Profiling（Veteran/Apprentice/Risk）→ 课程表 → 带测验的交互导览 | `.agents/skills/maglev-tutor/SKILL.md` 交互示例段 | established（契约文本） | 契约级 |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 消费者隔离 | 消费者项目默认只得到空白实例，不携带 Maglev 源仓库的 Reality、地图或事实页 | bootstrapper SKILL.md 概览与 Phase 3 边界句 | `../adoption-integration/verification/known-gaps.md` |
| 存量接入 | 接入过程不得破坏现有代码逻辑；仓库根/submodule/package 只能登记为 `source_units`，不得直接转成 domain | legacy-adopter SKILL.md 核心规则与 Phase 1 | — |
| 逆向能力 | 不修复业务代码、不补测试、不修改接口实现、不替系统做设计决策 | reverse-spec SKILL.md 适用范围与"不可越过的边界"段 | — |
| 教学 | 不代替项目级现状同步，不代替主流程对象执行需求/设计/实现 | tutor SKILL.md"不负责什么"段 | — |
| 运行证据 | 四个能力的触发-产出在本仓只有契约文本，无运行记录机制，触发与产出按契约理解 | 本域无运行日志类证据源 | `../adoption-integration/verification/known-gaps.md` |

消费者隔离是本域的硬边界（`rk.ad.cap.blank-instance-boundary`）：bootstrapper 仅在用户确认登记至少一个仓库后才生成/更新 `internal Reality/crosscutting/repository-map/repositories.md`，未登记时不得创建该文件。

## 4. 事实与深挖

- Claude Code 适配层（`.claude/` 只读快照）由 `packages/maglev-claude-code` 生成：`../adoption-integration/implementation/claude-code-adapter.md`。
- 适配层生成命令的选项、配置合并与冲突交互契约：`../adoption-integration/interfaces/cli.md`。
- 当前无法证明的点（运行记录、适配层陈旧条目、零测试等）：`../adoption-integration/verification/known-gaps.md`。
