# 扩展持续迭代

本指南面向维护已发布 Maglev Extension Pack 的作者。目标不是把扩展更新变成“复制文件后再试一次”，而是让每次变更都保留可验证的意图、兼容性判断和发布证据。

## 职责边界

| 位置 | 持有内容 |
|---|---|
| Maglev | `extension-evolver` 流程、协议、确定性 CLI 和消费者管理入口 |
| 扩展 source | `extension.yaml`、能力资产、用户 README、`maintenance/` 维护记录 |
| Registry | 可发现条目、source URL、发布 ref/tag 与推荐治理 |
| 消费者项目 | `.maglev/extensions.sources.yaml`、`.maglev/extensions.lock` 与已安装资产 |

`maintenance/` 是 source 维护资产，不应写入 `extension.yaml` 的 `contents`，因此不会被安装到消费者项目。

## 一次迭代的最小闭环

1. 读取 manifest、Registry entry 和已有消费者的 lock，明确基线 commit。
2. 评估变更是否影响安装路径、skill id、Slot、默认启用、运行时要求或已有输出。
3. 修改 pack 与 README；同步 manifest version 和 compatibility。
4. 依据 `extension-evolver` 的维护记录模板新增 `maintenance/records/` 条目。
5. 在隔离项目执行 `maglev-extension check` 与 `test-install`。
6. 对 Git source 执行 `search`、`install`、`update`、`remove`；记录两个 resolved commit。
7. 确认 Registry ref/tag 已发布。未推送的本地 ref 只能标记为 `ready_to_publish`。

## 兼容性判定

| 变化 | 处理 |
|---|---|
| 修正文档、引用或不改变安装结果的实现 | patch；记录无需迁移的依据 |
| 新增资产或可选能力 | minor；验证 update 后的新增结果 |
| 移动/删除受管资产、改 skill id/Slot/默认启用、增加必需运行时 | breaking；提供迁移或停止发布 |

## 维护记录为什么是发布条件

Registry 的 `ref` 只能说明从哪里取内容，不能解释为什么本次改动可升级。维护记录补齐以下不可由 lock 推导的事实：变更意图、受影响消费者、兼容性结论、验证命令、Registry commit 和 asset commit。缺少其中任一项时，不应宣称该扩展具备可持续迭代能力。
