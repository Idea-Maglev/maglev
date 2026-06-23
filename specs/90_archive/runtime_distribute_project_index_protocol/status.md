# Status

## 当前状态: Step 1-6 全部完成 / 综合验证 25✅+1⚠️ / 可进入 crystallization

## 综合验证报告 (integrated-validator 聚焦核验, 2026-04-29)

按 02_design v5.2 §6 (AC 矩阵) + §5 (行为对等性矩阵) 双维度验证。模式: 聚焦 finding 逐条核验 (与 v5.2 spec-audit 复审同范式), 不绕路 4 surface skill 全编排。

### A. AC 矩阵核验结果 (26/26 项)

| AC ID | 状态 | 证据摘要 |
|:---|:---:|:---|
| AC-F1-* | ✅ | Step 1 catalog `status: active` + `runtime_distribution: false` 落地; Step 5 物理废弃后路径已删 |
| AC-F2-1 | ✅ | `registry.yaml` `protocol_version: "2.0"` + `tracks:` 段 + 3 default tracks |
| AC-F2-2 | ✅ | 4 个 `track_*.py` 全部支持 `--track-id` 参数 |
| AC-F2-3 | ✅ | `_track_resolver.list_tracks()` 返回 3 实例 (specs / docs / repo-entry) |
| AC-F2-4 | ✅ | docs-tree 调 legacy index_*.py 行为不退化 (Step 4 矩阵 docs 行 4/4 ✅) |
| AC-F2-5 | ✅ | `track_scan.REPO_ENTRY_MAX_DEPTH=1` 硬约束 |
| AC-F2-6 | ✅ | `_scan_code_tree` 完整两段式实现 (anchors + radar_summary, C2.4) |
| AC-F2-7 | ✅ | `_track_resolver.list_tracks()` 读 registry.yaml；用户新增 track 立即可 resolve |
| AC-F2-8 | ✅ | 4 个 `registry.example.<type>.yaml` 文件全在 + SKILL.md 引用 |
| AC-F3-* | ✅ | `index-librarian/SKILL.md` v2.0 重写 (C3.1) |
| AC-F4-* | ✅ | 行为对等性矩阵 12 格全 ✅, 见下方 §B |
| AC-F5-* | ✅ | `maglev-librarian/` 目录 / workflow / smart_map.py 全部不存在 (Step 5) |
| AC-F6-* | ⚠️ | `step1b_verify_distribution_scope` + `step3b_split_catalog` 已 wired 并单元冒烟 OK; 但 **dry-run install 端到端未实测** (npm 发版前依赖真实流水线才能验证). 主路径无回退风险, 列为低优先级 follow-up |
| AC-F7-* | ✅ | `_track_resolver.REQUIRED_FIELDS` + `KNOWN_TYPES`; 非法 type 'warn + skip', 缺字段 ValueError; `track_scan.REPO_ENTRY_MAX_DEPTH=1` |
| AC-F8-* | ✅ | `registry.example.code-tree.yaml` 含 `radar_summary.{hotspot_top, max_output_lines}` per-track 阈值 |
| AC-F9-* | ✅ | `scripts/check_runtime_distribution.py` 存在; 当前 repo exit 0; 故意构造泄漏 dist exit 1 |
| AC-F10-* | ✅ | installer 输出未改; SKILL.md v2.0 不主动 banner |
| AC-F11-* | ✅ | 上游 `docs_knowledge_archival_methodology/02_design.md` 已加 K2 修订段 (2026-04-28) |
| AC-F12-1 | ✅ | `_scan_code_tree` 写出 `anchors:` 段 |
| AC-F12-2 | ✅ | `_code_tree_helpers.invoke_radar_summary` subprocess 调 radar + max_output_lines 截断 |
| AC-F12-3 | ✅ | except 兜底降级 `{skipped: True, reason}` (D26); C2.4 冒烟: radar 不在 PATH 时落盘 `reason: 'hotspot: radar binary not on PATH'` |
| AC-F12-4 | ✅ | `DEFAULT_IGNORE_DIRS` / `DEFAULT_ANCHOR_FILES` / `DEFAULT_MAX_DEPTH=5` / `DEFAULT_MAX_LINES=200` 继承自 smart_map.py |
| AC-F12-5 | ✅ | default 3 tracks 中无 `type: code-tree` |
| AC-F12-6 | ✅ | SKILL.md §"委派 radar 的边界（AC-F12-6）"段存在 |
| AC-F12-7 | ✅ | `REPO_ENTRY_MAX_DEPTH=1` + `DEFAULT_MAX_DEPTH=5` 双约束 |
| AC-F12-8 | ✅ | SKILL.md §"radar_summary 报告纪律" + "(+N more)" + ≤5 行约束 |
| AC-F12-9 | ✅ | SKILL.md §"多 track 状态报告模板" + 4 态枚举 (ok/partial/skipped/failed) |

