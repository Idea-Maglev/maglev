# 02 Design — Docs Knowledge Archival Methodology

> **TP 主导**。在 01_requirements.md 基线上，决策 K1-K7 并给出工程蓝图。
> **路径 C 决策**（2026-04-24）：新建 `index-protocol` + `index-librarian`，废弃 `maglev-librarian`。

---

## 1. 关键决策（解 K1-K7）

### K1 索引脚本路径 → `.agents/skills/index-librarian/protocol/scripts/`

**决策**：放 `_internal/`，不放 `scripts/`。

**理由**：
- 与 my-smart-workbench 对位（双仓概念一致）
- `_internal/` 表达"内部协议层，非用户可见 skill"
- `scripts/` 是 Maglev 项目级工具（如 `maglev_release.py`），不混在一起
- 分发时通过 `parse-visibility` 识别为 internal，不暴露给安装方

### K2 librarian 演进 → 新建 `index-librarian` + 废弃 `maglev-librarian`

> 🔄 **范围修订（2026-04-28）**：本决策仅覆盖 Track B（docs/）。Track A（specs/）与 Track C（仓库入口）的同等替代由 `runtime_distribute_project_index_protocol` 主题完成；`maglev-librarian` 的真正退役时序由该主题 Step 1-5 控制（先撤回 deprecated → 补齐三 Track → 行为对等性验证通过 → 物理废弃）。本段决策正文保持原状作历史溯源。

**决策**：路径 C，对位 workbench 命名。

**理由**：
- `maglev-librarian` 是 AI-driven 范式（旧），与新协议范式（脚本权威 + AI 编排）哲学冲突，无法平滑升级
- workbench 已用 `index-librarian` 名字 ~2 个月稳定，命名对位降低跨仓认知成本
- 旧 skill 走 deprecated 路径（不立删），catalog `relations: replaced_by: index-librarian`

### K3 重组 git 历史保留 → 强制 `git mv`

**决策**：所有重组动作必须 `git mv`，禁止 `rm + new`。分批 commit（每批 ≤ 10 文件），message 模板化。

**理由**：保留 blame 可追溯，符合 AC-F7-1。

### K4 子目录抽离阈值 → N=4

**决策**：单位段顶层文件 ≥ 4 时触发"是否升级为子目录"的人工评估（非强制）。

**理由**：低于 4 时子目录开销大于收益；≥ 4 时索引可读性下降。

### K5 `docs/thinking/90_archive/` 与 `specs/90_archive/` 边界 → 独立二轨

**决策**：保持二轨，不合并。

**理由**：
- `specs/90_archive/` 是**主题/需求级**归档（带完整生命周期产物：00-05 + status）
- `docs/thinking/90_archive/` 是**单文档/灵感级**归档（独立思考片段）
- 颗粒度不同，强行合并会污染语义
- 但二者都纳入 `index-protocol` registry 治理（统一协议，独立模块）

### K6 编号位段是否允许扩展位 → 严格 10 间距

**决策**：位段间距固定为 10（00/10/20/.../90）。位段内编号自由（30_xxx, 32_xxx, 35_xxx）。

**理由**：跨段连号会破坏语义边界（K6 风险）；位段内自由保留灵活度。

### K7 frontmatter schema 严格度 → 分级强制

**决策**：
- **强制字段**：`type / scope / segment / status / created / updated`
- **推荐字段**：`linked_to / superseded_by / cross_segments / room_name`
- **可选字段**：`authors / tags / draft`

**理由**：避免门槛过高劝退贡献者，但保证关键字段可校验。

---

## 2. 位段语义表（场景驱动版）

> **设计原则**：每个位段必须能回答 4 个问题——为什么存在 / 承载什么内容 / 谁会读 / 什么时机读。如果某段无法清晰回答，说明该段语义不成立，应删除或合并。

### 位段 00 — 元厅（Meta Hall）

- **为什么存在**：Maglev 自身的运作规则、术语、自查表，是"操作系统级"参考，不属于任何具体主题。
- **承载什么**：术语表、贡献者自查清单、命名规范、跨主题元规则、文档维护规则本身。
- **谁会读**：所有贡献者（包括 AI agent）。
- **什么时机读**：入职第一周通读；写新文档前查"该用什么命名"；困惑时查"这条规则在哪定义的"。
- **典型示例**：`00_meta/glossary.md`、`00_meta/contributor_checklist.md`。
- **不放什么**：具体设计、对标、复盘——这些有专属位段。

### 位段 10 — 批判间（Critique Room）

