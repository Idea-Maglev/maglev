# submodule adoption model

> 作用：评估并定义 Maglev 化项目中“代码仓库是否改用 Git Submodule 管理”的新接入模型，避免在旧 `git clone` 语义上直接硬改。

## 主入口

- `00_intent.md`
- `00_context.md`
- `01_requirements.md`
- `02_design.md`
- `03_plan.md`
- `04_decision_v1.md`
- `05_implementation_spec_v1.md`
- `06_pointer_sync_strategy_v1.md`
- `07_closeout.md`

## 当前说明

本主题不是在局部实现里把 `git clone` 替换成 `git submodule add`。

本主题处理的是更高一层的接入模型变更：

1. 这是否应成为新的默认接入方式
2. 是否推翻旧的 `Workstation Mode` 决策
3. 会影响哪些运行面、文档和 Reality 事实

当前首版决策已经形成：

- 结论不是 `Reject`
- 也不是直接 `Default`
- 当前定为 `Optional / Recommended`

当前首轮实现也已开始落地：

1. installer 已支持 `clone / submodule` 双模式登记
2. `.maglev/config.json` 已开始记录 `management_mode`
3. `repository_map.md` 已开始表达仓库管理方式
4. `update` 已开始观察已登记的 submodule 状态，但仍不做自动同步

当前已进入封板准备：

- 本轮主题已形成 closeout
- 后续如需继续推进 pointer sync，应另开新主题
