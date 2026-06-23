# skill结构性升级 阶段性收口总结

> 状态：已封板
> 作用：只保留本阶段最重要的完成项、稳定结论、反思与封板后的下一步入口。

## 1. 本阶段完成项

本阶段已经从“发现 skill 很乱”推进到“形成一套可继续落地的结构底座”。

已完成的关键内容：

1. 明确主线目标  
   不是修单个 skill，而是根据 Maglev 要解决的问题，反推出更合适的 skill 体系。

2. 收敛顶层能力骨架  
   当前顶层能力按 `5+3` 理解：
   - 主流程：`现状同步`、`需求收敛`、`方案设计`、`上下文实施`、`综合验证`
   - 体系级：`能力进化`、`现状表达`、`整体接入`

3. 明确双视图模型  
   - 能力骨架视图
   - 系统承接视图

4. 切开两条后段链路  
   - `思考归档触发链`
   - `事实结晶触发链`

5. 形成当前正式对象与 workflow  
   - `entry-router`
   - `knowledge-check`
   - `requirement-convergence`
   - `crystallization`
   - `spec-audit-surface`
   - `review-validation-surface`
   - `test-design-surface`

6. 建立统一治理面  
   - 结构判据
   - 治理清单
   - 巡逻批次
   - 元数据草案
   - 项目级 `private-catalog`

7. 完成关键外部对标  
   已覆盖前段缺口、后段闭环、质量层、体系级能力簇。

## 2. 当前最稳定的结论

以下判断已足够稳定，可作为后续默认前提：

1. `knowledge-check` 负责知识沉淀检查，不承担 Reality 回写。
2. `crystallization` 负责后段闭环，不承担知识沉淀检查。
3. 质量层应按三面对象存在，而不是并列碎片 skill。
4. `maglev-cross-validate` 继续作为主流程验证汇聚点。
5. `skill` 撰写与重写必须经过 `skill-scout`。
6. `skill-scout` 现在包含侦察、改造、生成与登记能力。
7. `skill-squadron` 现在应面向“治理对象”而不是只面向 skill。
8. 主流程核心对象的结构动作名已稳定，但运行面名称仍有历史名并存状态。

## 3. 当前进度判断

当前更准确的进度判断不是“主要 skill 都已完成”，而是：

> 主要骨架与高优先级对象已经完成第一轮结构升级，但还没有进入全面定稿状态。

### 已基本完成

1. 新骨架对象已落地
2. 质量层三面已落地
3. `skill-scout` / `skill-squadron` / `private-catalog` 治理底座已形成

### 已延后到下一轮

1. 主流程核心对象运行名与正式动作名的最终策略文档化
2. spec pipeline 四件套的物理内部模块化重构
3. 新回合对象进入治理清单的门槛继续稳住

### 当前可接受不做

1. 立即为所有现役 skill 完成物理重命名
2. 让所有运行面对象都进入治理清单
3. 对所有历史分析材料继续做深度瘦身

## 4. 当前高价值资产

本阶段最值得保留的是这几类资产：

- 总判据：
  - [design/02n_structural_upgrade_criteria_v1.md](./design/02n_structural_upgrade_criteria_v1.md)
- 主线骨架与映射：
  - [design/02a_problem_and_capability_model.md](./design/02a_problem_and_capability_model.md)
  - [design/02d_capability_mapping.md](./design/02d_capability_mapping.md)
- 治理与巡逻：
  - [design/02e_skill_batch_analysis_base_table.md](./design/02e_skill_batch_analysis_base_table.md)
  - [design/02g_skill_governance_queue.md](./design/02g_skill_governance_queue.md)
  - [design/02h_skill_squadron_patrol_batches.md](./design/02h_skill_squadron_patrol_batches.md)
- 元数据与落点：
  - [design/02r_skill_metadata_schema_v1.md](./design/02r_skill_metadata_schema_v1.md)
  - [design/02v_metadata_storage_plan_v1.md](./design/02v_metadata_storage_plan_v1.md)
- 最终复核清单：
  - [design/03as_active_skill_final_review_checklist_v1.md](./design/03as_active_skill_final_review_checklist_v1.md)
- 退出标准：
  - [design/03az_closeout_criteria_and_exit_standard_v1.md](./design/03az_closeout_criteria_and_exit_standard_v1.md)
- 完整历史过程：
  - [archive/00_context_full.md](./archive/00_context_full.md)
  - [design/archive/02_design_full_archive.md](./design/archive/02_design_full_archive.md)

## 5. 当前反思

本阶段暴露出的主要问题：

1. 我前面多次有“往前滑太快”的问题。  
   结构还没收稳时，就容易滑向具体 skill 改写。

2. 文档一度明显膨胀。  
   后面已经通过 `archive/` 与主归档拆分做了减入口处理。

3. 来源治理一开始没有完全按 Maglev 自己的规则走。  
   这点后面已经补回到 `skill-sources.yaml` 与项目级 source pool 校准。

## 6. 封板后下一步

当前更合理的后续动作只有两类：

1. 新开主题处理延后事项  
   例如 rename 策略专项、spec pipeline 物理内部化、治理对象准入规则。

2. 做最小运行面维护  
   仅在发现新的显性冲突或口径回退时，再做小范围修补。

## 7. 当前结论

到这个阶段为止，`skill结构性升级` 已完成本轮结构性收口，并正式封板。

后续不再继续把对象级讨论堆回本主题，而应把剩余事项拆入新主题。

当前更具体的封板落点已单列在：

- [design/03az_closeout_criteria_and_exit_standard_v1.md](./design/03az_closeout_criteria_and_exit_standard_v1.md)
