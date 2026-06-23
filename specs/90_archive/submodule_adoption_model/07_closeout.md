# Closeout

## 1. 主题结论

`submodule_adoption_model` 这一轮已经完成当前目标范围内的结构收口。

本轮形成的稳定结论是：

1. submodule 不应直接成为新的默认接入方式
2. 当前结论固定为 `Optional / Recommended`
3. `init` 已支持 `clone / submodule` 双模式登记
4. `update` 已支持 submodule 状态观察与解释
5. pointer sync 当前明确为“非默认自动行为”

## 2. 本轮已完成

### A. 决策层

1. 明确回读并承接了旧 `Workstation Mode` / submodule 反对理由
2. 正式输出 `Optional / Recommended` 决策

### B. 实现层

1. installer 已支持 `clone / submodule` 双模式
2. `.maglev/config.json` 已开始记录 `management_mode`
3. `repository_map.md` 已开始表达 `管理方式`
4. `update` 已开始观察已登记 submodule 的工作区状态

### C. 用户说明层

1. `maglev_init_manual.md` 已补双模式说明
2. `maglev_update_manual.md` 已补 submodule 状态观察说明

## 3. 本轮明确不做

本轮不进入：

1. pointer 自动同步
2. `git submodule update --remote` 自动执行
3. 自动切换 submodule 分支
4. 自动提交 wrapper 项目里的 pointer 变化

这些能力如果要继续推进，应单独开新主题处理。

## 4. 当前生效口径

当前仓库在 submodule 问题上的生效口径是：

1. `clone` 仍是默认接入模式
2. `submodule` 已是正式可选模式
3. `update` 默认只观察和解释 submodule 状态
4. 常规 `update` 不自动推进业务仓库 revision

## 5. 后续承接建议

如果后续仍要继续推进，建议另开一个更窄的新主题：

- `submodule_pointer_sync_execution`

该主题至少需要单独回答：

1. 是否采用显式 flag
2. 是否允许更新触及业务仓库 revision
3. 本地未提交改动时如何阻断
4. pointer 变化是否需要显式提交提醒

## 6. 封板判断

按当前目标看，这条主题已经具备封板条件：

1. 决策已形成
2. 首轮实现已落地
3. 用户手册已同步
4. 高风险后续项已被明确隔离
