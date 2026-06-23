# 01 Requirements — Docs Knowledge Archival Methodology

## A. 入口分流（Step 1: Triage）

| 维度 | 判定 |
|------|------|
| **入口类型** | 结构治理（既非新功能、也非 bug 修复） |
| **本轮核心对象** | `docs/` 知识归档方法论 + 索引机制 + librarian skill 集成（三件联动） |
| **输出模式** | `prd_document` — 稳定需求文档（方案设计前必须有基线） |
| **背景但不处理** | `specs/` 三态规则 / `contributors/` / 跨会话语义记忆 / 单文档写作风格 / `packages/`、`scripts/`、`tests/` 的索引 |

> 选择 `prd_document` 而非 `spec_design` 的理由：方法论 + 协议规范 + skill 升级是**三块互相依赖**的产物，若方案设计阶段没有稳定需求基线，规则演化会跳跃漂移。

## B. 范围定义（Step 2: Define）

### B.1 In Scope

1. **知识沉淀生命周期**：定义草稿 → 成熟 → 沉淀 → 归档的四态规则，含每态触发条件与转移条件，并显式映射 MemoryOS 三层范式（STM/MTM/LPM）。
2. **`docs/thinking/` 编号位段语义化**：把现状跳跃编号（30/35/40/50/52）固定为可解释的位段语义（00 元 / 10 批判 / 20 架构 / 30 哲学 / 40 论文 / 50 对标 / 60 案例 / 70 复盘 / 90 归档），并定义"如何选择编号"。配以空间隐喻名称（"房间名"）增强心智锚点。
3. **主题聚类规则**：同类相吸（合并到子目录）、跨类析出（新建主题）、何时允许新建主题、何时强制归并。
4. **命名轨道统一**：编号轨 vs 时间轨二选一，时间属性挪到 frontmatter；目录命名统一 kebab-case。
5. **索引协议引入**：参考 `my-smart-workbench/.agents/skills/_internal/index-protocol/`，含 registry / schema / scripts 三件套，特化到 Maglev `docs/` 颗粒度差异。
6. **`maglev-librarian` skill 升级**：把扫描型升级为编排型（scan → verify → calibrate），增 `navigate` 子命令支持按概念跨位段跳跃，成为 docs 索引唯一入口。
7. **归档触发条件**：时间窗（N 个月未引用）+ 上位重写（被新文档显式覆盖）+ 引用断链（链入数为 0 且时间 > 阈值）三选一即可触发归档；LPM 凝结态文档受保护，需人工确认。
8. **现存内容重组**：把现有 30+ 裸 md + 18 个子目录按新规则迁移到位（保留 git 历史）。
9. **认知地图与导航**：基于记忆宫殿"空间化 + 导航"思路，root INDEX.md 含 Mermaid 节点图，跨位段引用通过 frontmatter `linked_to:` 显式声明，聚合成机读知识图谱。

### B.2 Out of Scope

1. `specs/10_reality/` `specs/20_evolution/` `specs/90_archive/` 内部状态机规则（已固定）。
2. `contributors/contribution_log.md` 写法（已固定为 reverse-chronological 表格）。
3. 跨会话语义记忆机制（如 SQLite + FTS5），独立主题。
4. 单个 thinking 文档的写作风格、正文结构、长度限制。
5. `packages/` `scripts/` `tests/` 的索引化（不在本主题）。
6. `dist/` `.maglev_build/` 等构建产物（已 gitignore）。
7. `docs/releases/` 的归档规则（已由 release 流程治理）。
8. `references/` 目录（属于 skill 内部资产）。

### B.3 Success Signal

1. **方法论可决策**：任何贡献者读完方法论文档后，能独立回答三问——"这份新文档放哪？编号怎么选？什么时候该归档？"
2. **现状归位**：现有 `docs/thinking/` 30 + 18 个对象按规则重组到位，编号位段连续可解释，git log 可追溯每次重命名/移动。
3. **机器可校验**：索引脚本 `index_verify.py docs` exit code 0 表示全模块健康，1 表示有需修复项。
4. **可持续性**：半年后回看，新增内容遵循规则，无新一轮堆砌。
5. **Skill 闭环**：`maglev-librarian` 调用即可完成 scan / verify / calibrate 三步并报告。

### B.4 Key Unknowns

