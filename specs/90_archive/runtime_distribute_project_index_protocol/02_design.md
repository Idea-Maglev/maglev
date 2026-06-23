---
status: draft
opened_at: 2026-04-27
last_revised_at: 2026-04-28
revision: v5.2 (consistency fix)
mode: tech_design
upstream:
  - 00_intent.md
  - 01_requirements.md
---

# 02 设计：runtime_distribute_project_index_protocol

> 👤 **Executive Brief**
>
> **做什么**：让 `index-librarian` + 协议脚本演进为**通用项目级索引能力**——`registry.yaml` 声明式 `tracks:`、generic 脚本（`track_*.py`）按 track-id 参数化执行、maglev 仓库声明 default track set（specs/docs/repo-entry depth=1）、用户可在自己 registry.yaml 加 tracks。完成对等性验证后废弃 maglev-librarian，随 install 分发到用户。
>
> **核心 Trade-off**：放弃"硬编码三 Track"（v3 设计已被用户否决——索引是公共能力）；放弃"主动扫整仓库"（默认窄范围）；放弃"自己实现代码扫描"（委派 radar）；坚持"零改动 installer"；坚持"先补齐再废弃"。
>
> **显性风险**：①track schema 字段集（U-V4-1）需克制——过多字段=用户上手成本高；②default track set 的"specs/docs/repo-entry"在用户项目可能不全适用（用户可能没 specs/）—— generic 脚本必须对缺失 root 静默；③v5 的 code-tree 设计（D7/D24/D25/D26）引入 subprocess invoke radar，需要 radar binary 可用性保障（见 U-V5-1）；④v4 把 v3 的 "spec_index_scan / repo_map" 等具名脚本通通改为 `track_*.py` generic 形态，前向 implementer 工作量比 v3 略小但抽象层更高。

---

## 1. 架构判断 (Architecture Verdict)

### 1.1 通用 track 模型

| 概念 | 定义 |
|---|---|
| **track** | 一个声明式可索引对象，由 registry.yaml 中 `tracks:` 列表的一项描述 |
| **track schema 必填字段** | `id` / `type` / `root` |
| **track schema 可选字段** | `patterns` / `output` / `thresholds` / `depth_limit` / `delegate_to` |
| **default track set** | maglev 仓库 registry.yaml 预置的 3 个 track 实例：specs / docs / repo-entry |
| **generic 脚本** | `track_scan.py / track_verify.py / track_archive_triggers.py / track_map.py`，按 `--track-id` 参数化 |

### 1.2 default track set 示例

```yaml
# .agents/skills/_internal/docs-index-protocol/registry.yaml (maglev 自身)
tracks:
  - id: specs
    type: spec-tree
    root: specs/
    output: specs/_meta/index.yaml
    patterns: ["**/00_intent.md", "**/01_requirements.md", "**/02_design.md", "**/status.md"]
    thresholds:
      archive_age_days: 180

  - id: docs
    type: docs-tree
    root: docs/
    output: docs/_meta/index.yaml
    thresholds:
      archive:
        inactivity_days: 365
        inbound_link_min: 1
      cognitive_map:
        weak_link_threshold: 2

  - id: repo-entry
    type: repo-entry
    root: .
    depth_limit: 1
    patterns: ["README.md", "AGENTS.md", "llms.txt", "CHANGELOG.md", "package.json", "*.toml"]
    output: .agents/_meta/repo-entry.yaml
```

用户可在自己 registry.yaml 追加：

```yaml
tracks:
  - id: research
    type: docs-tree
    root: research/
    output: research/_meta/index.yaml
  - id: my-code
    type: code-tree
    root: src/
    output: src/_meta/index.yaml
    radar_summary:           # 可选：开启则调用 radar 获取摘要
      enabled: true
      hotspot_top: 10
      include_unused: true
      include_cycles_count: true
      max_output_lines: 200  # 摘要段截断阈值（防爆）
    ignore: [node_modules, dist, vendor]   # 覆盖默认 IGNORE_DIRS
```

### 1.3 改动半径

