# `entry-router` Scout 私域化改造规格 v1

> 状态：进行中
> 作用：在 `skill-scout` 的 `adapt` 步骤中，基于已选改造基线，为 `entry-router` 生成第一版私域化改造规格。

## 1. 当前前提

本轮输入来自：

- [02zf_entry_router_scout_evaluation_v1.md](02zf_entry_router_scout_evaluation_v1.md)
- [02w_scout_readiness_packets_v1.md](02w_scout_readiness_packets_v1.md)

当前默认前提是：

- `OpenAI Agents SDK: Handoffs` 作为主改造基线已被接受
- `Anthropic Routing Pattern` 作为结构原则辅证

## 2. 基线确认

```yaml
adaptation_baseline:
  skill_name: OpenAI Agents SDK Handoffs
  source_url: https://openai.github.io/openai-agents-python/handoffs/
  source_type: official_docs
  evaluation_summary: 作为 entry-router 的主改造基线，主要吸收 triage + handoff + specialist takeover 的结构，而不复制 SDK 实现细节。
  confirmed: true
```

## 3. AdaptationSpec v1

```yaml
adaptation_spec:
  baseline_skill: OpenAI Agents SDK Handoffs
  baseline_source: https://openai.github.io/openai-agents-python/handoffs/
  customizations:
    feature_trim:
      - 移除全能助手语义
      - 移除强人格化叙事
      - 移除“大而全建议器”表达
      - 不把地图优先写成唯一入口人格
    feature_extend:
      - 显式补齐入口信号识别
      - 显式补齐上下文成熟度判断
      - 显式补齐下游路径选择
      - 显式补齐 handoff 规则
      - 显式列出与 Maglev 核心对象的关系
    naming_convention: entry-router
    interaction_style: 简洁直接、低人格化、结构优先、明确交接
    integrations:
      - skill_name: maglev-standup
        relation: 调用
      - skill_name: requirement-convergence
        relation: 调用
      - skill_name: maglev-create-spec
        relation: 调用
      - skill_name: maglev-quick-dev
        relation: 调用
      - skill_name: maglev-cross-validate
        relation: 调用
      - skill_name: maglev-map-maker
        relation: 调用
      - skill_name: maglev-tutor
        relation: 调用
  created_at: 2026-03-30
```

## 4. 当前结论

本轮 `skill-scout adapt` 已形成可执行的私域化改造规格。

与 `需求收敛`、`现实结晶` 不同，这个对象当前适合继续推进为独立 skill，因为：

1. 它的对象形态已经稳定为 skill
2. 它承担的是显式入口路由职责
3. 它需要与一组现有技能形成清晰 handoff 关系

因此本对象后续可以进入 Forge / Register 路径。
