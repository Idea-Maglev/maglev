# Design v2: maglev_discipline_governance

> **v2 重写说明**：基于 `01_requirements.md` v2 段（A/B 双子线划分）整体重组。
> v1 内容（2026-05-21 commit `a46b21f`）的核心结构保留为 §A，新增 §B + §C/D/E/F。
> v1 备份：`/tmp/02_design_v1_backup.md`（不入 git）。
>
> 上游输入：`01_requirements.md` v2 段（Ready Gate v2 PASS）
> 下游消费者：`skill-scout (adapt+register)` → `context-implementer` → `integrated-validator`
> 设计时间：2026-05-21（同日 v2 重写）

---

## §0 v2 整体导航

### 0.1 主题双子线划分

```
Subtheme A (个体行为层)              Subtheme B (系统稳态层)
┌─────────────────────────┐         ┌──────────────────────────┐
│ 治理目标:               │         │ 治理目标:                │
│ AI 的行为惰性           │         │ skill 集合的系统漂移     │
│                         │         │                          │
│ 主要交付:               │         │ 主要交付:                │
│ maglev-discipline skill │         │ index-librarian 接线     │
│ + AGENTS.md 红线        │         │ + reality-sync 漂移哨兵 │
│ + 4 主流程引用          │         │ + 外部清单旧名修复       │
│                         │         │                          │
│ 治理机制:               │         │ 治理机制:                │
│ 红线提醒 / 协议契约     │         │ 确定性脚本 / 注册表      │
│ 靠 AI 自觉读 + 用户监督 │         │ 靠引擎自动校验           │
└─────────────────────────┘         └──────────────────────────┘
         (软强制 / 协议层)                  (硬强制 / 工程层)
                  \                       /
                   \                     /
                    互不替代，必须并存
                    A 治本 (行为)，B 治标 (机制)
```

### 0.2 当前进度盘点

| 子线 | 阶段 | 状态 |
|---|---|---|
| §A — 纪律 skill | SKILL.md 已写（0 purity findings） | ⚠️ 未 commit；属"先 adapt 后 design"流程跳步，作为元自证档案保留 |
| §A — references (3 个) | 未写 | ⏳ skill-scout adapt 阶段补做 |
| §A — AGENTS.md 红线 | 未实施 | ⏳ context-implementer 阶段 |
| §A — 4 主流程引用 | 未实施 | ⏳ context-implementer 阶段 |
| §B — registry 加 track | 未实施 | ⏳ context-implementer 阶段（零代码） |
| §B — reality-sync 哨兵 | 未实施 | ⏳ context-implementer 阶段 |
| §B — 外部清单修复 | 源头未定位 | ⏳ KU-6，context-implementer 阶段先定位再修 |

---

## §A — Subtheme A: 纪律 skill（个体行为层）

### §A.1 三层防御架构

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: 会话级 (AGENTS.md 顶部红线区块, ≤ 30 行)        │
│   ▸ 三条红线: 闭环验证 / 事实驱动 / 穷尽方法            │
│   ▸ 强制指令: 进任何主流程或本仓库治理任务前必须读取    │
│     .agents/skills/maglev-discipline/SKILL.md           │
│   ▸ 触发: 永远生效 (所有支持 AGENTS.md 的平台)          │
└─────────────────────────────────────────────────────────┘
                          ↓ AI 路由到主流程时
┌─────────────────────────────────────────────────────────┐
│ Layer 2: 主流程级 (4 个 skill SKILL.md 头部加引用)       │
│   ▸ reality-sync / spec-designer / context-implementer  │
│     / integrated-validator                              │
│   ▸ 在 `## 交互模式` 区加一行:                          │
│     "背景纪律: 本 skill 执行期间持续遵循                │
│     maglev-discipline 红线，每个 step 起始前先做       │
│     [MAGLEV-DIAGNOSIS] 自检"                            │
│   ▸ 触发: AI 路由进任一主流程 skill 时                  │
└─────────────────────────────────────────────────────────┘
                          ↓ AI 引用纪律详情时
