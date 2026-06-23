# `maglev-quick-dev` Scout 资源搜索 v1

> 状态：已确认
> 作用：记录 `maglev-quick-dev` 在 `skill-scout` 中的搜索结果，并显式保留实际联网检索证据。

## 来源池

- 私有来源池：
  - [skill-sources.yaml](../../../skill-sources.yaml)
- 当前主参考：
  - `OpenSpec`
  - `GitHub Spec Kit`
  - `cc-sdd`
- 内部现状参照：
  - `.agents/skills/maglev-quick-dev/`
  - `.agents/skills/maglev-create-spec/`
  - `.agents/skills/maglev-cross-validate/`

## 候选结果

### #1 GitHub Spec Kit

- 来源：<https://github.com/github/spec-kit>
- 来源文档：<https://github.github.com/spec-kit/index.html>
- 匹配点：
  - 明确把 `plan -> tasks -> implement` 切成连续阶段
  - `/speckit.implement` 更接近“基于既定依据进入实施”的能力
  - 有助于校正“实施对象不该吞并前段需求与方案阶段”
- 适配难度：`medium`

### #2 OpenSpec

- 来源：<https://github.com/Fission-AI/OpenSpec>
- 匹配点：
  - 强调先对齐 change / spec，再进入代码变更
  - 明确 `archive`、`validate` 等后段动作，不把实施对象做成全能入口
  - 适合作为“实施前提必须稳定”的主参考
- 适配难度：`medium`

### #3 cc-sdd

- 来源：<https://github.com/gotalab/cc-sdd>
- 匹配点：
  - 明确 `requirements -> design -> tasks -> implementation`
  - 适合作为“implementation 不应吞并前段阶段”的补充参考
  - 对多 agent / 多阶段执行边界有现实参考价值
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

- `GitHub Spec Kit`：主命名与阶段切分参考
- `OpenSpec`：实施前提与生命周期边界参考
- `cc-sdd`：implementation 阶段不吞并前段阶段的辅助参照

## 当前结论

- 本轮不存在一个与 `maglev-quick-dev` 完全同名的成熟对象。
- 但在“实施阶段应如何从 spec 链路中切出”这个问题上，`GitHub Spec Kit` 最接近主改造基线。
- 当前搜索足以进入 `evaluate`，重点不再是“是否存在同名对象”，而是“实施能力该如何命名和定边界”。
