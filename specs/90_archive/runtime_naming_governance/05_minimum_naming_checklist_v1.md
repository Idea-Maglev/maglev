# minimum naming checklist v1

> 状态：已形成首版清单
> 作用：为后续新对象接入、命名调整和 rename 请求提供最小检查清单。

## 1. 新对象准入前

至少检查：

1. 是否明确 `formal_action_name`
2. 是否明确唯一 `skill runtime name`
3. 是否明确是否需要 workflow 入口
4. 若存在 workflow，是否写明它是正式入口还是兼容入口
5. `.agents/private-catalog.yaml` 是否已补齐 `name/path/runtime_name_status/object_kind`

## 2. rename 请求前

至少检查：

1. 这是在改 `formal_action_name`，还是在改 `skill runtime name`
2. 是否会影响 catalog `name/path/relations.target`
3. 是否会影响现有 workflow 入口
4. 是否需要双写兼容阶段
5. 是否已有足够证据证明改名收益高于迁移成本

## 3. rename 执行时

若修改 `skill runtime name`，必须同步确认：

1. skill 目录名已切换
2. `SKILL.md` 的 `name` 已切换
3. catalog `name` 已切换
4. catalog `path` 已切换
5. 所有关联 `relations.target` 已切换
6. `runtime_name_status` 已在最后切到目标状态

## 4. 文档校验

至少检查：

1. 用户文档是否新名优先
2. 兼容入口是否已显式标注
3. 历史入口是否已显式标注
4. 是否仍存在会误导当前路径事实的旧路径说明

## 5. 当前阻断条件

出现以下任一情况，应阻断提交或继续推进：

1. catalog relation target 仍指向历史 runtime name
2. workflow 入口名被误当成 runtime name 写入 skill / catalog
3. skill 目录与 catalog path 不一致
4. 文档把兼容入口写成当前 active 名而未说明
