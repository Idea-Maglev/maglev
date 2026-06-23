# Quick Spec Refactor Task (中文)

- [x] **Phase 1: Rename & Cleanup (重命名与清理)**
    - [x] Rename directory `maglev-quick-spec` to `maglev-create-spec`.
    - [x] Update `SKILL.md` name.
    - [x] Update `coordinator.workflow.md` (Pending check).
    - [x] Update `.agents/workflows/create-spec.md` wrapper.
    - [x] Delete legacy `quick-spec.workflow.md`.

- [x] **Phase 2: Context Handoff (上下文交接)**
    - [x] Update `step-00-socratic-interview.md`: Output to `.maglev/temp/interview_context.md`.
    - [x] Update `wrapper-01-ingest.md`: Ingest from `.maglev/temp/interview_context.md`.

- [x] **Phase 3: Logic Optimization (逻辑优化)**
    - [x] Update `step-00-socratic-interview.md`: Dynamic questioning.
    - [x] Update `wrapper-01b-validate.md`: Interactive Gatekeeper (Retry/Force/Abort).

- [x] **Phase 4: Verification (验证)**
    - [x] Check file links (Verified via ls).