**汇总**: 26 项 AC, **25 ✅ + 1 ⚠️**, 0 ❌

### B. 行为对等性矩阵 (default 3 实例 × 4 维度)

复用 Step 4 验证记录 (HEAD `25b92b1` 实测; 见下方 "Step 4 验证记录" 段):

- specs (spec-tree): 4/4 维度 ✅ (scan 0 wrote 62 items / verify 0)
- docs (docs-tree): 4/4 维度 ✅ (scan 0 / verify 0, 6 nodes checked)
- repo-entry: 4/4 维度 ✅ (scan 0 8 anchors / verify 0 / map 0 47 entries; D10 行为合并通过)

**12/12 ✅, D15 强制 Gate 已达成**。

### C. Findings 汇总

| 级别 | 数量 | 描述 |
|:---|:---:|:---|
| 🔴 Critical | 0 | — |
| 🟡 Major | 0 | — |
| 🟢 Minor | 1 | AC-F6 dry-run install 端到端未实测 (依赖真实 NPM 发版流水线) |
| ℹ️ Info | 0 | — |

### D. 主题闭环判定

- 26 AC 中 25 ✅ + 1 ⚠️ Minor (非阻塞)
- 12 行为对等格全 ✅ (D15 Gate)
- 静默基建合规 (§7) 全 ✅
- 主题分支累积 12 commits 已 push 备份

**结论**: 主题已具备 crystallization 条件; AC-F6 follow-up 不阻塞主线闭环, 留作 Step 6 真发版时验证.

---

## Step 4 验证记录 (行为对等性矩阵 Gate, 2026-04-29)

按 02_design v5.2 §5 矩阵实测 default track set 3 实例 × 4 维度 = 12 格，全部 ✅ pass：

**实测命令与产物**（在 `feat/runtime-distribute-impl` 分支，HEAD = `edf5584`）：

| Track | scan | verify | map（如适用） | 产物 |
|:---|:---|:---|:---|:---|
| `specs` (spec-tree) | exit 0，wrote 62 items | exit 0，ok | — | `specs/_meta/index.yaml` |
| `docs` (docs-tree, 调 legacy) | exit 0 | exit 0，6 nodes checked | — | docs 旧索引网络（兼容） |
| `repo-entry` | exit 0，8 anchors（修隐藏目录漏扫后） | exit 0，5 patterns 信息态零匹配 | exit 0，47 entries | `.agents/_meta/repo-entry.yaml` + `.agents/_meta/repo-map.md` |

**关键观察**：
- 12 格全 ✅，达到 D15 强制 gate（"default track set 3 实例对等性矩阵全 pass 后才允许 Step 5"）
- D10 行为合并（smart_map → track_map type=repo-entry）实测通过，输出 47 entries markdown 风格地图与 smart_map.py 行为对等
- `code-tree` 不在 default 3 实例之内（Step 4 不强制覆盖），但已在 C2.4 完成 disabled / enabled+无 radar 两路径冒烟
- 实测产物为运行时副作用，未纳入仓库（Step 5 / 6 上线时再统一决策）

**Implementer 进展（commits on `feat/runtime-distribute-impl`）**：

