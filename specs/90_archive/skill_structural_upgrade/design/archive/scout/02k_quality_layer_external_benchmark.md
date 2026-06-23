# skill结构性升级 `质量层收口` 外部对标与 Batch 4 初步结果

> 状态：进行中
> 作用：记录围绕 audit、review、test design、guardrail 的第一轮外部对标，并形成 `skill-squadron` Batch 4 的初步巡逻结论。

## 1. 本轮对标目标

本轮只回答三个问题：

1. 行业里更成熟的质量层，通常如何组织检查、验证与测试设计
2. 这些能力更像一串并列 skill，还是更像少数能力面 + guardrail / eval 机制
3. 这些做法是否支持我们当前对 `Merge` 的判断

## 2. 参考来源

### A. OpenAI Agents SDK: Guardrails

来源：

- [Guardrails | OpenAI Agents SDK](https://openai.github.io/openai-agents-js/guides/guardrails/)

关键信号：

- guardrail 是正式结构对象，不是附属补丁
- 存在明确边界：
  - input guardrails
  - output guardrails
  - tool guardrails
- tool guardrails 用于“每次工具调用前后”的检查
- workflow 中不同位置的检查，应使用不同粒度的 guardrail

当前启发：

- 质量能力不应只表现为“最后审一下”
- 更成熟的结构是：
  - 入口检查
  - 过程检查
  - 输出检查

### B. Anthropic: Evaluator-optimizer

来源：

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

关键信号：

- evaluator-optimizer 适合：
  - 有清晰评价标准
  - 迭代 refinement 确实有价值
- 生成和评价应被明确拆开，而不是混成一个动作

当前启发：

- `review` / `audit` / `validation` 不应都压成一个 skill
- 更合理的是：
  - 生成或实施一层
  - 评价或反馈一层
  - 必要时形成循环

### C. Anthropic: Demystifying evals for AI agents

来源：

- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

关键信号：

- evals 能让问题和行为变化在影响用户前就可见
- eval 的价值会沿 agent 生命周期累积

当前启发：

- 质量层不只是“发现错误”
- 更是让行为变化可见、可追踪、可比较

### D. Anthropic: Writing effective tools for agents

来源：

- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

关键信号：

- 高质量 tools 和 evaluations 需要一起设计
- 应持续原型化、评估、再改进
- 应避免对策略路径过度过拟合

当前启发：

- 测试设计与 review 不该完全分裂成孤立 skill
- 更像同一质量层下的不同能力面

## 3. 外部模式的共同结论

把这些外部模式放在一起看，当前有四个稳定结论：

1. 质量层是正式结构，不是主流程外的附属补丁
2. 质量层通常按“检查位置和检查对象”分面，而不是按一长串具体动作平铺
3. `guardrail`、`review`、`eval`、`test design` 虽然相关，但不应混成一个黑箱动作
4. 更成熟的做法，是少数稳定能力面之下再保留必要专项差异

## 4. 对 Maglev 当前判断的支持

本轮对标整体支持我们之前对 `质量层收口` 的方向判断：

### A. `Merge` 方向是对的

当前这组对象：

- `maglev-audit-prd`
- `maglev-audit-spec`
- `maglev-code-review-backend`
- `maglev-code-review-frontend`
- `maglev-plan-unit-tests-backend`
- `maglev-plan-unit-tests-frontend`
- `maglev-create-test-cases`

如果继续并列平铺，会持续制造：

- 对象碎片化
- 入口过多
- 边界解释成本过高

### B. 质量层更适合“能力面”表达

当前更稳的质量层结构，仍然是这三面：

1. `Spec Audit Surface`
2. `Review / Validation Surface`
3. `Test Design Surface`

这三面已经能够覆盖当前对象簇的主要职责。

### C. `maglev-cross-validate` 不应吞掉整个质量层

外部做法更像：

- 局部检查在各自边界运行
- 汇聚层负责整合与最终判断

所以在 Maglev 里：

- `maglev-cross-validate`
  - 更适合作为 `综合验证` 的主流程汇聚点
- 质量层对象
  - 继续作为各自能力面的专项承载

## 5. 对当前对象簇的进一步修正

这轮对标后，当前更推荐的结构不是“把所有质量对象合成一个总 skill”，而是：

### A. `Spec Audit Surface`

承接：

- `maglev-audit-prd`
- `maglev-audit-spec`

作用：

- 评估输入文档或方案依据是否具备一致性与可执行性

### B. `Review / Validation Surface`

承接：

- `maglev-code-review-backend`
- `maglev-code-review-frontend`

作用：

- 评估实现结果与预期约束是否一致
- 在结果层发现问题、偏差与风险

### C. `Test Design Surface`

承接：

- `maglev-plan-unit-tests-backend`
- `maglev-plan-unit-tests-frontend`
- `maglev-create-test-cases`

作用：

- 设计覆盖策略
- 识别测试对象与测试方式
- 形成验证所需的测试支撑面

## 6. Batch 4 初步巡逻结果

基于当前内外部材料，`skill-squadron` 的 `Batch 4: 质量层收口批次` 可以先给出这版结果：

### 结论 1

质量层应继续保持 `Merge` 路径，不建议回退为并列 skill 平铺。

### 结论 2

当前质量层最稳的收口方式，仍是三面结构：

1. `Spec Audit Surface`
2. `Review / Validation Surface`
3. `Test Design Surface`

### 结论 3

`maglev-cross-validate` 应继续保留为主流程汇聚点，而不是改造成质量层总 skill。

### 结论 4

后续若进入实际重构，优先顺序应是：

1. 先统一质量层说明口径
2. 再收口对象分组
3. 最后才决定是否改入口名或目录形态

## 7. 当前结论

这轮对标进一步确认了：

- 质量层是正式结构层
- 但它不应以碎片化 skill 列表形式暴露
- 更合理的表达是少数质量能力面 + 专项对象
- 当前 `Merge` 判断成立，而且方向已足够稳定
