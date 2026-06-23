# create-spec rollout spec v1

> 状态：已执行并完成最小校验
> 作用：为第二个对象 `maglev-create-spec` 提供可直接落地的 rollout 规格。

## 1. 试点对象

当前对象：

- `maglev-create-spec`

推荐目标名：

- `spec-designer`

## 2. 为什么第二个做它

1. 它位于主流程中段，是 rename 对协作链影响最典型的对象
2. 它已经完成 spec pipeline 物理内部化，不再被外部显性模块链拖住
3. 它能验证 `requirement-convergence -> 主流程对象` 这类 relation 迁移是否稳定

## 3. 本对象的最小执行面

至少需要同步处理：

1. `.agents/skills/maglev-create-spec/` -> `.agents/skills/spec-designer/`
2. `.agents/private-catalog.yaml` 中：
   - `name: 'maglev-create-spec'` -> `name: 'spec-designer'`
   - `path: '.agents/skills/maglev-create-spec/'` -> `path: '.agents/skills/spec-designer/'`
3. catalog relation target 中所有主引用：
   - `requirement-convergence -> maglev-create-spec` -> `requirement-convergence -> spec-designer`
4. 该对象的 `runtime_name_status`
   - 最后再切到 `canonical_name_active`

## 4. 明确不处理

本对象 rollout 当前不处理：

1. `.agents/workflows/create-spec.md` 文件名
2. 历史设计文档中的旧运行名记录
3. `_internal/spec-pipeline/` 的模块命名

## 5. 执行前最小校验

执行前应先确认：

1. `.agents/private-catalog.yaml` 中不存在其它 relation target 的二义性写法
2. `requirement-convergence` 当前的现役 handoff 只把 `maglev-create-spec` 作为正式下游对象
3. `.agents/workflows/create-spec.md` 已明确是兼容入口，而不是未来物理 rename 的同轮目标

## 6. 执行后最小验证

### A. 目录层

1. `.agents/skills/spec-designer/` 存在
2. `.agents/skills/maglev-create-spec/` 已退出运行面

### B. catalog 层

1. `spec-designer` 已存在于 catalog
2. `maglev-create-spec` 不再作为 active skill name 存在
3. `requirement-convergence` 的 active relation target 已指向 `spec-designer`

### C. 口径层

1. workflow 仍可通过 `create-spec.md` 作为兼容入口存在
2. 文档中的双写说明仍保持“正式动作名优先，旧运行名兼容”
3. 不再残留 active path 或 active relation target 指向 `maglev-create-spec`

## 7. 暂停条件

若出现以下任一情况，应暂停：

1. `requirement-convergence` relation target 已改，但 skill 目录或 catalog path 未同步
2. `runtime_name_status` 被提前切换
3. `.agents/` 现役路径中仍存在旧 skill 目录引用

## 8. 当前结论

`maglev-create-spec -> spec-designer` 已完成第二轮真实 execution，并通过最小运行面校验：

1. 新 skill 目录已存在，旧目录已退出运行面
2. catalog 中的 `name`、`path`、`requirement-convergence relation target` 已完成同步切换
3. 兼容 workflow `/create-spec` 仍保留
4. 当前仓库中不再残留 active relation target、active path 或 active skill name 指向 `maglev-create-spec`

后续若继续推进，下一步应复用本轮模板，进入第三个对象 `maglev-quick-dev`。
