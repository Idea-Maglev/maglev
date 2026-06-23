# spec pipeline 物理内部化重构

> 作用：承接 `skill结构性升级` 封板后遗留的下一轮主题，负责把 spec pipeline 从“口径内部化”推进到“物理内部化”。
> 状态：已完成

上层归档总览可见：

- [specs archive index](../README.md)

## 主入口

- `02_design.md`
- `04_stage_summary.md`
- `05_closeout.md`

## 当前说明

这轮主题不再重判 spec pipeline 是否应该独立存在。

本轮已处理的对象是：

- `maglev-spec-ingest`
- `maglev-spec-draft`
- `maglev-spec-crystallize`
- `maglev-validate-spec-context`

它们都已被判定为：

> `spec-designer` / `maglev-reverse-spec` 的内部模块链

本主题已将这个判断落实到物理文件结构与引用关系上。

当前样板性入口文档已收敛，保留设计、阶段总结与 closeout 三个主阅读面。