- **为什么存在**：把"已知错误、反模式、走过的弯路"显式记录，避免后人重蹈，是项目的"免疫记忆"。
- **承载什么**：反模式案例、被废弃的设计思路、坑点警告、"为什么不该这样做"。
- **谁会读**：准备做新设计的 TP；review 同类提案的 reviewer；新人 onboarding。
- **什么时机读**：方案设计前查"是否撞过类似坑"；review 提案时查"这个反模式有没有被警示过"。
- **典型示例**：`10_critique/component_level_spec_decomposition_antipattern.md`。
- **不放什么**：单纯吐槽 / 情绪化抱怨——必须含可复用的"避免规则"。

### 位段 20 — 架构间（Architecture Room）

- **为什么存在**：主要架构决策、骨架级抽象、分层模式的设计与说明，是项目"骨头"的描述。
- **承载什么**：分层抽象、目录结构骨架、能力对象关系图、协议层设计。
- **谁会读**：新加入者建立全局理解；TP 设计涉及结构性变更时；外部审视者评估架构。
- **什么时机读**：onboarding 第一周；启动跨多 skill 改造前；与外部解释"Maglev 长什么样"时。
- **典型示例**：`20_architecture/skill_lifecycle_layering.md`、`20_architecture/governance_loop_overview.md`。
- **不放什么**：具体功能设计——那属于 `specs/`；对标分析——属位段 50。

### 位段 30 — 哲学殿（Philosophy Hall）

- **为什么存在**：项目存在的根本理念、第一性原理、设计哲学方程，回答"为什么这么做"而非"怎么做"。
- **承载什么**：方程式（如 `M = R + E + C`）、信念陈述、设计取舍背后的价值观、协议宣言。
- **谁会读**：决策者面临两难时；外部受众理解项目"灵魂"时；新人想看"这群人到底在想什么"时。
- **什么时机读**：跨范式重大决策前；写对外宣讲材料时；思考"这条路对不对"时。
- **典型示例**：`30_philosophy_maglev_equation.md`、`35_accuracy_and_correction_protocol.md`、`36_bidirectional_context_protocol.md`。
- **不放什么**：具体实施方案；对标文章——属位段 50。

### 位段 40 — 论文阁（Paper Loft）

- **为什么存在**：把项目沉淀为可对外学术化输出的素材，区别于内部文档的"严谨化、可发表化"产出。
- **承载什么**：论文草稿、可投稿的方法论提炼、学术对话回应、benchmark 设计。
- **谁会读**：参与对外学术交流的核心成员；想了解"项目对外定位"的访客。
- **什么时机读**：被邀请写文章/分享时；准备对外发言时；与学术界对话前。
- **典型示例**：`40_paper_potential.md`。
- **不放什么**：日常思考片段；非对外结构的内部讨论。

### 位段 50 — 对标厅（Alignment Hall）

- **为什么存在**：与外部框架/产品/理念的横向对比，**辨清自身定位**，避免闭门造车。
- **承载什么**：vs 类型文档（vs OpenAI / vs Hermes / vs Kuaishou Paradigm 等）、机会点分析、互补路径设计。
- **谁会读**：决策是否吸纳外部能力时；与外部受众沟通"Maglev 与 X 有何不同"时；做战略选型时。
- **什么时机读**：发现新对手/新参考时（本会话 52 就是这个场景）；面对"为什么不直接用 X"质疑时；制定演进方向前。
- **典型示例**：`50_maglev_vs_openai_frontier.md`、`51_maglev_vs_kuaishou_paradigm.md`、`52_maglev_vs_hermes_agent.md`。
- **不放什么**：单纯的工具评测；不带"Maglev 视角"的纯转述。

### 位段 60 — 案例馆（Case Gallery）

- **为什么存在**：具体场景下的实践证据，回答"这套理念在真实项目里怎么落地"，让抽象规则有血有肉。
- **承载什么**：单需求的真实落地复盘（区别于位段 70 的阶段性总结）、典型场景的端到端走读、"我们用 Maglev 做了 X"。
- **谁会读**：新接入项目的 owner；评估 Maglev 是否适合自己场景的潜在采纳者；写宣讲材料的人。
- **什么时机读**：决策"我的场景能套这个范式吗"；setup 自己的项目前；编写对外案例库时。
- **典型示例**：（当前缺失，待孵化——可从 specs 归档主题中提炼）。
- **不放什么**：单条 thinking；尚未结案的进行中观察。

### 位段 70 — 复盘室（Retrospective Room）

