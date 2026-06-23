# `spec-audit-surface` Scout 资源搜索 v1

> 状态：已确认
> 作用：记录 `Spec Audit Surface` 在 `skill-scout` 中的搜索结果。

## 来源池

- 私有来源池：
  - [skill-sources.yaml](../../../skill-sources.yaml)
- 当前主参考：
  - `OpenSpec`
  - `GitHub Spec Kit`
  - `cc-sdd`
- 内部现状参照：
  - `.agents/skills/maglev-audit-prd/`
  - `.agents/skills/maglev-audit-spec/`

## 候选结果

### #1 OpenSpec

- 来源：<https://github.com/Fission-AI/OpenSpec>
- 匹配点：
  - 强 spec/change 输入纪律
  - 明确 proposal/alignment before implementation
  - 适合吸收为输入质量面
- 适配难度：`medium`

### #2 GitHub Spec Kit

- 来源：<https://github.com/github/spec-kit>
- 匹配点：
  - 强模板纪律
  - 对 requirements / design / tasks 的结构约束更清晰
- 适配难度：`medium`

### #3 cc-sdd

- 来源：<https://github.com/gotalab/cc-sdd>
- 匹配点：
  - requirements-first
  - 对 spec 输入质量有流程约束
- 适配难度：`medium`

## 联网校验记录

本轮已补充实际联网检索并核对以下主来源：

- OpenSpec
  - <https://github.com/Fission-AI/OpenSpec>
- GitHub Spec Kit
  - <https://github.com/github/spec-kit>
  - <https://github.github.com/spec-kit/index.html>

当前使用这些来源的方式是：

- `OpenSpec` 作为主改造基线
- `GitHub Spec Kit` 作为模板纪律与 guardrail 补充
- `cc-sdd` 继续保留为来源池中的辅证来源，但本轮主判断不依赖它

## 当前结论

- `OpenSpec` 作为主改造基线更合适。
- `GitHub Spec Kit` 作为模板与 guardrail 补充。
- `cc-sdd` 作为低优先级流程辅证。
