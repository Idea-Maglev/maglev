# Reverse Spec Upgrade: Intent Enrichment (意图补全)

## 1. 核心问题 (Problem)
*   **Gap**: 逆向工程产出的 Spec 过于单薄，缺乏 "Why" (设计意图、业务背景、成功标准)。
*   **Cause**: 代码只能告诉你 "It prints Hello"，告诉不了你 "Why we need to greet users".
*   **Solution**: 在生成 Spec 前，强制插入一个 "意图补全" 环节，利用用户的知识为冷冰冰的代码注入灵魂。

## 2. 实施方案 (Implementation)

### A. New Step: Intent Speculation & Quests (意图推测与任务生成)
*   **File**: `step-03b-intent-enrichment.md`
*   **Logic**:
    *   **Inference (推理)**: Agent 分析代码（变量名、注释、复杂度），尝试反推业务意图。
    *   **Quest Generation (生成探索任务)**: 针对无法确定的逻辑，生成 "Investigation Questions"。
        > "Quest 1: `calculateTax` 函数中硬编码了 `0.15`，请确认这是什么税率？"
        > "Quest 2: 只有 `Status=9` 才能退款，数字 9 代表什么状态？"
    *   **Hypothesis (提问)**: 
        > "我发现了一些疑点，已生成 **[遗留问题清单]**。
        > 你可以现在回答，或者我将其写入 Spec 的 `Unresolved Questions` 章节，供你后续通过 AI 助手慢慢排查。"
    *   **Output**: `intent_context.md` (包含 Hypotheses 和 Quest List).

### B. Update Handoff (交接升级)
*   **File**: `wrapper-04-spec-handoff.md`
*   **Logic**:
    *   **Merge**: 将 `intent_context.md` (Why) 与 `stack_trace.md` (What) 合并。
    *   **Inject**:生成更完整的 `input_facts.md`。

### C. Workflow Wiring (流程接线)
*   **File**: `reverse-spec.workflow.md`
*   **Change**: `Step 3` (Stack Trace) -> `Step 3b` (Enrichment) -> `Step 4` (Handoff).

## 3. 预期效果
通过这一步，逆向生成的 Spec 将不再是代码的简单翻译，而是具备 "业务深度" 的文档，达到与 `create-spec` 同等的质量标准。
