---
description: 逆向现状重建的入口深入分析
---

# 入口深入分析

## 目标

从入口注册和入口实现中确认用户或外部系统如何进入当前能力，并把入口连接到后续页面、
接口、任务、事件或数据。这里是直接阅读，不是运行扫描器。

## 在阶段 A 中的使用条件

本文件不是独立阶段。只有入口地图已经标出需要深入确认的入口时，阶段 A 才按需使用本文件；
它消费入口地图，补充入口到实际处理过程的定位，不重新建立入口清单，也不决定模块边界。

## 适用入口

- 页面路由；
- 接口路由和处理函数；
- 任务、调度器和消息消费者；
- 命令和子命令注册；
- 软件开发工具包公开方法；
- 事件生产和订阅；
- 数据对象及其生命周期入口。

## 阅读方式

1. 找到入口注册位置；
2. 回到实际处理函数或页面文件；
3. 记录入口名称、路径、参数和返回结果；
4. 继续追踪直接调用的实现、数据和测试；
5. 为每条记录附相对路径和锚点；
6. 无法确认的内容标为未知，不用名称或目录补齐。

## 输出

```yaml
entry_analysis:
  - name: <入口名称>
    entry_type: ui | api | job | cli | sdk | event | data
    path_or_signal: <路径、命令、事件名或结构线索>
    implementation_refs:
      - <相对路径#锚点>
    related_sources:
      intent:
        - <相对路径#锚点>
      verification:
        - <相对路径#锚点>
    knowledge_status: established | unknown | not_established | not_applicable
    evidence_sufficiency: supported | partial | missing | blocked
    basis: <判断依据>
```

入口分析的结果仍然只是阶段 A 的入口事实。模块边界、公共内容和未归类项仍由语义审阅和
人工裁决形成。