| 编号 | 未知 | 影响下游设计 |
|------|------|--------------|
| K1 | 索引脚本路径策略：放 `scripts/` 还是 `.agents/skills/index-librarian/protocol/scripts/` | 高——决定调用约定与发版策略 |
| K2 | `maglev-librarian` 升级 vs 新建 `docs-librarian` 独立 skill | 高——决定职责边界与 catalog 治理对象数量 |
| K3 | 重组历史文档时使用 `git mv` 还是 `git rm + new`，是否接受 git blame 断裂 | 中——影响重组阶段的可逆性 |
| K4 | 单文件 vs 子目录抽离的阈值（什么时候一个主题该升级为子目录） | 中——影响位段语义稳定性 |
| K5 | `90_archive/` 与 `specs/90_archive/` 的边界（是否合一，或保持二轨） | 中——影响归档动作的一致性 |
| K6 | 编号位段是否允许"主版本扩展"（如 `21_xxx` 与 `20_xxx` 共存）还是严格 10 间距 | 低——影响命名灵活度 |
| K7 | 是否需要 `frontmatter` 强约束（type / scope / tags / status / archived_at） | 中——决定 schema 严格度 |

### B.5 Preferred Output Mode

- **`prd_document`**：本轮稳定需求文档化，作为 02_design.md 的设计基线。

### B.6 Why Minimum Handoff Is Not Enough

最小 handoff 只能输出"做哪几件事"，但本主题的核心价值在于**方法论本身**——若方法论不文档化，后续设计阶段每出现一个边界问题（如 K3、K5）都会回到方法论层面重新讨论，造成漂移。因此本轮在 `requirement-convergence` 内部完成稳定需求文档输出，再进入 spec-designer。

---

## C. 结构化功能需求（AC 体系）

### F1 — 知识沉淀生命周期定义

**用户故事**：作为贡献者，我希望知道一份新沉淀的文档处于哪个生命态，以便决定是继续打磨还是直接归档。

| AC | 描述 |
|----|------|
| **AC-F1-1** | 当文档处于"草稿"态时，方法论应规定其位置（如 `docs/thinking/_drafts/` 或带 `draft:` frontmatter 标记），且不计入正式编号。 |
| **AC-F1-2** | 当文档处于"成熟"态时，应有正式编号、归位到对应位段子目录或顶层。 |
| **AC-F1-3** | 当文档处于"沉淀"态时，应被 INDEX.md 索引，且可被其他文档引用。 |
| **AC-F1-4** | 当文档处于"归档"态时，应迁移到 `90_archive/`，且 INDEX.md 中可见但带归档标记。 |
| **AC-F1-5** | 每态之间的转移必须有显式触发条件（如：成熟 → 沉淀 = 至少被 1 处引用 + 经过 N 天稳定期）。 |
| **AC-F1-6** | 四态隐式映射 MemoryOS 的 STM/MTM/LPM 范式——草稿态（STM，`_drafts/`）/ 主动位段顶层（MTM）/ 被引用 ≥ N 且时间 ≥ M 月（LPM 凝结态）/ 90_archive（自然遗忘）。 |
| **AC-F1-7** | LPM 级文档（凝结态）受保护：归档动作必须人工确认，**不可由 `index_update.py` 自动触发归档**。 |

### F2 — 编号位段语义化

**用户故事**：作为贡献者，我希望基于位段就能猜到一份文档的主题，并知道新文档应取什么编号。

| AC | 描述 |
|----|------|
| **AC-F2-1** | 方法论应定义至少 8 个位段语义（如 00/10/20/30/40/50/60/70/90），每段附明确语义说明与示例。 |
| **AC-F2-2** | 同一位段内允许编号不连续（如 50_ 后下一份是 52_），但**禁止跨段连号**（如 49_ 不允许，必须升到 50_）。 |
| **AC-F2-3** | 当一个位段内文档 ≥ N 份（建议 N=4）时，应触发"是否升级为子目录"的人工评估。 |
| **AC-F2-4** | 子目录命名遵循 kebab-case，且 frontmatter 中声明 `segment: 50_alignment`。 |
| **AC-F2-5** | 每个位段编号必须配**空间隐喻名称**（"房间名称"），用于人类心智锚定，例如：`30_philosophy = 哲学殿`、`50_alignment = 对标厅`、`20_architecture = 架构间`、`90_archive = 归档库`。隐喻仅施加于**位段层**，叶子文档保持工程化命名。 |