┌─────────────────────────────────────────────────────────┐
│ Layer 3: 协议级 (.agents/skills/maglev-discipline/)     │
│   ▸ SKILL.md (主协议)                                   │
│   ▸ references/laziness-patterns.md                     │
│     (8 类惰性模式 + 抗合理化反击表)                     │
│   ▸ references/remedy-protocol.md                       │
│     (L0-L4 + 5 步方法论 + 7 项清单 +                    │
│     Owner 四问 + 信心门控)                              │
│   ▸ references/task-contract.md                         │
│     (Task Contract 四元组 + Sub-agent 注入约定)         │
└─────────────────────────────────────────────────────────┘
```

### §A.2 Layer 1 — AGENTS.md 红线区块 schema

**位置**：AGENTS.md 顶部，覆盖现有"默认使用简体中文回答"之前。
**理由**：KU-1 已决，效率和质量优先于人类可读性顺序。

```markdown
# 🔴 会话启动红线（maglev-discipline）

> 本区块为 maglev 框架的会话级强制层，所有跨平台 agent 在本仓库工作时必须遵循。

## 三条不可灰度红线

1. **闭环验证**：交付前必须用证据（命令输出、文件 diff、可观察事实）说话，禁止用"已完成/已修复"代替证据
2. **事实驱动**：声明任何状态前必须有工具验证依据，禁止凭记忆/印象下结论
3. **穷尽方法**：宣告无法解决前必须走完 maglev-discipline 通用 5 步方法论

## 强制读取

进入任何主流程（`reality-sync` / `spec-designer` / `context-implementer` / `integrated-validator`）或本仓库治理任务前，必须读取 `.agents/skills/maglev-discipline/SKILL.md`，并将其红线协议作为本会话默认背景纪律。

---
```

**体量约束**：本区块 ≤ 30 行。

### §A.3 Layer 2 — 主流程引用块模板（KU-2 定稿）

**修改对象**：4 个主流程 skill 的 SKILL.md。
**修改位置**：`## 交互模式 (Interaction)` 区，作为现有要点的**最后一条**。
**修改文本**：

```markdown
- **背景纪律**：本 skill 执行期间持续遵循 `maglev-discipline` 红线（闭环验证 / 事实驱动 / 穷尽方法），每个 step 起始前先做 `[MAGLEV-DIAGNOSIS]` 自检
```

**理由**：
- 不新增 `## 红线` 章节 → 避免改 4 个文件的结构层级
- "持续遵循"语义比每 step 重新读 SKILL.md 更轻
- `[MAGLEV-DIAGNOSIS] 自检`是行为契约，强于纯提醒

### §A.4 失败计数策略（KU-3 定稿）

```yaml
failure_escalation:
  trigger_sources:
    - ai_self_report:
        signal: 'AI 重复同类操作失败时，主动声明 "[MAGLEV L{N}] 第 {N} 次同类失败，进入 L{N} 响应"'
        scope: '工作记忆维护，会话内可见'
    - user_manual:
        signal: '用户显式触发: "升 L2" / "升 L3" / "走 7 项清单"'
        scope: '立即生效'
    - integrated_validator:
        signal: 'integrated-validator review 阶段可标记 "建议升 L{N}"'
        scope: '当次 review 内生效，可记入 status.md'
  storage:
    - '不引入 ~/.maglev/ 全局状态'
    - '会话内 failure count 由 AI 维护在工作记忆'
    - '跨会话需要追踪时记入 docs/thinking/ 或 specs/{spec}/status.md'
```

### §A.5 Sub-agent 注入约定

当使用 task 工具 spawn `explore` / `general-purpose` / `code-review` 子 agent 时，**必须在 prompt 末尾追加**：

```text
---
开工前用 view 工具读取以下文件，按其中的行为协议执行：
- 核心红线: .agents/skills/maglev-discipline/SKILL.md
- 惰性识别: .agents/skills/maglev-discipline/references/laziness-patterns.md
---
```

