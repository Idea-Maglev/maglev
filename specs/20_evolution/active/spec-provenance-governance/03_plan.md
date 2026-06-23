# Plan — Spec Provenance Governance

## 来源依据

| 来源 | 类型 | 用途 |
|---|---|---|
| [02_design.md](./02_design.md) | design | 实施任务拆解依据 |
| [01_requirements.md](./01_requirements.md) | requirements | 验收标准依据 |

## 实施任务

| Task | 内容 | 覆盖设计 | 状态 |
|---|---|---|---|
| T-1 | 更新 `requirement-convergence` 结构化需求生成规则，要求来源依据、来源摘要、上下文判定和证据。 | requirement-convergence 集成 | done |
| T-2 | 更新 `prd-output-contract.md`，在稳定需求契约中加入 AC provenance 字段和来源依据列表。 | PRD 输出契约 | done |
| T-3 | 更新 `unified-draft-template.md`，加入 requirements/design 来源依据、AC/Decision provenance 和内嵌变更记录模板。 | 模板设计 | done |
| T-4 | 更新 `step-02-polymorphic-design.md`，要求 design 消费 requirements provenance，不只消费最终 AC 文本。 | spec-designer 集成 | done |
| T-5 | 更新 `spec-audit-surface` requirements 审计，加入来源依据、AC provenance 和双向覆盖检查。 | 正向/反向来源审计 | done |
| T-6 | 更新 `spec-audit-surface` spec cluster 审计，加入 Decision provenance、语义变更记录和项目健康风险检查。 | design 审计 | done |
| T-7 | 更新 `spec-audit-surface` findings 汇总，加入来源覆盖评分与 provenance findings。 | 审计结果合成 | done |

## 验证计划

| 验证项 | 方法 | 期望 |
|---|---|---|
| 目标文件均被修改 | `rg` 检查 provenance 关键词 | 所有目标 skill/template/audit 文件出现对应规则 |
| 相对链接可达 | 脚本解析本 spec 中 Markdown 链接 | 全部链接存在 |
| 产物洁净度 | `artifact-purity-keeper` hard 扫描 | 无 hard findings |
| 工作区状态 | `git status --short --branch` | 变更集中在本 spec 与目标 skill 文件 |

## 变更记录

| 日期 | 变更对象 | 变更内容 | 变更原因 | 来源依据 |
|---|---|---|---|---|
| 2026-06-03 | 03_plan.md | 新增实施计划并记录已完成任务。 | 进入 context-implementer 后需要闭环记录实施任务。 | [02_design.md](./02_design.md) 实施顺序建议 |
