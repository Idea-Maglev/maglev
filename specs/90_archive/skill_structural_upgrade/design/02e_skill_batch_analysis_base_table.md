# skill结构性升级 Skill 批量分析底表 v1

> 状态：草案
> 作用：为 `skill-squadron` 的批量分析提供统一字段面。

## 1. 设计目标

这张底表不负责给出最终裁决，而负责提供一个统一分析面，使后续可以稳定回答：

1. 一个对象属于哪个顶层能力
2. 它在系统承接视图中属于哪一层
3. 它当前是稳定承接、协作承接、缺口还是已移除旧对象
4. 它的主要风险是什么
5. 后续更适合保留、改名、降级、合并还是继续观察

## 2. 建议字段

后续批量分析至少建议统一使用以下字段：

| 字段 | 说明 |
| :--- | :--- |
| `object_name` | 当前对象名 |
| `top_level_capability` | 所属顶层能力 |
| `exposure_level` | 用户显性 / 体系显性 / 体系内部 |
| `system_layer` | 所属系统承接层 |
| `current_role` | 一级能力对象 / 协作对象 / 内部模块 / workflow 步骤 / 已移除旧对象 |
| `coverage_status` | 稳定承接 / 协作承接 / 缺口 / 过度承接 |
| `risk_type` | 命名风险或结构风险类型 |
| `current_direction` | Keep / Rename / Demote / Merge / Workflow-first / Observe |
| `notes` | 简短备注 |

## 3. 底表 v1

