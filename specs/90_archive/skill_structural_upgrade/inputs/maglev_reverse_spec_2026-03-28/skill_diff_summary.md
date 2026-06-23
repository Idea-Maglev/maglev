# Skill Diff Summary

## 修改的核心文件

- `SKILL.md`
- `references/reverse-spec.workflow.md`
- `references/step-00-integrity-check.md`
- `references/step-01-project-map.md`
- `references/step-01b-router-analysis.md`
- `references/step-02-page-analysis.md`
- `references/step-03-stack-trace.md`
- `references/step-03b-intent-enrichment.md`
- `references/step-04-cross-examination.md`
- `references/step-06-verify-output.md`
- `references/wrapper-04-spec-handoff.md`

## 新增的核心文件

- `references/reverse-principles.md`
- `references/reality-maturity-model.md`
- `references/reverse-extension-pack.md`
- `references/step-00b-output-profile.md`
- `references/step-01-evidence-acquisition.md`
- `references/step-03-data-structure-analysis.md`
- `references/step-05-reality-boost.md`
- `references/templates/reverse-output-template.md`
- `references/templates/rmm_scorecard_template.md`
- `references/templates/expert_review_queue_template.md`
- `scripts/mri_scanner.py`

## 删除的旧文件

- `references/step-01-scope-lock.md`
- `references/step-02-strata-analysis.md`
- `references/step-03-reconstruction.md`
- `references/legacy-tech-spec-template.md`
- `references/review-adversarial-reverse.xml`

## 本轮最重要的变化

1. 从旧版 Page-First 逆向，升级为证据驱动、入口自适应的通用逆向流程
2. 把数据结构分析提升为独立主步骤
3. 增加 `Lean / Standard / Deep` 输出档位
4. 增加 `Reality Boost / RMM / Expert Queue`
5. 增加 `Module Partition`，强制按模块粒度生成 reality 目录，禁止多模块混写
6. 清理旧流程残留与单点弱引用文件
7. 去掉业务污染，保留 Maglev 拟合
8. 新增红线：reverse 默认禁止修改业务实现、补回填脚本、执行数据修复或顺手修契约
9. 新增语言约束：reverse / reality 产物默认必须以中文为主，除非用户明确要求其他语言