| 维度 | 选择 | 不选 |
|---|---|---|
| installer 端 | **零改动** | 不重构 manifest |
| release 端 | **改 1 个脚本** + 新增 step1b/step3b | 不引入独立打包工具 |
| `_internal/docs-index-protocol/` 物理命名 | **保留**（C 路径） | 不重命名 |
| 脚本架构 | **generic 4 脚本**（`track_*.py`），现有 6 docs 脚本视情况收编为 backing 或保留 | 不写 per-track 独立脚本 |
| Track A/C 实现 | **新写 generic 脚本支持 spec-tree / repo-entry 两种 type** | 不复制 docs 脚本改名 |
| smart_map.py 处置 | 仓库根 `scripts/smart_map.py` 行为合并到 `track_map.py`（type=repo-entry 时） | 不保留独立脚本 |
| catalog | **生成双视图**（full / user_visible） | 不维护两份源 |
| 阈值配置 | **per-track 在 registry.yaml 内** | 不引 CLI flag |

---

## 2. 关键设计决策 (Decisions)

| ID | 决策点 | 选择 | 理由 |
|---|---|---|---|
| **D1** | Step 1 撤回 deprecated 状态字段值 | `status: active` + `runtime_name_status: canonical_name_active` + SKILL.md 注释加 "replacement in progress"；catalog 加 `runtime_distribution: false` 字段（D8 配套） | 干净恢复；Step 1-5 期间精确控制 |
| **D2** | 协议命名（U-PR1） | **C 路径**：物理命名保留 `_internal/docs-index-protocol/`，schema 文档显式声明作用域扩为通用 | 零引用迁移；连续性优先 |
| **D3** | 脚本架构（v4 升级核心） | **generic 4 脚本** `track_scan.py / track_verify.py / track_archive_triggers.py / track_map.py`，按 `--track-id` 从 registry.yaml 读配置；现有 6 个 docs 脚本视情况收编（合并入 generic 或保留作 type=docs-tree backing） | v4 通用化的根本——索引脚本 type-aware 而非目录-aware |
| **D4** | track schema 字段（U-V4-1） | **必填 3 字段**：`id` / `type` / `root`；**可选 5 字段**：`patterns` / `output` / `thresholds` / `depth_limit` / `delegate_to`；type 枚举值：`spec-tree` / `docs-tree` / `repo-entry` / `code-tree`（其他 type 视为 unknown，generic 脚本 warn + skip） | 字段克制；type 枚举可控 |
| **D5** | default track set 内容 | **3 个**：specs（spec-tree）/ docs（docs-tree）/ repo-entry（repo-entry depth=1） | 覆盖 maglev-librarian 三 Track 职责；不预置代码 track |
| **D6** | 用户禁用 default track（U-V4-2） | 允许——用户 registry.yaml 中可以 override `tracks:` 整段；或单 track 加 `disabled: true` 字段（D4 可选字段补充）；但默认 track set 是 maglev 仓库声明的，用户清空只影响用户侧 | 不强加默认；用户掌控 |
| **D7** | `code-tree` 与 radar 的关系（v5 推翻 v4） | **radar 作辅助执行器**：generic 脚本主导 code-tree 4 动作，必要时 subprocess invoke radar 子命令拉取摘要（hotspot/unused/cycles），不让 radar 输出原始大结果，protocol 自己做摘要落盘；radar binary 缺失时降级为仅输出锚点导航 + warn | 索引主体仍由 protocol 承担；radar 解决的是"代码场景下不重写依赖分析"，不是范式替代 |
| **D8** | repo-entry track 的 depth_limit | **硬约束 depth_limit=1**：generic 脚本对 type=repo-entry 强制只扫第一层，patterns 限定为元数据文件 | 不侵入代码 |
| **D9** | maglev-librarian 6 docs 脚本去留 | **保留**作 type=docs-tree 的 backing 实现；track_*.py 在 type=docs-tree 时调用现有 cognitive_map.py / archive_triggers.py 等；保护 docs_knowledge_archival_methodology 主题已落地能力 | 行为不退化 |
| **D10** | smart_map.py 迁移路径（v3 D4 推翻） | **行为合并**进 `track_map.py`（type=repo-entry 时的实现），不保留独立 `smart_map.py` | generic 化收口 |
| **D11** | release.py 如何识别 runtime_internal | 从 catalog 读 `distribution_scope: 'runtime_internal'` 且 `status != 'deprecated'` 且 `runtime_distribution !== false` 的条目 | 单一事实来源 |
| **D12** | user 侧 catalog 是否曝光 runtime_internal | release 装配时生成 user_visible 版本，剔除全部 runtime_internal 条目 | 装但不列 |
| **D13** | 一致性校验 | release.py 新增 `step1b_verify_distribution_scope`；同时独立 `scripts/check_runtime_distribution.py` | 内置 + CI 双保险 |
| **D14** | 行为对等性"通过"定义（U-PR5） | "覆盖等价能力 + 输出可被相同消费方读取"，不要求 byte-identical | 工程可达成 |
| **D15** | Step 5 物理废弃门槛 | **default track set 3 实例对等性矩阵全 pass** 后才允许 | 强制 gate |
| **D16** | 用户 registry.yaml 与默认合并策略 | **覆盖式**：用户 `tracks:` 段完全替换 default；用户如要保留默认需自行复制 | 简单可预期；避免"幽灵 track" |
| **D17** | track schema 校验时机 | release.py 与 generic 脚本启动时各做一次（必填字段检查 + type 枚举检查 + root 路径合法性）；schema 错误立即 fail-fast | 防止用户配错沉默通过 |
| **D18** | 多 track 串行还是并行 | **串行**（按 registry.yaml 声明顺序）；单 track 失败不阻断后续 | 简单；输出可读性优先 |
| **D19** | track 的 output 路径冲突检测 | release.py & generic 脚本：检测多 track output 路径相同时 warn；用户自负责 | 不做强约束 |
| **D20** | 上游 K2 修订形式（F11） | 仅在上游 02_design 与 status 加修订标注，不改决策正文；标注指向本主题 | 跨主题最小耦合 |
| **D21** | 用户已有 catalog/registry.yaml 冲突 | 复用 installer 现有 `.local_backup_<ts>` 备份机制 | 不新造冲突策略 |
| **D22** | 脚本兜底是否抽象 helper | 抽出 `_track_resolver.py`（读 registry.yaml / 验证 schema / 返回 track config）；4 个 track_*.py 共用 | v4 通用化下助手函数复用价值高，与 v3 D12 决策反向 |
| **D23** | track root 缺失时 exit code | exit 0（缺基础设施 ≠ 错误）；其他真错误才非零 | 静默基建 |
| **D24** | code-tree scan 输出形态（v5 新增） | 两段式 yaml：`anchors:` 段（锚点文件列表 + 目录树，复刻 smart_map.py 锚点逻辑）+ `radar_summary:` 段（hotspot Top N / unused 计数 / cycles 计数，调用 radar 获取并截断）；摘要段在 track config 未启用 radar_summary 时省略 | 锚点导航是 librarian Track C 已验证范式；radar 摘要是新增能力，按需开启避免上下文爆炸 |
| **D25** | code-tree 防爆参数（v5 新增） | 复用 `scripts/smart_map.py` 现有常量作 generic 默认：`IGNORE_DIRS={node_modules,.git,.idea,.vscode,__pycache__,dist,build,coverage,.venv,venv}`、`ANCHOR_FILES={package.json,pom.xml,go.mod,Cargo.toml,requirements.txt,README.md,Dockerfile,Makefile}`、`MAX_DEPTH=5`、`MAX_LINES=200`；track config 可在 `radar_summary.{hotspot_top,max_output_lines,...}` 字段细化 | 已有验证过的防爆模式 + 配置可观测 |
| **D26** | radar 调用容错（v5 新增） | radar binary 不存在/版本不兼容/分析超时 → generic 脚本降级为仅输出 anchors 段 + 在 yaml 输出中记录 `radar_summary: { skipped: true, reason: "..." }` + warn；不阻断后续 track 执行 | radar 是辅助不是依赖；保持 generic 脚本可在无 radar 环境工作 |
| **D27** | runtime AI 报告契约（v5.1 新增） | `index-librarian/SKILL.md` 固定两条报告纪律：①`radar_summary` 段仅展示统计行 + Top 3 hotspot 名称，禁止展开依赖列表，超出部分以 "(+N more)" 引导用户直接用 radar；②多 track 状态用固定模板 `{track-id}: {status} ({summary})`，status 仅 4 态（ok/partial/skipped/failed） | 防止 AI 助手在 runtime 解读时上下文爆炸；输出可预期 |
| **D28** | track 配置 example 模板（v5.1 新增） | 每 type 提供 `registry.example.<type>.yaml` 模板（4 个文件），SKILL.md 引用其路径；AI 帮用户新增 track 时**复制 example 后修改**，而非凭记忆写 schema | 字段过多（10+）易出错，模板抄写降低 AI 写错风险 |

