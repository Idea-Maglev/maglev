---
title: "Spec Provenance Governance - 交叉验证报告"
generated_at: "2026-06-03"
generator: integrated-validator
---

# 交叉验证报告

## 执行摘要

| 维度 | 得分 | 状态 | 证据 |
|---|---:|---|---|
| Requirements ↔ Design | 100% | 通过 | 25 个 AC 全部在设计覆盖表中出现 |
| Design ↔ Implementation | 100% | 通过 | 7 个目标流程文件均包含对应 provenance 规则 |
| Spec ↔ Validation Rules | 100% | 通过 | spec-audit-surface 已包含正向/反向覆盖与来源覆盖评分 |
| Artifact Purity | 100% | 通过 | hard 扫描无 findings |
| Link Integrity | 100% | 通过 | 本 spec 所有相对链接均可达 |
| **综合** | **100%** | **通过** | 无 blocker / major finding |

## 验证范围

### Spec 文件

- [00_intent.md](./00_intent.md)
- [01_requirements.md](./01_requirements.md)
- [02_design.md](./02_design.md)
- [03_plan.md](./03_plan.md)
- [context/input_facts.md](./context/input_facts.md)

### 实施文件

- [requirement-convergence step-02](../../../../.agents/skills/requirement-convergence/references/step-02-define-requirements.md)
- [requirement-convergence PRD output contract](../../../../.agents/skills/requirement-convergence/references/prd-output-contract.md)
- [unified draft template](../../../../.agents/skills/_internal/spec-pipeline/draft/unified-draft-template.md)
- [spec draft polymorphic design step](../../../../.agents/skills/_internal/spec-pipeline/draft/step-02-polymorphic-design.md)
- [spec-audit requirements step](../../../../.agents/skills/spec-audit-surface/references/step-02-audit-requirements.md)
- [spec-audit cluster step](../../../../.agents/skills/spec-audit-surface/references/step-03-audit-spec-cluster.md)
- [spec-audit findings synthesis](../../../../.agents/skills/spec-audit-surface/references/step-04-synthesize-findings.md)

## 详细验证

### Requirements ↔ Design

| 检查项 | 结果 |
|---|---|
| requirements 中 AC 总数 | 25 |
| design 中未出现的 AC | 0 |
| design 覆盖表未覆盖的 AC | 0 |
| 结论 | 通过 |

### Design ↔ Implementation

| 目标文件 | 关键规则 | 结果 |
|---|---|---|
| `step-02-define-requirements.md` | 来源依据、`source_summary`、`context_judgement`、`evidence` | 通过 |
| `prd-output-contract.md` | `source_basis`、AC provenance 字段 | 通过 |
| `unified-draft-template.md` | requirements/design 来源依据、AC/Decision provenance、仅语义变更时保留变更记录 | 通过 |
| `step-02-polymorphic-design.md` | Provenance 要求、设计消费 requirements provenance、AI 对话分流 | 通过 |
| `step-02-audit-requirements.md` | requirements provenance 审计、反向覆盖、finding 分级 | 通过 |
| `step-03-audit-spec-cluster.md` | Decision provenance、语义变更记录、项目健康风险 | 通过 |
| `step-04-synthesize-findings.md` | 来源覆盖评分、`provenance_findings` | 通过 |

### 来源与覆盖验证

| 检查项 | 结果 |
|---|---|
| AC / Decision → 来源 | 已在模板和审计规则中要求 |
| 来源 → AC / Decision | 已在审计规则中要求反向覆盖 |
| AI 对话原始记录 | 已明确只保留摘要，高价值思考进入 `docs/thinking/` |
| 语义变更记录 | 已明确内嵌在对应 spec 文件 |
| 变更过多的项目健康风险 | 已在设计和审计规则中要求提示 |

## Findings

### Critical

无。

### Warning

无。

### Info

- 本次未实现自动化扫描脚本，符合当前 spec 的 Out of Scope。
- 后续如要提高可执行性，可在下一轮新增 provenance checker，但不影响当前流程规则落地。

## 验证命令

```bash
python3 - <<'PY'
from pathlib import Path
import re
base=Path('specs/20_evolution/active/spec-provenance-governance')
req=(base/'01_requirements.md').read_text()
design=(base/'02_design.md').read_text()
acs=sorted(set(re.findall(r'AC-F\\d+-\\d+', req)), key=lambda x: [int(n) for n in re.findall(r'\\d+', x)])
coverage_section=design.split('## 验收映射',1)[1]
covered=set(re.findall(r'AC-F\\d+-\\d+', coverage_section))
print(len(acs), [ac for ac in acs if ac not in covered])
PY
```

```bash
rg -n "来源依据|来源摘要|上下文判定|source_summary|context_judgement|evidence|双向覆盖|反向覆盖|provenance|语义变更|docs/thinking|来源覆盖" \
  .agents/skills/requirement-convergence/references/step-02-define-requirements.md \
  .agents/skills/requirement-convergence/references/prd-output-contract.md \
  .agents/skills/_internal/spec-pipeline/draft/unified-draft-template.md \
  .agents/skills/_internal/spec-pipeline/draft/step-02-polymorphic-design.md \
  .agents/skills/spec-audit-surface/references/step-02-audit-requirements.md \
  .agents/skills/spec-audit-surface/references/step-03-audit-spec-cluster.md \
  .agents/skills/spec-audit-surface/references/step-04-synthesize-findings.md
```

```bash
python3 .agents/skills/artifact-purity-keeper/scripts/scanner.py --severity hard \
  specs/20_evolution/active/spec-provenance-governance \
  .agents/skills/requirement-convergence/references/step-02-define-requirements.md \
  .agents/skills/requirement-convergence/references/prd-output-contract.md \
  .agents/skills/_internal/spec-pipeline/draft/unified-draft-template.md \
  .agents/skills/_internal/spec-pipeline/draft/step-02-polymorphic-design.md \
  .agents/skills/spec-audit-surface/references/step-02-audit-requirements.md \
  .agents/skills/spec-audit-surface/references/step-03-audit-spec-cluster.md \
  .agents/skills/spec-audit-surface/references/step-04-synthesize-findings.md
```

```bash
git diff --check
```

## 结论

本轮 spec provenance governance 已通过综合验证。当前状态可进入人工复核、提交或后续结晶判断。