| Step | Commit | 摘要 |
|:---|:---|:---|
| Step 1 | `3890a0f` (已 FF master) | 撤回 maglev-librarian DEPRECATED 标签 |
| Step 2 C2.1 | `2fe93b3` | registry.yaml v2.0 + 4 example 模板 |
| Step 2 C2.2 | `dcbb0d7` | `_track_resolver.py`（list/resolve/get_modules + 诊断 CLI） |
| Step 2 C2.3 | `e07b37a` | 4 个 generic `track_*.py` 骨架 |
| Step 2 C2.4 | `6e10435` | `_scan_code_tree` 完整 + `_code_tree_helpers.py` + repo-entry 隐藏目录漏扫修复 + smart_map 行为合并到 `track_map(repo-entry)` |
| Step 2 C2.5 | `adcf7bd` | `index-schema.md` §0 + `lifecycle.md` §0 Track 抽象作用域 |
| Step 3 C3.1 | `0f68871` | `index-librarian/SKILL.md` v2.0 重写（D27 报告契约 + 委派 radar 边界） |
| Step 3 C3.2 | `edf5584` | `index-librarian/references/track-extension.md`（用户加 track 最小指南） |
| Step 4 | _本 commit_ | §5 矩阵 ⏳ → ✅ + status.md 验证记录 |

**Gate 决策**：Step 5 解锁——可进入 maglev-librarian 物理废弃（删 skill 目录 / workflow / catalog 条目 / `smart_map.py`）。

---

## v5.2 修订记录 (consistency fix, 2026-04-28 晚)

经 spec-audit-surface 审计（综合 72/100，最低维度一致性 55/100），按 4 Critical + 6 Major findings 完成机械同步：

- **frontmatter 滞后**：3 份 spec frontmatter `revision` 字段全部从 `v4 (generic track abstraction)` 升到 `v5.2 (consistency fix)`
- **00_intent 标题号重号**：原 §4 与 §5 重号 → 章节号统一推后（§5 上游证据 / §6 上下文锚点 / §7 成功判据 / §8 设计原则 / §9 与上游主题的关系 / §10 与 radar 的关系）；§4 子号同步从 4.1~4.4 改为 5.1~5.5
- **In/Out Scope 自相矛盾**：00_intent §4 第 6 条 / 01_requirements §5 第 7 条 / 02_design §9 OoS 关于代码分析的措辞改为"不实现完整 AST/调用图深度分析；仅以摘要形式 subprocess 调 radar"，与 v5+v5.1 In Scope 兼容
- **02_design §6 AC mapping 残缺**：补 AC-F2-8 / AC-F12-5/6/7/8/9 共 6 条；同时修正 AC-F12-1/2 的指向（v4 "delegate_to 分支 D7" → v5 "_scan_code_tree 函数 / _invoke_radar_summary"）
- **02_design §7 静默基建合规**："不侵入代码"行从 v4 "type=code-tree → delegate radar（D7）" 改为 v5/v5.1 "防爆参数+radar 摘要截断（D7/D24/D25/D26）"
- **02_design §4 实施顺序**：在 Step 2 加 example 模板（D28/AC-F2-8）、`_scan_code_tree` 函数（D24/D25/D26）；在 Step 3 加 SKILL.md 报告契约 + 状态模板段（D27/AC-F12-6/8/9）
- **02_design Context Trace footer**：v4 段更新为 v5/v5.1/v5.2 完整轨迹

无新增决策、无 AC 语义变更——仅消除 v4 → v5/v5.1 修订时未回流的衍生不一致。

## v5.1 修订记录 (runtime AI 行为护栏, 2026-04-28 晚)

### 修订背景

- 用户审计：「v5 是否会过度复杂化导致 AI 助手无法真实执行——指的不是 spec 复杂度，而是索引能力本身的运行时复杂度」
- 评估发现：脚本独占写权已剥离确定性逻辑（runtime 执行层 AI 不会跑不动），但仍有两个 runtime AI 行为风险：
  - **schema 字段过多（10+）**：AI 现场帮用户写 track config 容易出错
  - **radar_summary 诱导上下文爆炸**：AI 倾向逐个展开 hotspot/unused 列表
  - **多 track 状态机混合**：AI 自由组织文字易丢状态信息

