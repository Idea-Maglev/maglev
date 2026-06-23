# Requirements

## 1. 路由要求

entry-router 的路由表必须覆盖"后段闭环"场景：

1. 当用户意图是"收尾/归档/做完了"时，必须路由到正确的后段技能
2. 路由到 crystallization 还是 knowledge-check 必须有明确判据
3. 不得将"归档"直接理解为文件系统操作

## 2. 边界要求

knowledge-check 和 crystallization 必须各自声明：

1. 正面触发条件（"什么场景来找我"）
2. 反面排除条件（"什么场景去找对方"）
3. 两者同时需要时的执行顺序

## 3. 防护要求

必须在可被 AI 助手读取的位置（AGENTS.md 或等效位置）明确声明：

1. `20_evolution → 90_archive` 直接搬运是反模式
2. 正确的归档操作是三步：提取结论到 10_reality → 收口 active → 可选归档过程记录
3. 核心不变量：只看 `10_reality` 就能了解项目当前状态

## 4. 关系图要求

private-catalog.yaml 中的主流程关系链必须补齐：

1. spec-designer → context-implementer（当前缺失）
2. context-implementer → integrated-validator（当前缺失）
3. integrated-validator → crystallization（当前缺失）
4. knowledge-check → crystallization 的时序关系（当前只标注 complements）

## 5. 验收标准

1. AI 助手收到"归档"请求时，不再直接执行 `mv 20_evolution/x 90_archive/x`
2. AI 助手能区分 knowledge-check 和 crystallization 的使用场景
3. 主流程 5 个核心技能之间的 handoff 在 private-catalog 中 100% 记录
4. entry-router 可以路由到后段闭环技能
