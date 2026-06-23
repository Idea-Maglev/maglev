# skill结构性升级 `maglev-create-prd` 吸收后删除方案 v2

> 状态：进行中
> 作用：明确 `maglev-create-prd` 已被 `requirement-convergence` 吸收后的删除口径、执行顺序与现役口径切换方式。

## 1. 当前判断

`maglev-create-prd` 不属于 `5+3` 主干骨架中的稳定一级对象，且当前目标已经明确为删除，而不是继续保留。

本轮纠偏后的判断是：

1. 前段仍需要“稳定需求产物输出”来抑制漂移并提升下游可消费性
2. 但这个问题应由 `requirement-convergence` 自身承接，而不是继续维持独立 `maglev-create-prd`
3. 只要吸收动作完成，独立 skill 的继续存在就不再有结构价值

因此，当前正确对象定义应变成：

> `requirement-convergence` 内部的稳定需求产物输出模式，而不是独立现役 skill。

## 2. 当前删除而非保留的原因

如果继续让 `maglev-create-prd` 作为并列 skill 存在，会持续制造四个问题：

1. 与 `requirement-convergence` 并列，导致前段再次出现两个“需求入口”
2. 与 `maglev-create-spec` 相邻，继续制造“需求收敛 / 方案设计”边界回混
3. 让用户误以为 PRD 生成就是 Maglev 前段主流程本体，而不是前段中的一种需求产物输出模式
4. 让“生成 PRD”覆盖真正的问题定义，反而忽视了产物是否稳定、是否可被下游充分消费

所以当前正确方向不是“继续过渡保留”，而是：

- 先吸收
- 再删除
- 仅把能力保留在 `requirement-convergence` 内部

## 3. 当前定位

从这一版开始，当前现役定位明确为：

- 现役对象：`requirement-convergence`
- 内部模式：稳定需求产物输出
- 被删除对象：`maglev-create-prd`
- 已吸收职责：将前段需求输入整理成稳定、低漂移、可被下游充分消费的需求产物

## 4. 删除方案

### 阶段 1：能力吸收

当前先完成：

- 由 `requirement-convergence` 直接承担稳定需求产物输出
- 用 `references/prd-output-contract.md` 约束输出契约
- 去掉所有把 `maglev-create-prd` 当现役下游的路由和说明

### 阶段 2：口径收口

现役口径统一改成：

1. 用户先进入 `entry-router`
2. 前段稳定需求产物输出属于 `requirement-convergence`
3. `maglev-create-prd` 不再作为一级入口或可路由下游存在

触发稳定需求产物输出的条件应是：

1. 当前需求若只停留在口头或松散总结，会继续漂移
2. 下游对象需要一个可反复引用、可评审、可验证的稳定需求产物
3. 仅靠最小 handoff 无法满足当前目标节点的消费强度

### 阶段 3：对象删除

当以下条件满足时，`maglev-create-prd` 可进入删除：

1. `requirement-convergence` 已显式支持 PRD 文档输出模式
2. 现役入口和说明不再把 `maglev-create-prd` 当独立前段对象推荐
3. 当前稳定需求产物输出契约已经可以被后续对象直接消费

到那时应执行：

- 删除 `.agents/workflows/create-prd.md`
- 删除 `.agents/skills/maglev-create-prd/`
- 在历史决策与 Scout 归档中保留客观痕迹

## 5. 当前最小执行动作

这轮先完成现役收口，再进入实体删除：

1. 去掉 `requirement-convergence` 对 `maglev-create-prd` 的现役路由
2. 把稳定需求产物输出改成 `requirement-convergence` 内部模式
3. 在主线文档中把 `maglev-create-prd` 从“保留待并入”改成“吸收后删除”
4. 删除独立 skill 与 workflow 实体

当前已完成的证据链：

- `03av_maglev_create_prd_scout_parse_v1.md`
- `03aw_maglev_create_prd_scout_search_v1.md`
- `03ax_maglev_create_prd_scout_evaluation_v1.md`
- `03ay_maglev_create_prd_scout_adaptation_spec_v1.md`

说明：

- 上述 `archive/scout` 产物保留为历史决策与证据记录
- 其中“暂不删除”的阶段性表述，已被本方案 v2 覆盖，不再代表现役口径

## 6. 当前结论

当前最稳的结论是：

- 前段“稳定需求产物输出”这个问题仍然存在
- 但它已经不需要独立 `maglev-create-prd` 对象继续承接
- 当前应由 `requirement-convergence` 直接承担该能力，并删除旧对象

因此，后续正确动作不是“继续并列保留”，而是：

> 把稳定需求产物输出彻底内化进 `requirement-convergence`，并删除 `maglev-create-prd` 的现役 skill 与 workflow。