### v5.1 升级核心

- 在 v5 基础上增加 **runtime AI 报告契约**（SKILL.md 层强制）：
  - radar_summary 段：统计行 + Top 3 + "(+N more)"，禁止展开
  - 多 track 状态：4 态枚举（ok/partial/skipped/failed）+ 固定模板
- 增加 **track config example 模板**：每 type 一份 `registry.example.<type>.yaml`，AI 抄而非现场写

### v5.1 新增决策

- **D27**：runtime AI 报告契约（radar 摘要不展开 + 多 track 状态固定模板）
- **D28**：每 type 一份 example 模板，避免 AI 现场写 schema 出错

### v5.1 新增 AC

- **AC-F2-8**：4 个 example 模板文件存在 + SKILL.md 引用
- **AC-F12-8**：SKILL.md 含 "禁止展开 radar 详细列表" 段 + ≤ 5 行报告示例
- **AC-F12-9**：SKILL.md 含 4 态状态枚举 + 报告模板

## v5 修订记录 (code-tree pivot, 2026-04-28 晚)

### 修订背景

- 用户审计：「需要识别下 radar 是否胜任当前的任务」
- 评估发现：radar 子命令（impact / hotspot / unused / cycles / path / analyze）输出**依赖图（图论视角）**，而 protocol 的 4 动作（scan / verify / archive_triggers / map）输出**索引清单（清单视角）**——两者不是替代关系
- **关键事实**：maglev-librarian 在代码层**从未有过 AST 能力**——Track A 是 Spec Curator (specs/)、Track B 是 Thought Organizer (docs/)、Track C 是 Cartographer (`smart_map.py` 只扫仓库根目录锚点)，因此 code-tree 是 v5 的绿地新增能力，没有遗产包袱
- 用户最终诉求：「就让 radar 做索引创建的辅助执行看看是否可以，主要还是靠索引技能本身的能力，只是对于代码场景要注意上下文爆炸的问题」

### v5 升级核心

- **角色翻转**：radar 从 v4 的"范式替代者（protocol 退出）"翻转为"辅助执行器（protocol 主导 + 调用 radar 拉摘要）"
- **code-tree 主导执行**：generic 脚本支持 type=code-tree，scan 输出两段式 yaml：`anchors:`（必出，复刻 smart_map.py 锚点逻辑）+ `radar_summary:`（可选，subprocess 调用 radar 摘要后截断）
- **核心约束细化**：从 v4 的"不侵入代码"细化为"防上下文爆炸"——继承 smart_map.py 防爆参数（IGNORE_DIRS / MAX_DEPTH=5 / MAX_LINES=200 / ANCHOR_FILES）+ radar 摘要按 `max_output_lines` 截断
- **容错降级**：radar 不可用时降级为仅 anchors 段，记录 skipped + reason，不阻断后续 track

### v4 → v5 决策修订

| 决策 | v4 | v5 |
|---|---|---|
| **D7** delegate_to: radar 实现 | 文档建议 + exit 0，不 subprocess invoke | radar 作辅助执行器，subprocess invoke 拉摘要，protocol 主导 4 动作 |
| code-tree 行为 | 退出场景（"该 track 由 radar 处理"提示） | 主动支持的 track type，输出两段式 yaml |
| F12 语义 | radar 边界划分 | radar 调用规范 + 防爆参数 + 容错降级 |

### v5 新增决策

- **D24**：code-tree scan 输出形态——两段式 yaml（`anchors:` 必出 + `radar_summary:` 可选）
- **D25**：code-tree 防爆参数继承 `scripts/smart_map.py` 现有常量（IGNORE_DIRS / ANCHOR_FILES / MAX_DEPTH=5 / MAX_LINES=200）
- **D26**：radar 调用容错——binary 不存在/超时/版本不兼容时降级为仅 anchors 段 + skipped 记录 + warn

