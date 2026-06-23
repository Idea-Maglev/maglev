# 逆向产物评分表

## 目标
用于快速评估一份逆向产物是否合格、当前大致处于 `Lean / Standard / Deep` 哪一档，以及还缺什么。

## 使用方式
- 每项按 `0 / 1 / 2` 打分
- `0`: 缺失或基本不可用
- `1`: 有内容，但明显不完整或不稳定
- `2`: 完整、清晰、可直接使用

## 一、骨架完整度 (满分 12)

| 维度 | 说明 | 分数 |
|---|---|---:|
| 功能地图 | 能看懂模块边界、入口和主要能力 | 0-2 |
| 数据结构 | 有核心结构和字段说明 | 0-2 |
| 架构图 | 有关键组件和调用方向 | 0-2 |
| 主流程图 | 至少有一条主链路流程 | 0-2 |
| 文件结构 | 知道关键文件在哪里 | 0-2 |
| Implementation Trace | 关键结论能追到代码 | 0-2 |

## 二、内容可信度 (满分 10)

| 维度 | 说明 | 分数 |
|---|---|---:|
| Evidence Summary | 明确区分 FACT / INFERENCE / UNKNOWN | 0-2 |
| Unknowns / Quests | 未知项被显式登记 | 0-2 |
| Cross-Layer Mapping | 前后端/接口/存储映射清晰 | 0-2 |
| 数据字典质量 | 字段含义、约束、用途清楚 | 0-2 |
| 一致性 | 文本、图、数据结构之间不打架 | 0-2 |

## 三、工程可用性 (满分 12)

| 维度 | 说明 | 分数 |
|---|---|---:|
| User Story / AC | 至少能支持后续理解或验证 | 0-2 |
| State Machine | 有状态变化或等价描述 | 0-2 |
| Dependency Topology | 上下游依赖与边界清晰 | 0-2 |
| Test Mapping | 知道有没有测试、差在哪 | 0-2 |
| Change Risk | 明确改动风险和脆弱点 | 0-2 |
| 可交接性 | 新人接手后知道下一步去哪看 | 0-2 |

## 四、深度能力 (Deep 档专用，满分 10)

| 维度 | 说明 | 分数 |
|---|---|---:|
| Runtime Behavior | 并发、异步、缓存、原子性讲清 | 0-2 |
| Error Taxonomy | 错误来源和传播路径清晰 | 0-2 |
| Security Surface | 权限、隔离、敏感数据边界清晰 | 0-2 |
| RMM Scorecard | 有成熟度评估和缺口总结 | 0-2 |
| Expert Review Queue | 高价值未知问题已系统登记 | 0-2 |

## 五、档位判断

### Lean 合格线
- 骨架完整度 >= 8
- 内容可信度 >= 5
- 且没有“架构图/主流程图/数据结构/trace”四项同时缺两项以上

### Standard 合格线
- 满足 Lean
- 工程可用性 >= 7
- 至少具备：
  - 数据字典
  - State Machine 或等价状态描述
  - Change Risk
  - Test Mapping

### Deep 合格线
- 满足 Standard
- 深度能力 >= 6
- 至少具备：
  - Runtime Behavior
  - Security Surface
  - RMM Scorecard
  - Expert Review Queue

## 六、红线问题

出现以下任一情况，直接判为“不合格”：

1. 没有数据结构
2. 没有架构图
3. 没有主流程图
4. 没有 Implementation Trace
5. 没有 Unknowns / Quests，但明显存在证据不足区域
6. 大量结论没有证据来源，明显依赖脑补

## 七、快速评语模板

### 1. Lean 合格
```markdown
结论: 当前结果达到 Lean 合格线，已可用于快速理解模块。
短板: 仍缺少 {数据字典/状态机/风险分析}。
建议: 如要支持交接或改动分析，至少补到 Standard。
```

### 2. Standard 合格
```markdown
结论: 当前结果达到 Standard 合格线，已可用于交接和改动前分析。
短板: 仍缺少 {运行时行为/安全面/评分卡}。
建议: 若目标是高风险重构，继续补到 Deep。
```

### 3. Deep 合格
```markdown
结论: 当前结果达到 Deep 合格线，已可用于高风险设计讨论和重构前评估。
短板: {列出仍未闭环的问题}。
建议: 优先处理 Expert Review Queue 中的高风险问题。
```

## 八、建议打分流程

1. 先看 Index 和 Design，判断骨架完整度
2. 再看 Requirements 和 Evidence，判断可信度
3. 再看 State / Test / Risk，判断工程可用性
4. 如果有 Deep 内容，再看 Runtime / Security / RMM / Queue
5. 最后给出档位结论和下一步建议