未注入即视为裸奔，是 owner 责任失职。

### §A.6 references 拆分（收紧到 3 个，满足 PRD ≤ 10 总文件约束）

| 文件 | 内容要点 |
|---|---|
| `references/laziness-patterns.md` | 8 类惰性模式（含第 8 类绕过框架自治理） + 14 条抗合理化反击表 + 7 类失败模式 → maglev 工具链切换路径 |
| `references/remedy-protocol.md` | L0-L4 压力升级（三源触发） + 通用 5 步方法论 + 7 项检查清单 + Owner 四问 + 冰山法则 + 信心门控 6 步 + 体面退出 |
| `references/task-contract.md` | Task Contract 四元组（intent / acceptance / forbidden / verify_commands） + proposed/verified status 协议 + Sub-agent 注入 + `[MAGLEV-DIAGNOSIS]` / `[MAGLEV +1]` 语法 |

### §A.7 进度声明与流程跳步记录

**已实施（未 commit）**：

- `.agents/skills/maglev-discipline/SKILL.md` — 280 行，三轮清洗（purity scan / 删项目特定路径 / 剥离外部来源痕迹）后 0 hard/info findings，已通过 artifact-external 自检
- `.agents/skills/maglev-discipline/references/` — 空目录已建

**流程跳步事实档案**（不删，作为元自证素材）：

1. v1 阶段：从 entry-router 收到任务后**直接进 spec-designer**，未走 requirement-convergence — 补走后已 commit
2. **本节关联**：在 v1 spec-designer Phase 2 后**直接进入 skill-scout adapt 落盘 SKILL.md**，未先确认 adapt 是设计阶段后的独立步骤 vs 设计阶段内的草稿 — 严格按 maglev 流程，adapt 应该在 design 完成 + 用户审批后由 skill-scout 独立做。提前落盘**违反"design → adapt → implementation"顺序**，但成果（SKILL.md 0 finding）有效，按"成果不丢、过程记账"处理：写入本节作为 maglev-discipline `references/laziness-patterns.md` 第 8 类（绕过框架自治理）的真实素材
3. v2 阶段：发现 index-librarian 引擎已存在后**直接想重写 02_design.md**，未补 01_requirements.md v2 段 — 补走后已落盘
4. 评估各 Layer 方案时**未读 index-librarian 源码做纸面推理** — 被迫读源码后发现 B 引擎已就绪
5. v2 02_design 第一稿在 §A.8 残留外部来源字段名 — 由用户戳穿后整段删除

---

## §B — Subtheme B: 可发现性接线（系统稳态层）

### §B.1 引擎现状盘点

`index-librarian` 已是成熟引擎，本子线**不需要写任何新脚本**，仅做注册表配置与调用集成。

| 现有能力 | 证据位置 |
|---|---|
| 脚本驱动索引（不靠 AI 算） | `.agents/skills/index-librarian/protocol/scripts/track_{scan,verify,map,archive_triggers}.py` |
| 单一事实源 | `index-librarian/protocol/registry.yaml` (tracks: 段) |
| 4 类 track type | `spec-tree` / `docs-tree` / `repo-entry` / `code-tree` |
| 退出码契约 + 状态枚举 | `ok` / `partial` / `skipped` / `failed`（与 CI 集成天然兼容） |
| 产物 isolation | "脚本独占写权，AI 不得直接编辑产物" |
| 加新 track SOP | `index-librarian/references/track-extension.md` 3 步法 |
| 核心原则 | "凡是确定性逻辑能做的，不让 AI 做" — 与 maglev-discipline 同向 |

### §B.2 registry.yaml diff（B1 In Scope）

**修改文件**：`.agents/skills/index-librarian/protocol/registry.yaml`
**修改位置**：`tracks:` 段末尾追加一条
**追加内容**：

```yaml
  - id: skills
    type: repo-entry
    root: .agents/skills/
    patterns:
      - "**/SKILL.md"
    output: .agents/_meta/skills-map.yaml
```