---

## 3. 组件改动清单 (Component Diff)

### 3.1 Step 1 — 撤回 maglev-librarian deprecated 标签（与 v3 一致）

| 文件 | 改动 |
|---|---|
| `.agents/private-catalog.yaml` | `maglev-librarian.status: active`；`runtime_name_status: canonical_name_active`；新增 `runtime_distribution: false` |
| `.agents/skills/maglev-librarian/SKILL.md` | metadata `runtime_name_status: canonical_name_active`；正文段改为 "🔄 替代进行中" |
| `.agents/skills/index-librarian/SKILL.md` | relations.replaces 语义从"已替代"调到"替代中" |

### 3.2 Step 2 — 通用 track 抽象 + 默认 track set

#### 3.2.1 `_internal/docs-index-protocol/registry.yaml` 重构

引入 `tracks:` 顶级字段，声明 default track set（见 §1.2 示例）。

#### 3.2.2 generic 脚本（`_internal/docs-index-protocol/scripts/`）

```
scripts/
├── _track_resolver.py        # 共用 helper：读 registry.yaml / schema 校验 / 返回 track config
├── track_scan.py             # 扫 track.root（按 patterns），输出 track.output
├── track_verify.py           # 健康度 / 孤儿检查（按 type 不同行为）
├── track_archive_triggers.py # 归档候选发现
├── track_map.py              # 认知图（type=docs-tree）/ 仓库入口图（type=repo-entry）
│
├── (legacy, 视情况保留)
│   ├── cognitive_map.py        # 被 track_map.py(type=docs-tree) 调用
│   ├── archive_triggers.py     # 被 track_archive_triggers.py(type=docs-tree) 调用
│   ├── index_scan.py           # 被 track_scan.py(type=docs-tree) 调用
│   ├── index_verify.py         # 被 track_verify.py(type=docs-tree) 调用
│   ├── index_update.py         # 保留（用户工作流入口）
│   └── index_init.py           # 保留
```

