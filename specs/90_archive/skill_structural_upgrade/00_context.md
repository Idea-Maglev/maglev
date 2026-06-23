# skill结构性升级 Context

> 状态：已封板
> 作用：只保留当前继续推进仍需要反复读取的上下文判断。
> 完整过程归档：
> - `archive/00_context_full.md`

## 1. 当前任务位置

本轮任务已完成封板，正文承载在：

- `specs/20_evolution/active/skill_structural_upgrade/`

而不是继续主要挂在 `issues/` 中。

当前对两者的分工判断为：

- `issue`：触发器、追踪入口、来源记录
- `specs/20_evolution/active/`：进行中的需求正文、结构讨论与演进依据

## 2. 当前主线判断

本轮目标不是修单个 skill 的局部病灶，而是根据 Maglev 真正要解决的问题，反推出更合适的 skill 体系。

当前已经收敛的根判断是：

> Maglev 的核心不是“skill 集合”，而是用一套可持续维护的结构，呈现项目现状，并承载从需求进入、方案形成、实施、验证到事实结晶的生命周期推进。

## 3. 当前主流程理解

当前提炼出的主流程不应继续简化为：

`Issue -> Spec -> Code`

而更接近：

`Reality -> Issue -> Intent -> Spec -> Execute -> Validate -> Crystallize`

对应的关键阶段含义是：

- `Reality`
  - 先理解当前项目真实处于什么状态
- `Issue`
  - 显式化一个需要处理的问题或机会
- `Intent`
  - 把 issue 收敛成清晰改动目标
- `Spec`
  - 把意图转成可执行设计依据
- `Execute`
  - 基于 Spec 落地改动
- `Validate`
  - 确认结果是否真正成立
- `Crystallize`
  - 将已成立的新事实写回体系

## 4. 当前关键边界

### 4.1 `issue` / `intent` / `evolution`

当前边界判断为：

- `issue`
  - 负责启动与追踪
- `intent`
  - 负责收敛“这次到底要改什么”
- `specs/20_evolution/active/`
  - 负责承载进行中的正文与演进过程

当前建议顺序：

`Issue -> Intent Clarification -> Evolution Active Spec -> Execution -> Crystallization`

### 4.2 `thinking archive` / `crystallization`

当前已经明确分开两条链：

- `思考归档触发链`
  - 面向知识沉淀
  - 当前由 `knowledge-check` 承接
- `事实结晶触发链`
  - 面向 Reality 回写、active 收口与可发现性回填
  - 当前由 `crystallization` 承接

这两条链生命周期不同，不能共用同一个入口语义。

## 5. 当前结构结论

### 5.1 顶层能力骨架

当前顶层骨架收敛为 `5+3`：

5 个主流程能力：

1. `现状同步`
2. `需求收敛`
3. `方案设计`
4. `上下文实施`
5. `综合验证`

3 个体系级能力：

1. `能力进化`
2. `现状表达`
3. `整体接入`

### 5.2 当前对象落点

当前已形成的正式对象与 workflow 主要是：

- `entry-router`
- `knowledge-check`
- `requirement-convergence`
- `crystallization`
- `spec-audit-surface`
- `review-validation-surface`
- `test-design-surface`

其中：

- `entry-router`
  - 作为正式入口对象继续推进
- `knowledge-check`
  - 作为正式知识沉淀检查对象继续推进
- `requirement-convergence`
  - 当前已形成正式 skill，对应 workflow 文件仅作为入口包装
- `crystallization`
  - 当前已形成正式 skill，对应 workflow 文件仅作为入口包装

## 6. 当前仍然开放的问题

后续若还需继续推进，当前仍值得复核的问题主要有：

1. 主流程核心对象的历史运行名与结构动作名并存状态是否会持续制造理解成本
2. `skill-squadron` 对治理对象和命名状态的巡逻规则是否已经足够稳定
3. 项目级 catalog 与治理底表是否还存在断层
4. `skill-scout` 吸收生成能力后的运行面与设计资产是否已经完全一致

## 7. 当前使用方式

从现在开始：

- 日常继续推进时，优先阅读本文件
- 若需要判断本轮是否可正式结束，优先阅读：
  - `design/03az_closeout_criteria_and_exit_standard_v1.md`
- 若需要追溯完整讨论过程、被放弃的方案或历史判断形成过程，再进入：
  - `archive/00_context_full.md`