### F3 — 主题聚类与命名轨

**用户故事**：作为贡献者，我希望同类文档自动聚到一起，且不被时间命名干扰。

| AC | 描述 |
|----|------|
| **AC-F3-1** | 同主题文档应聚集（同位段顶层文件、同子目录），不允许同主题分散到多个位段。 |
| **AC-F3-2** | 时间属性必须存在 frontmatter（`created`、`updated`），不允许出现在文件名（除非带主题前缀的 dated note 例外）。 |
| **AC-F3-3** | 现有 `xxx_2026_02_03/` 形态目录应迁移为 `<主题>/` + frontmatter 记日期，或归档。 |
| **AC-F3-4** | 当一份文档跨多个主题时，归到"最受影响"位段，并在 frontmatter 标注 `cross_segments: [...]`。 |

### F4 — 索引协议（Registry + Schema + Scripts）

**用户故事**：作为索引管家，我希望机器化校验文档元数据，避免人肉巡视。

| AC | 描述 |
|----|------|
| **AC-F4-1** | 应存在 `index-librarian/protocol/registry.yaml`（或同等位置），声明哪些 docs 子模块纳管。 |
| **AC-F4-2** | 每个纳管模块的 root INDEX.md 必须含 frontmatter（`type / scope / entity_type / index_protocol_version / child_count / stats / updated`）。 |
| **AC-F4-3** | 应存在 `index_scan.py / index_verify.py / index_update.py / index_init.py` 四个脚本，行为契约与 my-smart-workbench 对齐（exit code 0/1/2）。 |
| **AC-F4-4** | 任何 INDEX.md 不允许 AI 直接编辑，必须通过 `index_update.py`。 |
| **AC-F4-5** | 脚本输出应为 JSON，AI 仅负责读取与呈现。 |

### F5 — `maglev-librarian` skill 升级

**用户故事**：作为用户，我希望一句"检查 docs"就能拿到完整索引健康度报告。

| AC | 描述 |
|----|------|
| **AC-F5-1** | `maglev-librarian` 应能识别触发词（"检查 docs / docs 索引 / verify docs"）并启动 `scan → verify → (calibrate)` 流程。 |
| **AC-F5-2** | skill 必须严格按"脚本权威"原则执行，不直接做计数判断。 |
| **AC-F5-3** | 升级后 skill 必须在 `private-catalog.yaml` 更新元数据（如 `runtime_name_status`、`distribution_scope`），并保持 catalog 一致性。 |
| **AC-F5-4** | 与 my-smart-workbench 的 `index-librarian` 在 SKILL.md 结构、Exit Code 约定、references 组织上**对位**（差异仅在模块清单与特化规则）。 |

### F6 — 归档触发条件

**用户故事**：作为贡献者，我希望归档动作有明确触发条件，不依赖个人记忆。

| AC | 描述 |
|----|------|
| **AC-F6-1** | 三种触发条件之一即可归档：**时间窗**（M 个月未被任何 commit/issue/spec 引用）、**上位重写**（被新文档明确 supersede）、**引用断链**（入度为 0 且时间 > N 个月）。 |
| **AC-F6-2** | 归档动作应迁移文件到 `docs/thinking/90_archive/<原位段>/`，并在原位置留 `superseded_by:` frontmatter（若适用）。 |
| **AC-F6-3** | 归档不删除内容，可恢复（git mv，保留历史）。 |
| **AC-F6-4** | `index_verify.py` 应能识别归档态并不报错。 |

### F7 — 现存内容重组

**用户故事**：作为本主题的实施者，我希望有明确的现存内容重组步骤，避免破坏 git 历史。

| AC | 描述 |
|----|------|
| **AC-F7-1** | 重组应使用 `git mv` 保留历史，不允许 `rm + new` 形态。 |
| **AC-F7-2** | 重组前必须有现状 inventory（`tree docs/thinking/` 输出快照） + 重组后 inventory 对照表。 |
| **AC-F7-3** | 重组应**分批 commit**，每批不超过 10 个文件，commit message 模板化（"docs(reorg): move A,B,C from root to 50_alignment/"）。 |
| **AC-F7-4** | 重组完成后必须运行 `index_verify.py`，exit code 0 才视为成功。 |

