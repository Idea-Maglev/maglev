# Reverse Skill 通用性审查清单

> 用途：审查 `maglev-reverse-spec` 这类逆向 skill 是否仍然保持“Maglev 兼容，但业务中立”。

## 1. 结论档位

审查结果建议分为三档：

- `G1: Generic`
  - 方法论通用
  - 允许保留 Maglev 产物结构
  - 不携带当前业务项目的领域词汇、模块名、表名、接口名
- `G2: Maglev-Compatible but Example-Biased`
  - 方法论仍通用
  - 没有业务污染
  - 但示例明显偏某类技术栈或常见项目范式
- `G3: Project-Fitted`
  - skill 中出现当前项目特有领域对象、模块、表、服务、接口或目录假设
  - 会误导后续在其他项目中的复用

## 2. 第一层审查：业务污染检查

### 2.1 不应出现的内容
- 当前项目特有模块名
- 当前项目特有业务术语
- 当前项目中的表名、索引名、Topic 名、队列名
- 当前项目中的接口路径、RPC 名称、事件名
- 当前项目中的服务名、SDK 名、配置中心键名
- 当前项目中的仓库路径假设，但不属于 Maglev 规范本身

### 2.2 红线判断
若满足任一项，直接判为 `G3: Project-Fitted`：

- 示例直接使用当前项目的真实模块名
- 模板中直接出现当前项目的真实接口
- 原则文件把当前项目经验写成普适真理
- 输出要求隐含“只有当前项目才成立”的前提

## 3. 第二层审查：允许的 Maglev 拟合

以下内容允许保留，不算业务污染：

- `specs/10_reality/reverse_{slug}/`
- `.maglev/temp`
- `maglev-spec-draft`
- `maglev-spec-crystallize`
- `validation_report.md`
- `Implementation Trace`
- `Lean / Standard / Deep`
- `RMM / Expert Review Queue`

判断原则：
- 如果它是 Maglev 的协议、目录、工作流或交付标准，可以保留。
- 如果它是某个业务项目自己的实现细节，不应固化进 skill。

## 4. 第三层审查：示例偏置检查

这类问题不会直接变成业务污染，但会降低通用性。

### 4.1 常见偏置
- 所有示例都像 Web CRUD 项目
- 所有示例都默认前后端分离
- 所有调用链都固定成 `Controller -> Service -> Repository -> Entity`
- 所有页面都默认 `Vue / React`
- 所有协议都默认 REST，不覆盖 Event / CLI / Batch / Stream

### 4.2 判定方式
- 若只是示例偏技术栈，但未引用当前项目真实对象，判为 `G2`
- 若步骤设计本身把这种范式写成硬约束，应降级处理并考虑修订 skill

## 5. 第四层审查：方法论通用性检查

一个合格的通用逆向 skill，至少应支持：

- 多入口
  - UI-First
  - API-First
  - Event-First
  - Data-First
  - CLI-First
- 多证据等级
  - `FACT`
  - `INFERENCE`
  - `UNKNOWN`
  - `QUEST`
- 多产物档位
  - `Lean`
  - `Standard`
  - `Deep`
- 多结构对象
  - Entity
  - DTO
  - Schema
  - ViewModel
  - Store State
  - Event Payload
  - Cache Object

如果 skill 只能适用于一种项目形态，应降级判为 `G2` 或更低。

## 6. 第五层审查：逆向骨架完整性检查

无论项目类型如何，skill 至少应能引导产出这些骨架层内容：

- Feature Map
- Evidence Summary
- Data Structure Map
- Data Dictionary
- Architecture Overview
- Main Flow
- File Structure
- Implementation Trace
- Unknowns / Quests

如果这些内容缺失，说明不是“项目拟合”，而是“逆向能力不足”。

## 7. 第六层审查：运行时与风险能力检查

当 skill 声称支持 `Standard / Deep` 时，应进一步检查是否覆盖：

- State Machine
- Dependency Topology
- Runtime Behavior
- Error Taxonomy
- Security Surface
- Configuration Matrix
- Observability Map
- Change Risk
- RMM Scorecard
- Expert Review Queue

如果只会描述静态结构，不足以支撑高风险逆向。

## 8. 第七层审查：语言与措辞污染检查

应避免以下写法：

- “不再只逆向单个功能”
- “结合当前仓库经验”
- “针对本项目主线”
- “当前系统的核心目标是……”
- “本仓库主要围绕……”

这些话即使不出现具体模块名，也会把某个项目上下文偷偷带进 skill。

更好的写法是：

- “当目标是单模块理解时……”
- “当目标是跨模块整合时……”
- “若项目存在多入口或多上下文源……”

## 9. 快速打分表

总分 20 分，建议这样使用：

- 17-20: `G1 Generic`
- 13-16: `G2 Maglev-Compatible but Example-Biased`
- 0-12: `G3 Project-Fitted`

### 评分项

| 项目 | 分值 | 判断标准 |
|---|---:|---|
| 无当前项目业务术语 | 4 | 未出现真实业务模块、表、接口、配置项 |
| Maglev 拟合边界清晰 | 3 | 保留 Maglev 规范，但未把业务实现写进协议 |
| 示例中性程度 | 3 | 示例不明显偏向某个真实项目 |
| 多入口支持 | 2 | 不只支持 Page-First |
| 数据结构能力 | 2 | 明确把数据结构作为独立逆向对象 |
| 骨架完整性 | 2 | 至少覆盖图、流程、结构、trace |
| 风险与运行时能力 | 2 | `Standard / Deep` 支持合理 |
| 语言无上下文污染 | 2 | 没有“当前仓库/本项目主线”式措辞 |

## 10. 审查结论模板

```markdown
# Reverse Skill Genericity Review

## 结论
- Rating: G1 / G2 / G3
- Score: {score}/20
- Summary: {一句话结论}

## 发现
- [F1] ...
- [F2] ...

## 保留项
- 哪些属于允许的 Maglev 拟合

## 风险项
- 哪些地方仍可能误导为项目拟合

## 建议动作
1. ...
2. ...
3. ...
```

## 11. 当前这套 skill 的建议用法

如果你后面继续迭代 `maglev-reverse-spec`，建议每次改完都过一遍这份清单，特别是：

- 是否新加了某个真实项目里的案例
- 是否把某次逆向经验写成了默认规则
- 是否把“样例”偷偷升级成了“协议”
- 是否因为补强某个场景而削弱了通用性

这能帮助 skill 保持：

- `Maglev-compatible`
- `Business-neutral`
- `Reverse-capability-complete`
