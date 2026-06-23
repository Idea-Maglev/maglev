# cross-validate rollout spec v1

> 状态：已执行并完成最小校验
> 作用：为第四个对象 `maglev-cross-validate` 提供可直接落地的 rollout 规格。

## 1. 试点对象

当前对象：

- `maglev-cross-validate`

推荐目标名：

- `integrated-validator`

## 2. 为什么最后做它

1. 它位于主流程末段，同时承接三面质量层协作，影响面最大
2. 前三轮主流程对象完成后，才能更稳定地验证质量层 relation 的整体迁移
3. 它作为最后一个对象，适合承接 execution 主题的封板判断

## 3. 本对象的最小执行面

至少需要同步处理：

1. `.agents/skills/maglev-cross-validate/` -> `.agents/skills/integrated-validator/`
2. `.agents/private-catalog.yaml` 中：
   - `name: 'maglev-cross-validate'` -> `name: 'integrated-validator'`
   - `path: '.agents/skills/maglev-cross-validate/'` -> `path: '.agents/skills/integrated-validator/'`
3. catalog relation target 中所有主引用：
   - 三个质量面指向 `maglev-cross-validate` 的 relation target
   - 其它主流程或结晶层对 `maglev-cross-validate` 的直接调用
4. 该对象的 `runtime_name_status`
   - 最后再切到 `canonical_name_active`

## 4. 明确不处理

本对象 rollout 当前不处理：

1. `.agents/workflows/validate-all.md` 文件名
2. 历史文档中的旧运行名记录
3. 质量层三面的对象名本身

## 5. 执行前最小校验

执行前应先确认：

1. `.agents/private-catalog.yaml` 中三面质量层 relation target 已全部列清
2. `validate-all.md` 已明确是兼容入口，而不是未来物理 rename 的同轮目标
3. 不存在仍依赖旧 skill 目录路径的 active 文档或 workflow

## 6. 执行后最小验证

### A. 目录层

1. `.agents/skills/integrated-validator/` 存在
2. `.agents/skills/maglev-cross-validate/` 已退出运行面

### B. catalog 层

1. `integrated-validator` 已存在于 catalog
2. `maglev-cross-validate` 不再作为 active skill name 存在
3. 质量层三面的 active relation target 已全部指向 `integrated-validator`

### C. 口径层

1. workflow 仍可通过 `validate-all.md` 作为兼容入口存在
2. 文档中的双写说明仍保持“正式动作名优先，旧运行名兼容”
3. 不再残留 active path 或 active relation target 指向 `maglev-cross-validate`

## 7. 暂停条件

若出现以下任一情况，应暂停：

1. catalog 的 relation target 仅部分切换
2. `runtime_name_status` 被提前切换
3. `.agents/` 现役路径中仍存在旧 skill 目录引用

## 8. 当前结论

`maglev-cross-validate -> integrated-validator` 已完成第四轮真实 execution，并通过最小运行面校验：

1. 新 skill 目录已存在，旧目录已退出运行面
2. catalog 中的 `name`、`path`、四处主要 relation target 已完成同步切换
3. 兼容 workflow `/validate-all` 仍保留
4. 当前仓库中不再残留 active relation target、active path 或 active skill name 指向 `maglev-cross-validate`

后续若继续推进，应直接进入主流程四对象 rename execution 的封板判断。
