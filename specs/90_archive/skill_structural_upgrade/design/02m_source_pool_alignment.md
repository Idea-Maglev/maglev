# skill结构性升级 资源池校准与来源链纠偏

> 状态：进行中
> 作用：记录本轮外部对标与 `skill-scout` 资源来源机制的对齐结果，确保后续巡逻先走私有资源池，再使用公开补充来源。

## 1. 纠偏背景

本轮前几次外部对标，虽然使用了高质量公开资料，但没有先经过 `skill-scout` 定义的来源加载顺序：

1. 内置层 `references/source-registry.yaml`
2. 用户层 `skill-sources.yaml`
3. 偏好过滤 `references/user-source-preferences.yaml`
4. 形成 Effective Sources 后，再进入外部搜索

这意味着：

- 结论未必错
- 但来源链不符合 Maglev 已定义的私有资源池优先策略

因此这里需要补一次来源链纠偏。

## 2. 当前来源配置

### A. 内置层

来源：

- `.agents/skills/skill-scout/references/source-registry.yaml`

当前条目：

1. `Agent Skills`
2. `OpenAI Skills Catalog`
3. `Vercel Skills`
4. `Learn Skills Hub`

### B. 用户层

来源：

- `skill-sources.yaml`

当前条目：

1. `SkillHub`
2. `ClawHub`
3. `GitHub Spec Kit`
4. `OpenSpec`
5. `cc-sdd`
6. `Awesome AI Agents`
7. `Awesome GPT Prompt Engineering`

### C. 偏好配置

来源：

- `.agents/skills/skill-scout/references/user-source-preferences.yaml`

当前与本轮最相关的场景配置：

- `spec_driven_development`
  - `enabled_sources`
    - `GitHub Spec Kit`
    - `OpenSpec`
    - `cc-sdd`
  - `preferred_types`
    - `github`
  - `priority_boost`
    - `GitHub Spec Kit: +2`
    - `OpenSpec: +1`

## 3. 当前 Effective Sources 判断

结合本轮主题 `skill结构性升级`，尤其是：

- `需求收敛`
- `方案设计`
- 生命周期承载
- spec-driven workflow

当前最合理的来源场景应优先映射到：

- `spec_driven_development`

因此，本轮第一优先级 Effective Sources 应收敛为：

1. `GitHub Spec Kit`
2. `OpenSpec`
3. `cc-sdd`

这三者比直接泛搜官方文档更符合：

- 当前任务的主题
- 用户定义的来源池
- `skill-scout` 的执行协议

## 4. 基于私有资源池的重放结果

### A. `GitHub Spec Kit`

来源：

- [GitHub Spec Kit](https://github.com/github/spec-kit)

对当前主线的直接支持：

- 强调 `Intent-driven development`
- 强调 `guardrails`
- 强调 `multi-step refinement`

这支持了我们当前对：

- `需求收敛`
- `方案设计`
- `Ready Gate`

的分段判断。

### B. `OpenSpec`

来源：

- [OpenSpec](https://github.com/Fission-AI/OpenSpec)

对当前主线的直接支持：

- 强调在编码前先达成对 spec 的一致理解
- 强调 proposal / tasks / spec updates 的显式分离
- 强调 current truth 与 proposed changes 分开维护

这支持了我们当前对：

- `10_reality`
- `20_evolution/active`
- 生命周期分层承载

的判断。

### C. `cc-sdd`

来源：

- [cc-sdd](https://github.com/gotalab/cc-sdd)

对当前主线的直接支持：

- 明确要求 `requirements -> design -> tasks -> implementation`
- 强调 steering / validation / brownfield enhancement
- 强调 project memory

这支持了我们当前对：

- `需求收敛` 不应被 `方案设计` 吞并
- workflow 分段比单一大 skill 更稳
- 长期现状 / 记忆层应独立存在

## 5. 纠偏后的结论

基于私有资源池重放后，当前可以更稳地说：

### 结论 1

本轮关于 `需求收敛`、生命周期承载、Reality / Evolution 分层的关键判断，并没有因为引入私有资源池而被推翻。

### 结论 2

这些判断现在有了更符合 Maglev 规则的第一层证据来源：

- `GitHub Spec Kit`
- `OpenSpec`
- `cc-sdd`

### 结论 3

后续若继续在线对标，应优先遵循：

1. 先判当前问题映射到哪个 `scenario_profile`
2. 先用 Effective Sources 做第一轮搜索
3. 再用公开官方资料做第二层校正

### 结论 4

本轮已产出的外部对标文档，应从现在开始按以下方式理解：

- 私有资源池命中的来源：第一层证据
- 官方公开文档：第二层校正证据

## 6. 当前结论

这次纠偏最重要的价值，不是重新推翻结论，而是把来源链重新接回 Maglev 已定义的治理顺序：

- 先私有资源池
- 再公开补充

这样后续 `skill-scout` / `skill-squadron` 的外部对标，才能真正成为可复用、可治理的长期资产。
