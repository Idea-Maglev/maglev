# `maglev-create-prd` Scout 私域化改造规格 v1

> 状态：已确认
> 作用：在 `skill-scout` 的 `adapt` 步骤中，为 `maglev-create-prd` 后续并入 `requirement-convergence` 生成第一版私域化改造规格。

## 1. 当前前提

本轮输入来自：

- [03ax_maglev_create_prd_scout_evaluation_v1.md](03ax_maglev_create_prd_scout_evaluation_v1.md)
- [03au_maglev_create_prd_transition_plan_v1.md](../../03au_maglev_create_prd_transition_plan_v1.md)

当前默认前提是：

- `GitHub Spec Kit` 作为 requirements / specification 分段关系的主参考
- `OpenSpec` 作为 proposal / spec / tasks 分层与 lifecycle 切分的主边界参考
- `cc-sdd` 作为 requirements 显性步骤提升后续消费能力的辅助参照

## 2. 基线确认

```yaml
adaptation_baseline:
  skill_name: GitHub Spec Kit + OpenSpec + cc-sdd
  source_url: https://github.com/github/spec-kit
  source_type: github
  evaluation_summary: 作为 `maglev-create-prd` 并入 `requirement-convergence` 的联合改造基线，主要吸收其“前段 requirements/proposal 显性化 + 分层流转 + 可消费性约束”结构，而不复制任一项目的完整工作流。
  confirmed: true
```

## 3. AdaptationSpec v1

```yaml
adaptation_spec:
  baseline_skill: GitHub Spec Kit + OpenSpec + cc-sdd
  baseline_source: https://github.com/github/spec-kit
  object_kind: workflow
  customizations:
    feature_trim:
      - 不保留 `maglev-create-prd` 作为并列前段一级入口
      - 不把 PRD 生成解释为“为了兼容传统流程”
      - 不并入 `maglev-create-spec`
      - 不要求所有前段任务默认都生成完整 PRD
    feature_extend:
      - 把 PRD 生成重定义为 `requirement-convergence` 的稳定需求产物输出模式
      - 显式增加“最小 handoff 是否足够”的判断
      - 显式增加“是否存在产物漂移风险”的判断
      - 显式增加“下游是否需要更强消费基线”的判断
      - 为 `maglev-create-prd` 定义更清楚的交接输入契约
    naming_convention:
      formal_action_name: PRD 生成
      canonical_skill_name: pending_demote
      current_runtime_name: maglev-create-prd
      future_shape: requirement-convergence output mode
    interaction_style: 结构化、问题导向、强调稳定需求产物、避免把文档流程当成目的本身
    integrations:
      - skill_name: requirement-convergence
        relation: 被吸收 / 下游模式
      - skill_name: maglev-create-spec
        relation: 间接支撑
      - skill_name: entry-router
        relation: 上游路由
  created_at: 2026-03-30
```

## 4. 结构化解释

### 4.1 功能裁剪

本轮明确不保留的部分：

1. 不再让 `maglev-create-prd` 继续作为并列前段 skill 被独立推荐
2. 不把“团队里有产品经理”当成它的核心存在理由
3. 不把 PRD 生成动作并入 `maglev-create-spec`
4. 不要求所有前段请求默认进入完整 PRD 流程

### 4.2 功能扩展

本轮明确要补齐的部分：

1. `requirement-convergence` 需要显式判断“最小 handoff 是否足够”
2. 需要显式判断“当前是否存在前段产物漂移风险”
3. 需要显式判断“下游是否需要更强的稳定消费基线”
4. 当以上条件成立时，允许将 `maglev-create-prd` 作为唯一主去向

### 4.3 命名判断

当前判断是：

- `maglev-create-prd` 暂不立即删除
- 当前运行名继续保留
- 但未来不再把它视为长期稳定 skill 名
- 更合理的最终形态是：
  - `requirement-convergence` 内部输出模式
  - 或兼容 workflow 入口

### 4.4 交互风格

当前明确要求：

- 结构化
- 问题导向
- 强调稳定需求产物
- 以“让下游充分消费”为判断标准
- 不把文档写作本身误当成目标完成

### 4.5 集成关系

当前最关键的集成关系是：

1. 与 `requirement-convergence`
   - 后续由其判断是否触发 PRD 模式

2. 与 `entry-router`
   - 不直接承担入口分流，而由上游先做路由

3. 与 `maglev-create-spec`
   - 不直接合并，但作为后续设计阶段的稳定需求基线输入

## 5. 当前私域化判断

基于本轮 AdaptationSpec，当前对 `maglev-create-prd` 的私域化判断是：

1. 它仍有保留价值
2. 这个价值已经被重定义为“稳定需求产物输出”
3. 它更适合降级并被 `requirement-convergence` 吸收
4. 当前不应继续以并列独立 skill 的结构目标推进

## 6. 当前不直接删除独立 skill 的原因

虽然本轮已经形成了降级方向，但当前仍不建议立刻删除 `maglev-create-prd`。

原因是：

1. `requirement-convergence` 虽已接入 PRD 模式判断，但还没有完全吸收其完整输出契约
2. 现有团队仍可能需要一个明确的过渡入口
3. 在未完成过渡前直接删除，会让“稳定需求产物输出”再次退回口头补充和松散交接

所以当前更合理的结论是：

- `AdaptationSpec` 已形成
- 降级方向已明确
- 立即删除暂缓
- 后续优先把 `requirement-convergence` 的 PRD 模式补到足够稳定，再进入真正移除回合

## 7. 当前结论

本轮 `skill-scout adapt` 已经形成了可复用的私域化改造规格：

- 主参考：`GitHub Spec Kit`
- 主边界参考：`OpenSpec`
- 辅助参照：`cc-sdd`
- 当前运行对象：`maglev-create-prd`
- 未来形态：`requirement-convergence` 的稳定需求产物输出模式

因此后续如果继续推进，不应再围绕“留不留 create-prd”空转，而应优先做两件事之一：

1. 继续把 `requirement-convergence` 的 PRD 模式补足输出契约
2. 或在条件满足后，再进入真正的降级 / register 收口回合