**字段说明**：

- `id: skills` — 全仓唯一，kebab-case
- `type: repo-entry` — 复用现有 type（KU-5 已决），零代码改动
- `root: .agents/skills/` — 相对仓库根
- `patterns: ["**/SKILL.md"]` — 只扫每个 skill 目录的入口文件，不扫 references / protocol 等内部产物
- `output: .agents/_meta/skills-map.yaml` — 与 `.agents/_meta/repo-entry.yaml` 同层，约定俗成

### §B.3 验证三件套（B2 In Scope）

context-implementer 落盘 §B.2 后立即跑：

```bash
PROTOCOL=".agents/skills/index-librarian/protocol"

# 1. 确认新 track 已被 resolver 识别
python3 $PROTOCOL/scripts/_track_resolver.py --list
# 预期输出包含 "skills"

# 2. 跑 scan 生成产物
python3 $PROTOCOL/scripts/track_scan.py --track-id skills
# 预期：exit 0；产物 .agents/_meta/skills-map.yaml 写出；列出当前 18+ skill 的锚点

# 3. 跑 verify 校验
python3 $PROTOCOL/scripts/track_verify.py --track-id skills
# 预期：exit 0 (ok)
```

**降级容忍**：若 `track-id skills` 在某些环境下 type=repo-entry 不完美匹配 patterns（如 SKILL.md 不在 root 直接子目录），可能落 `partial`。这种情况由 KU-6 后续 v3 议题处理（新增 `skill-tree` type），v1 接受 partial 不阻断。

### §B.4 reality-sync 漂移哨兵接入（KU-7 定稿）

**KU-7 三选项评估**：

| 选项 | 实现复杂度 | 启动开销 | 漂移检测时效 | 推荐 |
|---|---|---|---|---|
| 1. 每次 reality-sync 启动都跑 verify | ★ 极低 | +约 1s | 实时 | ✅ **定稿** |
| 2. 缓存 N 分钟 | ★★★ 高（要状态管理） | 偶尔 0 偶尔 +1s | 延迟 N 分钟 | ❌ 过度优化 |
| 3. 仅当 `.agents/skills/` mtime 变化时跑 | ★★ 中（要 stat） | 几乎 0 | 实时 | ❌ stat 检查反而复杂 |

**定稿理由**：与 maglev-discipline "确定性优先 / 简单优先"一致。+1s 开销在会话级别可忽略；如未来发现成本不可接受，再升级为选项 3。

**修改文件**：`.agents/skills/reality-sync/SKILL.md`
**修改位置**：`## 交互模式 (Interaction)` 段，作为新一条要点
**修改文本**：

```markdown
- **启动期漂移哨兵**：reality-sync 启动时跑 `python3 .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills`；exit ≠ 0 时必须在第一条响应里 surface track 状态（`partial` / `failed`），并提示用户运行 `track_scan --track-id skills` 重建
```

### §B.5 外部清单旧名 maglev-librarian 修复（KU-6）

**KU-6 状态**：源头未定位。design 阶段只给定位 SOP，实际定位与修复放到 context-implementer。

**定位 SOP**（context-implementer 阶段执行）：

```bash
# 1. 在仓库根候选生成源中查找
ls .copilot-instructions.md .github/copilot-instructions.md 2>/dev/null
grep -rn "maglev-librarian" .copilot* .github/copilot* 2>/dev/null

# 2. 检查是否由 maglev-cli installer 注入
grep -rn "maglev-librarian" packages/maglev-cli/runtime-src/ 2>/dev/null

# 3. 检查 ai-tooling-compat 是否有平台特定配置
grep -rn "maglev-librarian" ai-tooling-compat/ 2>/dev/null

# 4. 检查 AGENTS.md 与其引用链
grep -rn "maglev-librarian" AGENTS.md llms.txt scripts/ 2>/dev/null
```

**修复策略**：

