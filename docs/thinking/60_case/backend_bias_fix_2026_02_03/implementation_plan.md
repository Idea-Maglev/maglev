# Backend Bias Fix Plan (后端偏科修正方案 - Split Edition)

## 1. 修正策略 (Correction Strategy)

### Part 1: Spec Fix (技术方案修正)
*   **Target Skill**: `maglev-create-spec`
*   **A. Interview (访谈)**: `step-00-socratic-interview.md`
    *   **Action**: 增加开局检查 "Has UI?"。
    *   **Logic**:
        *   If UI: 强制询问 Visuals/Interaction。
        *   If Headless: 聚焦 API/Security。
*   **B. Draft (生成)**: `maglev-spec-draft/step-02-polymorphic-design.md`
    *   **Action**: Zone 2 增加条件判断。
        *   Has UI -> 强制生成 Frontend Spec。
        *   Headless -> 标记 N/A。

### Part 2: PRD Fix (产品文档修正)
*   **Target Skill**: `maglev-create-prd`
*   **A. Discovery (定性)**: `step-c-02-discovery.md`
    *   **Action**: 在确认 Goal 时，顺便确认 "Project Type" (App/Web/API-Service)。
    *   **Output**: 将 `type: ui | headless` 写入 Context 或临时变量。
*   **B. Journeys (故事)**: `step-c-04-journeys.md`
    *   **Action**: 引导策略分支。
        *   **UI Project**: Story 必须包含 "Screen/Page" 描述 (e.g., "See the Dashboard").
        *   **Headless Project**: Story 聚焦数据流 (e.g., "Receive webhook").

## 2. 实施清单 (Execution List)

### Phase 1: Spec Fix
*   [ ] Update `create-spec/step-00` (Has UI check).
*   [ ] Update `spec-draft/step-02` (Conditional Frontend).

### Phase 2: PRD Fix
*   [ ] Update `create-prd/step-c-02` (Add Type Check).
*   [ ] Update `create-prd/step-c-04` (Conditional Story Guide).
