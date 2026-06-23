---
name: 'wrapper-01-ingest'
description: '调用 spec pipeline 的 ingest 内部模块'
sub_workflow: './pipeline/ingest/ingest.workflow.md'
nextStepFile: './wrapper-01b-validate.md'
---

# Phase 1: Ingest (摄入)

## 指令
作为协调器，请按照以下指示调用内部模块链：

1.  **加载 ingest 模块**:
    读取并执行 `{sub_workflow}` 中的所有步骤。
    *   注意：这是一次 "子程序调用" (Subroutine Call)。
    *   **Context Injection**: 确保 `{project-root}/.maglev/temp/interview_context.md` 被作为 `input_facts` 的一部分读取 (如果存在)。
    *   请完整执行 `identify-source` 和 `extract-facts`。

2.  **验证产物**:
    检查以下文件是否生成：
    *   `{project-root}/.maglev/temp/ingest_context.json`
    *   `{project-root}/.maglev/temp/input_facts.md`

3.  **前进**:
    一旦确认产物存在，加载 `{nextStepFile}` 进入 Phase 2。
