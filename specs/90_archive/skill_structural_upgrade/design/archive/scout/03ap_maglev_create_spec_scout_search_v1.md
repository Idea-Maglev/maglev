# `maglev-create-spec` Scout 资源搜索 v1

> 状态：已确认
> 作用：记录 `maglev-create-spec` 在 `skill-scout` 中的搜索结果，并显式保留实际联网检索证据。

## 来源池

- 私有来源池：
  - [skill-sources.yaml](../../../skill-sources.yaml)
- 当前主参考：
  - `OpenSpec`
  - `GitHub Spec Kit`
  - `cc-sdd`
- 内部现状参照：
  - `.agents/skills/maglev-create-spec/`
  - `.agents/skills/requirement-convergence/`
  - `.agents/skills/maglev-quick-dev/`

## 候选结果

### #1 OpenSpec

- 来源：<https://github.com/Fission-AI/OpenSpec>
- 匹配点：
  - 明确在实现前先锁定 proposal / design / tasks
  - 强调变更边界、设计依据和归档链路
  - 最接近“方案设计不应吞并前段问题定义”的当前判断
- 适配难度：`medium`

### #2 GitHub Spec Kit

- 来源：<https://github.com/github/spec-kit>
- 来源文档：<https://github.github.com/spec-kit/index.html>
- 匹配点：
  - 明确把 intent/spec/tasks/implementation 切成分阶段过程
  - 有助于校正“spec 不是从模糊想法直接一路吞到实现”的边界
  - 对规范化模板和 guardrail 组织有参考价值
- 适配难度：`medium`

### #3 cc-sdd

- 来源：<https://github.com/gotalab/cc-sdd>
- 匹配点：
  - requirements → design → tasks 结构清楚
  - 更适合作为阶段分离的辅助参考
  - 对 `design` 作为独立阶段的心智支持较强
- 适配难度：`medium`

## 联网校验记录

本轮已实际联网检索并核对以下来源：

- OpenSpec
  - <https://github.com/Fission-AI/OpenSpec>
- GitHub Spec Kit
  - <https://github.com/github/spec-kit>
  - <https://github.github.com/spec-kit/index.html>
- cc-sdd
  - <https://github.com/gotalab/cc-sdd>

当前使用方式：

- `OpenSpec`：主改造基线
- `GitHub Spec Kit`：模板纪律与阶段切分补充
- `cc-sdd`：design 阶段独立性的辅助参照

## 当前结论

- 在“方案设计应如何从前后阶段切开”这个问题上，`OpenSpec` 最接近主改造基线。
- `GitHub Spec Kit` 和 `cc-sdd` 主要提供阶段切分和模板纪律的辅助校正。
- 当前搜索足以进入 `evaluate`，重点不再是“找一个同名对象”，而是“方案设计能力该如何定边界和定名”。
