# Maglev Quick Spec Refactor Plan

## 1. 验证结论 (Verification Findings)
经过审计，AI 提出的 critique **完全合理 (Valid)**，且切中要害：
1.  **Workflow Confusion**: `quick-spec.workflow.md` 引用了不存在的 `step-01-understand.md`，确系废弃文件。
2.  **Context Fragility**: `step-00` 使用相对路径 `./00_context.md`，极其危险 (Spec 目录可能尚不存在)。`wrapper-01` 确实忽略了这个输入。
3.  **Rigid Validation**: `wrapper-01b` 处于 "Strict Mode"，没有任何余地，不符合快速迭代直觉。
4.  **Mechanical**: 访谈脚本确实过于僵化。

## 2. 详细重构方案 (Refactoring Strategy)

### A. Renaming (Identity Correction)
*   **Rename**: `maglev-quick-spec` -> `maglev-create-spec`.
*   **Rationale**: "Quick" 具有误导性，暗示质量妥协。`create-spec` 与 `create-prd` 对齐，强调标准生产。
*   **Actions**:
    *   Move directory `solutions/starter-kit/.agents/skills/maglev-quick-spec` to `solutions/starter-kit/.agents/skills/maglev-create-spec`.
    *   Update `SKILL.md` name field.
    *   Update `coordinator.workflow.md` content references.
    *   Update `.agents/workflows/create-spec.md` (Wrapper) to point to new skill.
    *   Delete legacy `quick-spec.workflow.md`.

### B. Context Anchoring (Fixing Brain Drain)
*   **Target**: `references/step-00-socratic-interview.md`
*   **Change**:
    *   将输出路径改为 `{project-root}/.maglev/temp/interview_context.md` (绝对路径，临时区)。
    *   更新 Prompt：不仅是问答，更要"侧写" (Profile)。
*   **Target**: `references/wrapper-01-ingest.md`
*   **Change**:
    *   在指令中显式把 `{project-root}/.maglev/temp/interview_context.md` 作为 `input_facts` 的来源之一。

### C. Interactive Gatekeeper (Choice, not Compromise)
*   **Target**: `references/wrapper-01b-validate.md`
*   **Change**:
    *   **Logic**: 校验失败时，**暂停**并展示错误。
    *   **Menu**: 提供明确选项：
        *   `[R]etry`: 修正输入再试 (Safe Path)。
        *   `[F]orce`: 强制继续 (User Accepts Risk)。
        *   `[A]bort`: 退出。
    *   **Rationale**: 只有用户显式确认 "I accept the risk" 时才允许 "带病运行"，从而保证 Spec 的安全感。

### D. Dynamic Persona
*   **Target**: `references/step-00-socratic-interview.md`
*   **Change**:
    *   将 "Script" 改为 "Guidelines"。
    *   增加 "Adaptive Questioning" 指令：根据用户的回答深度，决定追问还是跳过。

## 3. 执行清单
1.  **Delete** `quick-spec.workflow.md`.
2.  **Update** `coordinator.workflow.md`.
3.  **Refactor** `step-00-socratic-interview.md`.
4.  **Update** `wrapper-01-ingest.md`.
5.  **Update** `wrapper-01b-validate.md`.
