# governance decision v1

> 状态：已决策
> 作用：确认 `runtime_naming_governance` 的首版规则与检查清单已成为当前生效口径。

## 1. 当前决策

本轮决策：

- `adopt`

即：

1. [04_naming_governance_rule_v1.md](./04_naming_governance_rule_v1.md) 作为当前命名治理规则
2. [05_minimum_naming_checklist_v1.md](./05_minimum_naming_checklist_v1.md) 作为当前最小检查清单

## 2. 决策含义

从当前起，以下判断不再是临时讨论结果，而是正式治理口径：

1. `formal_action_name`、`skill runtime name`、`workflow filename / slash entry`、`catalog relation target` 必须显式分层
2. 允许 workflow filename 与 skill runtime name 不同
3. 不允许 catalog relation target 指向历史 runtime name 或 workflow filename
4. 若修改 `skill runtime name`，catalog `name/path/relations.target` 必须同轮同步

## 3. 当前默认执行方式

后续对象或改名请求进入仓库时，应默认按以下方式执行：

1. 先用规则判断请求是否合法
2. 再用最小检查清单判断是否可进入 execution
3. 若违反阻断条件，则不进入 execution

## 4. 当前不进入的后续动作

本轮决策同时确认：

1. 不立即新增 rename execution 主题
2. 不重开 workflow rename 主题
3. 不对 archive / 历史文档做命名统一强制清洗
