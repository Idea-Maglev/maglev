# `需求收敛` Scout 私域化改造规格 v1

> 状态：进行中
> 作用：在 `skill-scout` 的 `adapt` 步骤中，基于已选改造基线，为 `需求收敛` 生成第一版私域化改造规格。

## 1. 当前前提

本轮输入来自：

- [02z_requirement_convergence_scout_evaluation_v1.md](02z_requirement_convergence_scout_evaluation_v1.md)
- [02w_scout_readiness_packets_v1.md](02w_scout_readiness_packets_v1.md)
- [03e_requirement_convergence_workflow.md](../plan/03e_requirement_convergence_workflow.md)

当前默认前提是：

- `OpenSpec` 作为主改造基线已被接受
- `cc-sdd` 作为 requirements-first 的辅助参照
- `GitHub Spec Kit` 作为规范化与 guardrail 的补充参照

## 2. 基线确认

```yaml
adaptation_baseline:
  skill_name: OpenSpec
  source_url: https://github.com/Fission-AI/OpenSpec
  source_type: github
  evaluation_summary: 作为需求收敛的主改造基线，主要吸收其 change proposal / alignment before implementation 的前段结构，而不整体复制其完整 change workflow。
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
      - 不引入 OpenSpec 的完整任务实施链
      - 不把 archive / spec update 后段能力混入需求收敛
      - 不保留对专用 CLI 和固定目录布局的硬依赖
    feature_extend:
      - 显式补齐入口分流
      - 显式补齐需求定义
      - 显式补齐 Ready Gate
      - 与现状同步形成稳定前后接口
      - 与方案设计形成清晰 handoff
      - 允许以 workflow-first 形态承载，而不是强制 skill 化
    naming_convention: requirement-convergence
    interaction_style: 结构化、直接、前段收束优先、避免大而全访谈
    integrations:
      - skill_name: maglev-standup
        relation: 互补
      - skill_name: maglev-create-spec
        relation: 调用
      - skill_name: skill-squadron
        relation: 互补
  created_at: 2026-03-30
```

## 4. 结构化解释

### 4.1 功能裁剪

本轮明确不吸收的部分：

1. 不把 `OpenSpec` 的完整 change lifecycle 原样搬入 Maglev
2. 不把 `需求收敛` 扩成“从变更提案到实施”的全链大对象
3. 不把后段 `archive / update specs` 能力混入前段
4. 不为当前对象引入强 CLI 依赖

### 4.2 功能扩展

本轮明确要补齐的部分：

1. `入口分流`
2. `需求定义`
3. `Ready Gate`
4. `现状同步 -> 需求收敛 -> 方案设计` 的稳定主流程接口

### 4.3 命名判断

当前先收一个工作名：

- `requirement-convergence`

这个名字的作用仅限于：

- 表达当前私域化改造对象的结构语义

它现在还不代表：

- 已正式定稿为未来 skill 名
- 现在就要创建对应 skill 目录

### 4.4 交互风格

当前明确要求：

- 简洁直接
- 结构优先
- 前段收束优先
- 少闲聊
- 不做大而全访谈器

### 4.5 集成关系

当前最关键的集成关系是：

1. 与 `maglev-standup` 互补
   - `standup` 负责读取和组织现状
   - `需求收敛` 负责把入口任务收成稳定边界

2. 向 `maglev-create-spec` 交接
   - `需求收敛` 完成后，后续才能稳定进入 `方案设计`

3. 与 `skill-squadron` 互补
   - 后续进入批量治理时，`需求收敛` 可作为新的前段对象参与结构编队

## 5. 当前私域化判断

基于本轮 AdaptationSpec，当前对 `需求收敛` 的私域化判断是：

1. 该对象已经有足够稳定的外部改造基线
2. 该对象已经有足够稳定的私域化裁剪和扩展方向
3. 但它当前仍更适合：
   - `workflow-first`
   而不是
   - 立即生成独立 skill

## 6. 当前不直接生成独立 skill 的原因

虽然本轮已经进入 `adapt`，但当前仍不建议立即把该对象固化为独立 skill。

原因是：

1. `需求收敛` 目前在结构上仍是 `workflow-first`
2. 当前重点是稳住前段三段式结构，而不是抢先生成 skill 物理目录
3. 其未来正式 `canonical_skill_name` 仍未进入正式定稿阶段

所以当前更合理的结论是：

- `AdaptationSpec` 已形成
- 独立 skill 生成暂缓
- 后续优先先把它作为前段 workflow 对象继续收稳

## 7. 当前结论

本轮 `skill-scout adapt` 已经形成了可复用的私域化改造规格：

- 主基线：`OpenSpec`
- 辅助参照：`cc-sdd`、`GitHub Spec Kit`
- 当前工作名：`requirement-convergence`
- 当前承载形态：`workflow-first`

因此后续若继续推进，不应直接跳去写 skill，而应优先做两件事之一：

1. 继续把该对象落成正式 workflow 草案
2. 或在后续确认条件满足后，再进入 Forge / Register
