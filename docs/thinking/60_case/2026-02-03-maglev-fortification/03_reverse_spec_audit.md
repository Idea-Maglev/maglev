# Reverse Spec 修复与加固方案 (Repair & Fortify Strategy)

## 1. 修复 (Repair Phase)

### A. 归档逻辑修复 (Critical)
*   **Target**: `reverse-spec.workflow.md`
*   **Action**: 替换 Step 5 为 `maglev-spec-crystallize`。
*   **Config**: `output_base: specs/10_reality`

### B. 语言与格式统一 (Standardization)
*   **Target**: `step-02-page-analysis.md` & `step-03-stack-trace.md`
*   **Action**:
    1.  将所有 Prompts 和 Examples 翻译为中文。
    2.  增加 `<rule>所有解释性文本必须为中文</rule>`。
    3.  优化输出 YAML 结构，使其更易被 `wrapper-04` 提取。

## 2. 加固 (Fortification Phase)

### A. 启动自检 (Step 00)
创建 `step-00-integrity-check.md`:
1.  **Check**: `.maglev/temp` 是否存在？(不存在则创建)
2.  **Check**: `step-04` 所需的 `maglev-spec-draft` 技能是否就绪？
3.  **Check**: `step-05` 所需的 `maglev-spec-crystallize` 技能是否就绪？

### B. 产出验证 (Step 06)
创建 `step-06-verify-output.md`:
1.  **Assert**: `specs/10_reality/reverse_{slug}/00_index.md` 存在。
2.  **Assert**: `specs/10_reality/reverse_{slug}/context/input_facts.md` 存在 (归档检查)。
3.  **Message**: 如果验证失败，提示用户手动检查；如果成功，打印最终位置。

## 3. 执行顺序
1.  Create Step 00 & 06.
2.  Refactor Step 02 & 03.
3.  Wire everything into `reverse-spec.workflow.md`.
