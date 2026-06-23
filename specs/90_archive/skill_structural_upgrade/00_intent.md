# skill结构性升级 Intent

> 状态：进行中
> 作用：作为当前需求在 `requirements`、`spec`、`validate` 与 `crystallize` 之间的稳定约束面。

## Change Target

将 Maglev 当前分散、边界模糊的 skill 体系，收敛为一套与主流程一致的能力结构；优先解决 `issue`、`intent`、`evolution`、`reality` 之间的流程错位，以及由此带来的 skill 膨胀问题。

本轮的核心目标不是修复现有 skill 的局部病灶，而是根据 Maglev 真正要解决的问题，反推出最合适的 skill 体系。

当前这个“问题定义”的中心已收敛为：

Maglev 要解决的，是 AI Coding 时代项目现状难以被稳定表达、需求生命周期难以被稳定推进、以及会话产出难以沉淀成团队能力的问题。

## Why Now

当前 skill 数量已经增长到需要结构治理的阶段；如果继续在未对齐主流程的前提下增量修 skill，只会放大后续维护复杂度，并继续制造补丁式能力。

## In Scope

- 重新识别 Maglev 当前主流程
- 对齐 `issue`、`intent`、`evolution`、`reality` 的关系
- 定义 `intent` 是否需要独立产物层
- 反推 skill 体系应该如何围绕主流程重组
- 用现有 skill 的问题作为反证材料，而不是把“逐个治病”当作目标本身

## Out of Scope

- 立即重写全部 skill
- 逐个 skill 的内容优化
- 直接启动公开分发链路重构
- 在未完成流程对齐前先做全面 skill 裁撤

## Success Signal

- 能清楚说明进行中需求应承载在 `issues/` 还是 `specs/20_evolution/active/`
- 能清楚说明 `intent` 在主流程里的职责和后续作用
- 能基于对齐后的流程重新判断 skill 分层，而不是继续按现有目录并列理解

## Reality Tension

- 当前 `specs/20_evolution/active/` 为空，说明进行中需求没有稳定进入 Evolution 层
- 当前 issue 与 active spec 的实际分工不清
- 当前部分 skill 很可能是在流程接口缺失的情况下被迫长出的补丁

## Asset Position

本轮分析结果不是一次性讨论记录，而是 Maglev 后续自省、重构与能力进化的判据资产。

因此本轮产出需要满足：

- 能被后续 skill 升级反复引用
- 能作为 `skill-scout` / `skill-squadron` 的稳定分析依据
- 能在未来对当前判断进行复核、推翻或升级
- 能沉淀为 Maglev 反省与进化的长期上下文，而不是会话性结论