每脚本 main 入口：

```python
def main():
    parser.add_argument("--track-id", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    track = _track_resolver.resolve(args.track_id)  # exit 0 if not found

    if track.get("delegate_to") == "radar":
        # v5: delegate_to 仅作为旧式标记保留兼容（不再代表"protocol 退出"）
        # 实际 code-tree 行为由 _scan_code_tree 主导，按 radar_summary 配置调用 radar
        pass

    if not Path(track["root"]).is_dir():
        print(f"[skip] track {track['id']} root {track['root']} not found.")
        sys.exit(0)

    if track["type"] == "repo-entry":
        _scan_repo_entry(track)  # 强制 depth_limit=1
    elif track["type"] == "docs-tree":
        _scan_docs(track)        # 调用 legacy index_scan.py 等
    elif track["type"] == "spec-tree":
        _scan_specs(track)       # 新写实现
    elif track["type"] == "code-tree":
        _scan_code_tree(track)   # v5: 锚点 + (可选) radar 摘要
    else:
        print(f"[warn] unknown type {track['type']}, skip.")
        sys.exit(0)
```

`_scan_code_tree(track)` 行为骨架（v5 新增）：

```python
def _scan_code_tree(track):
    # 第一段：锚点导航（继承 smart_map.py 防爆参数）
    anchors = _walk_with_anchors(
        root=track["root"],
        ignore_dirs=track.get("ignore", DEFAULT_IGNORE_DIRS),
        anchor_files=track.get("anchor_files", DEFAULT_ANCHOR_FILES),
        max_depth=track.get("depth_limit", DEFAULT_MAX_DEPTH),  # 默认 5
        max_lines=DEFAULT_MAX_LINES,  # 200
    )
    output = {"anchors": anchors}

    # 第二段：radar 摘要（按 radar_summary 配置）
    rs_cfg = track.get("radar_summary", {})
    if rs_cfg.get("enabled"):
        try:
            output["radar_summary"] = _invoke_radar_summary(
                root=track["root"],
                hotspot_top=rs_cfg.get("hotspot_top", 10),
                include_unused=rs_cfg.get("include_unused", False),
                include_cycles_count=rs_cfg.get("include_cycles_count", True),
                max_output_lines=rs_cfg.get("max_output_lines", 200),
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, RadarError) as e:
            output["radar_summary"] = {"skipped": True, "reason": str(e)}
            print(f"[warn] track {track['id']} radar summary skipped: {e}")

    _write_yaml(track["output"], output)
```

