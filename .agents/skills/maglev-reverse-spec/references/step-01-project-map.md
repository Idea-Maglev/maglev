---
description: 逆向现状重建的入口与功能地图
---

# 入口与功能地图

## 目标

把静态证据地图整理成用户可理解的阅读导航，帮助智能体从稳定入口继续深入。功能地图不是
模块清单，也不负责决定业务边界。

## 在阶段 A 中的位置

本文件是入口地图的唯一整理位置。它只消费
`step-01-evidence-acquisition.md` 产出的来源覆盖和定位种子，形成供后续阅读使用的入口导航；
不重新盘点来源，不生成模块，也不进行边界审阅。

## 每个入口至少记录

```yaml
features:
  - name: <功能或入口名称>
    entry_type: ui | api | job | cli | sdk | event | data
    path_or_signal: <路径、命令、事件名或结构线索>
    source_refs:
      - <相对路径或基线提交>
    knowledge_status: established | unknown | not_established | not_applicable
    evidence_sufficiency: supported | partial | missing | blocked
    basis: <判断依据>
```

入口还没有经过原文核对时，知识状态不能标为 `established`；证据不足时保留
`unknown`/`not_established` 与 `missing`，没有读取许可时保留 `blocked`。

## 入口整理方式

- 页面明显主导时，优先列用户可见页面和用户操作；
- 接口服务优先列接口资源和处理入口；
- 异步系统优先列任务、消费者、生产者和事件；
- 命令行或开发工具优先列命令、参数和输出；
- 数据系统优先列核心对象和生命周期；
- 入口太多时先标出主要阅读起点，不要求一次穷尽。

整理只决定阅读起点。需要确认具体处理过程时，再使用
`step-01b-router-analysis.md`；存在页面时才使用 `step-02-page-analysis.md`。模块、公共内容
和未归类项必须由阶段 A 总协议的直接阅读形成，并交给人工审阅。

## 失败处理

- 入口分散时保留入口列表，不强行合并；
- 入口名称无法确认时可使用技术占位名，但必须标为推断；
- 没有稳定入口时保留未知，并写明还需要什么材料；
- 不用目录结构、数量或命名替代入口证据。