- **为什么存在**：阶段性回看（季度/版本/重大事件后）的整理性产出，提炼"我们这段做了什么、什么有效、什么不奏效"。
- **承载什么**：版本回看、重大决策事后分析、范式演进里程碑回顾、年度盘点。
- **谁会读**：决策者制定下一阶段方向时；外部受众理解"项目走到哪了"时；新成员快速建立时间感时。
- **什么时机读**：版本发布后 review；季度规划前；写履历/年报时。
- **典型示例**：`2026-02-03-maglev-fortification/`、`distribution_iteration_closeout_2026_03_19.md`。
- **不放什么**：单点思考；横向对标——属位段 50。

### 位段 80 — 预留

- **为什么存在**：保留一段空位用于未来语义需求（如 80 = "教程"、"实验报告"），避免现在过早占段。
- **现状**：暂不启用。

### 位段 90 — 归档库（Archive）

- **为什么存在**：让"过时但仍有追溯价值"的内容有去处，区别于"删除"。归档保留 git 可追溯，但不污染现状视图。
- **承载什么**：被新文档显式覆盖的旧版（带 `superseded_by:`）、长期未引用的低价值产出、自然遗忘条件触发的归档。
- **谁会读**：追溯历史决策的考古者；想知道"为什么当年这么做"的人；写复盘时取证。
- **什么时机读**：极少；git blame 触发；写复盘需要历史证据时。
- **典型示例**：`90_archive/old_protocol_v1.md`。
- **不放什么**：从未被引用过且无追溯价值的草稿——直接 `git rm`。

---

## 2.1 段间连接（认知地图边）

| 高频共读对 | 触发场景 |
|-----------|----------|
| 30 哲学 ↔ 50 对标 | "Maglev 的哲学如何区别于 X" |
| 20 架构 ↔ 60 案例 | "这个架构在真实场景如何工作" |
| 10 批判 ↔ 70 复盘 | "复盘时发现的反模式归到哪" |
| 00 元 ↔ 任何位段 | "用什么术语描述这件事" |

这些高频边由 `linked_to:` frontmatter 显式声明，由 `index_update.py` 聚合成 Mermaid 认知地图（见 F8 AC-F8-1）。

---

## 3. 协议层设计（`index-librarian/protocol/`）

### 3.1 目录结构（搬运 + 特化）

```
.agents/skills/index-librarian/protocol/
├── README.md                          # 协议说明
├── registry.yaml                      # Maglev 模块清单（特化）
├── index-schema.md                    # 搬运 + 增 LPM/cognitive map 字段
├── index-verify.md                    # 校验规则（搬运 + 增 F8 知识图谱校验）
├── index-update.md                    # 更新规则（搬运）
└── scripts/
    ├── index_init.py                  # 搬运（~243 行）
    ├── index_scan.py                  # 搬运（~203 行）
    ├── index_verify.py                # 搬运 + 增 cognitive map 校验（~600+ 行）
    ├── index_update.py                # 搬运 + 增 knowledge_graph.json 聚合（~500+ 行）
    ├── common/                        # 共用工具
    ├── module_checks/                 # 模块特定 check（如 thinking/ 的 segment 校验）
    └── templates/                     # INDEX.md 模板
```

### 3.2 Registry（首批纳管）

```yaml
protocol_version: "1.0"

modules:
  - name: thinking
    root_path: docs/thinking/
    root_index: docs/thinking/INDEX.md
    entity_type: thinking-note
    management_level: managed
    description: "思考与决策日志（位段 + 隐喻名）"

  - name: releases
    root_path: docs/releases/
    root_index: docs/releases/index.md
    entity_type: release-note
    management_level: managed
    description: "版本发布归档"

  - name: guides
    root_path: docs/guides/
    root_index: docs/guides/INDEX.md
    entity_type: guide
    management_level: managed
    description: "操作手册与开发指南"

  # 后续可扩展：specs / contributors 等
```

### 3.3 Schema 增量（相对 workbench）

新增字段（仅 thinking 模块）：

```yaml
# Root frontmatter (docs/thinking/INDEX.md)
segments:                              # 位段语义表
  - id: "30_philosophy"
    room_name: "哲学殿"
    description: "..."
cognitive_map:                          # F8 认知地图
  enabled: true
  output_path: "docs/_meta/knowledge_graph.json"

# Leaf frontmatter (docs/thinking/30_xxx.md)
segment: "30_philosophy"               # 必填
status: "draft|active|crystallized|archived"  # F1 四态映射
linked_to:                              # F8 跨位段引用
  - "docs/thinking/52_maglev_vs_hermes_agent.md"
superseded_by: null                    # 上位重写归档时填
room_name: null                        # 仅位段层有
```

