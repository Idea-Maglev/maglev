# Maglev Commit Protocol (提交协议)

> **Goal**: 确保每一次代码提交都是 "Methodology Compliant" 的。
> **Enforcement**: 🤖 Executed by `/.agents/workflows/generate-commit-message` automatically.

## 1. 核心校验逻辑 (The 3 Checks)

在生成 Commit Message 之前，必须通过以下三次握手：

### Check 1: 同步完整性 (Sync Integrity)
*   **规则**: 如果 `src/` (Code) 变更了，检查 `specs/` (Truth) 是否有对应变更。
*   **状态**:
    *   ✅ **Synced**: `src/` 和 `specs/` 同时修改。
    *   ⚠️ **Debt (Risk)**: 只有 `src/` 修改。需在 Commit Message 中显式声明 "Pending Reverse Sync" 或 "Trivial Fix"。

### Check 2: 验证多维性 (Validation Dimensions)
根据变更类型，强制填写通过的验证手段：
*   **Spec -> Code**: 重点验证 **完整性 (Completeness)** (e.g., "所有字段都入库了吗？")。
*   **Code -> Spec**: 重点验证 **准确性 (Accuracy)** (e.g., "文档里的流程图和代码逻辑一致吗？")。
*   **Visual/UI**: 重点验证 **体验 (UX)** (e.g., 截图/录屏)。
*   **Test Case**: 重点验证 **鲁棒性 (Robustness)** (e.g., 单元测试/集成测试)。

### Check 3: 历史可追溯性 (Traceability)
Commit Message 必须包含标准化的 Trailer 信息。

## 2. Commit Message 模板

```text
{type}({scope}): {subject}

{body} (Why & What)

## 🔍 Verification (Maglev Check)
- [x] **Sync Status**: {Synced / Debt / Pure Doc}
- [ ] **Validation**:
    - 🧪 Unit Test: `{test_case_name}` ({Passed/Skipped})
    - 👁️ Visual: `{screenshot_url_or_description}`
    - 📄 Spec Diff: `{spec_filename}`

## 🔗 Context
- Task: #{issue_id}
- Doc: {relevant_doc_link}
```

## 4. 降级模式 (Fallback Mode)

当自动化条件不满足或遇紧急情况时，允许进入"非严格模式"。

**前提**:
*   AI 服务不可用或 IDE 插件失效。
*   生产环境紧急修复 (Hotfix)。
*   探索性实验 (Spike)。

**操作**:
在 Commit Message 中必须包含 `[Debt]` 标记，并说明原因。

*(Note: 现代 AI 助手通常能自动处理 Scan，Fallback 仅用于极端断网情况)*

```text
...
## ⚠️ Fallback
- [Debt]: AI Plugin timeout. Pending reverse sync.
```

**治愈 (Healing)**:
后续通过 `/maglev_audit` 发现此 Debt，并通过 "Reverse Sync" 补全 Spec 后，新的提交应引用原 Commit ID 标记 `[Healed]`.
