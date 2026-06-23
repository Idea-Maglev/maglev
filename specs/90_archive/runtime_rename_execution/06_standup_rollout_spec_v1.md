# standup rollout spec v1

> 状态：已执行并完成最小校验
> 作用：为第一个试点对象 `maglev-standup` 提供可直接执行的 rollout 规格。

## 1. 试点对象

当前试点对象：

- `maglev-standup`

推荐目标名：

- `reality-sync`

## 2. 为什么先做它

1. 它位于主流程最前段，职责清楚
2. relation 影响面相对四对象里最简单
3. 成功后能为后续三个对象提供统一执行模板

## 3. 本对象的最小执行面

未来真实执行时，至少需要同步处理：

1. `.agents/skills/maglev-standup/` -> `.agents/skills/reality-sync/`
2. `.agents/private-catalog.yaml` 中：
   - `name: 'maglev-standup'` -> `name: 'reality-sync'`
   - `path: '.agents/skills/maglev-standup/'` -> `path: '.agents/skills/reality-sync/'`
3. `entry-router` 在 catalog 中的 relation target：
   - `maglev-standup` -> `reality-sync`
4. 该对象的 `runtime_name_status`
   - 最后再切到 `canonical_name_active`

## 4. 明确不处理

本对象 rollout 当前不处理：

1. `.agents/workflows/standup.md` 文件名
2. 历史文档中的“历史入口”说明
3. `.maglev_build/` 等构建镜像路径

## 5. 执行后最小验证

### A. 目录层

1. `.agents/skills/reality-sync/` 存在
2. `.agents/skills/maglev-standup/` 已退出运行面

### B. catalog 层

1. `reality-sync` 已存在于 catalog
2. `maglev-standup` 不再作为 active skill name 存在
3. `entry-router` 的 target 已指向 `reality-sync`

### C. 口径层

1. workflow 仍可通过 `standup.md` 作为兼容入口存在
2. 文档中的双写不需要立刻重洗
3. “历史入口”说明仍然自洽

## 6. 暂停条件

若出现以下任一情况，应暂停：

1. `entry-router` target 已改，但 skill 目录或 catalog path 未同步
2. `runtime_name_status` 被提前切换
3. 仍残留 active relation target 指向 `maglev-standup`

## 7. 当前结论

`maglev-standup -> reality-sync` 已完成第一轮真实 execution，并通过最小运行面校验：

1. 新 skill 目录已存在，旧目录已退出运行面
2. catalog 中的 `name`、`path`、`entry-router` relation target 已完成同步切换
3. 兼容 workflow `/standup` 仍保留
4. 当前仓库中不再残留 active relation target、active path 或 active skill name 指向 `maglev-standup`

后续若继续推进，下一步应复用本轮模板，进入第二个对象 `maglev-create-spec`。
