# skill结构性升级

> 作用：作为当前主题目录的精简导航页，只保留后续仍会继续被直接消费的入口。

上层归档总览可见：

- [specs archive index](../README.md)

## 1. 主入口

- `00_context.md`
- `00_intent.md`
- `01_requirements.md`
- `02_design.md`
- `03_plan.md`
- `04_stage_summary.md`
- `05_closeout.md`
- `design/03az_closeout_criteria_and_exit_standard_v1.md`
  - 当前封板标准与退出条件落点

## 2. 当前主线设计

优先阅读这些文档：

- `design/02a_problem_and_capability_model.md`
  - 问题定义、能力骨架、顶层结构
- `design/02b_system_structure_model.md`
  - 系统承接视图、workflow 与 skill 的关系
- `design/02d_capability_mapping.md`
  - 一级能力与现有对象映射
- `design/02n_structural_upgrade_criteria_v1.md`
  - 统一结构判据
- `design/02o_future_explicit_skill_roster_v1.md`
  - 未来显性对象边界
- `design/02r_skill_metadata_schema_v1.md`
  - 元数据字段草案
- `design/02v_metadata_storage_plan_v1.md`
  - 元数据落点方案
- `design/03az_closeout_criteria_and_exit_standard_v1.md`
  - 本轮 closeout criteria 与退出标准

## 3. 当前治理与巡逻

- `design/02e_skill_batch_analysis_base_table.md`
- `design/02f_direction_rules.md`
- `design/02g_skill_governance_queue.md`
- `design/02h_skill_squadron_patrol_batches.md`
- `design/archive/governance/README.md`
  - 集中索引迁移矩阵、对象图预演与默认巡逻报告样例

## 4. 当前 Scout 资产

当前说明：

- `skill-scout` 现在同时负责侦察、改造、生成与登记
- `maglev-skill-forge` 已退出运行面，仅在历史资料中保留客观痕迹

- `design/archive/scout/README.md`
  - 集中索引本轮所有 Scout 对标、证据链与登记台账

## 5. 当前运行对象落地

当前前后段补位对象已经落成真实 skill，本地 workflow 文件只作为调用入口包装。

- `.agents/workflows/requirement-convergence.md`
  - `需求收敛` 的调用入口包装
- `.agents/skills/requirement-convergence/`
  - `需求收敛` 的真实 skill 对象
- `.agents/workflows/crystallization.md`
  - `现实结晶` 的调用入口包装
- `.agents/skills/crystallization/`
  - `现实结晶` 的真实 skill 对象
- `.agents/workflows/entry-router.md`
  - `entry-router` 的 workflow 入口
  - 作为当前唯一入口路由 skill 的调用入口
- `.agents/workflows/knowledge-check.md`
  - `knowledge-check` 的 workflow 入口
  - 作为当前知识沉淀检查 skill 的调用入口
- `.agents/workflows/spec-audit-surface.md`
  - `spec-audit-surface` 的 workflow 入口
  - 作为质量层输入审计面的调用入口
- `.agents/workflows/review-validation-surface.md`
  - `review-validation-surface` 的 workflow 入口
  - 作为质量层结果审查面的调用入口
- `.agents/workflows/test-design-surface.md`
  - `test-design-surface` 的 workflow 入口
  - 作为质量层测试设计面的调用入口

## 6. 当前项目级治理对象面

- `.agents/private-catalog.yaml`
  - 当前项目级治理对象清单
  - 供 `skill-scout` / `skill-squadron` 共同消费
  - 不是 `.agents/skills/` 与 `.agents/workflows/` 的文件系统镜像

## 7. 输入材料

外部输入与参考实践目录。

- `inputs/maglev_reverse_spec_2026-03-28/`
  - 来自逆向能力优化的补充输入，主要用于约束 Reality 详细度与稳定性讨论

## 8. 归档与约束

保留证据价值的主归档：

- `archive/00_context_full.md`
- `design/archive/02_design_full_archive.md`
- `design/archive/scout/README.md`
- `design/archive/governance/README.md`

从现在开始：

- 新的设计判断优先写入 `design/` 下对应子文档
- `02_design.md` 不再承载大段完整推演
- 计划附属材料优先进入 `plan/`
- 外部输入统一进入 `inputs/`
- 旧对象 `atomizer` 与 `maglev_archival_check` 已从运行面移除；设计文档中的相关内容仅保留为历史分析证据

## 9. 当前主线状态

当前这条主线已完成本轮封板。

后续默认顺序应为：

1. 以 `05_closeout.md` 作为本轮结束标记
2. 后续新工作另开主题，不再继续向本目录堆叠新的对象级讨论
3. 当前目录只保留复盘、引用与历史证据价值
