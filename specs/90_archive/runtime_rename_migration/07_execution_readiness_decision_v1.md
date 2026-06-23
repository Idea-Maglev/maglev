# runtime rename execution readiness decision v1

> 状态：已完成
> 作用：基于 `runtime_rename_migration` 当前已完成的影响面盘点、双写统一和 catalog 策略，判断主流程核心四对象是否已经具备进入真正物理 rename execution 主题的条件。

## 1. 判断对象

本次判断只覆盖：

1. `maglev-standup`
2. `maglev-create-spec`
3. `maglev-quick-dev`
4. `maglev-cross-validate`

## 2. 当前已满足条件

### A. 结构语义已稳定

当前四对象都已具备稳定的正式动作名：

1. `现状同步`
2. `方案设计`
3. `上下文实施`
4. `综合验证`

这部分当前不再构成阻塞。

### B. 双写统一已形成稳定基础

当前已完成：

1. `entry-router`
2. `requirement-convergence`
3. `skill-squadron`
4. Reality 文档
5. capability snapshot
6. 多篇现役 marketing 文档
7. 核心 workflow 说明与一批现役技能说明

这意味着：

- 当前读者面与协作面已经基本能接受“正式动作名优先、旧运行名兼容”的口径

### C. catalog 迁移策略已明确

当前已明确：

1. catalog 迁移必须同轮处理 `name`、`path`、`relations.target`
2. `formal_action_name` 不再作为迁移对象
3. `runtime_name_status` 只能最后再切

这意味着：

- 真正进入 rename execution 时，不再需要重新定义 catalog 迁移原则

## 3. 当前仍未满足条件

### A. workflow 文件名策略仍未最终拍板

虽然 workflow 描述已经完成双写统一，但仍未最后决定：

1. 是否只改 skill 名
2. 是否 skill 与 workflow 文件名一起改
3. 若 workflow 暂不改，兼容期如何定义

这是当前最直接的执行阻塞。

### B. catalog 仍未进入 relation-level 执行准备

虽然 catalog 策略已明确，但还没有形成真正的逐项执行清单，例如：

1. 哪个 relation target 先迁
2. 哪些 target 需要同步改写
3. 迁移时如何做一致性校验

也就是说：

- 当前是“策略已清”，还不是“执行脚本已清”

### C. 仍存在一批合理保留的旧运行名

当前仓库中仍可见旧运行名，但大多属于以下可接受类型：

1. `name:` 字段
2. skill / workflow 路径
3. step metadata 的内部标识
4. Reality 文档中的“历史入口”说明
5. 少量 release / guide 中的历史语境

这说明当前已不再是“文档混乱”问题，而是：

- 是否正式进入物理 rename 的策略选择问题

## 4. 结论

当前结论是：

> 已基本完成 rename execution 前的文档与策略准备，但还不建议立刻进入物理 rename execution。

更准确地说：

1. 当前已经具备进入 execution 主题的前置认知条件
2. 但还不具备“马上执行目录改名”的最终条件
3. 在真正进入 execution 前，还应先补一份更窄的执行前规格

## 5. 推荐下一步

如果继续推进，下一步不应直接改名，而应新开一个更窄的 execution-preflight 主题，只处理两件事：

1. 决定 `skill-only` 还是 `skill + workflow` 的迁移方案
2. 形成 relation-level 的 catalog migration checklist

只有这两件事完成后，才值得进入真正的物理 rename execution。
