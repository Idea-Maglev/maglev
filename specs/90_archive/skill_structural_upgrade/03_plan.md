# skill结构性升级 Plan

> 状态：进行中
> 作用：只保留当前仍有效的行动项、执行边界与下一步。
> 输入：
> - `00_intent.md`
> - `01_requirements.md`
> - `02_design.md`
> - `04_stage_summary.md`

## 1. 当前执行原则

本轮继续遵守以下原则：

- 先以 Maglev 要解决的问题为准，再反推 skill 体系
- 优先减少入口冗余，而不是继续扩写分析文档
- 运行面只保留现役对象，历史对象不再作为推荐入口
- 真正进入 skill 撰写或重写时，必须走 `skill-scout`
- `skill-scout` 若没有实际联网检索证据，不得继续进入 `evaluate / adapt / register`

## 2. 当前已落地结果

当前已经形成并进入运行面的对象：

- `entry-router`
- `knowledge-check`
- `requirement-convergence`
- `crystallization`
- `spec-audit-surface`
- `review-validation-surface`
- `test-design-surface`
- `.agents/private-catalog.yaml`

当前已经稳定的结构判断：

- 顶层能力骨架按 `5+3` 理解
- `需求收敛` 已形成正式 skill，workflow 文件仅作为入口包装
- `现实结晶` 已形成正式 skill，workflow 文件仅作为入口包装
- `knowledge-check` 只负责知识沉淀检查，不承担 Reality 回写
- `skill-scout` 已吸收对象生成能力
- `skill-squadron` 当前应面向“能力对象”，而不只是 skill

## 3. 当前完成状态判断

### 3.1 已完成

以下内容当前可以视为本轮主线中的“已完成项”：

1. 顶层能力骨架已收敛为 `5+3`
2. `entry-router`、`knowledge-check`、`requirement-convergence`、`crystallization` 已进入运行面
3. 质量层三面已形成现役对象：
   - `spec-audit-surface`
   - `review-validation-surface`
   - `test-design-surface`
4. `skill-scout` / `skill-squadron` / `.agents/private-catalog.yaml` 的治理链已经打通
5. 高风险旧对象已退出运行面：
   - `atomizer`
   - `maglev_archival_check`
   - 旧质量碎片对象
   - `maglev-skill-forge`

### 3.2 尚未完成

以下内容当前仍不能算结束：

1. 全量现役 skill 的最终结构复核
2. 主流程核心对象的运行名与正式动作名策略最终定稿
3. catalog、workflow、README、skill 本体之间的长期一致性机制
4. 本主题的正式退出条件与封板标准

### 3.3 可暂缓

以下内容当前不必作为本轮收口前置条件：

1. 所有现役对象立刻完成物理改名
2. 所有运行面对象都进入治理清单
3. 所有历史分析文档继续压缩到极限

## 4. 当前剩余行动项

### 4.1 入口与运行面

需要继续确认：

- `entry-router` 的路由规则是否已覆盖当前现役对象
- 推荐入口文档是否仍有旧结构口径残留
- `.agents/private-catalog.yaml` 是否与真实运行对象保持一致

### 4.2 现役对象稳定性

对象级复核本轮已基本收口，现阶段只继续观察两类稳定性：

- `requirement-convergence`
  - 是否持续保持三段式：
    - `入口分流`
    - `需求定义`
    - `Ready Gate`
- `crystallization`
  - 是否持续保持三段式后段闭环：
    - `现实回写判定`
    - `active 状态收口`
    - `索引与可发现性回填`

### 4.3 治理与巡逻

需要继续验证：

- `skill-squadron` 的对象图是否已能同时消费 `skill` 和 `workflow`
- 批量分析底表与 `.agents/private-catalog.yaml` 是否持续对齐
- `direction rules` 是否足够支撑后续治理批次

### 4.4 文档瘦身

继续控制主题目录体量：

- 新内容优先进入对应子文档，不回堆到主入口文档
- 只保留主归档：
  - `archive/00_context_full.md`
  - `design/archive/02_design_full_archive.md`
- 已被现行对象覆盖的工作草稿，继续按需删除

### 4.5 全量现役对象最终复核

参照：

- `design/03as_active_skill_final_review_checklist_v1.md`
- `design/03at_non_core_skill_retention_decision_v1.md`
- `design/03az_closeout_criteria_and_exit_standard_v1.md`

当前对象级复核已完成主流程核心对象、私有更新对象与专项支持对象的这一轮收口。

后续不再以“再做一轮全量对象复核”为目标，而是转入：

1. rename 策略文档化
2. 退出条件与封板标准收口
3. 新进入治理清单对象的门槛控制
4. 非主干 skill 的保留、豁免与清理分流执行
5. spec pipeline 四件套的去显性化与内部模块链收口

## 5. 明确不做的事

当前阶段不继续做：

- 为了“看起来完整”继续新增分析稿
- 把所有 workflow 立即硬化成独立 skill
- 在未经过 `skill-scout` 时直接重写 skill 正文
- 在只有来源池映射、没有联网检索证据时生成 skill
- 大规模改动与当前主线无关的仓库文档

## 6. 当前退出条件落点

当前正式退出标准已落在：

- `design/03az_closeout_criteria_and_exit_standard_v1.md`

本文件只保留与当前执行直接相关的压缩版判断：

1. 主流程核心对象与新生成对象的运行面口径不再明显冲突
2. `skill-scout` / `skill-squadron` / `private-catalog` 的字段与说明稳定
3. 对象级最终复核清单不再存在阻塞项
4. 本主题的 rename 策略与退出条件有明确落点
5. 主线文档不再持续膨胀，主入口保持精简

## 7. 下一步优先级

当前更合理的下一步顺序是：

1. 按 `design/03az_closeout_criteria_and_exit_standard_v1.md` 做封板判断
2. 继续校正运行面与项目级 catalog 的一致性
3. 用 `skill-squadron` 当前模型验证对象图与分组结果
4. 仅在出现新阻塞项时，再回到对象级治理

## 8. 当前结论

`03_plan.md` 不再承担历史阶段计划，而只承担：

- 当前剩余行动项
- 执行边界
- 下一步优先级

后续如果某项行动已经落地，应直接从本文件移除，而不是继续累积阶段性历史说明。