#### 3.2.3 schema/lifecycle 文档更新

- `index-schema.md` 顶部新增章节"Track 抽象与作用域"
- `lifecycle.md` 同步说明"按 registry.yaml tracks 声明驱动"

### 3.3 Step 3 — `index-librarian` SKILL.md 重写

```yaml
metadata:
  formal_action_name: 项目索引维护
  top_level_capability: 项目索引维护
  ...
```

正文：
- "按 `_internal/docs-index-protocol/registry.yaml` 中 `tracks:` 声明执行索引/统计/认知图/归档触发"
- 列出 default track set 实例（specs/docs/repo-entry）作示例
- **委派 radar 边界**："代码仓库的依赖/调用/死代码分析请使用 radar skill；本能力只做目录索引。"
- references：`spec-track.md` / `docs-track.md` / `repo-track.md` / `track-extension.md`（如何加 track）

### 3.4 Step 4 — 行为对等性验证矩阵（在 default 3 实例上）

见 §5。

### 3.5 Step 5 — 物理废弃 maglev-librarian（与 v3 一致）

| # | 动作 | 路径 |
|---|---|---|
| A1 | 删 skill 目录 | `.agents/skills/maglev-librarian/` |
| A2 | 删 workflow | `.agents/workflows/maglev-librarian.md` |
| A3 | 删 catalog 条目 | `.agents/private-catalog.yaml` 中 `name: 'maglev-librarian'` 整段 |
| A4 | 删合并源（D10） | 仓库根 `scripts/smart_map.py`（行为已合并到 track_map.py(type=repo-entry)） |
| B1 | live 引用改写 | `issues/draft/draft_issue_capability_matrix_skills.md`（3 处） |
| B2 | 调 index-librarian relations | `replaces` 语义改为"已替代" |

历史 trace 保留：与 v3 同。

### 3.6 Step 6 — release.py 修齐 + 用户分发（与 v3 主结构一致）

#### 3.6.1 `scripts/maglev_release.py` 改造

新增/修改步骤同 v3：`step1b_verify_distribution_scope` / `step3_assemble_dist`（copytree runtime_internal）/ `step3b_split_catalog`（生成 user_visible 版）。

#### 3.6.2 `scripts/check_runtime_distribution.py`（新增）

独立可执行；CI 与本地直接调用。

#### 3.6.3 catalog `path:` 字段补齐（与 v3 同）

#### 3.6.4 用户加 track 的体验

- 用户可编辑自己项目的 `.agents/skills/_internal/docs-index-protocol/registry.yaml` 在 `tracks:` 末尾追加项
- 重新运行 `index-librarian` 即生效；无需改任何代码
- 错误（root 不存在 / type 未知 / 字段非法）由 generic 脚本 friendly fail

### 3.7 上游 K2 修订标注（与 v3 同）

---

## 4. 实施顺序 (Execution Order)

按 Step 1-6 顺序：

