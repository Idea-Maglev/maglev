# Reverse Recheck Entry Guide

> 用途：当第一轮 reverse 已完成后，指导你第二轮应从哪个入口复核，以判断结果是否稳定。

## 核心原则

第二轮复核不要沿着第一轮完全相同的入口再走一遍。

目标是：

- 换一个观察角度
- 验证主结论是否仍成立
- 找出第一轮容易漏掉的层

## 通用选择规则

### 如果第一轮是 UI-First
第二轮优先选：
- API-First
- Data-First

为什么：
- UI 很容易让人只看到交互，不一定看清契约和真实数据承载体

### 如果第一轮是 API-First
第二轮优先选：
- Data-First
- Event-First
- UI-First

为什么：
- API 容易让人停留在接口层，不一定看清页面状态和运行时副作用

### 如果第一轮是 Data-First
第二轮优先选：
- API-First
- UI-First

为什么：
- 数据结构能看清对象，但不一定能看清流程、交互和实际触发条件

### 如果第一轮是 Event-First
第二轮优先选：
- Data-First
- API-First

为什么：
- 事件流能暴露异步链路，但不一定能解释对象语义和同步入口

### 如果第一轮是 CLI-First / Job-First
第二轮优先选：
- Data-First
- Event-First
- API-First

为什么：
- 脚本和任务入口容易看到执行链，但不一定能看清上下游契约

## 按模块类型推荐复核入口

### 1. CRUD / Query 型

第一轮常见入口：
- UI-First
- API-First

第二轮推荐：
- Data-First

重点核对：
- 字段语义
- 请求/响应结构
- 分页、筛选、排序参数
- DTO 与实体映射

### 2. State Machine 型

第一轮常见入口：
- API-First
- UI-First

第二轮推荐：
- State / Event 入口
- Data-First

重点核对：
- 状态枚举
- 转移条件
- 非法状态
- 副作用是否跟状态切换一致

### 3. Event / Realtime 型

第一轮常见入口：
- Event-First

第二轮推荐：
- Data-First
- UI-First

重点核对：
- 事件载荷
- 消费后状态变化
- 前端展示状态与事件语义是否一致

### 4. Agent / Workflow 型

第一轮常见入口：
- Workflow / Orchestrator

第二轮推荐：
- Data-First
- Tool / Step 入口

重点核对：
- 输入输出上下文
- 中间状态
- 子步骤职责边界
- 重试、回滚、中断点

### 5. Config / Preference 型

第一轮常见入口：
- Data-First
- UI-First

第二轮推荐：
- Runtime / API 入口

重点核对：
- 配置覆盖顺序
- 默认值
- 环境差异
- 配置生效时机

### 6. Asset / Knowledge 型

第一轮常见入口：
- Data-First
- UI-First

第二轮推荐：
- Query / Retrieval 入口
- Event / Update 入口

重点核对：
- 检索结果结构
- 更新链路
- 缓存与索引一致性
- 展示模型与存储模型映射

### 7. Bridge / Integration 型

第一轮常见入口：
- API-First
- Event-First

第二轮推荐：
- Config-First
- Data-First

重点核对：
- 外部契约
- 映射逻辑
- 错误传播
- 重试 / 补偿 / 幂等

## 如何判断第二轮复核是否有效

第二轮复核应至少回答其中 2 个问题：

- 第一轮里最核心的对象，第二轮是否还能识别为同一个对象？
- 第一轮的主流程，第二轮是否还能还原为相同主线？
- 第一轮标出的风险点，第二轮是否仍然成立？
- 第一轮的 Unknowns，第二轮是否能收敛一部分？

如果第二轮只是重复确认已经知道的内容，而没有提供新的校验角度，那这轮复核价值不高。

## 复核后的结论判断

### 稳定
- 主对象不变
- 主流程不变
- 风险点基本不变
- Unknowns 有收敛或至少未扩大

### 部分稳定
- 主对象不变
- 但状态机、契约或运行时行为出现补充修正

### 不稳定
- 主对象变了
- 主流程变了
- 风险判断大改
- 第一轮大量“事实”被降级

## 快速建议

如果你来不及想太多，直接用这个简化规则：

- UI 第一轮 -> Data 第二轮
- API 第一轮 -> UI 或 Data 第二轮
- Event 第一轮 -> Data 第二轮
- Data 第一轮 -> API 第二轮
- Workflow 第一轮 -> Data 第二轮

通常这样已经足够把大多数不稳定结果筛出来。
