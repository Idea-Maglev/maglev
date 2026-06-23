# Requirements (PRD): maglev_discipline_governance

> 输出模式：`prd_document`
> Ready Gate：PASS（2026-05-21）
> 字段契约：见 `.agents/skills/requirement-convergence/references/prd-output-contract.md`

## PRD Output Package

```yaml
prd_output_package:
  core_object: maglev-discipline (治理纪律 skill) + AGENTS.md 红线触发器 + 主流程引用块
  target_user: maglev 框架用户在跨平台 agent 环境（Codex / Claude Code / GitHub Copilot 等）下的 AI 行为本身
  collaboration_context: |
    本主题是一轮跨阶段改造（涉及新建 skill + 改 AGENTS.md + 改 4 个主流程 skill +
    catalog 登记），下游会经过 spec-designer / skill-scout / context-implementer /
    integrated-validator / crystallization 多个对象，必须用 PRD 固定基线避免漂移。
    且本主题元学性极强，AI 在执行过程中正是治理对象，必须有外部基准对照。

  in_scope:
    - 新建 .agents/skills/maglev-discipline/ 目录（SKILL.md + 关键 references）
    - AGENTS.md 顶部加 "会话启动红线" 区块（≤ 30 行，含三条红线 + 强制读取 maglev-discipline 指令）
    - 4 个主流程 skill (reality-sync / spec-designer / context-implementer / integrated-validator) 的 SKILL.md 在 `## 交互模式` 区加 1-2 行 maglev-discipline 引用
    - .agents/private-catalog.yaml 登记 maglev-discipline (Governance Layer / user_visible)
    - maglev 专有惰性模式表（含 8 类，其中第 8 类 = "做治理任务时绕过框架自身治理流程"，本会话自证）
    - 真实新会话冷启动验证（Codex + Claude Code 各一遍）

  out_of_scope:
    - pua 的 14 种企业文化味道库（打卡、汇报话术、Sprint Banner 等具象 fixture）
    - Claude Code 专属 hook（PreCompact / PostToolUse / SessionStart）实现
    - ~/.maglev/ 全局状态持久化（计数器 / journal）
    - task 工具 spawn 子 agent 时自动注入 — v1 仅在文档约定
    - Cursor 平台适配 .cursor/rules/maglev-discipline.mdc — v2 再做
    - spec 模板加 forbidden / verify_commands 字段 — v1 仅在 maglev-discipline 定义规范
    - crystallization / reality-sync 引入独立 verifier 子 agent — v2 再做
    - 重命名现有 skill 或修改 catalog 治理结构

  success_signal:
    - 冷启动注入信号：Codex 和 Claude Code 各开全新会话，AI 在响应第一条用户消息前应读取过 AGENTS.md 与 maglev-discipline SKILL.md，可通过工具调用历史验证
    - 主流程二次激活信号：新会话中显式触发任一主流程 skill，AI 应在执行第一个动作前再次声明 maglev-discipline 红线
    - 惰性识别信号：故意制造"声称读完但只读一点"或"绕过流程"场景，AI 应在 1-2 轮内自我识别并触发红线
    - AGENTS.md 体量限：增量后总长 ≤ 6000 字节
    - 维护成本可控：变更涉及文件数 ≤ 10

  key_unknowns:
    - KU-2 (暂定 / 不阻塞)：主流程 SKILL.md 引用形式 — 在 `## 交互模式` 加一行 vs 新增 `## 红线` 小节。倾向前者，spec-designer 阶段定稿
    - KU-3 (暂定 / 不阻塞)：失败计数策略 — AI 自报 vs 用户手动触发 vs 两者并存。倾向"两者并存"，spec-designer 阶段定稿
    - KU-4：已决 — 进 specs/20_evolution/active/maglev_discipline_governance/，走完整 evolution 流程含结晶归档
    - KU-1：已决 — AGENTS.md 红线区块放最顶部，优先 AI 第一时间读取，不顾人类可读性顺序

  drift_risk: |
    1. 没有 PRD：方案细节会在 spec-designer 与 skill-scout 之间反复返工
    2. 没有显式成功信号：会出现"skill 写完就算完"的虚假交付（恰恰是本主题要解决的惰性）
    3. 没有 Out of Scope：v1 容易膨胀（尤其"加企业味道库""做 hook"等吸引人的扩展）

  why_minimum_handoff_is_not_enough: |
    最小 handoff（核心对象 + In/Out scope + 成功信号 + 关键未知 + Ready Gate 结论）虽然结构完整，
    但本主题：
    1. 跨 5+ 个下游对象消费，需要稳定基线
    2. 主题本身就是"治 AI 惰性"，自身在执行过程必须遵守自己的流程，PRD 是元规约
    3. 多文件协同（≥ 7 个文件协同改动），需要显式交付清单
    4. 跨平台验证需要 fixture 协议，必须明列交付物

  expected_prd_outcome:
    - 一份 spec-designer 可直接消费的稳定需求基线
    - 一组冷启动可验证的成功信号
    - 一份明确的 Out of Scope 清单防止 v1 膨胀
    - 一组维护成本上限约束（文件数 / AGENTS.md 体量）
    - 一份惰性模式清单（含本会话自证的"绕过框架自治理"）作为后续 maglev-discipline skill 的核心 references 输入

  downstream_consumers:
    - spec-designer (下一步)
    - skill-scout (adapt + register 阶段)
    - context-implementer (实施 4 个文件改动 + 1 个新 skill 目录)
    - integrated-validator (跑冷启动验证 fixture)
    - crystallization (本主题完成后走完整归档)