```
Step 1（独立 commit，最小止血）
  └─ §3.1 撤回 deprecated 标签
  └─ §3.7 上游 K2 修订标注

Step 2（多 commit）
  ├─ §3.2.1 registry.yaml 引入 tracks: + default track set
  ├─ §3.2.1 新增 4 个 `registry.example.<type>.yaml` 模板（v5.1 D28，AC-F2-8）
  ├─ §3.2.2 _track_resolver.py + 4 个 track_*.py generic 脚本
  ├─ §3.2.2 `_scan_code_tree` 函数（v5 D24/D25/D26，AC-F12-1~5/7）
  ├─ §3.2.2 legacy docs 脚本重连为 backing
  ├─ smart_map.py 行为合并到 track_map.py(type=repo-entry)
  └─ §3.2.3 schema/lifecycle 文档说明

Step 3（独立 commit）
  ├─ §3.3 index-librarian SKILL.md 重写
  └─ §3.3 SKILL.md 新增"radar_summary 报告契约"+"多 track 状态报告模板"段（v5.1 D27，AC-F12-6/8/9）

Step 4（gate commit + status 更新）
  └─ §5 行为对等性矩阵填充并验证全 pass

Step 5（独立 commit）
  └─ §3.5 maglev-librarian 物理废弃 + smart_map.py wrapper 删除

Step 6（多 commit）
  ├─ §3.6.1 release.py step1b/3b
  ├─ §3.6.2 check_runtime_distribution.py
  ├─ catalog path 字段补齐
  └─ 本地 --local-dist 全链路验证 + push
```

> **强制 gate**：Step 4 矩阵任一行 partial/miss 时禁止推进 Step 5。

---

## 5. 行为对等性验证矩阵 (Step 4 Gate)

> 对照 default track set 3 实例（specs / docs / repo-entry）×4 维度。

| Track 实例 | 维度 | maglev-librarian 现状 | 新机制（generic 脚本 + track config） | 对等性 | 备注 |
|---|---|---|---|---|---|
| specs | 输入 | specs/{10_reality, 20_evolution, 90_archive}/ | track_scan.py --track-id specs | ✅ | Step 4 实测：扫到 62 items |
| specs | 输出 | spec 索引/统计 | track config.output (specs/_meta/index.yaml) | ✅ | Step 4 实测：写出 specs/_meta/index.yaml |
| specs | 触发条件 | 主动调用 | index-librarian 调度 | ✅ | SKILL.md v2.0 已纳入多 track 总览 |
| specs | 失败兜底 | 旧 skill 无显式兜底 | _track_resolver root 校验 + exit 0 | ✅ | 新机制更优 |
| docs | 输入 | docs/{thinking, projects}/ | track_scan.py --track-id docs（调 legacy index_scan） | ✅ pre-validated | Step 4 实测：scan/verify 全 exit 0 |
| docs | 输出 | docs 索引 + cognitive_map | 同（保护 docs_knowledge_archival_methodology 落地） | ✅ | |
| docs | 触发条件 | thinking 写入后 | 同 | ✅ | |
| docs | 失败兜底 | _ensure_docs_root | 同 | ✅ | |
| repo-entry | 输入 | 仓库根 README/AGENTS.md/llms.txt 等 | track_scan.py --track-id repo-entry, depth_limit=1, patterns | ✅ | Step 4 实测：8 anchors（修隐藏目录漏扫后） |
| repo-entry | 输出 | smart_map 仓库入口图 | track_map.py(type=repo-entry) | ✅ | Step 4 实测：47 entries 写到 .agents/_meta/repo-map.md（D10 行为合并验证通过） |
| repo-entry | 触发条件 | 仓库结构变更 | 同 | ✅ | |
| repo-entry | 失败兜底 | 旧 skill 无 | _track_resolver + depth_limit 强制 | ✅ | 新机制更优 |

通过定义（D14）：覆盖等价能力 + 输出可被相同消费方读取，不要求 byte-identical。

**Step 4 验证状态**：default track set 3 实例 × 4 维度 = 12 格全 ✅ —— Gate Pass，可进入 Step 5（物理废弃 maglev-librarian）。详见 `status.md` "Step 4 验证记录" 段。

---

## 6. AC 映射 (AC Mapping)