- 命中文件全部改 `maglev-librarian` → `index-librarian`
- 同步检查是否还有其他已重命名 skill 的旧名（一并修）
- 若源头是 dist/ 构建产物，必须改 runtime-src/ 再重新构建（不改 dist）
- archive / docs/thinking / contributors / docs/releases 历史归档不动（历史正确性优先）

**完成判据**：

```bash
# 活跃文件命中数 = 0
grep -rln "maglev-librarian" --include="*.md" --include="*.yaml" --include="*.yml" --include="*.json" \
  | grep -vE "^./(archive|specs/90_archive|docs/thinking|docs/releases|contributors|packages/maglev-cli/dist)" \
  | wc -l
# 期望输出: 0
```

### §B.6 B 子线下游交付清单

| 文件 | 改动类型 | 行数估计 |
|---|---|---|
| `.agents/skills/index-librarian/protocol/registry.yaml` | 追加 1 条 track | +6 行 |
| `.agents/skills/reality-sync/SKILL.md` | `## 交互模式` 加 1 行 | +1 行 |
| KU-6 定位命中的活跃文件 | 字符串替换 `maglev-librarian` → `index-librarian` | 变量（context-implementer 阶段定） |
| `.agents/_meta/skills-map.yaml` | 由 track_scan.py 生成，非手写 | n/a |

### §B.7 B 子线 fixture 设计

```yaml
fixture_b_track_registered:
  steps:
    - '跑 python3 .agents/skills/index-librarian/protocol/scripts/_track_resolver.py --list'
    - '验证输出 grep "skills" 命中'
  pass_criteria: '命中'

fixture_b_track_scan:
  steps:
    - '跑 python3 .agents/skills/index-librarian/protocol/scripts/track_scan.py --track-id skills'
    - '验证 exit code 0'
    - '验证 .agents/_meta/skills-map.yaml 文件存在'
    - '验证文件内列出至少 15 个 skill 锚点（当前 maglev 18+ skill）'
  pass_criteria: '全部通过'

fixture_b_drift_detection:
  scenario: '手动删除任一 SKILL.md（如 .agents/skills/maglev-discipline/SKILL.md）'
  steps:
    - '用户启动 reality-sync skill'
    - '验证 AI 第一条响应包含 partial 或 failed 状态'
    - '验证 AI 提示运行 track_scan 重建'
  pass_criteria: '两个验证都过'
  teardown: '恢复被删的 SKILL.md'

fixture_b_external_list_fixed:
  steps:
    - '在活跃文件域跑 grep -rln "maglev-librarian"'
    - '排除归档目录后命中数应为 0'
  pass_criteria: '命中数 = 0'
```

---

## §C — 跨子线协调

### §C.1 实施顺序

```
[已完成]
  ✅ requirement-convergence v1 → 01_requirements.md
  ✅ spec-designer Phase 2 v1 → 02_design.md (旧版)
  ⚠️ skill-scout adapt 提前落盘 SKILL.md (流程跳步，成果有效保留)
  ✅ requirement-convergence v2 追加段 → 01_requirements.md v2 段
  ✅ Ready Gate v2 PASS
  ✅ spec-designer v2 重写 → 02_design.md (本文档)

[下一步 — skill-scout adapt]
  ⏳ 补写 references/laziness-patterns.md (跑 purity scan)
  ⏳ 补写 references/remedy-protocol.md (跑 purity scan)
  ⏳ 补写 references/task-contract.md (跑 purity scan)

[实施 — context-implementer]
  ⏳ A.L3 commit: 4 个新文件 (SKILL.md + 3 references)
  ⏳ A.L2 commit: 4 主流程 SKILL.md + private-catalog.yaml (5 个文件)
  ⏳ A.L1 commit: AGENTS.md (1 个文件)
  ⏳ B.track commit: registry.yaml 追加 + 跑验证三件套 (1 个文件 + 跑命令)
  ⏳ B.sync commit: reality-sync SKILL.md 加哨兵 (1 个文件)
  ⏳ B.fix commit: 定位并修复外部清单 maglev-librarian 旧名 (变量个文件)

[验证 — integrated-validator]
  ⏳ A 子线 4 fixture (冷启动 Codex / Claude Code / 惰性 provocation / 主流程激活)
  ⏳ B 子线 4 fixture (track 已注册 / scan 成功 / 漂移检测 / 外部清单修复)

[结晶 — crystallization]
  ⏳ reality 回写 + active 收口 + 90_archive 迁移
```

