---
description: Maglev Gatekeeper - 执行代码校准、索引检查并生成 Commit Message
metadata:
  formal_action_name: 提交信息生成
  object_kind: workflow
  author: Maglev contributors
  last_updated: 2026-03-30
---

# The Maglev Gatekeeper (守门人)

> **Context**: 你即将提交代码。在生成 Message 之前，必须通过 **"Gatekeeper Check"**。

## Step 1: Calibration Check (关口校准)
1.  **Drift Detection**:
    *   扫描本次 Commit 的代码变更 (`git status`).
    *   检查这些变更是否有对应的 Spec 支撑？
    *   *Smart Check*: 推荐调用 `spec-audit-surface` 进行输入一致性扫描。
    *   *Self-Correction*: 如果发现代码逻辑变更但没有关联的 Spec 修改，**必须**询问用户：
        > "检测到代码变更 [文件X]，但未发现 Spec 变更。这是否符合预期？建议先更新 Spec 以保持一致性。"

## Step 2: Indexing Check (索引维护)
2.  **Breadcrumb Audit**:
    *   对于每个修改的源码目录，检查其父级 `README.md` (或 `INDEX.md`) 是否存在。
    *   如果存在但未更新（缺少新函数的摘要），**主动提议**更新索引。
    *   *Prompt*: "我注意到 `src/utils/` 下新增了 `verifyToken` 函数，我将帮您把它的摘要写入 `src/utils/README.md`。"

## Step 3: Generate Message (生成文案)
3.  **Commit Message**:
    *   生成符合 Maglev 规范的 Commit Message。
    *   **Structure**:
        ```text
        <Type>(<Scope>): <Subject>

        <Body>
        - Point 1
        - Point 2

        Verification:
        - [x] Test A Passed
        
        Ref: #Issue-ID | Spec: feat-XXX
        ```
    *   **Traceability**: 必须填满 `Ref` 字段，关联 Issue 或 Spec 文件。

---
**Turbo Mode**: 如果用户使用 `/generate-commit-message -y`，则假设所有检查通过，但仍需在生成的 Message 中注明 "Skipped Calibration"。
