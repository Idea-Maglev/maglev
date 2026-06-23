# skill结构性升级 Design

> 状态：已封板
> 作用：作为本轮设计总览入口，只保留当前仍有效的结构结论与子文档导航。
> 完整讨论沉淀：
> - `design/archive/02_design_full_archive.md`

## 1. 当前设计总目标

本轮目标不是修复现有 skill 的局部病灶，而是根据 Maglev 真正要解决的问题，反推出最合适的 skill 体系。

当前设计判断顺序固定为：

1. Maglev 要解决什么问题
2. 为解决这些问题，必须具备哪些能力断点
3. 这些能力断点中，哪些应成为顶层一级能力
4. 这些一级能力再由什么层次对象承接

## 2. 当前核心结论

### 2.1 问题定义

当前已收敛的根问题是：

Maglev 要解决的，是 AI Coding 时代项目现状难以被稳定表达、需求生命周期难以被稳定推进、以及会话产出难以沉淀成团队能力的问题。

### 2.2 一级能力草案 v2

当前顶层能力骨架先收敛为 `5+3`：

5 个主流程一级能力：

1. `现状同步`
2. `需求收敛`
3. `方案设计`
4. `上下文实施`
5. `综合验证`
3 个体系级能力：

1. `能力进化`
2. `现状表达`
3. `整体接入`

### 2.3 双视图结构模型

当前已确认 Maglev 后续应采用“双视图结构模型”：

1. `能力骨架视图`
   - 回答顶层应具备哪些能力
2. `系统承接视图`
   - 回答这些能力由哪些对象和层次承接

### 2.4 当前最重要缺口

当前最明显的剩余缺口，已经不再是对象边界本身，而是对象收口后的制度化表达：

1. 主流程核心对象的结构动作名已稳定，但运行面名称仍存在历史名称与正式动作名并存的状态，仍需单独形成 rename 策略说明
2. `skill-scout` 与 `skill-squadron` 的运行面已基本对齐，但仍需持续收敛 catalog、metadata 与巡逻输出的一致性
3. 本主题的退出条件与封板标准已单独落到 `design/03az_closeout_criteria_and_exit_standard_v1.md`

## 3. 设计子文档

后续不再把所有内容继续堆入本文件，而是只保留当前主线真正需要的子文档入口。

### 3.1 问题与能力骨架

- `design/02a_problem_and_capability_model.md`

承载：

- Maglev 问题定义
- 能力断点
- 一级能力草案

### 3.2 系统承接结构

- `design/02b_system_structure_model.md`

承载：

- 七层系统承接视图
- workflow / skill / 基础设施 / Reality 的关系
- 现实结晶与思考沉淀链路位置

### 3.3 一级能力与现有对象映射

- `design/02d_capability_mapping.md`

承载：

- 一级能力与现有对象的映射草案
- 当前稳定承接区、协作承接区与缺口

### 3.4 统一判据

- `design/02n_structural_upgrade_criteria_v1.md`

承载：

- 当前最可复用的结构升级总判据
- 后续 `skill-scout` / `skill-squadron` 的统一判断底座

### 3.5 显性对象边界与命名口径

- `design/02o_future_explicit_skill_roster_v1.md`
- `design/02p_naming_readiness_matrix_v1.md`
- `design/02q_formal_action_names_v1.md`

承载：

- 基于统一判据反推的未来显性 skill 边界
- 哪些对象已接近正式定名
- 哪些对象当前只能保留结构语义
- 当前已接近稳定的主流程对象正式动作名

### 3.6 Skill 元数据

- `design/02r_skill_metadata_schema_v1.md`
- `design/02v_metadata_storage_plan_v1.md`

承载：

- 后续 skill 治理最小元数据字段
- 元数据字段与真实载体的第一版落点方案

### 3.7 治理与巡逻

- `design/02e_skill_batch_analysis_base_table.md`
- `design/02f_direction_rules.md`
- `design/02g_skill_governance_queue.md`
- `design/02h_skill_squadron_patrol_batches.md`
- `design/03at_non_core_skill_retention_decision_v1.md`
- `design/03au_maglev_create_prd_transition_plan_v1.md`
- `design/03az_closeout_criteria_and_exit_standard_v1.md`
- `design/archive/governance/README.md`

### 3.8 Scout 结果

- `design/02m_source_pool_alignment.md`
- `design/archive/scout/README.md`

承载：

- 来源池与私有资源池对齐规则
- 关键对象通过 `skill-scout` 形成的 parse / search / evaluate / adapt / register 证据链
- 当前哪些对象已完成对象生成与登记
- 当前哪些旧对象只完成结构重判，尚未进入正式改名

## 4. 归档说明

以下内容已转入主归档，不再作为当前主线入口：

- `design/archive/02_design_full_archive.md`
- `design/archive/scout/README.md`
- `design/archive/governance/README.md`

## 5. 当前工作方式

从本轮开始：

- `02_design.md` 只保留有效结论和导航
- 大段推演与完整讨论留在 `design/archive/02_design_full_archive.md`
- 新增结构判断优先写入对应子文档

## 6. 当前结论

当前设计已经从“结构讨论”推进到“运行面已落地一批新对象”的阶段。

当前较稳定的运行面结果是：

- 新对象已落地：
  - `entry-router`
  - `knowledge-check`
  - `requirement-convergence`
  - `crystallization`
  - `spec-audit-surface`
  - `review-validation-surface`
  - `test-design-surface`
- `skill-scout` 已吸收对象生成能力
- `maglev-skill-forge` 已退出运行面

后续重点不再是扩讨论，而是按 closeout 标准完成封板判断，并把后续事项转入新主题。
