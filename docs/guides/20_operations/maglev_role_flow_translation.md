# Maglev 角色与流程翻译

> 目标：帮助传统项目团队把 Maglev 的对象名翻译成自己熟悉的协作语言，而不是先去记一堆 skill 名。

## 1. 先记阶段，不先记名字

如果你来自传统项目流程，理解 Maglev 最稳的方式不是先记 skill 名，而是先记阶段：

1. 先看现状
2. 再收需求
3. 再做方案
4. 再推进实施
5. 最后做验证

对应到 Maglev 主流程，就是：

| 传统协作里的理解 | Maglev 当前对象 |
| :--- | :--- |
| 先把项目现状、风险和下一步对齐 | `现状同步（reality-sync，兼容入口：/standup）` |
| 先把边界和目标收清 | `requirement-convergence` |
| 把需求整理成可执行方案 | `方案设计（spec-designer，兼容入口：/create-spec）` |
| 按方案推进实现和自检 | `上下文实施（context-implementer，兼容入口：/quick-dev）` |
| 把需求、方案、代码、测试重新拉回同一条线上检查 | `综合验证（integrated-validator，兼容入口：/validate-all）` |

所以你完全可以先按流程理解，再慢慢记对象名。

## 2. `entry-router` 怎么理解最不容易跑偏

`entry-router` 不是方案设计师，也不是实现者。

它更像：

- 研发流程前台
- 项目分诊台
- 判断“当前问题应该流到哪个阶段”的入口

一句话记法：

> 它先帮你判断，现在该先看现状、收需求、做方案、直接实施，还是进入验证。

### 对不同角色来说，它像什么

对产品经理：

- 像需求分诊入口
- 帮你判断现在缺的是背景、边界还是方案

对技术负责人：

- 像研发流转台
- 帮你避免任务直接跳进实现，导致阶段错位

对开发：

- 像“先别急着写，先确认现在该进哪一步”的入口

对测试：

- 像“确认当前是不是已经到了可验证阶段”的前置判断

## 3. `maglev-tutor` 怎么理解最容易用起来

`maglev-tutor` 也不适合按“教学机器人”去理解。

它更像：

- 新成员入场引导员
- 传统项目角色理解 Maglev 的翻译层
- 帮人把 skill 名翻成协作语言的说明对象

它最有价值的地方，不是教你背概念，而是帮你回答：

- 我是产品，现在该从哪里进入？
- 我是开发，现在该先读方案还是已经可以写代码？
- 我是测试，现在什么时候该开始介入？
- 我是技术负责人，怎么让团队按同一条流程协作？

## 4. 不同角色最适合怎么进入

### 产品经理

最稳的理解方式：

- 先把 Maglev 当成一套“让需求别漂移”的流程

通常最相关的对象是：

1. `entry-router`
2. `requirement-convergence`
3. `方案设计（spec-designer）`

### 开发

最稳的理解方式：

- 先把 Maglev 当成一套“别一上来就误判任务”的流程

通常最相关的对象是：

1. `现状同步（reality-sync）`
2. `方案设计（spec-designer）`
3. `上下文实施（context-implementer）`

### 测试

最稳的理解方式：

- 先把 Maglev 当成一套“让验证不再最后才补”的流程

通常最相关的对象是：

1. `requirement-convergence`
2. `方案设计（spec-designer）`
3. `综合验证（integrated-validator）`

### 技术负责人

最稳的理解方式：

- 先把 Maglev 当成一套“让团队在同一条主流程上协作”的流程

通常最相关的对象是：

1. `entry-router`
2. `现状同步（reality-sync）`
3. `综合验证（integrated-validator）`

## 5. 一个最小顺序

如果你不想记太多名字，可以先只记这条：

1. 不确定从哪开始，就先进 `entry-router`
2. 刚开工或上下文混乱，就先做 `现状同步（reality-sync）`
3. 边界不稳，就先做 `requirement-convergence`
4. 已经能进入方案，就去 `方案设计（spec-designer）`
5. 已经能进入实施，就去 `上下文实施（context-implementer）`
6. 要交付前收口，就去 `综合验证（integrated-validator）`

## 6. 接下来读什么

如果你想继续把入口关系看清，可以接着读：

1. [多入口使用说明](./maglev_entrypoints.md)
2. [用户导航手册](./user_manual_atlas.md)
3. [面向传统团队的 kickoff 引导](../00_start/maglev_traditional_team_kickoff.md)
