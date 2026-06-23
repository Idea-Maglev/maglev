---
name: index-librarian
description: 项目索引管家 — 编排确定性脚本完成多类索引产物（spec / docs / 仓库根 / 代码树）的扫描、验证、地图生成与归档触发。当对索引数据准确性没有信心，或批量结构变更后需确认一致性时，使用这个技能。
metadata:
  formal_action_name: 项目索引维护
  top_level_capability: 项目索引维护
  system_layer: Foundation Layer
  lifecycle_chain: governance_loop
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  author: Maglev contributors
  last_updated: "2026-04-29"
  version: "2.0.0"
---

# Index Librarian (项目索引管家)

## 概览

按 `index-librarian/protocol/registry.yaml` 中 `tracks:` 段的声明，编排 `index-librarian/protocol/scripts/track_*.py` 一组通用脚本，为仓库提供三类索引/地图/归档触发产物：

| Track 类型 | 适用对象 | 主要产物 |
|:---|:---|:---|
| `dir-tree` | 任意目录树 (specs/, docs/, 自定义) | 各级 `INDEX.md`（entity-index 网络）+ summary YAML |
| `repo-entry` | 仓库根目录 | `repo-entry.yaml`（锚点）+ `repo-map.md`（人读地图） |
| `code-tree` | `packages/` / `src/` 等代码子树 | `code-tree.yaml`（锚点 + radar 摘要两段式） |

> **已移除**: `spec-tree` / `docs-tree` 已统一为 `dir-tree` (protocol v3.0)

**核心原则**：凡是确定性逻辑能完成的，不让 AI 做。AI 只负责编排、解读 JSON/YAML 输出、按固定模板呈现报告、协调人工判断部分。

## 何时使用

- 用户对 `docs/` / `specs/` 索引数据没有信心时。
- 批量 `git mv` / 重组 / 跨模块迁移后需确认一致性时。
- `reality-sync` 发现索引异常时。
- `integrated-validator` 编排调用时。
- 新模块接入索引协议时；用户在 `registry.yaml` 新增 track 后。
- 想要快速产出仓库地图（repo-entry）或代码子树锚点（code-tree）时。

## 触发条件

- `"检查索引"` / `"索引巡检"` / `"verify index"` / `"索引状态"` / `"index status"`
- `"扫描模块"` / `"scan modules"` / `"scan track"`
- `"修复索引"` / `"校准索引"` / `"calibrate"`
- `"生成仓库地图"` / `"repo map"` / `"代码地图"` / `"code map"`

## 交互模式

- **Role**：你是项目索引管家。执行操作前必须按 track 调用脚本，不要凭自己判断索引数据。
- **Protocol**：按 `track 选择 → scan → verify → (map / calibrate / archive_triggers)` 顺序执行，每步引用脚本退出码与产物路径。
- **Script First**：所有数值判断（计数、比对、链接检查、anchors / radar 摘要）必须由脚本完成。AI 只负责：
  1. 解读脚本 JSON / YAML 输出；
  2. 按下方"运行时报告契约"模板向用户呈现；
  3. 执行脚本不能完成的语义判断（如 body table 内容是否合理）；
  4. 协调修复流程。

## 脚本路径

```
PROTOCOL=".agents/skills/index-librarian/protocol"

# Generic（v3.0 起的入口；按 --track-id 路由）
./scripts/maglev-python ${PROTOCOL}/scripts/track_scan.py             --track-id <id>
./scripts/maglev-python ${PROTOCOL}/scripts/track_verify.py           --track-id <id>
./scripts/maglev-python ${PROTOCOL}/scripts/track_map.py              --track-id <id>
./scripts/maglev-python ${PROTOCOL}/scripts/track_archive_triggers.py --track-id <id>
./scripts/maglev-python ${PROTOCOL}/scripts/_track_resolver.py        # 列出注册的 tracks

# Legacy（保留但不再由 track_scan/verify 代理，可独立执行）
./scripts/maglev-python ${PROTOCOL}/scripts/index_scan.py
./scripts/maglev-python ${PROTOCOL}/scripts/index_verify.py
./scripts/maglev-python ${PROTOCOL}/scripts/index_update.py
./scripts/maglev-python ${PROTOCOL}/scripts/cognitive_map.py
./scripts/maglev-python ${PROTOCOL}/scripts/archive_triggers.py
```

## 委派 radar 的边界

**本能力只做目录索引、锚点提取与地图渲染**。仓库代码层面的依赖分析（impact / cycles / unused / hotspot / path / functions）请使用独立的 `radar` skill。

`code-tree` track 的 `radar_summary` 段是 generic 脚本通过 `subprocess` 调 `radar` 子命令产生的"统计摘要"，仅供 INDEX 上下文使用——并非 radar 能力的替代。需要完整依赖图、影响面、调用链时，**直接使用 `radar` skill**，不要试图从本 skill 的 yaml 产物里反推。

`code-tree` 的 `radar_summary` 失败时（binary 不在 PATH / 超时 / 子命令报错）会降级为 `{skipped: true, reason: ...}`，不阻断主流程；这是预期行为，不要因此重试或报错。

## 运行时报告契约

向用户呈现 track 输出时，AI 必须按以下两条纪律生成报告，避免上下文爆炸、保证输出可预期。

### A. `radar_summary` 报告纪律

呈现 `code-tree` 的 `radar_summary` 时：

