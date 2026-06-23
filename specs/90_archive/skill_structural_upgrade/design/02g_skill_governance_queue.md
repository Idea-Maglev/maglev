# skill结构性升级 Skill 治理清单 v1

> 状态：草案
> 作用：将批量分析底表按 `current_direction` 分组，形成可直接供 `skill-squadron` 使用的治理清单。

## 1. 使用方式

本清单不负责重新分析对象，而负责把底表里的结论按治理动作聚合。

同时，这份清单及其上游分析结果，应被视为 Maglev 的治理资产，而不是一次性巡逻记录。

后续 `skill-squadron` 可直接按以下分组巡逻：

1. 先看哪一组对象需要优先处理
2. 再在组内按能力簇或系统层继续细分
3. 最后进入具体对象判断或实施

## 2. `Keep`

这些对象当前方向明确，应保留并继续作为稳定能力或协作对象存在。

### 主流程稳定承接

- `maglev-standup`
- `maglev-create-spec`
- `maglev-quick-dev`
- `maglev-cross-validate`
- `entry-router`
- `requirement-convergence`
- `crystallization`
- `knowledge-check`

### 接入能力簇

- `maglev-bootstrapper`
- `maglev-legacy-adopter`
- `maglev-reverse-spec`
- `maglev-updater`

### 进化能力簇

- `skill-scout`
- `skill-squadron`

### 现状表达能力簇

- `maglev-map-maker`
- `maglev-librarian`
- `10_reality`

### 专项支持对象

- `maglev-content-sync`
- `maglev-design-ux`
- `maglev-tutor`
- `maglev-changelog-generator`
- `mermaid-expert`

## 3. `Demote`

这些对象在上一阶段被判定为应降显性，现已完成物理内部化并退出运行面。

- 已转入 `Removed`

## 4. `Keep as Surfaces`

这些对象已经收口成现役质量层能力面，应直接按现役对象治理，而不是继续当作“待聚合中的碎片”。

### 质量层现役能力面

- `spec-audit-surface`
- `review-validation-surface`
- `test-design-surface`

当前治理重点：

- 保持三面边界清晰
- 保持与 `maglev-cross-validate` 的汇聚关系稳定
- 不再把历史碎片对象当作主入口

## 5. `Removed`

这些对象已经退出运行面，不再作为现役治理对象巡逻。

### Spec Audit Surface 专项子对象

- `maglev-audit-prd`
- `maglev-audit-spec`

### Review / Validation Surface 专项子对象

- `maglev-code-review-backend`
- `maglev-code-review-frontend`

### Test Design Surface 专项子对象

- `maglev-plan-unit-tests-backend`
- `maglev-plan-unit-tests-frontend`
- `maglev-create-test-cases`

当前治理重点：

- 不恢复运行面入口
- 仅在历史分析和 Scout 证据中保留其客观痕迹
- 当前统一由质量层三面承接

## 6. `Observe`

这些对象当前保留观察，不立即进入重写或重组。

- `思考沉淀`

当前治理重点：

- 继续观察其上位结构是否稳定
- 再决定是否需要进入明确方向

## 7. `Removed`

这些旧对象已从运行面移除，不再进入治理候选。

- `contribute_methodology`
- `maglev-create-prd`
- `maglev-spec-ingest`
- `maglev-spec-draft`
- `maglev-spec-crystallize`
- `maglev-validate-spec-context`
- `atomizer`
- `maglev_archival_check`

当前治理重点：

- 不再作为运行面入口恢复
- 仅在历史分析材料中保留其问题证据

## 8. 当前优先级

如果按治理优先级排序，当前更建议：

### 第一优先级

`Keep as Surfaces`
  - 质量层三面

原因：

- 三面已进入运行面，但仍需要确认边界是否稳定

### 第二优先级

- `Merge`
  - 质量层专项子对象

原因：

- 这组会持续制造对象碎片化，需要持续压回三面之下

### 第三优先级

- `Demote`
  - spec pipeline 对象

原因：

- 方向已经相对明确，更多是后续表达收口问题

## 9. 当前结论

这张治理清单意味着：

- `skill-squadron` 现在已经不仅有分析底表
- 还有一份按处理方向分组的直接巡逻清单

后续如果进入批量治理，应优先以本清单而不是原始 skill 列表作为入口。
