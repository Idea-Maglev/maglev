# 修复逆向事实 (Facts) 归档缺失

## 问题 (Problem)
在 `maglev-reverse-spec` 流程中，生成的 `input_facts.md`（包含关键的意图与推测）在任务结束后丢失。这是因为原有的 `step-05-commit-index.md` 只是简单地写入了 Spec 文件，没有执行标准的 "上下文归档" (Context Archival) 动作，且临时文件被后续流程清理。

## 解决方案 (Solution)
废弃手写的 Step 5，替换为调用标准的 `maglev-spec-crystallize` 工作流。

### 变更详情

1.  **修改 `reverse-spec.workflow.md`**:
    *   将 Step 5 的引用从 `step-05-commit-index.md` 改为 `../maglev-spec-crystallize/references/crystallize.workflow.md`。
    *   传递参数 `output_base: specs/10_reality`，确保逆向生成的 Spec 落库到 Reality 层（现状层）。

2.  **废弃 `step-05-commit-index.md`**:
    *   该文件将被不再被引用。

## 影响 (Impact)
*   **一致性**: 逆向 Spec 的归档逻辑与正向生成完全一致。
*   **可靠性**: `input_facts.md` 将被自动复制到 `specs/.../context/` 目录下，作为永久的上下文留存。
*   **整洁性**: 临时文件将由 Crystallize 技能统一清理。
