---
description: 基于项目级治理对象清单分析关系图、分组并执行编队巡逻 (Use skill-squadron skill)
metadata:
  formal_action_name: 编队巡逻
  top_level_capability: 能力进化
  object_kind: workflow
  lifecycle_chain: governance_loop
  author: Maglev contributors
  last_updated: 2026-03-30
---
# Skill Squadron Workflow

在以下场景中，优先进入 `skill-squadron`：

- 需要批量分析多个能力对象之间的关系
- 需要按组巡逻，而不是单点扫描
- 需要评估某个对象优化后对关联对象的影响
- 需要生成按对象组组织的治理报告

当前输入面：

- `.agents/private-catalog.yaml`

当前口径：

- `skill-squadron` 读取的是项目级治理对象清单
- 不是对 `.agents/skills/` 和 `.agents/workflows/` 的全量文件系统扫描
- 当前既能处理 `skill`，也能处理 `workflow-first` 对象
- 当前会显式读取 `runtime_name_status`，把运行面命名状态作为正式巡逻维度

当前默认巡逻切片：

1. 主流程前中段组
   - `entry-router`
   - `现状同步（reality-sync）`
   - `requirement-convergence`
   - `方案设计（spec-designer）`
   - `上下文实施（context-implementer）`
   - `综合验证（integrated-validator）`
2. 体系级与后段闭环组
   - `crystallization`
   - `knowledge-check`
   - `maglev-bootstrapper`
   - `maglev-legacy-adopter`
   - `maglev-reverse-spec`
   - `maglev-map-maker`
   - `index-librarian`
   - `skill-scout`
   - `skill-squadron`
3. 质量层组
   - `spec-audit-surface`
   - `review-validation-surface`
   - `test-design-surface`

推荐触发方式：

1. 关系图与分组分析
   > "请启动 `skill-squadron`，分析当前治理对象的关系图和分组。"
2. 编队巡逻
   > "请启动 `skill-squadron`，按当前默认巡逻切片执行编队巡逻。"

当前注意事项：

- 若 `.agents/private-catalog.yaml` 的 active 对象或 relations 发生变化，应先重跑分组
- `skill-squadron` 负责分组、编队与影响分析
- 单个 `skill` 的具体 Patrol 扫描继续委托给 `skill-scout`
- 主流程核心对象若仍处于 `active_legacy_name`，巡逻时应额外关注旧运行名是否继续制造理解成本
