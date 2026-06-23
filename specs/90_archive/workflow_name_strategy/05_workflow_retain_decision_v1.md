# workflow retain decision v1

> 状态：已决策
> 作用：基于当前影响面与角色判断，确认四个兼容 workflow 文件名当前不进入物理 rename。

## 1. 当前结论

本轮决策：

- `retain`

即：

1. 保留 `standup.md`
2. 保留 `create-spec.md`
3. 保留 `quick-dev.md`
4. 保留 `validate-all.md`

当前不进入 workflow 文件名物理 rename。

## 2. 决策理由

### A. workflow 当前承接的是“入口语义”，不是“结构真名”

当前结构真相已经由 skill runtime name 承担：

1. `reality-sync`
2. `spec-designer`
3. `context-implementer`
4. `integrated-validator`

workflow 层更像：

1. slash 入口
2. 用户记忆点
3. 兼容层

因此 workflow 与 skill 不需要强制同名。

### B. 当前 workflow 名更贴近使用习惯

例如：

1. `/standup` 比 `/reality-sync` 更短、更像会话启动动作
2. `/create-spec` 比 `/spec-designer` 更直接表达“我要产一个 spec”
3. `/quick-dev` 比 `/context-implementer` 更口语化
4. `/validate-all` 虽然不整齐，但对用户来说更像一个可执行命令

### C. rename 成本高于当前收益

如果继续改 workflow 文件名，至少要同步影响：

1. guides
2. tutor
3. Reality
4. 排障与发版说明
5. 用户已有记忆与操作习惯

而当前并没有足够证据表明旧 workflow 文件名已经造成显著阻力。

## 3. 允许保留的不一致

当前允许并应显式承认：

1. skill runtime name 使用新名
2. workflow 文件名保留旧入口名

只要满足以下条件，这种不一致就是可接受的：

1. 文档明确写出“兼容入口”
2. 不把 workflow 文件名误写成当前 skill runtime name
3. 用户文档优先解释“这是什么入口”，而不是强行追求命名整齐

## 4. 后续触发条件

只有当出现以下情况，才重新考虑 workflow rename：

1. 用户持续把 workflow 文件名和 skill runtime name 混淆
2. 入口数量继续增长，导致命名治理成本明显上升
3. 产品层决定统一 slash command 命名体系

## 5. 当前结论的含义

`workflow_name_strategy` 当前更接近“确认继续保留兼容入口层”，而不是“准备进入 workflow rename execution”。