### v5 AC 修订

- F12 重写为 7 条 AC（v4 4 条）：从边界划分变为调用规范 + 防爆 + 容错

### v5 设计观察记录

- **m maglev-librarian Track C `smart_map.py` 行为**：用 `os.walk` 平铺；IGNORE_DIRS 排除 `node_modules/.git/dist/build/.venv` 等；ANCHOR_FILES 识别 `package.json/pom.xml/go.mod/Cargo.toml/requirements.txt/README.md/Dockerfile/Makefile`；DEFAULT_MAX_DEPTH=5，DEFAULT_MAX_LINES=200；不做 AST，不做依赖图——v5 把这套防爆模式作为 code-tree 默认值。
- **radar 能力面（v0.4.0）**：impact/functions/cycles/unused/hotspot/path/analyze 7 个子命令；输出依赖关系图；Java/Vue 函数级不支持需降级为文件级；total_affected>30 需收窄 depth；vendor/node_modules 必须排除——v5 在 code-tree 调用 radar 时遵循这些约束。
- **职责对齐**：scan 主体责任 = protocol（输出索引清单 yaml）；radar 提供子能力调用（hotspot Top N / unused 计数 / cycles 计数）作为摘要段，不让 radar 独立输出索引。

## v4 修订记录 (generic track abstraction, 2026-04-28 下午)

### 修订背景

- v3 写死 Track A=specs/ B=docs/ C=repo-entry，按 maglev-librarian 当前能力镜像设计
- 用户审计：「索引机制是一个公共能力，不是为某个目录服务的能力」
- 用户进一步约束：「可以对任何目录对象都跑，但要限制范围避免浪费；对代码不要侵入，必要时借助 radar 技能；只对仓库根目录追加索引，不深入二级代码目录」

### v4 升级核心

- **抽象升级**：从硬编码三 Track 改为 `registry.yaml` 声明式 `tracks:` + generic 脚本（`track_*.py`）按 `--track-id` 参数化执行
- **默认窄范围**：default track set 仅声明 specs/docs/repo-entry 三个；用户加 track 是显式动作
- **不侵入代码**：repo-entry track depth_limit=1 硬约束；type=code-tree 时委派 radar
- **与 radar 边界明确**：track schema 支持 `delegate_to: radar` 字段；index-librarian SKILL.md 显式声明边界

### v3 → v4 决策修订

| 决策 | v3 | v4 |
|---|---|---|
| 脚本架构 | 三 Track 各写独立脚本（spec_index_scan / index_scan / repo_map） | generic 4 脚本（track_scan/verify/archive_triggers/map）按 type 分支 |
| smart_map.py | 迁移到 `_internal/.../scripts/repo/repo_map.py` | 行为合并到 `track_map.py(type=repo-entry)` |
| Track A 脚本 | 新写 3 个独立 spec_index_* | 由 track_*.py 在 type=spec-tree 时实现 |
| 兜底 helper | 不抽（v3 D12） | 抽 `_track_resolver.py` 共用（v4 D22） |
| 代码扫描 | 未明确 | 明确委派 radar，本机制不实现 |

### v4 新增决策

- **D4**：track schema 必填 3 字段（id/type/root），可选 5 字段
- **D5**：default track set = specs+docs+repo-entry 3 个
- **D6**：用户可禁用 default（覆盖式合并）
- **D7**：delegate_to: radar 仅文档建议，不 subprocess invoke
- **D8**：repo-entry depth_limit=1 硬约束
- **D9**：legacy 6 docs 脚本保留作 backing
- **D16**：用户 registry.yaml 与默认覆盖式合并
- **D17**：track schema 启动时校验

### v4 新增 AC

- AC-F2-1~7：通用 track 抽象 + default track set
- AC-F12-1~4：与 radar 边界

## v3 修订记录 (PR-A scope expansion, 2026-04-28 上午)

（v3 历史保留作溯源）

