# `review-validation-surface` Scout 资源搜索 v1

> 状态：已确认
> 作用：记录 `Review / Validation Surface` 在 `skill-scout` 中的搜索结果。

## 来源池

- 私有来源池：
  - [skill-sources.yaml](../../../skill-sources.yaml)
- 当前主参考：
  - `OpenSpec`
  - `GitHub Spec Kit`
  - `Awesome AI Agents`
- 内部现状参照：
  - `.agents/skills/maglev-code-review-backend/`
  - `.agents/skills/maglev-code-review-frontend/`
  - `.agents/skills/maglev-cross-validate/`

## 候选结果

### #1 OpenSpec

- 来源：<https://github.com/Fission-AI/OpenSpec>
- 匹配点：
  - 强结果与变更一致性意识
  - 可吸收为结果层 review / validation 的流程纪律
- 适配难度：`medium`

### #2 GitHub Spec Kit

- 来源：<https://github.com/github/spec-kit>
- 匹配点：
  - 对变更验证与规范化交付有较强约束
- 适配难度：`medium`

### #3 Awesome AI Agents

- 来源：<https://github.com/e2b-dev/awesome-ai-agents>
- 匹配点：
  - 提供结果评审、验证与 evaluator 相关的资源入口
- 适配难度：`medium`

## 联网校验记录

本轮已补充实际联网检索并核对以下主来源：

- OpenSpec
  - <https://github.com/Fission-AI/OpenSpec>
- GitHub Spec Kit
  - <https://github.com/github/spec-kit>
  - <https://github.github.com/spec-kit/index.html>
- OpenAI Agents Guardrails
  - <https://openai.github.io/openai-agents-js/guides/guardrails/>

当前使用这些来源的方式是：

- `OpenSpec` 作为主改造基线
- `GitHub Spec Kit` 作为流程纪律补充
- `OpenAI Guardrails` 作为质量层边界与 guardrail 结构辅证

## 当前结论

- `OpenSpec` 作为主改造基线更合适。
- `GitHub Spec Kit` 作为流程纪律补充。
- 泛化资源只作为低优先级辅证。
