# runtime rename migration Design

## 1. 设计目标

本主题不是执行 rename，而是把 rename migration 变成一份可控、可分阶段推进的执行对象。

## 2. 影响面分层

### A. 运行入口层

包括：

- `.agents/workflows/standup.md`
- `.agents/workflows/create-spec.md`
- `.agents/workflows/quick-dev.md`
- `.agents/workflows/validate-all.md`

判断：

- 这是物理 rename 的直接阻塞面
- 必须先决定 workflow 是否跟随改名

### B. 协作路由层

包括：

- `entry-router`
- `requirement-convergence`
- `skill-squadron`
- 其他直接以对象名协作的运行对象

判断：

- 这是最容易造成内部断层的部分
- 应先做双写口径统一，再讨论物理改名

### C. 治理与分发层

包括：

- `.agents/private-catalog.yaml`
- Reality runtime 说明
- capability snapshot

判断：

- 这是名称治理的一致性基线
- 应优先形成单一迁移规则，避免 catalog 与文档各写各的

### D. 对外说明层

包括：

- `docs/marketing/assets/`
- 用户指南、案例与对外表达文档

判断：

- 这是影响范围最大但执行优先级可后置的一层
- 更适合先双写统一，再逐轮清理

## 3. 推荐推进顺序

1. 先盘清运行入口层与协作路由层
2. 再固定 catalog / Reality / capability snapshot 的迁移规则
3. 最后才处理营销与对外说明层

## 4. 当前结论

当前最稳的做法不是立刻 rename，而是先形成：

1. 一份影响面 inventory
2. 一份迁移 checklist
3. 一组分层优先级

只有这些稳定后，才值得新开真正的 rename execution 主题。
