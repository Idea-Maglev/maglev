# PRD Generation Audit & Fortification Plan

## 0. 目标 (Goal)
将 "Maglev Fortification" 标准应用到 `maglev-create-prd` 技能。
建立 **Pre-flight Check (Step 00)** 和 **Post-flight Verify (Step 99)** 机制，并完成全链路汉化。

## 1. 审计范围 (Audit Scope)
*   **Workflow**: `create-prd.workflow.md`
*   **Steps**:
    *   `step-c-01-init.md` (Initialization)
    *   `step-c-04-journeys.md` (Already audited/fixed for OpenSpec)
    *   `step-c-11-polish.md` (Final Polish)
    *   `step-c-12-complete.md` (Completion)

## 2. 发现的问题 (Potential Issues)
*   **No Pre-flight**: 启动前未检查 `.maglev/temp` 或依赖环境。
*   **No Post-flight**: 结束后未验证 `01_requirements.md` 等是否真正生成。
*   **Language**: `step-c-01` 等旧步骤可能仍包含英文。

## 3. 加固方案 (Strategy)

### A. Pre-flight (Step 00)
创建 `step-c-00-integrity-check.md`:
*   Check `.maglev/temp` existence.
*   Clean slate (remove old PRD drafts).

### B. Post-flight (Step 99)
创建 `step-c-99-verify-output.md`:
*   Verify `docs/prd/00_analysis.md` (if exists)
*   Verify `docs/prd/01_requirements.md` (The OpenSpec file)
*   Verify `docs/prd/02_plans.md`

### C. Localization
*   Scan `step-c-01` and others for English text and translate to Chinese.

## 4. 执行顺序
1.  **List**: Confirm file names.
2.  **Audit**: Read workflow & init step.
3.  **Create**: Step 00 & Step 99.
4.  **Refactor**: Localize steps.
5.  **Wire**: Update Workflow.
