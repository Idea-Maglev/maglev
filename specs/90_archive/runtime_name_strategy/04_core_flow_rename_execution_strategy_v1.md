# runtime name 主流程核心对象 rename 执行策略 v1

> 状态：进行中
> 作用：为主流程核心四对象提供一套可执行的 rename 策略，明确双写范围、兼容入口策略与进入物理 rename 回合的门槛。

## 1. 适用对象

本策略只覆盖以下四个主流程核心对象：

1. `maglev-standup` -> `现状同步`
2. `maglev-create-spec` -> `方案设计`
3. `maglev-quick-dev` -> `上下文实施`
4. `maglev-cross-validate` -> `综合验证`

## 2. 当前判断

这四个对象当前都满足：

1. `formal_action_name` 已稳定
2. `runtime_name_status = active_legacy_name`
3. 运行面旧名仍有真实使用惯性
4. 当前直接物理改名的风险高于收益

因此这轮不进入“立即改名”，而进入：

> 文档先行、入口兼容、迁移预备

## 3. 当前双写规范

### A. 结构文档

在结构文档、设计文档、Reality 文档、治理文档中，优先使用：

- `现状同步（maglev-standup）`
- `方案设计（maglev-create-spec）`
- `上下文实施（maglev-quick-dev）`
- `综合验证（maglev-cross-validate）`

如果上下文已充分明确，也可以只写正式动作名。

### B. 运行面文件

在实际 skill / workflow 文件中：

1. 保留旧文件名
2. `metadata.formal_action_name` 继续稳定
3. `runtime_name_status` 继续维持 `active_legacy_name`
4. 明确写出“结构动作名已稳定，但尚未进入物理改名”

### C. 用户教程与入口说明

在用户会直接跟着操作的地方：

1. 优先保留旧运行名，避免教程立即失效
2. 若要引入正式动作名，必须双写
3. 不得只写新动作名而省略旧运行名

## 4. 兼容入口策略

### `maglev-standup`

- 保留 workflow: `standup.md`
- 保留 skill 目录: `maglev-standup/`
- 文档中优先解释为 `现状同步`

### `maglev-create-spec`

- 保留 workflow: `create-spec.md`
- 保留 skill 目录: `maglev-create-spec/`
- 文档中优先解释为 `方案设计`

### `maglev-quick-dev`

- 保留 workflow: `quick-dev.md`
- 保留 skill 目录: `maglev-quick-dev/`
- 文档中优先解释为 `上下文实施`

### `maglev-cross-validate`

- 保留 workflow: `validate-all.md`
- 保留 skill 目录: `maglev-cross-validate/`
- 文档中优先解释为 `综合验证`

## 5. 进入物理 rename 回合的门槛

仅当以下条件同时成立时，这四个对象才应进入真正的物理 rename 回合：

1. 主线结构至少一个阶段内不再发生大幅调整
2. 用户文档、README、Reality、治理文档已完成双写兼容
3. workflow 名称、skill 名称、CLI/会话习惯的影响面已盘清
4. 可以接受一轮集中迁移带来的认知成本
5. 已明确是否要“只改 skill 名”还是“skill + workflow 一起改”

## 6. 当前不建议的动作

当前不建议：

1. 直接把 skill 目录名改成中文动作名
2. 直接把 workflow 文件全部改名
3. 在文档里只保留正式动作名，不保留旧运行名
4. 把所有 `active_legacy_name` 对象一并推进 rename

## 7. 当前结论

当前最稳的执行策略是：

1. 主流程核心四对象继续保持旧运行名
2. 所有结构文档优先稳定正式动作名
3. 对用户可执行入口继续保留旧名称
4. 后续若真的要改名，应新开“runtime rename migration” 主题，而不是在当前策略主题里直接动手