- 主题目录 rename：runtime_distribute_docs_index_protocol → runtime_distribute_project_index_protocol
- 主题分支同步 rename
- v3 边界：完整替代 maglev-librarian 三 Track + 分发；行为对等性矩阵作 Step 5 强制 gate
- 上游 K2 修订标注（不改决策正文）

## 开题事实

- 开题日期: 2026-04-27
- v3 修订: 2026-04-28 上午
- v4 修订: 2026-04-28 下午
- 当前分支: `feat/runtime-distribute-project-index-protocol`
- 触发: 上一会话用户质询"这套是否 maglev 用户共用" → 本会话两轮对抗性审计 + 用户 v4 通用化诉求

## v4 已收敛产物

- `00_intent.md` v4: 主题边界 + 设计护栏（默认窄范围/不侵入代码/委派 radar）+ Step 1-6 锚点 + §9 与 radar 关系
- `01_requirements.md` v4: F1-F12 共 12 个功能需求；F2/F3/F7 重写为通用化语义；新增 F12（与 radar 边界）；术语表加 track / default track set / generic 脚本概念
- `02_design.md` v4: 9 节技术设计；D1-D23 共 23 项决策；§1.2 default track set YAML 示例；§3.2.2 generic 脚本 main 入口示例；§5 行为对等性矩阵在 default 3 实例上验证

## v4 实施顺序（Step 1-6）

```
Step 1: 撤回 maglev-librarian deprecated 标签 + 上游 K2 修订标注
Step 2: registry.yaml 引入 tracks: + default track set + 4 个 generic track_*.py + _track_resolver.py + smart_map.py 行为合并
Step 3: index-librarian SKILL.md 重写为 generic 编排 + 委派 radar 边界
Step 4: 行为对等性验证矩阵（default 3 实例 × 4 维度）填充并全 pass
Step 5: 物理废弃 maglev-librarian + smart_map.py wrapper 删除
Step 6: release.py step1b/3b + check_runtime_distribution.py + catalog 字段补齐
```

## 已知关键事实

- catalog 中 15 个 `distribution_scope: 'runtime_internal'` 对象当前**全部错误曝光**
- 其中 `maglev-librarian` 当前标 deprecated（需 Step 1 撤回）
- `index-librarian` 当前仅基于 docs-index-protocol 6 脚本（全聚焦 docs/）
- `maglev-librarian` 自带 `scripts/smart_map.py`（v4 D10：行为合并到 track_map.py）
- `packages/maglev-cli/runtime-src/` 下无 `.agents/`，installer 实际未分发任何 skill
- installer file-by-file 模型，零改动可承接本主题
- radar skill 已存在；本主题不重叠

## 下一步

1. ~~context-implementer 接手 02_design v4，按 §4 实施顺序 Step 1 起步~~ ✅ Step 1-3 完成
2. ~~每 Step 完成后更新本 status.md 的对应进度~~ ✅
3. ~~Step 4 完成时在 status 加"Step 4 验证记录"段（行为对等性矩阵填充结果）~~ ✅ 见上方"Step 4 验证记录"段
4. **Step 5（物理废弃 maglev-librarian）— 已解锁**：删 skill 目录 / workflow / catalog 条目 / `scripts/smart_map.py`；改 issues 中 3 处 live 引用
5. **Step 6（release.py 修齐 + 用户分发）**：`maglev_release.py` 三处改造 + 新增 `check_runtime_distribution.py` + catalog `path:` 字段补齐
6. Step 6 完成时由 integrated-validator 按 AC 矩阵 + 行为对等性矩阵双重验证
7. 完成后由 crystallization 回写 reality；同时回写上游主题 K2 修订关系；主题分支 MR 合入 master

## 仍开放的次级风险（02_design §8 R1-R11）

R1 PyYAML 依赖 / R2 用户 registry.yaml 冲突 / R3 catalog 双职责 / R4 schema 字段过多 / R5 用户禁用 default / R6 用户期望扫代码被 radar 拒 / R7 generic 脚本 implementation 量 / R8 depth_limit 过严 / R9 对等性矩阵长时间 partial / R10 上游 K2 误解 / R11 周期与发布节奏冲突

