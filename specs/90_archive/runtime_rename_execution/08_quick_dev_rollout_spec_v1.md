# quick-dev rollout spec v1

> 状态：已执行并完成最小校验
> 作用：为第三个对象 `maglev-quick-dev` 提供可直接落地的 rollout 规格。

## 1. 试点对象

当前对象：

- `maglev-quick-dev`

推荐目标名：

- `context-implementer`

## 2. 为什么第三个做它

1. 它处在主流程实施段，能验证 `方案设计 -> 实施` 的主链迁移是否自洽
2. 它与 `spec-designer` 已有直接路径引用，适合在第二轮完成后承接
3. 它的 rename 能为最后的 `maglev-cross-validate` 提供更完整的主流程动作名链条

## 3. 本对象的最小执行面

至少需要同步处理：

1. `.agents/skills/maglev-quick-dev/` -> `.agents/skills/context-implementer/`
2. `.agents/private-catalog.yaml` 中：
   - `name: 'maglev-quick-dev'` -> `name: 'context-implementer'`
   - `path: '.agents/skills/maglev-quick-dev/'` -> `path: '.agents/skills/context-implementer/'`
3. catalog relation target 中所有主引用：
   - `entry-router -> maglev-quick-dev` -> `entry-router -> context-implementer`
4. 该对象的 `runtime_name_status`
   - 最后再切到 `canonical_name_active`

## 4. 明确不处理

本对象 rollout 当前不处理：

1. `.agents/workflows/quick-dev.md` 文件名
2. 历史文档中的旧运行名记录
3. 代码实现与对抗性审查步骤的内部写作风格

## 5. 执行前最小校验

执行前应先确认：

1. `entry-router` 当前对实施段的现役路由只指向 `maglev-quick-dev`
2. `spec-designer` 与 `quick-dev` 间不存在旧 path 的硬编码残留
3. `.agents/workflows/quick-dev.md` 已明确是兼容入口，而不是未来物理 rename 的同轮目标

## 6. 执行后最小验证

### A. 目录层

1. `.agents/skills/context-implementer/` 存在
2. `.agents/skills/maglev-quick-dev/` 已退出运行面

### B. catalog 层

1. `context-implementer` 已存在于 catalog
2. `maglev-quick-dev` 不再作为 active skill name 存在
3. `entry-router` 的 active relation target 已指向 `context-implementer`

### C. 口径层

1. workflow 仍可通过 `quick-dev.md` 作为兼容入口存在
2. 文档中的双写说明仍保持“正式动作名优先，旧运行名兼容”
3. 不再残留 active path 或 active relation target 指向 `maglev-quick-dev`

## 7. 暂停条件

若出现以下任一情况，应暂停：

1. `entry-router` relation target 已改，但 skill 目录或 catalog path 未同步
2. `runtime_name_status` 被提前切换
3. `.agents/` 现役路径中仍存在旧 skill 目录引用

## 8. 当前结论

`maglev-quick-dev -> context-implementer` 已完成第三轮真实 execution，并通过最小运行面校验：

1. 新 skill 目录已存在，旧目录已退出运行面
2. catalog 中的 `name`、`path`、`entry-router relation target` 已完成同步切换
3. 兼容 workflow `/quick-dev` 仍保留
4. 当前仓库中不再残留 active relation target、active path 或 active skill name 指向 `maglev-quick-dev`

后续若继续推进，下一步应复用本轮模板，进入第四个对象 `maglev-cross-validate`。