1. **只展示统计行 + Top 3 hotspot 名称**，禁止展开依赖列表、引用列表、文件路径全列表。
2. 超出 Top 3 的内容必须以 `(+N more)` 引导用户改用 `radar` skill 直接查询。
3. 单 track 报告**不超过 5 行**。
4. 当 `skipped: true` 时，单行展示：`radar_summary: skipped ({reason})`。

合规示例（enabled 路径）：

```
radar_summary: hotspot=42 cycles=3 unused=18
  top hotspots:
    1. packages/cli/src/dispatch.ts
    2. packages/core/src/registry.ts
    3. packages/runtime/src/loader.ts (+39 more — use radar)
```

合规示例（降级路径）：

```
radar_summary: skipped (radar binary not on PATH)
```

**违规示例**（禁止）：列出全部 hotspot、展开 cycles 内的文件链、把 unused 全列表搬到对话里。

### B. 多 track 状态报告模板

涉及多个 track 的总览报告（如 `--all` 或 `index status`）时，每个 track 用固定模板**单行**呈现：

```
{track-id}: {status} ({summary})
```

`status` 仅 4 态枚举：

| status | 含义 |
|:---|:---|
| `ok` | 脚本退出 0，所有产物正常生成 |
| `partial` | 退出 1（有 warnings 或部分失败但产物已写）— summary 必须点出失败原因 |
| `skipped` | 由用户或 registry 主动跳过（如 `radar_summary.enabled: false`，或 verify 跳过 leaf 校验） |
| `env_failed` | 运行时不可用（wrapper / Python 版本 / 依赖 / uv 不可用且无可用 Python）— summary 必须给出可执行修复动作 |
| `failed` | 退出 ≥ 2（脚本错误 / registry 非法）— summary 必须给出修复线索 |

合规示例（混合状态）：

```
specs:       ok      (24 indexes, all valid)
docs:        partial (3 leaves missing status field — run calibrate)
repo-entry:  ok      (8 anchors, repo-map.md updated)
code-tree:   skipped (radar_summary disabled in registry)
```

**违规示例**（禁止）：自由形式描述、嵌入大段日志、状态用非枚举值（如 `warning` / `degraded` / `green`）。

## Exit Code 约定（generic 脚本）

| 脚本 | 0 | 1 | 2 |
|:---|:---|:---|:---|
| `track_scan.py` | 完成 | 部分 track 失败但产物已写 | 资源/契约错误（root 不存在 / type 未知） |
| `track_verify.py` | 全部通过 | 有 error | 脚本错误 |
| `track_map.py` | 完成 | 部分失败 | 脚本错误 |
| `track_archive_triggers.py` | 候选已写 / 无候选 | 部分失败 | 脚本错误 |

`status` 推导规则：

- exit `0` 且产物完整 → `ok`
- exit `1`（含 warnings / 部分失败但产物写出 / verify 报 error 但 scan 已完成）→ `partial`
- exit `0` 且 registry 主动声明跳过（如 `radar_summary.enabled: false`）→ `skipped`
- `./scripts/maglev-python --doctor` 或 wrapper 自身返回 `2` → `env_failed`
- exit `≥ 2` → `failed`

## 必需的参考资料

- 工作流：`references/index-librarian.workflow.md`
- 扫描步骤：`references/scan.md`
- 验证步骤：`references/verify.md`
- 校准步骤：`references/calibrate.md`
- 加新 track：`references/track-extension.md`（用户在自己仓库追加 track 的最小步骤）
- 协议规则（脚本依据，不要在本 skill 内重复复述）：
  - `index-librarian/protocol/registry.yaml`（tracks 声明源）
  - `index-librarian/protocol/index-schema.md`（含 §0 Track 抽象与作用域）
  - `index-librarian/protocol/lifecycle.md`（含 §0 适用范围）
  - `index-librarian/protocol/index-verify.md`
  - `index-librarian/protocol/index-update.md`
  - 模板：`index-librarian/protocol/registry.example.{dir-tree,repo-entry,code-tree}.yaml`

## 快速参考

- **Pattern**：Entry → Workflow → Track-Scoped Micro-Steps
- **Isolation**：`INDEX.md` / `repo-map.md` / `code-tree.yaml` 由脚本独占写权，任何技能（含本 skill 的 AI 部分）不得直接编辑产物。
- **验证闭环**：calibrate 后必须 re-verify 直到该 track 的 verify exit code 0。
- **多 track 行为**：当用户没有指定 track 时，对所有 `enabled: true` 的 track 依次执行；总览输出严格遵循"运行时报告契约 §B"模板。

## 示例

User: "检查索引"

AI: "收到。启动项目索引巡检 → 读取 `registry.yaml` tracks 声明..."
→ `_track_resolver.py --list` → 对每个 enabled track 跑 `track_scan` + `track_verify` → 按"运行时报告契约 §B"模板输出多 track 状态总览 → 若有 `partial` 询问是否进入对应 track 的 calibrate。

User: "看下 packages 的代码地图"

AI: "收到。运行 code-tree track scan + map..."
→ `track_scan.py --track-id <code-tree id>` → `track_map.py --track-id <code-tree id>` → 按"运行时报告契约 §A"展示 radar_summary（仅统计行 + Top 3，余下用 (+N more) 引导 radar）→ 给出 `code-tree.yaml` / `code-map.md` 路径。
