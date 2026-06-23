# Reflection: Atomic Spec System (Phase 1)

> **Trigger**: Post-implementation Review (User Request)
> **Context**: Completed Ingest (Zoom-in), Draft, Crystallize, Coordinator.

## 1. 复杂度爆炸 (Complexity Explosion)
*   **Blind Spot**: 我们从简单的单文件脚本变成了 "1 Coordinator + 3 Skills + 4 Workflow Files"。
*   **Risk**: 对于简单任务（比如“改个错别字”），这套流程过于沉重 (Overkill)。用户可能会因为觉得繁琐而绕过它，直接写代码，导致 Spec 与 Code 分离。
*   **Mitigation Idea**: 在 Coordinator 中增加 **"Fast Track" (快速通道)**。如果 Intent 很简单，跳过 Deep Dive，跳过繁琐的 Draft 确认，直接生成 Spec。

## 2. 上下文传递的脆弱性 (Context Fragility)
*   **Blind Spot**: 技能间通过 `.maglev/temp/*.json` 传递数据。Markdown 也不是强类型语言。
*   **Risk**: 如果 `spec-ingest` 输出的 JSON 结构变了（比如 `deep_dive_targets` 字段名改了），下游的 `spec-draft` 会直接报错或产生幻觉，而且很难 Debug。
*   **Mitigation Idea**: 定义 **"Context Schema" (契约)**。虽然我们不能在 Markdown 里做 Type Check，但可以在 `SKILL.md` 里明确输入输出的 JSON 样例，作为“协议标准”。

## 3. 基准腐烂 (Baseline Rot)
*   **Blind Spot**: 我们存档了 `input_facts.md` 作为 "Premise"。
*   **Risk**: 代码库是活的。如果其他人（或不通过 Maglev）修改了代码，`input_facts.md` 并不会自动更新。Spec 里的 "Pre-condition" 就会变成谎言。
*   **Mitigation Idea**: 需要引入 **"Maglev Audit"** 机制。每次启动 Maglev 时，或者在 CI 环节，检查 `input_facts.md` 里的签名是否还能在代码里找到。

## 4. Token 爆炸 (Token Explosion)
*   **Blind Spot**: Zoom-in 策略允许用户选择 Deep Dive 模块。
*   **Risk**: 如果用户选择了 `src/` (全选)，或者选了一个巨型模块，`read_file` 会把几万行代码塞进 `input_facts.md`。这会撑爆 Draft 阶段 Context Window，或者导致 AI 遗忘。
*   **Mitigation Idea**: 在 `step-03-zoom-extract.md` 中增加 **"Safety Check" (安全阀)**。如果文件超过一定行数，强制降级为 Skeleton 或只读 Head/Tail。

## 5. 开发者体验 (DX)
*   **Blind Spot**: 现在的交互充满了 "File Select" 和 "JSON confirm"。
*   **Risk**: 这种体验非常 "Bot-like"，不够自然。
*   **Mitigation Idea**: 优化 Prompt，让 Bot 的语气更像是同事而非机器。减少不必要的 JSON 展示，只展示人类可读的 Summary。
