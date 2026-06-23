# skill结构性升级 skill-squadron 第一轮巡逻任务单

> 状态：草案
> 作用：将治理清单转成可执行的批量巡逻批次，供 `skill-squadron` 使用。

## 1. 使用原则

本任务单的目标不是一次性处理全部对象，而是：

1. 按结构问题类型分批巡逻
2. 优先处理高杠杆、高误导、高缺口对象
3. 保持每一批的目标单一，避免批次内问题类型过杂

## 2. 巡逻批次

### Batch 1: 前段缺口批次

目标：

- 补齐当前最关键的显性能力缺口

对象：

- `需求收敛`

当前任务：

1. 继续稳定 `需求收敛` 的 workflow 结构
2. 明确它和 `现状同步`、`方案设计` 的接口
3. 评估它是否需要进入显性对象化阶段
4. 引入外部对标，验证其是否应固定为：
   - `入口分流`
   - `需求定义`
   - `Ready Gate`

优先级：

- P0

### Batch 2: 生命周期后段闭环批次

目标：

- 补齐后段闭环，而不是继续只做前段设计和中段实施

对象：

- `crystallization`
- `思考沉淀`
- `knowledge-check`

当前任务：

1. 继续切清“思考归档链”和“事实结晶链”
2. 保证 `knowledge-check` 不再误占需求归档语义
3. 继续稳定 `现实结晶` workflow 的编排结构
4. 引入外部对标，验证“知识资产链”和“事实状态链”的分离是否符合更成熟做法

优先级：

- P0

### Batch 3: 质量层稳定性批次

目标：

- 保持质量层三面稳定，并持续把碎片对象压回能力面之下

对象：

- `spec-audit-surface`
- `review-validation-surface`
- `test-design-surface`

当前任务：

1. 检查质量层三面边界是否仍稳定
2. 确认旧碎片对象不会被重新恢复为运行面入口
3. 避免 `maglev-cross-validate` 重新吞掉整个质量层
4. 引入外部对标，验证质量层是否仍应以“能力面 + guardrail / eval 机制”组织

优先级：

- P1

### Batch 4: spec pipeline 降显性批次

目标：

- 把内部模块重新收回一级能力对象内部

对象：

- `maglev-spec-ingest`
- `maglev-spec-draft`
- `maglev-spec-crystallize`
- `maglev-validate-spec-context`

当前任务：

1. 已固定它们在 `方案设计` 内部的模块链位置
2. 已避免继续作为一级心智暴露
3. 已完成与 `现实结晶` 的语义切分

当前状态：

- 本批次已完成
- 四个旧目录已退出运行面
- 物理内部化结果已转入 `spec_pipeline_internalization` 新主题

优先级：

- P2

### Batch 5: 体系级能力簇稳定性批次

目标：

- 检查协作承接区是否已经足够稳定，不急于误拆或误合

对象：

- `maglev-bootstrapper`
- `maglev-legacy-adopter`
- `maglev-reverse-spec`
- `skill-scout`
- `skill-squadron`
- `maglev-map-maker`
- `maglev-librarian`

当前任务：

1. 检查能力簇内部边界是否清楚
2. 检查修辞表达是否持续压过结构职责
3. 避免过早把协作承接簇错误收成单点对象
4. 引入外部对标，验证体系级能力是否更适合协作承接而不是单点收口

优先级：

- P2

## 3. 当前执行顺序

当前更建议的巡逻顺序是：

1. `Batch 1: 前段缺口批次`
2. `Batch 2: 生命周期后段闭环批次`
3. `Batch 3: 质量层收口批次`
4. `Batch 4: spec pipeline 降显性批次`
5. `Batch 5: 体系级能力簇稳定性批次`

## 4. 当前默认巡逻切片

基于 `02zl_skill_squadron_graph_preflight_v1.md` 的预演结果，当前可直接复用三组默认巡逻切片：

1. `主流程前中段组`
   - `entry-router`
   - `maglev-standup`
   - `requirement-convergence`
   - `maglev-create-spec`
   - `maglev-quick-dev`
   - `maglev-cross-validate`
2. `体系级与后段闭环组`
   - `crystallization`
   - `knowledge-check`
   - `maglev-bootstrapper`
   - `maglev-legacy-adopter`
   - `maglev-reverse-spec`
   - `maglev-map-maker`
   - `maglev-librarian`
   - `skill-scout`
   - `skill-squadron`
3. `质量层组`
   - `spec-audit-surface`
   - `review-validation-surface`
   - `test-design-surface`

使用方式：

- 当巡逻目标是“主流程承接是否顺滑”时，优先从主流程前中段组开始。
- 当巡逻目标是“后段闭环、现状表达与能力进化是否协同”时，优先从体系级与后段闭环组开始。
- 当巡逻目标是“质量层边界是否清楚、碎片对象是否回收到能力面之下”时，优先从质量层组开始。
- 只要 catalog 关系图发生变化，仍应先重新跑分组，再决定是否沿用默认切片。

## 5. 当前结论

到这一步为止，`skill-squadron` 已经不只是有分析底表和治理清单，而是有了可执行的第一轮巡逻批次。

后续如果进入真正的批量治理，建议优先按本任务单逐批推进，而不是从全量对象列表随机开始。

其中 `Batch 1` 的第一轮外部对标结果已落在：

- `02i_requirement_convergence_external_benchmark.md`

`Batch 2` 的第一轮外部对标结果已落在：

- `02j_crystallization_and_knowledge_capture_external_benchmark.md`

`Batch 4` 的第一轮外部对标结果已落在：

- `02k_quality_layer_external_benchmark.md`

`Batch 5` 的第一轮外部对标结果已落在：

- `02l_system_level_clusters_external_benchmark.md`
