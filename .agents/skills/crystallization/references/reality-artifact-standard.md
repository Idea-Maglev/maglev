---
name: reality-artifact-standard
description: Reality Artifact Contract 的兼容入口
---

# Reality Artifact Contract（兼容入口）

Reality 的页面结构与写法由本轮选定的 **Reality 模板包**（`templates/reality-packs/registry.yaml`
登记）唯一决定；共享 `.agents/skills/_internal/reality-admission/` 持有的是**机器可追溯
协议**（frontmatter 身份、证据绑定、投影摘要与准入确认），不规定页面章节、标题或措辞。
本文件保留旧引用路径，避免历史流程链接断裂；它不再定义第二套目录、页面或质量规则。

权威资产：

- [Reality Contract](../../_internal/reality-admission/protocol/reality_contract.yaml)
- [Reality Projection schema](../../_internal/reality-admission/protocol/reality_projection.schema.json)
- [Validation Result schema](../../_internal/reality-admission/protocol/validation_result.schema.json)
- [Admission CLI](../../_internal/reality-admission/scripts/reality_admission.py)

自检兼容入口仍可运行：

```bash
maglev-python .agents/skills/crystallization/references/scripts/crystallization_check.py \
  specs/10_reality
```

脚本验证的角色边界：Admission 只做客观可追溯性校验（证据存在、摘要一致、身份唯一），
并对占位符残留输出非阻断提示。页面结构或内容质量问题一律回到模板包对照反思修复，
不得通过改写内容去拟合脚本检查项。

Reality 修改必须先与既有事实合并并提交为 candidate commit，再由独立 worktree
验证完整 Projection。只有 `accepted` 或 `no_change` Receipt 才能驱动
Crystallization 的 active close。
