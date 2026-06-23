# Maglev 加固与 OpenSpec 标准化 (2026-02-03)

**摘要**: 本目录汇总了 2026年2月3日 进行的重大加固与标准化工作的思考过程。目标是将 Maglev 的三大核心工作流（逆向、Spec生成、PRD生成）全面对齐到 "企业级鲁棒性" 标准。

## 整合计划列表

| 序号 | 标题 | 描述 |
| :--- | :--- | :--- |
| **01** | [OpenSpec 标准化](./01_openspec_adoption.md) | 决定将 Spec 标准从 User Story 升级为 BDD 风格的 OpenSpec (Gherkin)。 |
| **02** | [逆向归档修复](./02_fix_reverse_archival.md) | 诊断并修复了逆向工程中 `input_facts.md` 丢失的问题。 |
| **03** | [逆向工程加固](./03_reverse_spec_audit.md) | 对 `maglev-reverse-spec` 技能的深度审计与加固策略。 |
| **04** | [Spec 生成加固](./04_create_spec_audit.md) | 将对称的加固标准应用到 `maglev-create-spec` 工作流。 |
| **05** | [PRD 生成加固](./05_create_prd_audit.md) | 将最终的加固标准应用到 `maglev-create-prd` 工作流。 |

## 关键成果
1.  **OpenSpec 标准**: 所有需求文档现在均使用 Gherkin (Given/When/Then) 格式。
2.  **三模态安全 (Tri-Modal Security)**: 所有核心工作流均具备 `step-00` (启动自检) 和 `step-XX` (产出验证) 双重门禁。
3.  **深度汉化**: 所有交互步骤均已完全汉化。
