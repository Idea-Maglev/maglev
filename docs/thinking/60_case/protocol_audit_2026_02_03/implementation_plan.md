# Commit Workflow Refinement Plan (Commit 工作流优化计划)

## 诊断 (Diagnosis)
*   **Workflow**: `generate-commit-message.md`
    *   **发现**: 未使用 Python 脚本，完全依靠 AI 原生能力。
    *   **问题 1**: 引用了非标准的 `README_INDEX.md`，应统一为 `README.md` 或 `INDEX.md`。
    *   **问题 2**: "Drift Detection" 依赖 AI 自主判断，可明确建议其参考 `maglev-audit-spec` 的逻辑。
*   **Protocol**: `commit_standard.md`
    *   **问题**: 与 Workflow 缺乏互链。

## 优化方案 (Refinement Strategy)

### 1. 升级 Workflow
*   **Step 2 (Indexing)**: 将 `README_INDEX.md` 修正为标准 `README.md`。
*   **Step 1 (Calibration)**: 增加提示 "可调用 `maglev-audit-spec` 进行深度检查"。

### 2. 更新 Protocol
*   在 `commit_standard.md` 头部增加 "🤖 Executed by: `/generate-commit-message`"。
*   简化 Fallback 描述。

## 验证
*   检查 Starter Kit 中是否有 `README_INDEX.md` 的残留文件 (如有则删)。
