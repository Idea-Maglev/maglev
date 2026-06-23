# Skill Change Manifest

## 当前应回传的 skill 目录

- [maglev-reverse-spec](/Users/Maglev contributors/workspace/<private-repo-path-redacted>/pcp/mp-x-project/.agents/skills/maglev-reverse-spec)

建议直接以当前仓库中的：

- `.agents/skills/maglev-reverse-spec/`

作为回传基线，不再依赖 handoff 包中的 skill 快照副本。

## 当前应回传的核心文件

### 主入口
- `SKILL.md`

### 工作流与原则
- `references/reverse-spec.workflow.md`
- `references/reverse-principles.md`
- `references/reverse-extension-pack.md`
- `references/reality-maturity-model.md`

### 主流程步骤
- `references/step-00-integrity-check.md`
- `references/step-00b-output-profile.md`
- `references/step-01-evidence-acquisition.md`
- `references/step-01-project-map.md`
- `references/step-01b-router-analysis.md`
- `references/step-02-page-analysis.md`
- `references/step-03-data-structure-analysis.md`
- `references/step-03-stack-trace.md`
- `references/step-03b-intent-enrichment.md`
- `references/wrapper-04-spec-handoff.md`
- `references/step-04-cross-examination.md`
- `references/step-05-reality-boost.md`
- `references/step-06-verify-output.md`

### 模板与脚本
- `references/templates/reverse-output-template.md`
- `references/templates/rmm_scorecard_template.md`
- `references/templates/expert_review_queue_template.md`
- `scripts/mri_scanner.py`

## 本轮清理掉的冗余旧文件

以下文件已确认不再需要回传：

- `references/step-01-scope-lock.md`
- `references/step-02-strata-analysis.md`
- `references/step-03-reconstruction.md`
- `references/legacy-tech-spec-template.md`
- `references/review-adversarial-reverse.xml`

## 说明

这些删除项属于旧流程残留或已被新版主流程吸收的材料。
如果 Maglev 主仓仍存在这些文件，应优先以当前仓库中的最新 skill 为准，而不是再把它们合并回去。

## 本次同步补充的关键约束

- reverse 默认只允许观察、记录、建模、验证与归档，不允许顺手进入业务修复
- 除非用户明确要求其他语言，否则 reverse / reality 产物必须以中文为主
- 这两条约束已写入最新 `SKILL.md`、`reverse-principles.md`、`reverse-spec.workflow.md` 和 `reverse-output-template.md`

## 维护说明

- handoff 包不再维护 `skill_snapshot`，避免同仓双版本
- 后续若 skill 再变更，只需要同步 `.agents/skills/maglev-reverse-spec/`