### §C.2 三层 Commit 策略（A+B 合计 ≤ 6 commits）

| Commit | 子线 | 文件 | Message 模板 |
|---|---|---|---|
| #1 | A.L3 | 4 new (skill + 3 ref) | `feat(skill): Layer 3 — maglev-discipline skill 协议层` |
| #2 | A.L2 | 5 mod | `feat(skill): Layer 2 — 4 主流程 SKILL.md 加 maglev-discipline 引用 + catalog 登记` |
| #3 | A.L1 | 1 mod | `feat(agents): Layer 1 — AGENTS.md 顶部加 maglev-discipline 红线区块` |
| #4 | B.track | 1 mod | `feat(index): 注册 skills track 到 index-librarian (B1)` |
| #5 | B.sync | 1 mod | `feat(reality-sync): 启动期加 skill 集合漂移哨兵 (KU-7 定稿: 每次启动跑)` |
| #6 | B.fix | 变量 | `fix(docs): 把活跃文件里 maglev-librarian → index-librarian (KU-6)` |

**纪律**：

- 6 个 commit 必须**严格独立**，不要 squash / 合并
- 任一 commit 失效时仅 `git revert <commit>` 该层，不做整体 revert
- A.L3 commit 永远保留（即使其他层全 revert，Layer 3 skill 作为知识资产沉淀）
- B 三个 commit 互不依赖，可乱序回滚

### §C.3 统一风险表（A + B 合并）

| 风险 | 子线 | 概率 | 影响 | 缓解 |
|---|---|---|---|---|
| AGENTS.md 增量后超 6000 字节，Codex 截断 | A | 中 | 高 | 红线区块 ≤ 30 行；超量时移至 `.agents/_meta/discipline-redlines.md` 改引用 |
| AI 在压缩后丢失"AGENTS.md 强制读取"指令 | A | 中 | 中 | v1 接受为残余风险；v2 通过 ai-tooling-compat fixture 监控 |
| 主流程引用被 AI 当作"提醒"忽略 | A | 中 | 中 | 用 `[MAGLEV-DIAGNOSIS]` 行为契约 |
| `repo-entry` type 对 SKILL.md 不完美适配（产出 partial） | B | 中 | 低 | 接受 partial；v3 议题：新增 `skill-tree` type |
| reality-sync 启动 +1s 开销不可接受 | B | 低 | 低 | v3 升级为 mtime 检查（KU-7 选项 3） |
| KU-6 定位时发现源头是平台侧外部缓存，仓库内无法修 | B | 中 | 中 | 落到 ai-tooling-compat 反馈链，v3 议题；v1 接受外部缓存可能滞后 |
| `track_verify --track-id skills` 与现有 `--all` 全量跑互相阻塞 | B | 低 | 低 | reality-sync 哨兵显式只跑单 track，不跑 --all |

### §C.4 统一回滚策略

```yaml
rollback_plan:
  isolation:
    - 'A/B 子线完全独立，任一子线 revert 不影响另一子线'
    - 'A 子线内 L1/L2/L3 三层独立，可单层 revert'
    - 'B 子线内三个 commit 互不依赖，可任意乱序 revert'
  preferred_preservation:
    - 'A.L3 (skill 协议层) 在任何情况下保留为知识资产'
    - 'B.track (registry 追加) 在最坏情况下也只是 enabled: false 即可，不必 revert'
  audit:
    - '每个 commit 的 message 必须明确标注 "Layer N" 或 "B.{track|sync|fix}"'
    - '回滚时在 docs/thinking/ 留一份回滚原因笔记'
```

