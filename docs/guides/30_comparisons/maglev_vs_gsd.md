# Maglev vs GSD: 深度对比与定位边界

> 更新时间：2026-04-01
> 目的：把本轮分散在会话中的对比结论统一沉淀到对比目录，便于后续归档、复盘和持续迭代。

## 1. 结论先行

两者在机制上高度同构，但在系统中心上明显分化：

1. GSD 更像高自动化执行引擎，优先解决把事快速做完。
2. Maglev 更像工程治理操作系统，优先解决长期协作不乱与资产可持续演进。

因此它们不是简单替代关系，而是重心不同的系统。

## 2. 对比范围与边界

本文件只比较以下维度：

1. 生命周期编排
2. 上下文与状态管理
3. 执行与验证机制
4. 组织治理与长期沉淀
5. 分发与用户第一小时体验

不在本轮范围：

1. 逐行源码审计
2. 商业化策略评判
3. 单一场景下绝对优劣排名

## 3. 核心同构点

| 维度       | GSD                             | Maglev                                   | 结论 |
| :--------- | :------------------------------ | :--------------------------------------- | :--- |
| 方法主线   | spec/plan/execute/verify        | requirement/spec/implement/validate      | 同构 |
| 上下文工程 | 强调 fresh context 与 artifacts | 强调结构化上下文与阶段分流               | 同构 |
| 状态持久化 | `.planning/` 文件化状态         | specs/docs/issues/skills 协同沉淀        | 同构 |
| 多代理编排 | orchestrator + subagents        | entry-router + skill orchestration       | 同构 |
| 质量闭环   | plan checker + verifier + UAT   | audit/review/test + integrated-validator | 同构 |

## 4. 关键差异点

### 4.1 系统中心

1. GSD：命令流水线中心，强调低摩擦自动推进。
2. Maglev：治理对象中心，强调分层语义、边界纪律和可追溯演进。

### 4.2 执行偏好

1. GSD：wave 并行 + 原子提交，执行引擎可感知度高。
2. Maglev：受控实施 + 对抗性审查，治理约束表达更强。

### 4.3 验证取向

1. GSD：流程内验证产品化程度高，命令驱动强。
2. Maglev：全域一致性验证更强，强调 requirements ↔ spec ↔ code ↔ tests 对齐。

### 4.4 长期资产化

1. GSD：偏项目级执行状态沉淀。
2. Maglev：偏组织级知识资产与生命周期分层沉淀（现实/演进/归档）。

## 5. 结构化评分（本轮评估）

| 维度             | 分值（0-100） | 说明                       |
| :--------------- | :------------ | :------------------------- |
| 方法同构度       | 85            | 核心链路相近               |
| 执行机制同构度   | 82            | 计划-执行-验证闭环高度一致 |
| 治理语义同构度   | 68            | Maglev 在组织治理语义更强  |
| 首小时体验同构度 | 60            | GSD 的命令化体验更直给     |
| 长期资产化同构度 | 78            | 两者都重沉淀，但重心不同   |
| 综合指数         | 74.6          | 中高同构，非同类复制       |

## 6. 对 Maglev 的启发

1. 保持治理深度优势，同时增强首小时可见价值。
2. 在对外口径上承认同构，避免无效对立。
3. 把治理收益指标化，减少抽象叙事。

建议优先补三件事：

1. 提供 30 分钟最小闭环演示路径。
2. 输出治理收益指标面板（偏差率、返工率、验证前置率、跨会话恢复成本）。
3. 固化公开对比口径，避免被拉入单纯执行效率赛道。

## 7. 对外口径建议

可复用表达：

Maglev 与 GSD 都在解决 AI 交付可靠性。GSD 更像高自动化执行引擎，Maglev 更像团队级协作治理系统。前者优先把事做完，后者优先长期不乱、可持续演进。

## 8. 证据来源

Maglev 仓库内依据：

1. [README.md](../../../README.md)
2. [Maglev 当前定位](../../../internal Reality/positioning.md)
3. [Maglev 当前事实入口](../../../internal Reality/README.md)
4. [协作生命周期](../../../internal Reality/collaboration-lifecycle/README.md)
5. [治理与质量](../../../internal Reality/governance-quality/README.md)

GSD 公开依据：

1. https://github.com/gsd-build/get-shit-done/blob/main/README.zh-CN.md
2. https://raw.githubusercontent.com/gsd-build/get-shit-done/main/docs/USER-GUIDE.md
3. https://raw.githubusercontent.com/gsd-build/get-shit-done/main/docs/ARCHITECTURE.md