| object_name | top_level_capability | exposure_level | system_layer | current_role | coverage_status | risk_type | current_direction | notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `maglev-standup` | `现状同步` | 用户显性 | `Core Flow Layer` | 一级能力对象 | 稳定承接 | 结构重要性被轻量词压低 | Keep | 对外优先按“现状同步”解释 |
| `maglev-create-spec` | `方案设计` | 用户显性 | `Core Flow Layer` | 一级能力对象 | 稳定承接 | 跨生命周期语义吞并 | Keep | 对外优先按“方案设计”解释 |
| `maglev-quick-dev` | `上下文实施` | 用户显性 | `Core Flow Layer` | 一级能力对象 | 稳定承接 | 错误价值重心前置 | Keep | 对外优先按“上下文实施”解释 |
| `maglev-cross-validate` | `综合验证` | 用户显性 | `Core Flow Layer` + `Quality / Guardrail Layer` | 一级能力对象 / 汇聚点 | 稳定承接 | 动作语义与结构角色混写 | Keep | 防止重新吞并整个质量层 |
| `maglev-bootstrapper` | `整体接入` | 体系显性 | `Infrastructure Layer` | 协作对象 | 协作承接 | 低 | Keep | 接入能力簇成员 |
| `maglev-legacy-adopter` | `整体接入` | 体系显性 | `Infrastructure Layer` | 协作对象 | 协作承接 | 低 | Keep | 接入能力簇成员 |
| `maglev-reverse-spec` | `整体接入` | 体系显性 | `Infrastructure Layer` | 协作对象 | 协作承接 | 低 | Keep | 接入能力簇成员，同时约束 Reality 标准 |
| `skill-scout` | `能力进化` | 体系显性 | `Evolution & Governance Layer` | 协作对象 | 协作承接 | 修辞表达可控 | Keep | 进化能力簇成员 |
| `skill-squadron` | `能力进化` | 体系显性 | `Evolution & Governance Layer` | 协作对象 | 协作承接 | 修辞表达可控 | Keep | 进化能力簇成员 |
| `maglev-map-maker` | `现状表达` | 体系内部 | `Infrastructure Layer` | 协作对象 | 协作承接 | 修辞表达偏强 | Keep | 现状表达能力簇成员 |
| `maglev-librarian` | `现状表达` | 体系内部 | `Infrastructure Layer` | 协作对象 | 协作承接 | 角色化命名 | Keep | 现状表达能力簇成员 |
| `entry-router` | `需求收敛` | 体系显性 | `Entry / Routing Layer` | 一级能力对象 | 稳定承接 | 需持续维护下游路由表 | Keep | 当前正式入口路由对象 |
| `knowledge-check` | `思考沉淀` | 体系内部 | `Quality / Guardrail Layer` | 一级能力对象 | 稳定承接 | 与现实结晶边界需持续保持清楚 | Keep | 当前正式知识沉淀检查对象 |
| `10_reality` | `现状表达` | 体系内部 | `Reality / Context Layer` | 反向约束对象 | 稳定承接 | 无 | Keep | 不是 skill，但必须进入分析视图 |
| `requirement-convergence` | `需求收敛` | 用户显性 | `Core Flow Layer` | 一级能力对象 | 稳定承接 | 前段三段式仍需继续观察 | Keep | 当前已形成真实 skill，workflow 文件仅作为入口包装 |
| `crystallization` | `现实结晶` | 体系内部 | `Reality / Context Layer` + `Infrastructure Layer` | 一级能力对象 | 稳定承接 | 与知识沉淀链边界需持续保持清楚 | Keep | 当前已形成真实 skill，workflow 文件仅作为入口包装 |
| `思考沉淀` | 非用户主流程能力 | 体系内部 | `Core Flow Layer` + `Reality / Context Layer` | 触发链 / 检查动作 | 协作承接 | 语义易与需求归档混写 | Observe | 当前由知识沉淀链承接 |
| `maglev-spec-ingest` | `方案设计` | 体系内部 | `Core Flow Layer` | 历史内部模块 | 已退出运行面 | 已并入 `maglev-create-spec/references/pipeline/ingest/` | Removed | 物理内部化已完成 |
| `maglev-spec-draft` | `方案设计` | 体系内部 | `Core Flow Layer` | 历史内部模块 | 已退出运行面 | 已并入 `.agents/skills/_internal/spec-pipeline/draft/` | Removed | 物理内部化已完成 |
| `maglev-spec-crystallize` | `方案设计` | 体系内部 | `Core Flow Layer` | 历史内部模块 | 已退出运行面 | 已并入 `.agents/skills/_internal/spec-pipeline/crystallize/` | Removed | 物理内部化已完成 |
| `maglev-validate-spec-context` | `方案设计` / `综合验证` 边界 | 体系内部 | `Quality / Guardrail Layer` | 历史内部模块 | 已退出运行面 | 已并入 `maglev-create-spec/references/pipeline/validate-context/` | Removed | 物理内部化已完成 |
| `contribute_methodology` | `能力进化` | 体系内部 | `Evolution & Governance Layer` | 历史专项对象 | 已退出运行面 | 不再承接当前 Maglev 主干 | Removed | 已完成清理，不再作为现役治理对象 |
| `maglev-audit-prd` | `综合验证` | 体系内部 | `Quality / Guardrail Layer` | 历史质量对象 | 已退出运行面 | 已被三面替代 | Removed | 历史上并入 `spec-audit-surface` |
| `maglev-audit-spec` | `综合验证` | 体系内部 | `Quality / Guardrail Layer` | 历史质量对象 | 已退出运行面 | 已被三面替代 | Removed | 历史上并入 `spec-audit-surface` |
| `maglev-code-review-backend` | `综合验证` | 体系内部 | `Quality / Guardrail Layer` | 历史质量对象 | 已退出运行面 | 已被三面替代 | Removed | 历史上并入 `review-validation-surface` |
| `maglev-code-review-frontend` | `综合验证` | 体系内部 | `Quality / Guardrail Layer` | 历史质量对象 | 已退出运行面 | 已被三面替代 | Removed | 历史上并入 `review-validation-surface` |
| `maglev-plan-unit-tests-backend` | `综合验证` | 体系内部 | `Quality / Guardrail Layer` | 历史质量对象 | 已退出运行面 | 已被三面替代 | Removed | 历史上并入 `test-design-surface` |
| `maglev-plan-unit-tests-frontend` | `综合验证` | 体系内部 | `Quality / Guardrail Layer` | 历史质量对象 | 已退出运行面 | 已被三面替代 | Removed | 历史上并入 `test-design-surface` |
| `maglev-create-test-cases` | `综合验证` | 体系内部 | `Quality / Guardrail Layer` | 历史质量对象 | 已退出运行面 | 已被三面替代 | Removed | 历史上并入 `test-design-surface` |
| `maglev-changelog-generator` | 非核心主流程能力 | 体系内部 | `Specialized Support Layer` | 支撑对象 | 协作承接 | 低 | Keep | 发布场景专项支持 |
| `maglev-content-sync` | 非核心主流程能力 | 体系内部 | `Specialized Support Layer` | 支撑对象 | 协作承接 | 名称较稳 | Keep | 内容写作前置同步 |
| `maglev-create-prd` | `需求收敛` 前段相关 / 非核心主流程能力 | 体系显性 | `Specialized Support Layer` | 支撑对象 | 吸收后退出运行面 | 已被 `requirement-convergence` 吸收 | Removed | 稳定需求产物输出已并入 `requirement-convergence`，对象进入删除回合 |
| `maglev-design-ux` | 非核心主流程能力 | 体系显性 | `Specialized Support Layer` | 支撑对象 | 协作承接 | 低 | Keep | 设计专项支持能力 |
| `maglev-tutor` | 非核心主流程能力 | 体系显性 | `Specialized Support Layer` | 支撑对象 | 协作承接 | 修辞表达偏强 | Keep | 教学与上手支持 |
| `maglev-updater` | `整体接入` 相关 | 体系显性 | `Infrastructure Layer` | 协作对象 | 协作承接 | 低 | Keep | 安装后更新与同步能力 |
| `mermaid-expert` | 非核心主流程能力 | 体系内部 | `Specialized Support Layer` | 支撑对象 | 协作承接 | 低 | Keep | 通用图示专项能力，作为 Mermaid 语法修复工具保留 |

## 4. 当前结论

这张底表现在已经覆盖当前仓库的关键 skill 与 workflow-first 对象，并足以支撑 `skill-squadron` 做第一轮批量分析，但还不足以直接支撑自动治理。

后续若要进入更稳定的批量治理，下一步应继续补：

1. catalog 与底表的持续同步
2. 更稳定的字段枚举
3. 每种 `current_direction` 的标准处理规则
