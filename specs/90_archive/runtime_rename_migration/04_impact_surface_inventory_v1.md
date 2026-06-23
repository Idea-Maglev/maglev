# runtime rename migration impact surface inventory v1

> 状态：已完成
> 作用：盘点主流程核心四对象在当前仓库中的主要 rename 影响面，为后续迁移 checklist 提供依据。

## 1. 对象范围

1. `maglev-standup`
2. `maglev-create-spec`
3. `maglev-quick-dev`
4. `maglev-cross-validate`

## 2. 当前主要影响面

### A. Workflow 入口层

当前直接绑定旧运行名的 workflow 包括：

- `.agents/workflows/standup.md`
- `.agents/workflows/create-spec.md`
- `.agents/workflows/quick-dev.md`
- `.agents/workflows/validate-all.md`

判断：

- 这是最直接的运行入口面
- 任何物理 rename 都必须先明确这些 workflow 是否同步迁移

### B. 主流程协作层

当前仍直接引用旧运行名的对象包括：

- `.agents/skills/entry-router/SKILL.md`
- `.agents/skills/entry-router/references/step-02-assess-context.md`
- `.agents/skills/entry-router/references/step-03-select-route.md`
- `.agents/skills/requirement-convergence/SKILL.md`
- `.agents/skills/requirement-convergence/references/step-03-ready-gate.md`
- `.agents/skills/requirement-convergence/references/step-04-handoff.md`
- `.agents/skills/skill-squadron/references/step-02-group.md`
- `.agents/skills/skill-squadron/references/step-03-patrol.md`
- `.agents/skills/skill-squadron/references/step-04-impact.md`

判断：

- 这是 rename 的一类硬依赖面
- 若不统一，这些协作对象会继续按旧名工作

### C. Catalog 与治理层

当前 `.agents/private-catalog.yaml` 中，四对象的：

- `name`
- `path`
- `target`

仍全部绑定旧运行名。

判断：

- 这是迁移时最需要集中处理的一层
- 若只改 skill 目录而不改 catalog，分发会直接失真

### D. Reality 与能力快照层

当前仍涉及四对象名称表达的现役说明包括：

- `specs/10_reality/01_requirements.md`
- `specs/10_reality/distribution_runtime.md`
- `docs/marketing/assets/capability_snapshot/published.md`

判断：

- 这层已开始双写，但仍未完成统一
- 属于物理 rename 前应先稳定的结构说明层

### E. 对外表达层

当前 `docs/marketing/assets/` 下多篇面向外部受众文档仍以旧运行名为主要表达方式，包括：

- `for_developers/published.md`
- `for_tech_leads/published.md`
- `for_decision_makers/published.md`
- `for_enterprises/published.md`
- `problem_statement/published.md`
- `why_ai_coding_needs_governance/published.md`
- `legacy_system_showcase/published.md`

判断：

- 这是影响面最大的一层
- 适合放在结构与运行面稳定之后，再按批次做双写统一

## 3. 当前分层优先级

建议优先级如下：

1. Workflow 入口层
2. 主流程协作层
3. Catalog 与治理层
4. Reality 与能力快照层
5. 对外表达层

## 4. 当前结论

四对象的 rename 不是“改四个目录名”这么简单，而是一个跨运行入口、协作对象、catalog、Reality 与对外文档的多层迁移动作。

因此，后续若真的进入 rename execution，必须严格按分层优先级推进。
