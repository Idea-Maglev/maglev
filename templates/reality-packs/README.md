---
title: Reality Template Pack Registry
status: guarded
---

# Reality Template Pack Registry

`registry.yaml` 是 Reality 模板包的唯一登记入口。核心逆向、验证和结晶能力只能消费登记且获准
使用的模板包，不能从目录名称、历史产物或样本推断模板。

当前登记并使用的软件研发模板是 `software-development/v2`。它是当前项目的来源模板资产；
核心能力可以消费其登记内容，但不得把其中的页面名称、目录细节或项目事实硬编码进能力层。

与该模板相关的实验适配器、实验 Schema 和专属测试不属于模板本身，仍按处置账本保留在
[`specs/90_archive/abandoned/`](../../specs/90_archive/abandoned/) 中，不能作为当前执行入口或生产证据。

替换或迁移当前模板必须先经过用户确认、兼容性审查和回滚设计；不能通过归档或清空 Registry
隐式改变当前使用的模板。