```

## 非目标的显式补充说明

- 本主题不重新设计 maglev 主流程；不引入新的角色（如 P7/P8/P9）；不引入 pua 的企业文化味道库
- 本主题不解决"AI 完全离线 / 完全不读 AGENTS.md"的极端情况 — 接受这层残余风险，v2 通过 ai-tooling-compat fixture 监控
- 本主题不修改 task 工具源码 / 不引入 hook 注入 — 全部靠文档级强制

## 与 issues / 现有 active 主题的关系

- 当前 `specs/20_evolution/active/` 无其他活跃主题（搁置 `extension_point_architecture` 不冲突）
- 当前 `issues/draft/` 无相关条目，本主题创建后建议补一条 issue 链回 spec
- 与 `specs/90_archive/` 中 `main_flow_quality_gates` 是上下游关系：本主题在主流程质量门基础上加"治理强制层"

## 术语表

- **D 方案**：本主题选用的实施方案 = AGENTS.md 红线 + 主流程引用 + 独立 skill 三层
- **红线触发器**：AGENTS.md 顶部 ≤ 30 行的会话级强制段，定义三条红线 + 强制读取 maglev-discipline SKILL.md 指令
- **三条红线**（源自外部参考，私域化收敛）：闭环验证 / 事实驱动 / 穷尽方法
- **冷启动注入信号**：在无任何历史上下文的新会话中，AI 第一时间是否读取过红线文件
- **元自证**：本主题执行过程自身正在产生本主题要治理的惰性，作为方案有效性的自证基准
- **track**：`index-librarian/protocol/registry.yaml` 中声明的可索引资产（spec-tree / docs-tree / repo-entry / code-tree 四类）
- **可发现性接线**：把 `.agents/skills/` 作为一类资产正式纳入 index-librarian 治理协议，让索引/校验/漂移检测**靠确定性脚本而非靠 AI 记得**

---

## v2 — 主题扩展（基于会话二次发现）

> 落盘日期：2026-05-21（同日，发生在 spec-designer Phase 2 commit 之后）
> 触发原因：用 maglev-discipline 治理 skill 适配过程中发现 — 仅治理"个体行为惰性"不足以解决"系统稳态漂移"。把单线主题正式拆为两条并行子线。

### 触发性事实（必须先认清）

1. **`index-librarian` 引擎已存在且成熟**：脚本驱动（`track_scan/verify/map/archive_triggers.py`）+ 退出码契约（ok/partial/skipped/failed）+ registry.yaml 单一事实源 + 产物 isolation。**核心原则与 maglev-discipline 同向**："凡是确定性逻辑能做的，不让 AI 做"。
2. **缺口**：当前 `registry.yaml` 注册的 tracks = `specs` / `docs` / `repo-entry`，**`.agents/skills/` 自己作为一类资产没有任何 track 覆盖**。意味着新增/重命名/删除 skill 不会被 index-librarian 自动感知。
3. **活漂移证据**：系统提示词 / Copilot 平台缓存的 "Repo-local Skills" 清单仍写着 `maglev-librarian`，**实际仓库已迁移到 `index-librarian`**（crystallization step-04 references 第 19 行明确标注"取代废弃的 maglev-librarian"）。这是**外部消费者缓存层漂移**的真实案例，证明漂移检测不能只看仓库内。
4. **元教训**：本会话先后两次（绕过 requirement-convergence 直接进 design；评估 librarian 方案时不查源码做纸面推理）发病，证明"反个体惰性"和"系统稳态"是两个抽象层，不能合并。

### v2 子线划分

#### Subtheme A — 纪律 skill（个体行为层）

保持 v1 In Scope 不变（即上方 prd_output_package.in_scope 全部条目），覆盖反个体惰性。

#### Subtheme B — 可发现性接线（系统稳态层）

**v2 In Scope（新增）**：

- B1. 在 `index-librarian/protocol/registry.yaml` 新增一条 track：`id: skills`，`type: repo-entry`（复用现有 type，零代码改动），`root: .agents/skills/`，`patterns: [**/SKILL.md]`，`output: .agents/_meta/skills-map.yaml`
- B2. 跑通验证三件套：`_track_resolver.py --list` 看到 `skills` / `track_scan.py --track-id skills` 产出 `.agents/_meta/skills-map.yaml` / `track_verify.py --track-id skills` 退 0
- B3. `reality-sync` skill 的 `## 交互模式` 段补一行 — 启动期跑 `track_verify --track-id skills`（仅 skill 集合，非 `--all`，避免与 specs/docs verify 互相阻塞），exit ≠ 0 时显式 surface partial/failed 状态
- B4. 修复外部缓存层漂移：定位"Repo-local Skills"清单的生成源头（可能是 `.copilot-instructions.md` / 仓库根某 yaml / 外部平台缓存），把 `maglev-librarian` 改为 `index-librarian`

