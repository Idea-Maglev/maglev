# `test-design-surface` Scout 资源搜索 v1

> 状态：已确认
> 作用：记录 `Test Design Surface` 在 `skill-scout` 中的搜索结果，并显式保留实际联网检索证据。

## 来源池

- 私有来源池：
  - [skill-sources.yaml](../../../skill-sources.yaml)
- 当前主参考：
  - `OpenSpec`
  - `GitHub Spec Kit`
- 官方质量辅证：
  - `Anthropic Demystifying evals for AI agents`
  - `OpenAI Agents Guardrails`
- 内部现状参照：
  - `.agents/skills/maglev-plan-unit-tests-backend/`
  - `.agents/skills/maglev-plan-unit-tests-frontend/`
  - `.agents/skills/maglev-create-test-cases/`

## 候选结果

### #1 OpenSpec

- 来源：<https://github.com/Fission-AI/OpenSpec>
- 匹配点：
  - 强 spec/change 输入纪律
  - 适合吸收为测试设计的前置约束来源
- 适配难度：`medium`

### #2 GitHub Spec Kit

- 来源：<https://github.com/github/spec-kit>
- 来源文档：<https://github.github.com/spec-kit/index.html>
- 匹配点：
  - requirements / design / tasks 结构清晰
  - 适合作为测试设计的模板纪律补充
- 适配难度：`medium`

### #3 Anthropic Demystifying evals

- 来源：<https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- 匹配点：
  - 明确 eval / grader / suite 的结构
  - 适合吸收为测试设计与验证支撑的质量辅证
- 适配难度：`low`

### #4 OpenAI Agents Guardrails

- 来源：<https://openai.github.io/openai-agents-js/guides/guardrails/>
- 匹配点：
  - 明确 input / output / tool guardrails 的边界
  - 适合作为测试设计中“检查位置”的结构辅证
- 适配难度：`low`

## 联网校验记录

本轮已实际联网检索并核对以下来源：

- OpenSpec
  - <https://github.com/Fission-AI/OpenSpec>
- GitHub Spec Kit
  - <https://github.com/github/spec-kit>
  - <https://github.github.com/spec-kit/index.html>
- Anthropic Demystifying evals
  - <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- OpenAI Agents Guardrails
  - <https://openai.github.io/openai-agents-js/guides/guardrails/>

当前使用方式：

- `OpenSpec`：主改造基线
- `GitHub Spec Kit`：模板纪律与结构补充
- `Anthropic Demystifying evals`：测试设计 / grader / suite 结构辅证
- `OpenAI Guardrails`：检查位置与 guardrail 边界辅证

## 当前结论

- `OpenSpec` 作为主改造基线更合适。
- `GitHub Spec Kit` 作为模板纪律补充。
- `Anthropic Demystifying evals` 与 `OpenAI Guardrails` 共同提供测试设计面的质量结构辅证。
