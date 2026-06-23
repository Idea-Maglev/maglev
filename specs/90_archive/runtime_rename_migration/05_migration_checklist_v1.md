# runtime rename migration checklist v1

> 状态：已完成
> 作用：给主流程核心四对象提供进入物理 rename execution 主题前必须满足的最小迁移清单。

## 1. 执行前门槛

进入真正的 rename execution 主题前，至少必须确认：

1. 已决定是否同时修改 skill 名与 workflow 文件名
2. 已确认 `.agents/private-catalog.yaml` 的迁移方式
3. 已确认 `entry-router`、`requirement-convergence`、`skill-squadron` 的协作改造方式
4. 已确认 Reality 与 capability snapshot 的统一写法
5. 已确认用户侧文档采用双写过渡还是直接改写

## 2. 先做双写统一的对象

在任何物理 rename 之前，应优先处理：

1. `entry-router`
2. `requirement-convergence`
3. `skill-squadron`
4. `specs/10_reality/01_requirements.md`
5. `specs/10_reality/distribution_runtime.md`
6. `docs/marketing/assets/capability_snapshot/published.md`

目标：

- 先把“正式动作名优先、旧运行名兼容”的写法稳定下来

## 3. 物理 rename 前必须复核的对象

在真正改 skill 或 workflow 名之前，必须逐项复核：

1. `.agents/workflows/standup.md`
2. `.agents/workflows/create-spec.md`
3. `.agents/workflows/quick-dev.md`
4. `.agents/workflows/validate-all.md`
5. `.agents/private-catalog.yaml`

目标：

- 确认入口、分发与对象路由不会因改名直接断裂

## 4. 可后置处理的对象

以下对象不应阻塞 rename execution 主题立项，但应在执行后续批次中逐步清理：

1. `docs/marketing/assets/for_developers/published.md`
2. `docs/marketing/assets/for_tech_leads/published.md`
3. `docs/marketing/assets/for_decision_makers/published.md`
4. `docs/marketing/assets/for_enterprises/published.md`
5. `docs/marketing/assets/problem_statement/published.md`
6. `docs/marketing/assets/why_ai_coding_needs_governance/published.md`
7. `docs/marketing/assets/legacy_system_showcase/published.md`

## 5. 当前结论

只要上面的前置清单还没被逐项确认，就不应该直接开做 rename execution。

当前更合理的推进方式是：

1. 先以本 checklist 作为下一轮执行主题的准入门槛
2. 再决定是否真的值得进入物理 rename
