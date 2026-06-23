# Phase 3 红队对抗反思（Docs Archival Methodology）

> **Created**: 2026-04-25
> **Status**: active
> **Segment**: 70_retrospective
> **Context**: `specs/20_evolution/active/docs_knowledge_archival_methodology/` Phase 1+2+3 完成后做的对抗性审查
> **Trigger**: 用户明确要求"做一轮反思对抗 看看现在整体需求有没有问题"

---

## 1. 为什么留这份反思

Phase 1+2+3 一鼓作气完成 11 commits 上 master 后，用户没接受"全部完成"的乐观汇报，直接触发对抗性审查。事后看，这一轮审查产出的批判**比执行本身更有价值**——它揭示了"看似全绿"背后的系统性盲区。

如果不独立沉淀这份方法学：
- Phase 4-6 实施时会重复发现同样问题
- 下一次大型重组工作（其他模块 / 其他范式）丢掉这套审查模板
- 红队作为一种工程能力在团队层面失传

## 2. 触发条件

红队审查的触发不需要"出错"作为理由，**进展顺利本身就是触发条件**：

- 多 commit 一气呵成（11 个）
- 验证全绿（exit 0）
- 用户主动要求"反思"
- 涉及生命周期边界（Phase 跨度）

任一条件命中就应主动启动审查，不要等"问题暴露"。

## 3. 审查框架（按严重度三级）

### S 级（严重）— 设计承诺与实施落地之间的断层

| ID | 模式 | 本案例 |
|----|------|--------|
| S1 | "设计文档说 X，但实施只做了 Y（或没做）" | schema 增量章节定义在 02_design.md §3.3，但 index-schema.md 没有对应字段；新字段无 ground truth |
| S2 | "验证通过 ≠ 验证充分" | `verify --level local` 实际只校验 root 单文件，5 个 check 全针对 INDEX.md；浅绿被误读为深绿 |
| S3 | "工具承诺存在，但从未真跑过" | `index_update.py` 全程未跑，手写 INDEX.md 与脚本生成格式可能冲突，round-trip 未验证 |

### M 级（中等）— 决策可逆但缺验证

| ID | 模式 | 本案例 |
|----|------|--------|
| M1 | "批量决策靠启发式，未抽样复审" | 28 个文件按文件名分类进 60_case，未做内容 vs 位段语义的一致性抽检 |
| M2 | "新旧角色并存，职责未划清" | README.md（人编辑）vs INDEX.md（脚本管理）共存 thinking/ 根目录，用户路径未收口 |
| M3 | "新关系建立，旧引用未扫" | catalog 加新边但旧 `maglev-librarian` 引用散落各处未清理 |

### L 级（轻度）— 待办积压

| ID | 模式 | 本案例 |
|----|------|--------|
| L1 | "覆盖不全（部分子模块缺产物）" | 9 个 segment 中 4 个老 dir（00/10/20/90）没补 collection-scope INDEX.md |
| L2 | "计划写但没写" | `module_checks/thinking.py` 设计承诺 segment / room_name / linked_to 校验，全未实现 |
| L3 | "状态文档与现实脱节" | spec status.md 仍标"03_plan ⏳"，但 Phase 1+2+3 都已上 master |

### 哲学层（最尖锐）— 价值层质疑

> **Q**：把 36 个文件 git mv 进位段，完成的是"位段化"还是"目录改名"？

设计中位段是认知地图的"房间"。但执行时：
- 没建立任何文件之间的 `linked_to` 关系
- 位段与思考者真实回访路径未对位
- 段间连接（02_design §2.1）是空的

**结论**：当前完成的是"目录骨架 + 文件分类"。F8 一日不实现，整套位段化在认知层就是个伪命题——只是用九个数字给文件夹换分组。

这个质疑的价值：
- 防止把"目录干净"误认为"知识结构升级"
- 提醒下游 Phase 5（认知地图）才是兑现承诺的关键里程碑

## 4. 这套框架可复用吗？

可以——它是一个通用的"批后审查模板"：

```
对一段刚完成的工作做对抗审查时，依次问：

1. S 级：设计承诺与实施之间是否有断层？
   - 设计文档中是否有字段/能力/约束我没落实？
   - 验证通过的检查项是否真覆盖了我宣称的范围？
   - 工具是否真跑过？还是只跑了相邻工具？

2. M 级：批量决策与新旧并存是否留了未审查面？
   - 启发式分类是否抽样过？
   - 新建对象的旧引用是否扫过？
   - 角色重叠是否收口？

3. L 级：覆盖完整度与状态文档同步度？
   - 子模块是否全覆盖？
   - 计划项是否全实现？
   - 状态文档是否反映现实？

4. 哲学层：表面完成是否对应价值兑现？
   - 我做的是"形"还是"神"？
   - 兑现承诺的关键里程碑是否还远？
```

后续重组工作（其他模块、其他范式、新会话）应**主动**走这个模板，不依赖外部"被要求反思"。

## 5. 本案例的修复决策

红队报告产出 9 项问题 + 1 个哲学质疑后，用户选择"先修 S1 + L3"：
- ✅ S1 已修：commit `4ceff3f` — index-schema.md §6 落地
- ✅ L3 已修：commit `4ceff3f` — status.md 同步

其余项（S2/S3/M1-M3/L1/L2 + 哲学层 F8）滚到下会话或后续 Phase。

**这个"分级 + 选择性修复"本身也是一种纪律**：不要被"全部修完"的洁癖绑架，按价值密度分批解。

## 6. 关联文档

- `specs/20_evolution/active/docs_knowledge_archival_methodology/02_design.md` — 设计承诺源
- `specs/20_evolution/active/docs_knowledge_archival_methodology/status.md` — 红队摘要
- `docs/thinking/70_retrospective/docs_segment_classification_heuristics.md` — A8 配套
- `.agents/skills/index-librarian/protocol/index-schema.md` §6 — S1 修复