**v2 Out of Scope（新增）**：

- 新增 `skill-tree` 自定义 track type 与 `track_skills.py` 脚本（v3 提质议题，需要时再做）
- 按 `system_layer / lifecycle_chain / distribution_scope` 做 layered 分组渲染（同上 v3）
- 重写 / 重命名 index-librarian 引擎本身
- 给现有 `specs` / `docs` tracks 加新字段
- 把 `track_verify --all` 接入 CI / pre-commit（v2 仅接 reality-sync 启动，CI 集成 v3 再做）
- 把 maglev-discipline 与 index-librarian 合并为同一 skill（两个抽象层应保持独立）

**v2 Success Signal（新增）**：

- B1-Sig：`_track_resolver.py --list` 输出包含 `skills` track
- B2-Sig：跑 `track_scan --track-id skills` 后 `.agents/_meta/skills-map.yaml` 存在且列出当前 18+ 个 skill
- B3-Sig：在 reality-sync 启动期，若有 skill 漂移（如手动删一个 SKILL.md），AI 必须在第一条响应里报告 partial 状态
- B4-Sig：grep 整仓 `maglev-librarian` 字符串，活跃文件命中数 = 0（archive / docs/thinking 历史归档允许保留）

**v2 Key Unknowns**：

- KU-5：已决 — Subtheme B1 复用 `repo-entry` track type（不新增 `skill-tree`），最小代码改动路径
- KU-6（不阻塞 spec-designer，但实施前需查）：系统提示词清单的生成源头在哪？候选：`.copilot-instructions.md` / 仓库根 yaml / 外部平台侧缓存。spec-designer 阶段定位即可
- KU-7（spec-designer 阶段定稿）：reality-sync 启动跑 `track_verify --track-id skills` 的频次策略 — 每次启动都跑（简单但每次冷启动 +1s 开销） vs 缓存 N 分钟（复杂但快） vs 仅当 `.agents/skills/` mtime 变化时跑（最优但需 stat 检查）

**v2 drift_risk（追加）**：

- 不接 B → 未来每加一个 skill 都靠 AI 记得调用 librarian，5 个 skill 后必出漏；恰恰陷入本主题要治理的"靠自觉"模式
- 不接 B3 → B1+B2 落成静态产物，第一次跑后没人维护，等同于不接
- 不修 B4 → 外部消费者继续被错误清单误导，AI 像本会话一样误信、误评估，再次发病

### Ready Gate 重判

```yaml
gate_result: ready
next_object_candidate: spec-designer
reason: |
  v2 范围扩展后，Subtheme A 保持 v1 已定结构；Subtheme B 的核心
  阻塞 KU (KU-5 track type 选型) 已就地解开（复用 repo-entry，
  零代码改动）。剩余 KU-6/KU-7 在 spec-designer 阶段定稿即可，
  不改变设计主路径。
consumption_rationale: |
  spec-designer 需要的输入：稳定边界（A/B 子线划分清晰）+ 成功信号
  （A v1 + B v2 全部已定）+ 关键未知（KU-5 已收口，KU-6/7 由 design
  阶段定稿）+ 风险表（drift_risk 已补 B 线三条）。Ready 输入完整。
prd_mode_required: true
missing_items: []
```

### 流程纪律记录（不删，作为元自证档案）

本主题在 v1→v2 演进过程中暴露的 maglev 流程跳步：

1. v1 阶段：从 entry-router 收到任务后**直接进 spec-designer**，未走 requirement-convergence — 后由用户戳穿，补走
2. v2 阶段：发现 index-librarian 引擎已存在后**直接想重写 02_design.md**，未补 01_requirements.md v2 段 — 由用户戳穿，按此段补走
3. 评估各 Layer 方案时**未读 index-librarian 源码做纸面推理** — 由用户要求"评估落地有效性"暴露，被迫读源码后发现 B 引擎已就绪

以上三条全部命中 maglev-discipline SKILL.md §"8 类惰性" 第 4 类（磨洋工：描述代替证据）+ 第 8 类（绕过框架自治理流程）。**写入本节作为 maglev-discipline references/laziness-patterns.md 的真实素材，不丢弃**。

