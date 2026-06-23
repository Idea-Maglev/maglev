# `maglev-create-prd` Scout 资源搜索 v1

> 状态：已确认
> 作用：记录 `maglev-create-prd` 在 `skill-scout` 中的搜索结果，并显式保留实际联网检索证据。

## 来源池

- 私有来源池：
  - [skill-sources.yaml](../../../skill-sources.yaml)
- 当前主参考：
  - `GitHub Spec Kit`
  - `OpenSpec`
  - `cc-sdd`
- 内部现状参照：
  - `.agents/skills/maglev-create-prd/`
  - `.agents/skills/requirement-convergence/`
  - `.agents/skills/maglev-create-spec/`

## 候选结果

### #1 GitHub Spec Kit

- 来源：<https://github.com/github/spec-kit>
- 来源文档：<https://github.github.com/spec-kit/index.html>
- 匹配点：
  - 明确从 high-level requirements 进入 specification creation，再进入实现
  - 强调 intent-driven development 与多阶段 refinement
  - 支持“需求文档 / requirements”应作为前段显性产物存在，但不应与方案设计和实现混写
  - 更支持“前段产物必须可被后续充分消费”，而不是停留在口头共识
- 适配难度：`medium`

### #2 OpenSpec

- 来源：<https://github.com/Fission-AI/OpenSpec>
- 匹配点：
  - 强调在代码前先达成一致理解，并把 proposal、tasks、spec updates 分开维护
  - 更支持“需求 / proposal 属于前段治理与对齐对象”，而不是直接滑入设计或编码
  - 适合作为 `maglev-create-prd` 不应并入 `maglev-create-spec` 的主边界参考
  - 支持“proposal / spec”分层可以减少前段信息在流转中的漂移
- 适配难度：`medium`

### #3 cc-sdd

- 来源：<https://github.com/gotalab/cc-sdd>
- 匹配点：
  - 明确 `Requirements -> Design -> Tasks -> Implementation`
  - 支持团队审批、模板化和项目记忆，更贴近现实团队协作
  - 说明“显性 requirements 文档步骤”在团队工作流中仍有独立价值，但更应作为前段的一部分，而不是与方案设计并列漂移
  - 强调 requirements 的显性化是为了让后续设计和执行可消费，而不是为了形式上的文档存在
- 适配难度：`medium`

## 联网校验记录

本轮已实际联网检索并核对以下来源：

- GitHub Spec Kit
  - <https://github.com/github/spec-kit>
  - <https://github.github.com/spec-kit/index.html>
- OpenSpec
  - <https://github.com/Fission-AI/OpenSpec>
- cc-sdd
  - <https://github.com/gotalab/cc-sdd>

当前使用方式：

- `GitHub Spec Kit`：作为 requirements / specification 分段关系的主参考
- `OpenSpec`：作为 proposal / spec / tasks 分层与 lifecycle 切分的主边界参考
- `cc-sdd`：作为 requirements 显性步骤提升后续消费能力的辅助参照

## 当前结论

- 本轮不存在一个与 `maglev-create-prd` 完全同名、且能直接一比一迁移的成熟对象。
- 但三个主参考都支持一个稳定结论：
  - 前段显性的需求 / requirements / proposal 产物仍有价值
  - 它们的价值首先在于减少漂移、提升可消费性，而不只是“兼容文档流”
  - 它不应与方案设计和实现混成同一对象
  - 它更适合作为前段能力簇中的一种模式，而不是并列一级对象
- 当前搜索足以进入 `evaluate`。
- 后续 `evaluate` 的重点应从“是否保留”转向：
  - “作为稳定需求产物输出模式保留是否合理”
  - “并入 requirement-convergence 而不是并入 maglev-create-spec 是否成立”