| AC ID | 实现位置 | 验证方式 |
|---|---|---|
| AC-F1-* | §3.1 | catalog/SKILL.md grep |
| AC-F2-1 | §3.2.1 registry.yaml tracks schema | YAML 字段检查 |
| AC-F2-2 | §3.2.2 generic 脚本 | 脚本签名 grep --track-id |
| AC-F2-3 | §3.2.1 default track set | registry.yaml diff |
| AC-F2-4 | §3.2.2 legacy 收编（D9） | 行为不退化测试 |
| AC-F2-5 | §3.2.2 _scan_repo_entry depth_limit (D8) | 故意放代码到根，验证不被扫到 |
| AC-F2-6 | §3.2.2 type=code-tree 分支（v5 推翻 D7，主导执行 4 动作） | type=code-tree track 测试 |
| AC-F2-7 | §3.2.2 _track_resolver.py 读用户 registry.yaml | 用户加 track 后调度可见 |
| AC-F2-8 (v5.1) | §3.2.1 + 新增 `_internal/docs-index-protocol/registry.example.<type>.yaml` 4 个模板（D28） | 4 个 example 文件存在 + SKILL.md 引用 |
| AC-F3-* | §3.3 SKILL.md 重写 | grep |
| AC-F4-* | §5 矩阵 | status.md "Step 4 验证记录" |
| AC-F5-* | §3.5 物理废弃 | grep -rn maglev-librarian |
| AC-F6-* | §3.6 | dry-run install |
| AC-F7-* | §3.2.2 generic 脚本兜底逻辑 + D8 depth_limit + D17 schema 校验 | 异常用例测试 |
| AC-F8-* | §3.2.1 registry.yaml thresholds（per-track） | grep |
| AC-F9-* | §3.6.2 check_runtime_distribution.py | CI 集成测试 |
| AC-F10-* | 不改 installer 输出 + §3.3 SKILL.md | 视检 |
| AC-F11-* | §3.7 上游 K2 标注 | 文档查阅 |
| AC-F12-1 | §3.2.2 `_scan_code_tree` 函数（v5 新增）→ 输出 anchors 段 | code-tree track 测试 |
| AC-F12-2 | §3.2.2 `_scan_code_tree` 中 `_invoke_radar_summary`（subprocess invoke radar + 截断写 yaml radar_summary 段，D24） | radar_summary.enabled=true 后 yaml 内容检查 |
| AC-F12-3 | §3.2.2 `_scan_code_tree` 中 try/except 降级路径（D26） | mock radar binary 不存在场景测试 |
| AC-F12-4 | §3.2.2 `_walk_with_anchors` 默认参数继承自 smart_map.py 常量（D25） | 单测 DEFAULT_IGNORE_DIRS / MAX_DEPTH=5 / MAX_LINES=200 |
| AC-F12-5 | §3.2.1 default track set 不含 type=code-tree（D5） | registry.yaml diff |
| AC-F12-6 | §3.3 SKILL.md 边界声明（v5.1 修订：code-tree 由 protocol 主导，依赖分析子能力 subprocess 调 radar） | grep |
| AC-F12-7 | §3.2.2 `_scan_repo_entry` 强制 depth=1（D8）+ `_scan_code_tree` 默认 depth_limit=5（D25） | 单测 |
| AC-F12-8 (v5.1) | §3.3 SKILL.md 新增"radar_summary 报告契约"段（D27）——禁止展开，统计行+Top 3+"(+N more)" | SKILL.md grep + 单 track 报告示例 ≤5 行 |
| AC-F12-9 (v5.1) | §3.3 SKILL.md 新增"多 track 状态报告模板"段（D27）——4 态枚举 ok/partial/skipped/failed | SKILL.md grep + 多 track 部分失败报告样例 |

---

## 7. 静默基建合规检查

| 检查项 | 设计如何满足 |
|---|---|
| 不主动 banner | release.py / installer 输出无本主题能力单独条目 |
| 不主动询问 | legacy-adopter / bootstrapper 不调用本主题 |
| 用错给提示 | _track_resolver schema 校验 + generic 脚本 friendly fail |
| 主动查可见 | catalog 客观存在；`.agents/skills/_internal/docs-index-protocol/` 物理可见 |
| 默认窄范围 | default track set 仅 3 个；用户加 track 是显式动作 |
| 不侵入代码 | repo-entry depth_limit=1（D8）；type=code-tree 通过防爆参数 + radar 摘要截断防止上下文爆炸（D7/D24/D25/D26） |

