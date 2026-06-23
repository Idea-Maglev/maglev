# skill结构性升级 迁移矩阵 v1

> 状态：进行中
> 作用：定义新对象落地后，哪些入口应直接切换，哪些旧对象应从运行面移除。

## 1. 目标

当前已经落地的新对象有：

- `entry-router`
- `knowledge-check`
- `requirement-convergence`（workflow-first）
- `crystallization`（workflow-first）

现在需要回答的不是“它们是否存在”，而是：

1. 后续应该优先推荐谁
2. 哪些旧对象应直接移除
3. 哪些说明文档应切到新口径

## 2. 迁移原则

1. 对已确认高误导性的旧对象直接移除
2. 优先迁移“推荐入口”和“默认解释口径”
3. 历史分析文档可保留提及，但不再保留运行面兼容写法
4. 对入口层对象，优先迁移调用路径；对后段对象，优先迁移语义解释

## 3. 对象迁移表

| 历史对象 | 新对象 / 新路径 | 当前迁移策略 | 说明 |
| :--- | :--- | :--- | :--- |
| `atomizer` | `entry-router` | 直接替换 | 旧对象已移除，入口语义完全由 `entry-router` 接管 |
| `maglev_archival_check` | `knowledge-check` | 直接替换 | 旧对象已移除，知识沉淀检查完全由 `knowledge-check` 接管 |
| 无稳定前段对象 | `requirement-convergence` | 新增承接 | 先以 workflow 承接，不急着立 skill |
| 无稳定后段闭环对象 | `crystallization` | 新增承接 | 先以 workflow 承接，不急着立 skill |

## 4. 入口层迁移

### A. `atomizer` -> `entry-router`

后续应优先使用：

- `entry-router`
- `.agents/workflows/entry-router.md`

当前状态：

- `.agents/skills/atomizer/` 已移除

### B. 推荐迁移动作

优先迁移：

1. 仓库入口说明
2. workflow 列表
3. 新会话入口建议

暂不强制迁移：

1. 所有历史归档文档
2. 已归档的旧案例

## 5. 沉淀检查迁移

### A. `maglev_archival_check` -> `knowledge-check`

后续应优先使用：

- `knowledge-check`
- `.agents/workflows/knowledge-check.md`

当前状态：

- `.agents/skills/maglev_archival_check/` 已移除

### B. 推荐迁移动作

优先迁移：

1. 所有将其解释为“需求归档”的说明
2. 所有把它当作 Reality 回写入口的误导口径
3. 所有“任务结束时就用 archival_check”这一类默认建议

## 6. Workflow-first 对象迁移

### A. `需求收敛`

当前推荐入口：

- `.agents/workflows/requirement-convergence.md`

当前策略：

- 在主流程说明中显式出现
- 不急着提升为独立 skill

### B. `现实结晶`

当前推荐入口：

- `.agents/workflows/crystallization.md`

当前策略：

- 在后段闭环说明中显式出现
- 不急着提升为独立 skill

## 7. 第一阶段迁移清单

当前第一阶段建议先迁移这些位置：

1. `README.md`
2. `AGENTS.md`
3. workflow 入口列表
4. 与入口层和归档语义直接相关的仓库说明

## 8. 当前结论

从现在开始，仓库内更推荐的入口语义应逐步变成：

- 入口层：`entry-router`
- 前段收敛：`requirement-convergence`
- 中段主流程：`maglev-standup` / `maglev-create-spec` / `maglev-quick-dev` / `maglev-cross-validate`
- 后段闭环：`crystallization`
- 知识沉淀检查：`knowledge-check`

而不是继续默认：

- `atomizer`
- `maglev_archival_check`
