# Create Spec Workflow Audit & Fortification Plan

## 0. 目标 (Goal)
将 "Maglev Fortification" 标准应用到 `maglev-create-spec` 技能。
建立 **Pre-flight Check (Step 00)** 和 **Post-flight Verify (Step 04)** 机制，并确保全链路中文与 OpenSpec 的一致性。

## 1. 审计发现 (Likely Issues)
基于逆向工程的经验，预计存在以下问题：
*   **Missing Self-Check**: 启动前未检查依赖 (Draft/Crystallize)。
*   **Missing Verification**: 结束后未验证文件是否落地。
*   **Language Leak**: 部分 Prompt 可能仍包含英文。
*   **Consistency**: 需要确认 `wrapper-01-ingest.md` 和 `step-02` 是否完全对齐了新的 OpenSpec 标准。

## 2. 加固方案 (Strategy)

### A. Pre-flight (Step 00)
创建 `step-00-integrity-check.md`:
*   Check `.maglev/temp` dir.
*   Check `maglev-spec-ingest` availability.
*   Check `maglev-spec-draft` availability.
*   Check `maglev-spec-crystallize` availability.

### B. Post-flight (Step 04)
创建 `step-04-verify-output.md`:
*   Assert `specs/20_evolution/active/{slug}/00_index.md` exists.
*   Check `context/input_facts.md` presence.

### C. Workflow Update
修改 `create-spec.workflow.md` 串联新步骤。

## 3. 执行顺序
1.  **List & Read**: Audit current files.
2.  **Create**: Step 00 & Step 04.
3.  **Refactor**: Ensure Step 01 (Ingest) & Step 02 (Draft) prompts are Chinese.
4.  **Wire**: Update Workflow.