---

## 8. 风险与未决 (Risks & Open)

| ID | 风险 | 缓解 |
|---|---|---|
| R1 | PyYAML 在 release.py 是新依赖 | 已是仓库通用栈；fallback：手写最小 yaml |
| R2 | user 已有 registry.yaml 与新版冲突（用户加过 tracks 后再 update） | D21：installer 现有 `.local_backup_<ts>`；index-librarian 文档说明合并策略 |
| R3 | catalog 同时承担"声明"与"分发指令"双重职责 | 顶部 comment 显式声明 |
| R4 | track schema 字段过多 | D4 必填仅 3 字段；可选字段克制 |
| R5 | 用户禁用 default track 后行为不可预期 | D6 + D16：覆盖式合并；文档明示 |
| R6 | type=code-tree 用户期望本机制扫，但被 delegate radar 拒绝 | SKILL.md 显式声明边界（AC-F12-2）；用户自决 |
| R7 | generic 脚本 implementation 量比 v3 略大（type 分支） | 可控；type 枚举仅 4 种 |
| R8 | repo-entry depth_limit=1 在某些项目过严 | 用户可在自己 registry.yaml override（warn 但允许，D8 注释） |
| R9 | Step 4 对等性矩阵长时间 partial 阻塞 | 强制 gate 优先于周期 |
| R10 | 上游 K2 修订被误解为重写 | D20：仅加标注 |
| R11 | 本主题周期与发布节奏冲突 | 本主题完成前不做 patch release；如需紧急可绕过（runtime_distribution: false 白名单） |

---

## 9. Out of Scope（设计层再确认）

- 不改 `index-schema.md` 核心方法论内容（仅加 Track 抽象章节）
- 不引 CLI flag / env var
- 不为 `index-librarian` 写 user-facing 文档
- 不实现 archive 候选自动 PR / 自动 archive
- **不实现代码仓库的完整 AST / 调用图深度分析**（仅以摘要形式 subprocess 调 radar 拉 hotspot/unused/cycles，由 protocol 截断后落盘）
- 不实现跨 track 关系图（specs ↔ docs ↔ repo）
- 不解决 `docs/` 是 git submodule 的情况

---

<details><summary>🤖 Context Trace</summary>

- 输入 PRD: `01_requirements.md` v5.2
- v4 决策: U-V4-1（schema 字段克制）/ U-V4-2（用户可禁用 default）/ D8（depth_limit=1 硬约束）/ D9（legacy docs 脚本保留作 backing）/ D22（抽 _track_resolver helper）
- v5 决策: D7 推翻（v4 "不 subprocess invoke" → v5 radar 作辅助执行器，subprocess invoke 拉摘要）/ D24（code-tree 两段式 yaml）/ D25（防爆参数继承 smart_map.py）/ D26（radar 调用容错降级）
- v5.1 决策: D27（runtime AI 报告契约——radar_summary 不展开 + 多 track 4 态状态模板）/ D28（每 type example 模板）
- v3 部分决策保留: U-PR1=C（保留 docs-index-protocol 命名）/ U-PR4=对齐（formal_action_name=项目索引维护）/ U-PR5=覆盖等价
- v3 部分决策推翻: v3 D3（spec_index_*.py 新写）→ v4 D3（generic track_*.py）；v3 D4（smart_map 迁移到 repo_map.py）→ v4 D10（行为合并到 track_map.py）
- 关键事实: `scripts/maglev_release.py:170-194`；`maglev_installer.py:576-600`；上游 spec K2 范围错配；maglev-librarian Track C `smart_map.py` 不做 AST，仅锚点导航（v5 据此判定 code-tree 是绿地）
- 用户 v4 诉求: "索引机制是公共能力"；"对任何目录都跑但要限制范围避免浪费"；"代码索引不要侵入"
- 用户 v5 诉求: "radar 是否胜任当前的任务"；"让 radar 做索引创建的辅助执行，主要靠索引技能本身的能力，代码场景注意上下文爆炸"
- 用户 v5.1 诉求: "v5 是否会过度复杂化导致 AI 助手无法真实执行——指的是索引能力本身的运行时复杂度"

</details>
