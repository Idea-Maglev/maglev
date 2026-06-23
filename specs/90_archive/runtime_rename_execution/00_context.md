# runtime rename execution Context

## 已稳定前提

来自 [../runtime_rename_execution_preflight/README.md](../runtime_rename_execution_preflight/README.md) 的稳定前提：

1. 迁移形态已决定为 `skill-only`
2. relation-level 的 catalog checklist 已形成
3. 现役文档与协作面已基本完成双写统一

## 当前关键问题

虽然现在已经足够进入 execution 主题，但真正动手前仍需要把以下问题写成明确规格：

1. 四个对象的实际执行顺序
2. 每一步执行后的验证动作
3. 什么情况下应暂停或回滚，而不是继续推进

不补这层规格，后续真正执行时仍会面临：

- 改到一半才发现影响面未封口
- relation graph 被局部改坏
- catalog 与目录状态短暂失真
