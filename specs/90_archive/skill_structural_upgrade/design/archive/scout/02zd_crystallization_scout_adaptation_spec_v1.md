# `现实结晶` Scout 私域化改造规格 v1

> 状态：进行中
> 作用：在 `skill-scout` 的 `adapt` 步骤中，基于已选改造基线，为 `现实结晶` 生成第一版私域化改造规格。

## 1. 当前前提

本轮输入来自：

- [02zc_crystallization_scout_evaluation_v1.md](02zc_crystallization_scout_evaluation_v1.md)
- [02w_scout_readiness_packets_v1.md](02w_scout_readiness_packets_v1.md)
- [03c_crystallization_workflow.md](../plan/03c_crystallization_workflow.md)

当前默认前提是：

- `OpenSpec` 作为主改造基线已被接受
- `GitHub Spec Kit` 作为流程纪律补充
- `cc-sdd` 作为低优先级辅助参照

## 2. 基线确认

```yaml
adaptation_baseline:
  skill_name: OpenSpec
  source_url: https://github.com/Fission-AI/OpenSpec
  source_type: github
  evaluation_summary: 作为现实结晶的主改造基线，主要吸收其 archive/update-specs 的后段收口逻辑，而不整体复制其 change lifecycle。
  confirmed: true
```

## 3. AdaptationSpec v1

```yaml
adaptation_spec:
  baseline_skill: OpenSpec
  baseline_source: https://github.com/Fission-AI/OpenSpec
  customizations:
    feature_trim:
      - 不引入完整的 change 目录体系
      - 不引入 postmortem / knowledge capture 逻辑
      - 不把思考沉淀混入现实结晶
      - 不保留对专用 CLI 和固定目录布局的硬依赖
    feature_extend:
      - 显式补齐结晶条件确认
      - 显式补齐现实回写判定
      - 显式补齐 active 状态收口
      - 显式补齐索引与可发现性回填
      - 与综合验证形成稳定前后接口
      - 与 map-maker / librarian / reality 更新动作形成协同接口
      - 允许以 workflow-first 形态承载，而不是强制 skill 化
    naming_convention: crystallization
    interaction_style: 结构化、闭环优先、事实优先、避免把知识沉淀混入状态收口
    integrations:
      - skill_name: maglev-cross-validate
        relation: 互补
      - skill_name: maglev_archival_check
        relation: 互补
      - skill_name: maglev-map-maker
        relation: 调用
      - skill_name: maglev-librarian
        relation: 调用
  created_at: 2026-03-30
```

## 4. 结构化解释

### 4.1 功能裁剪

本轮明确不吸收的部分：

1. 不把 `OpenSpec` 的整套 change lifecycle 原样搬入 Maglev
2. 不把知识沉淀、复盘、postmortem 混入该对象
3. 不为当前对象引入强 CLI 依赖

### 4.2 功能扩展

本轮明确要补齐的部分：

1. `结晶条件确认`
2. `现实回写判定`
3. `active 状态收口`
4. `索引与可发现性回填`

### 4.3 命名判断

当前先收一个工作名：

- `crystallization`

这个名字现在只表达结构语义，不代表已经进入正式 skill 定稿。

### 4.4 交互风格

当前明确要求：

- 简洁直接
- 闭环优先
- 事实优先
- 不把“归档”当宽泛兜底词

### 4.5 集成关系

当前最关键的集成关系是：

1. 与 `maglev-cross-validate` 互补
   - `综合验证` 负责判断结果是否成立
   - `现实结晶` 负责把已成立结果沉淀为新现实

2. 与 `maglev_archival_check` 互补
   - `maglev_archival_check` 负责知识沉淀检查
   - `现实结晶` 不承担思考归档

3. 调用 `maglev-map-maker` 与 `maglev-librarian`
   - 完成末端可发现性回填

## 5. 当前私域化判断

基于本轮 AdaptationSpec，当前对 `现实结晶` 的私域化判断是：

1. 该对象已经有足够稳定的外部改造基线
2. 该对象已经有足够稳定的私域化裁剪和扩展方向
3. 但它当前仍更适合：
   - `workflow-first`
   而不是
   - 立即生成独立 skill

## 6. 当前不直接生成独立 skill 的原因

虽然本轮已经进入 `adapt`，但当前仍不建议立即把该对象固化为独立 skill。

原因是：

1. `现实结晶` 当前在结构上仍是 `workflow-first`
2. 当前重点是稳住后段四步闭环，而不是抢先生成 skill 物理目录
3. 其未来正式 `canonical_skill_name` 仍未进入正式定稿阶段

## 7. 当前结论

本轮 `skill-scout adapt` 已形成可复用的私域化改造规格：

- 主基线：`OpenSpec`
- 辅助参照：`GitHub Spec Kit`、`cc-sdd`
- 当前工作名：`crystallization`
- 当前承载形态：`workflow-first`

因此后续若继续推进，不应直接跳去写 skill，而应优先把该对象落成正式 workflow。
