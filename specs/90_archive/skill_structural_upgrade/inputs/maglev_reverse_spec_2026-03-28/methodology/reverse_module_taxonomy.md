# 逆向模块分类法

## 目标
把常见模块按行为特征分型，给每一类定义默认逆向重点、默认图形产物和高频风险点。

这样做的目的不是限制逆向，而是减少每次从零决定“这个模块到底该补什么”的成本。

## 使用方式

做逆向前，先判断目标模块最接近哪一类：

1. `CRUD / Query 型`
2. `State Machine 型`
3. `Event / Realtime 型`
4. `Agent / Workflow 型`
5. `Config / Preference 型`
6. `Asset / Knowledge 型`
7. `Bridge / Integration 型`

如果一个模块同时落在多类里，选一个主类，再补一个副类。

例如：
- Memory Center: `Asset / Knowledge 型` + `CRUD / Query 型`
- Tasks Management: `State Machine 型` + `Event / Realtime 型`

---

## 1. CRUD / Query 型

### 典型特征
- 以创建、查询、更新、删除为主
- 主要复杂度在数据结构、查询条件、筛选和分页
- 前端通常是表单、列表、详情页

### 默认必须补
- Feature Map
- Data Structure Map
- Data Dictionary
- Main Query / Write Flow
- File Structure
- Implementation Trace

### 默认建议画图
- 架构图
- 查询流程图
- 写入流程图

### 高频风险
- 前后端字段漂移
- 分页/排序/筛选参数不一致
- 删除和更新约束未闭环
- 列表结构与详情结构不一致

### 最小合格档位
- `Lean`: 可快速理解
- `Standard`: 更常见，适合交接

---

## 2. State Machine 型

### 典型特征
- 模块核心是状态变化
- 存在 `status / phase / step / confirm_status` 等字段
- 用户最关心“现在在哪一步”“为什么失败”“还能不能继续”

### 默认必须补
- State Machine
- State-to-UI Mapping
- Transition Rules
- Hidden States / Implicit States
- Change Risk

### 默认建议画图
- 状态机图
- 主流程图
- 状态更新流程图

### 高频风险
- 新增状态后 UI 没同步
- 隐式状态没被记录
- 状态跳转规则分散在多处
- 删除/重试/回滚条件和规格不一致

### 最小合格档位
- `Standard`

---

## 3. Event / Realtime 型

### 典型特征
- 依赖 WebSocket、事件总线、SSE、消息推送
- 数据不是只靠接口拉取，还靠订阅驱动
- 复杂度在事件格式、时序、兼容和最终一致性

### 默认必须补
- Event Contract
- Event Flow
- Realtime Update Mapping
- 订阅主题或频道规则
- 事件新旧格式兼容策略

### 默认建议画图
- 事件流时序图
- 实时更新流程图
- 依赖拓扑图

### 高频风险
- 事件格式漂移
- 消息丢失或重复
- 前端状态合并错误
- 新旧事件协议兼容层未收口

### 最小合格档位
- `Standard`
- 涉及核心主链路时建议 `Deep`

---

## 4. Agent / Workflow 型

### 典型特征
- 模块核心是任务规划、执行链路、多步骤流转
- 常见对象包括 `plan / task / executor / confirmation / interrupt`
- 风险集中在状态链、幂等、异步中断和工具执行副作用

### 默认必须补
- Workflow Map
- Step Definition
- State Machine
- Runtime Behavior
- Error Taxonomy
- Change Risk

### 默认建议画图
- 主工作流图
- 执行时序图
- 中断/失败分支图

### 高频风险
- 计划与执行态混淆
- 中断和重试不闭环
- 执行结果落库/落状态不一致
- 工具副作用缺补偿

### 最小合格档位
- `Deep`

---

## 5. Config / Preference 型

### 典型特征
- 模块核心是配置、开关、偏好或个性化设定
- 数据量不大，但影响范围广
- 复杂度在默认值、环境差异、优先级和覆盖关系

### 默认必须补
- Config Matrix
- Data Dictionary
- Priority / Override Rule
- Scope Definition

### 默认建议画图
- 配置生效路径图
- 配置优先级图

### 高频风险
- 默认值与线上实际值不一致
- 多来源配置覆盖顺序不清
- 单用户配置和全局配置混淆

### 最小合格档位
- `Standard`

---

## 6. Asset / Knowledge 型

### 典型特征
- 模块核心在于“承载内容”
- 可能是 Prompt、Memory、Dataset、Evaluator、知识条目、素材等
- 复杂度在数据结构、检索方式、版本与语义边界

### 默认必须补
- Data Structure Map
- Data Dictionary
- Retrieval / Query Flow
- Domain Model
- Asset Mapping

### 默认建议画图
- 检索流程图
- 资产映射图
- 结构图

### 高频风险
- 检索结果结构漂移
- 资产版本和代码依赖关系不透明
- 主存储与索引存储边界不清
- 字段语义不稳定

### 最小合格档位
- `Standard`
- 涉及平台资产治理时建议 `Deep`

---

## 7. Bridge / Integration 型

### 典型特征
- 模块本身不产生太多业务对象，而是连接两个或多个系统
- 典型场景包括 API 代理、同步器、适配器、桥接服务
- 复杂度在协议转换、字段映射、失败补偿、上下游契约

### 默认必须补
- Dependency Topology
- Cross-System Mapping
- Error Taxonomy
- Configuration Matrix
- Runtime Behavior

### 默认建议画图
- 上下游依赖图
- 协议转换流程图
- 失败/重试流程图

### 高频风险
- 上下游契约漂移
- 映射逻辑散落
- 重试和幂等边界不清
- 环境配置差异导致行为不同

### 最小合格档位
- `Deep`

---

## 模块判型速查表

| 模块类型 | 默认档位 | 默认重点 |
|---|---|---|
| CRUD / Query 型 | Standard | 数据结构、查询写入流程、字段约束 |
| State Machine 型 | Standard | 状态机、状态映射、变更风险 |
| Event / Realtime 型 | Standard / Deep | 事件契约、实时更新流程、兼容性 |
| Agent / Workflow 型 | Deep | 工作流、运行时、错误与副作用 |
| Config / Preference 型 | Standard | 配置矩阵、优先级、生效范围 |
| Asset / Knowledge 型 | Standard | 数据结构、检索流程、资产映射 |
| Bridge / Integration 型 | Deep | 上下游依赖、协议映射、补偿与幂等 |

---

## 判型建议

### 问自己 3 个问题
1. 这个模块最核心的是“数据对象”“状态变化”还是“系统连接”？
2. 用户最关心的是“查到什么”“现在到哪一步”还是“为什么系统之间不一致”？
3. 如果这个模块出问题，最常见的症状会是“字段错”“状态错”还是“时序/集成错”？

根据这三个问题，通常就能快速判型。

---

## 当前样例映射

### Memory Center
- 主类: `Asset / Knowledge 型`
- 副类: `CRUD / Query 型`

### Tasks Management
- 主类: `State Machine 型`
- 副类: `Event / Realtime 型`

---

## 推荐下一步

后续如果继续扩展逆向方法，建议为每一类模块再补一份：
- 最小章节清单
- 最小图清单
- 最小评分项

这样就可以形成“判型 -> 模板 -> 产物 -> 评分 -> 评审”的完整闭环。