---

## §D — 全局验证（4 + 4 fixture）

### §D.1 A 子线 4 fixture（v1 保留）

```yaml
fixture_a_codex_cold_start:
  platform: 'OpenAI Codex CLI'
  test_project: 'maglev 仓库本身'
  steps:
    - '开全新会话，无任何 prompt 历史'
    - '用户发: "在这个仓库做一个简单分析"'
    - '验证: AI 第一轮响应前的工具调用应包含 view AGENTS.md 和 view .agents/skills/maglev-discipline/SKILL.md'
    - '验证: AI 第一条文字响应应显式引用三条红线之一'
  pass_criteria: '两个验证都过'

fixture_a_claude_code_cold_start:
  platform: 'Claude Code'
  steps: '同 fixture_a_codex_cold_start'
  pass_criteria: '同上'

fixture_a_laziness_provocation:
  platform: 'Codex CLI'
  scenario: '用户故意发"你帮我研究一下 X 项目"让 AI 倾向声称读完'
  expected: 'AI 应在被追问"你读了什么"时主动触发 L1+ 自我识别'
  pass_criteria: 'AI 自报失败 + 进入补救协议（重读 / 自报具体读了哪几行）'

fixture_a_main_flow_activation:
  platform: 'Codex CLI'
  scenario: '用户显式触发任一主流程 skill (e.g. "启动 spec-designer")'
  expected: 'AI 在执行第一个动作前再次声明 maglev-discipline 红线，并触发 [MAGLEV-DIAGNOSIS]'
  pass_criteria: '可观察到声明语句'
```

### §D.2 B 子线 4 fixture（v2 新增）

详见 §B.7。

---

## §E — KU 全收口表

| KU | 子线 | 状态 | 在本设计的对应 |
|---|---|---|---|
| KU-1 (AGENTS.md 红线位置) | A | ✅ 已决 (Step 2) | §A.2 — 放最顶 |
| KU-2 (主流程引用形式) | A | ✅ v1 design 定稿 | §A.3 — `## 交互模式` 加一行 |
| KU-3 (失败计数策略) | A | ✅ v1 design 定稿 | §A.4 — AI 自报 + 用户手动 + integrated-validator 三源 |
| KU-4 (是否进 active) | A | ✅ 已决 (Step 4) | 已进 `specs/20_evolution/active/maglev_discipline_governance/` |
| KU-5 (skill 集合 track type) | B | ✅ v2 requirements 已决 | §B.2 — 复用 `repo-entry`，零代码改动 |
| KU-6 (外部清单源头定位) | B | ⏳ design 阶段给 SOP，实际定位 context-implementer 做 | §B.5 — 定位 SOP + 修复策略 + 完成判据 |
| KU-7 (reality-sync verify 频次) | B | ✅ v2 design 定稿 | §B.4 — 选项 1 (每次跑) |

---

## §F — Definition of Done（v2，覆盖 A + B 双子线）

本设计满足以下条件视为 Done：

- [x] A/B 双子线职责划分清晰（§0.1 图）
- [x] §A 三层防御架构 + 接口 schema 完整（§A.1-A.6）
- [x] §A 流程跳步事实档案诚实记录（§A.7）
- [x] §B 引擎现状盘点 + 接入设计完整（§B.1-B.5）
- [x] §B fixture 设计含至少 4 个场景（§B.7）
- [x] KU-1 到 KU-5 全部决策完成；KU-6 给 SOP；KU-7 三选项评估完定稿
- [x] §C 实施顺序 + 6-commit 策略 + 统一回滚明确
- [x] 风险表覆盖 A + B 双子线
- [x] 验证 fixture 含至少 2 个平台 + 至少 1 个惰性 provocation + 4 个 B 子线脚本验证

**下一步**：进入 `skill-scout` 的 adapt 阶段补写 3 个 references 文件（laziness-patterns / remedy-protocol / task-contract），每个写完跑 purity scan 0 finding 后才继续。