### F8 — 认知地图与导航（记忆宫殿启发）

**用户故事**：作为贡献者，我希望能像走进宫殿一样在 docs 中导航，而不是面对一堆扁平文件。

| AC | 描述 |
|----|------|
| **AC-F8-1** | root INDEX.md 必须含 Mermaid 节点图：节点 = 位段（如 `30_philosophy`），边 = 跨位段引用 ≥ 1 即建边。 |
| **AC-F8-2** | 每份文档可在 frontmatter 声明 `linked_to: [path, ...]`，由 `index_update.py` 聚合成 `docs/_meta/knowledge_graph.json`，作为可机读图谱。 |
| **AC-F8-3** | `maglev-librarian` 应支持 `navigate` 子命令（如 `librarian navigate <concept>`），按概念跳跃查找跨位段相邻文档。 |
| **AC-F8-4** | 知识图谱仅对**沉淀态及以上**的文档建边，草稿态不入图，避免噪音。 |

> **范围与风险约束**（来自记忆宫殿可借鉴性分析）：
> - 隐喻命名仅施加于**位段**层（参见 F2 增强 AC-F2-5），叶子文档保持工程化命名，避免心智负担过重。
> - 知识图谱仅做**Mermaid 静态图 + frontmatter 显式声明**，不引入语义向量检索 / GraphRAG 等运行时机制，避免越界。
> - 借鉴对象（记忆宫殿、MemoryOS、MemGPT）是面向**运行时记忆**的，本主题仅借**空间化思路**，不借**检索算法**。

---

## D. 术语表

- **位段（Segment）**：编号 00-90 的语义分组（如 `30_philosophy`），位段内允许跳号，跨段不连号。每个位段配"房间名称"作空间隐喻锚点。
- **沉淀态（Crystallized）**：文档已被 INDEX.md 索引、被其他文档引用、过了稳定期（与 `crystallization` skill 的 spec 归档语义对位但不等价）。
- **轨道（Track）**：命名规则二选一——编号轨（00_xxx）或时间轨（2026-02-03-xxx）。本主题统一为编号轨 + frontmatter 日期。
- **纳管模块（Managed Module）**：在 `registry.yaml` 中显式声明、由索引脚本巡检的目录。
- **归档触发（Archive Trigger）**：时间窗 / 上位重写 / 引用断链三种条件之一。LPM 凝结态除外。
- **位段升级（Segment Promotion）**：当顶层文件 ≥ N 份时，把它们抽离到同名子目录的人工评估动作。
- **STM / MTM / LPM**：MemoryOS 范式的三层记忆——短期 / 中期 / 长期持久。本主题映射为草稿 / 主动位段 / 凝结态。
- **凝结态（LPM Consolidated）**：被引用 ≥ N 且时间 ≥ M 月的文档，受保护不可自动归档。
- **空间隐喻名称（Room Name）**：位段编号配套的中文心智锚点（如"哲学殿"、"对标厅"），仅施加于位段层。
- **认知地图（Cognitive Map）**：root INDEX.md 内嵌的 Mermaid 节点图，节点为位段，边为跨位段引用。
- **知识图谱（Knowledge Graph）**：由 `linked_to:` frontmatter 聚合而成的 `docs/_meta/knowledge_graph.json`，机读。

---

## E. 与下游 02_design.md 的交接

**Ready Gate 判定**：✅ 通过

- ✅ In/Out 边界清晰
- ✅ 8 个功能需求 + 35 条 AC 已结构化（含记忆宫殿启发的 F8 + F1/F2 增强）
- ✅ 7 项 Key Unknowns 已识别（属设计阶段决策）
- ✅ 输出模式 = prd_document，本文件即基线
- ✅ 与 reality (`maglev-librarian` 现状) 已对齐
- ⚠️ K1-K7 需在 02_design.md 中给出明确决策

**下游收件人**：`spec-designer`（TP 主导）

**最小交接清单**：
1. 本文件（`01_requirements.md`）作为设计输入基线
2. `00_intent.md` 作为意图锚点
3. `my-smart-workbench` 索引协议作为参考实现
4. `maglev-librarian` 当前 SKILL.md 作为升级起点
5. 记忆宫殿 / MemoryOS（[arXiv:2506.06326](https://arxiv.org/abs/2506.06326)）作为概念参考