---

## 4. Skill 层设计

### 4.1 新建 `index-librarian`

```
.agents/skills/index-librarian/
├── SKILL.md                           # 对位 workbench
└── references/
    ├── index-librarian.workflow.md    # scan → verify → calibrate → navigate
    ├── scan.md
    ├── verify.md
    ├── calibrate.md
    └── navigate.md                    # F8 新增（跨位段跳跃）
```

### 4.2 废弃 `maglev-librarian`

- SKILL.md 顶部加 deprecation banner
- frontmatter `runtime_name_status: deprecated`
- catalog 改 `replaced_by: index-librarian`
- 保留 references/ 不删（过渡期）

### 4.3 catalog 关系调整

**原 `maglev-librarian` 的边**（calls / called_by / complements）→ **全部转移到 `index-librarian`**：

```yaml
- id: index-librarian
  status: active
  formal_action_name: 索引管理
  top_level_capability: 数据治理
  system_layer: Foundation Layer
  lifecycle_chain: governance_loop
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  relations:
    - type: calls
      target: index-protocol  # 内部协议
    - type: complements
      target: project-board
    - type: replaces
      target: maglev-librarian

- id: maglev-librarian
  status: deprecated
  runtime_name_status: deprecated
  relations:
    - type: replaced_by
      target: index-librarian
```

---

## 5. 实施阶段拆解

### Phase 1：协议层搬运（~1 天）
- 复制 workbench `_internal/index-protocol/` 到 Maglev `index-librarian/protocol/`
- 改 registry 为 Maglev 模块清单
- schema 增 segment / room_name / linked_to / status 字段

### Phase 2：Skill 层建立（~0.5 天）
- 写 `index-librarian` SKILL.md + references
- catalog 登记新 skill
- `maglev-librarian` 标记 deprecated

### Phase 3：thinking/ 重组（~1-1.5 天）
- 现状 inventory snapshot
- 按位段 + 隐喻名归位（git mv 分批 commit）
- 写 root INDEX.md（含位段表 + Mermaid 认知地图）
- 跑 `index_verify.py thinking` exit code 0

### Phase 4：扩展到 releases / guides（~0.5 天）
- 各自补 INDEX.md frontmatter
- registry 启用
- verify 通过

### Phase 5：F8 认知地图实现（~1 天）
- 实现 `index_update.py` 的 knowledge_graph.json 聚合
- root INDEX.md 自动注入 Mermaid
- `index-librarian navigate` 子命令

### Phase 6：废弃过渡（~0.5 天）
- 旧 skill deprecation banner
- 文档更新（README、AGENTS.md 引用）
- contributors/contribution_log 补登

**总工程量估算**：4-5 个工作日

---

## 6. 验收标准（对应 01_requirements 的 Success Signal）

- ✅ S1: `index_verify.py --all` exit code 0
- ✅ S2: thinking/ 现有 30+18 对象全部归位 + git history 完整
- ✅ S3: root INDEX.md 含 Mermaid 认知地图 + 位段表
- ✅ S4: `index-librarian` 触发 `检查 docs` 即跑完整流程
- ✅ S5: `maglev-librarian` deprecated，但仍可用（过渡期）
- ✅ S6: catalog 一致性测试通过

---

## 7. 风险与缓解

| 风险 | 缓解 |
|------|------|
| **搬运 workbench 脚本时漏掉私有逻辑** | 第一步先 diff 双仓脚本，列出依赖 |
| **schema 增量与 workbench 协议漂移** | 把 Maglev 增量字段标记为 `optional + maglev_only` |
| **重组时 git mv 失败导致历史断链** | 分批 commit + 每批前后 verify + 失败可 reset |
| **catalog 关系图错误（孤悬边）** | 跑 `tests/test_private_catalog_consistency.py` |
| **F8 认知地图过度膨胀** | 仅对 crystallized 及以上文档建边（AC-F8-4） |

---

## 8. 与 02_design 后续阶段的交接

下游收件人：`spec-designer` 完成 → `context-implementer`（XG 主导）

**Ready for Plan**：⚠️ 需用户确认本设计后才进入 03_plan.md（详细任务拆解）。

**Open Questions**（如有）：
1. 是否在 Phase 1 之前先冻结 thinking/ 写入（避免重组期间冲突）？建议：**否**，但分支隔离。
2. 是否需要 CI 集成 `index_verify.py`？建议：**否**（Maglev 暂无 CI），纳入 reality-sync 启动检查即可。
