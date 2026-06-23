# `knowledge-check` Scout 私域化改造规格 v1

> 状态：进行中
> 作用：在 `skill-scout` 的 `adapt` 步骤中，基于已选改造基线，为 `knowledge-check` 生成第一版私域化改造规格。

## 1. 当前前提

本轮输入来自：

- [02zi_knowledge_check_scout_evaluation_v1.md](02zi_knowledge_check_scout_evaluation_v1.md)
- [02w_scout_readiness_packets_v1.md](02w_scout_readiness_packets_v1.md)

当前默认前提是：

- `Atlassian Incident Postmortem` 作为主改造基线已被接受
- `OpenAI Session Memory` 作为资产保全辅证
- `Anthropic Gates` 作为结构原则辅证

## 2. 基线确认

```yaml
adaptation_baseline:
  skill_name: Atlassian Incident Postmortem
  source_url: https://www.atlassian.com/incident-management/postmortem/templates
  source_type: official_docs
  evaluation_summary: 作为 knowledge-check 的主改造基线，主要吸收状态结束后的知识沉淀检查逻辑，而不复制 incident 专有语义。
  confirmed: true
```

## 3. AdaptationSpec v1

```yaml
adaptation_spec:
  baseline_skill: Atlassian Incident Postmortem
  baseline_source: https://www.atlassian.com/incident-management/postmortem/templates
  customizations:
    feature_trim:
      - 移除 incident 专有语义
      - 移除状态恢复语义
      - 移除需求归档语义入口
    feature_extend:
      - 显式补齐 thinking 检查
      - 显式补齐 solution 检查
      - 显式补齐 references / archive 检查
      - 显式补齐 contribution log 检查
      - 显式补齐 skill 影响检查
      - 与 crystallization 形成边界说明
    naming_convention: knowledge-check
    interaction_style: 简洁直接、检查导向、少叙事、强调沉淀边界
    integrations:
      - skill_name: crystallization
        relation: 互补
      - skill_name: contribute_methodology
        relation: 互补
      - skill_name: skill-scout
        relation: 互补
  created_at: 2026-03-30
```

## 4. 当前结论

本轮 `skill-scout adapt` 已形成可执行的私域化改造规格。

这个对象当前适合继续推进为独立 skill，因为：

1. 它本质上就是一个检查型对象
2. 它与 `现实结晶` 的边界已被明确切开
3. 它需要一个新的正式名字退出“归档”大词占位

因此本对象后续可以进入 Forge / Register 路径。
