# Submodule Adoption Decision v1

> 状态：首版决策已形成
> 结论档位：`Optional / Recommended`

## 1. 结论

当前不建议把“代码仓库改用 submodule 管理”直接升为新的默认接入方式。

当前更合理的结论是：

- `Optional / Recommended`

也就是说：

1. Maglev 应允许并推荐在“多仓库聚合、需要稳定可复现工作台”的场景下使用 submodule
2. 但当前不应强制所有 Maglev 化项目都改成 submodule 默认模型

## 2. 为什么不是 `Reject`

维持纯 `git clone` 模型已经暴露出两个真实问题：

1. wrapper 项目无法稳定绑定下游代码仓库的 revision
2. 多人协作时，很难保证每个人拿到完全一致的代码拓扑

如果 Maglev 继续承诺“统一工作台 / 多仓库现实对齐”，submodule 至少值得成为一个正式可选模型。

## 3. 为什么不是 `Default`

旧文档 [docs/thinking/20_architecture/adoption_model_evolution.md](../../../docs/thinking/20_architecture/adoption_model_evolution.md) 反对 submodule 的理由，并没有完全失效。

当前仍然成立的风险包括：

1. `Git Submodule` 的工程摩擦仍然高
   - detached HEAD
   - recursive clone / update
   - pointer 变更需要单独理解
2. Code / Spec 仍不具备天然原子提交
3. 团队成员如果不理解 submodule 工作方式，反而会产生新的环境错位

这些风险在“默认强制”场景下仍足以构成阻断。

## 4. 哪些旧反对理由已经弱化

相比旧决策时期，现在有两点变化，使 submodule 从“纯拒绝”升级为“可以进入推荐模式评估”：

1. `init / update` 已经具备正式执行链路
   - 可以承接 submodule 初始化、同步、检查与解释
2. Maglev 已经形成更稳定的入口和结构治理能力
   - 可以把 submodule 从“手工技巧”变成“受控接入模式”

也就是说，旧的“工程不可承接”问题已经弱化，但“默认强推成本过高”仍成立。

## 5. 当前建议的适用场景

当前更适合推荐 submodule 的场景：

1. 一个 Maglev wrapper 需要稳定聚合多个业务仓库
2. 团队明确需要可复现的多仓库工作台
3. 团队能接受 submodule 的 Git 操作纪律
4. `init / update` 后续愿意承接 submodule 生命周期

当前不建议强推 submodule 的场景：

1. 单仓项目
2. 团队 Git 基础较弱
3. 只想最小接入 Maglev，而不想引入新的仓库治理复杂度

## 6. 当前影响面判断

如果后续进入实现，推荐先按“可选模式”设计，而不是直接替换现有 clone 行为：

1. `init`
   - 增加“仓库接入模式”选择
2. `update`
   - 明确 submodule pointer 是否同步、如何同步
3. `.maglev/config.json`
   - 从 `clone_status` 扩展为更通用的仓库管理状态
4. `repository_map.md`
   - 增加仓库管理方式字段
5. 用户手册
   - 单独说明 submodule 模式的协作约束

## 7. 下一步建议

下一步不应直接改代码，而应先写一份 implementation spec，回答：

1. `init` 里的模式选择长什么样
2. `.maglev/config.json` 要新增哪些字段
3. `repository_map.md` 如何表达 `submodule`
4. `update` 是否要同步 submodule pointer，还是只检查状态
