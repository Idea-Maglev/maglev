# Index Schema — 索引结构规则定义

> 设计权威: 本文件定义索引节点的 frontmatter schema 和结构规则。
> 执行权威: `scripts/track_verify.py` — 如有矛盾以脚本实际行为为准。
> 来源: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md

---

## 0. Track 抽象与作用域

自 protocol_version `3.0` 起，索引能力按 **track** 声明，每个 track 以 `registry.yaml` 中的一条 `tracks` 条目驱动一类索引/地图产物。一个仓库可同时挂多个 track。

### 0.1 三类 Track

| `type` | 适用对象 | 驱动脚本 | 产物形态 | 本文件 schema 适用范围 |
|:---|:---|:---|:---|:---|
| `dir-tree` | 任意目录树 (specs/, docs/, 自定义) | `track_scan.py` / `track_verify.py` | `INDEX.md` 网络 + summary YAML | ✅ 完整适用 |
| `repo-entry` | 仓库根目录 | 同上 | `repo-entry.yaml` (锚点) + `repo-map.md` (人读地图) | ❌ 不产生 `INDEX.md`，不走本 schema |
| `code-tree` | `packages/` / `src/` 代码树 | 同上 | `code-tree.yaml`（anchors + radar_summary 两段式） | ❌ 不产生 `INDEX.md`，不走本 schema |

> **已移除**: `spec-tree` 和 `docs-tree` 已合并为 `dir-tree`（protocol v3.0）。

### 0.2 Schema 适用边界

本文件第 §1-§6 章节定义的 frontmatter / stats / body table / INDEX.md 规则，**仅适用于 `dir-tree`** 类型。

`repo-entry` 与 `code-tree` 是"代码层与仓库层"扩展能力：

- **不**为目录写 `INDEX.md`、**不**走 entity-index frontmatter，因此本 schema 整体不适用。
- 产物 schema 由对应脚本契约约束。
- `code-tree` 的 `radar_summary` 段是机读结构（hotspot/cycles/unused 摘要），失败时降级为 `{skipped: true, reason: ...}`，不阻断主流程。

### 0.3 Track 声明（驱动方式）

实际启用何种 track 由仓库内 `registry.yaml` 的 `tracks` 段声明，每个 track 至少包含 `id` / `type` / `root` / `output`。完整字段见 `registry.example.<type>.yaml` 模板。

行为对等性矩阵（`spec-tree` 与 `docs-tree` 在 INDEX 网络维度等价；其余 track 走各自最小契约）由验证脚本（`track_verify.py`）收口。

---

## 1. 统一类型

所有索引节点使用统一类型 `entity-index`，通过 `scope` 区分层级：

| scope | 含义 | 位置示例 |
|:---|:---|:---|
| `root` | 模块入口 (唯一) | `meetings/INDEX.md` |
| `year` | 年度分区 | `meetings/2026/INDEX.md` |
| `month` | 月度分区 | `meetings/2026/04/INDEX.md` |
| `collection` | 逻辑分组 | `comms/groups/INDEX.md` |

叶子节点 (实际实体) 使用各自的 `type`（如 `meeting`, `p2p-contact`），不属于索引体系。

## 2. Frontmatter Schema

### 2.1 必填字段 (所有 scope)

```yaml
type: entity-index                    # 固定值
scope: root|year|month|collection     # 层级标识
entity_type: "{模块自定义}"            # 由模块 root 声明
child_count: N                        # 直接子节点数 (整数)
stats:
  total: N                            # 必填: 子节点 total 之和 (root/partition) 或 child_count (底层)
updated: "YYYY-MM-DD"                 # 最后更新日期
```

### 2.2 Root 专属字段

```yaml
index_protocol_version: "1.0"         # 必须声明，表示已接入协议
stats_schema:                         # 定义本模块的统计分桶
  total:
    rule: "count(*)"
    type: computed
  # ... 模块自定义分桶

sort_key: "date"                      # 子节点排序依据 (默认: "name")
sort_order: "asc"                     # asc | desc (默认: "asc")
child_type: "directory"               # directory | file | mixed
```

### 2.3 可选字段

```yaml
table_columns:                        # 声明后，脚本接管 body table 生成
  - header: "..."
    source: "frontmatter.{field}" | "computed.{name}"
    fallback: "—"                     # 值不存在时的替代
    format: "bool_emoji|date_short|truncate:N"

custom_checks:                        # 模块特定验证 (仅 root)
  - id: "M01"
    name: "..."
    scope: "module"
    severity: "error|warning"
    implementation: "script"
    script_function: "check_function_name"
```

## 3. Stats 类型系统

| 类型 | 特征 | 脚本处理 |
|:---|:---|:---|
| `computed` | 总是从实际文件数计算 | `count(*)` — 每次重算 |
| `immutable` | 一旦设定不变 | `count(field != null)` — 直接计数 |
| `dynamic` | 可能随时间变化 | 计数 + 标注 `status_changed_at` |

### 3.1 Stats DSL 语法 (受限)

```
count(*)                              # 所有子节点
count(field != null)                  # 字段存在
count(field == null)                  # 字段不存在
count(field == 'value')               # 字段等于值
count(field != 'value')               # 字段不等于值
count(f1 != null OR f2 != null)       # OR 组合 (最多2个条件)
count(f1 == null AND f2 == null)      # AND 组合 (最多2个条件)
```

不支持: 正则、函数调用、嵌套表达式、三个以上条件组合。

## 4. Body Table 规则

- **有 `table_columns`**: 脚本根据声明从子节点 frontmatter 提取数据生成表格
- **无 `table_columns`**: AI 负责 body table 内容（脚本仅验证行数和链接）

### 4.1 Computed 字段

| 名称 | 含义 |
|:---|:---|
| `computed.row_number` | 行号 (从 1 递增) |
| `computed.relative_link` | `[→](./{dirname}/)` |
| `computed.dirname` | 子节点目录名 |
| `computed.duration_display` | `{duration_minutes}min` |
| `computed.analysis_badge` | `✅` / `⚪` |
| `computed.child_scope` | 子节点 scope |

### 4.2 Format 修饰符

| 修饰符 | 效果 |
|:---|:---|
| `bool_emoji` | true→✅, false→❌ |
| `date_short` | YYYY-MM-DD → MM-DD |
| `truncate:N` | 截断为 N 字符 |

## 5. INDEX.md 文件规则

- INDEX.md 仅存在于索引节点 (不在叶子实体上)
- INDEX.md 由脚本独占管理 — 其他技能不得直接编辑
- INDEX.md 删除后可通过 `index_init.py` 完全重建
- frontmatter 是 AI/脚本的消费入口，body table 是人的阅读入口

---

## 6. Maglev 增量字段（位段化与认知地图）

> 来源：`specs/20_evolution/active/docs_knowledge_archival_methodology/02_design.md` §3.3
> 作用范围：仅 `thinking` 模块当前生效；其他模块按需启用。
> 校验状态：以下字段当前**未在脚本中强校验**，仅作为约定记录。后续由 `module_checks/thinking.py` 落实。

### 6.1 Root 增量字段（`docs/thinking/INDEX.md`）

```yaml
segments:                              # 位段语义表（记忆宫殿房间）
  - id: "30_philosophy"                # 必填，格式 \d{2}_[a-z_]+
    room_name: "哲学殿"                  # 必填，中文房间隐喻
    description: "..."                  # 必填，一句话
    status: "active|planned"           # 必填

cognitive_map:                          # F8 认知地图（可选启用，由 enabled 控制）
  enabled: false                        # 当前 false；启用后由脚本聚合
  output_path: "docs/_meta/knowledge_graph.json"

migration_status:                       # 大型重组期间标记
  phase3_in_progress|phase3_complete|stable
```

**约束**：
- `segments[].id` 必须与实际子目录名一致；脚本应校验存在性
- `room_name` 仅施加在位段层；叶子文档不要使用

### 6.2 Leaf 增量字段（`docs/thinking/<segment>/<file>.md`）

```yaml
segment: "30_philosophy"               # 必填；与父目录 id 一致
status: "draft|active|crystallized|archived"
                                        # F1 LPM 四态映射；
                                        # crystallized 之后才进入认知地图
linked_to:                              # F8 跨位段引用（可选）
  - "docs/thinking/50_alignment/maglev_vs_hermes_agent.md"
superseded_by: null                    # 上位重写归档时填路径
```

**约束**：
- `segment` 必填，内容必须等于父目录名
- `status` 缺省视为 `draft`，警告级
- `linked_to` 仅在 `status >= crystallized` 时纳入认知地图聚合
- 不允许在叶子层声明 `room_name`、`segments`、`cognitive_map`

### 6.3 强校验状态

| 字段 | 当前 | 启用后 | 强校验来源 |
|:---|:---|:---|:---|
| `segments[]` | 软约束 | 强制 | `module_checks/thinking.py` |
| `cognitive_map.enabled` | 软约束 | 强制（与脚本对齐） | `index_update.py` |
| 叶子 `segment` | 软约束 | 强制（与父目录对齐） | `module_checks/thinking.py` |
| 叶子 `status` | 软约束 | 警告级 | `module_checks/thinking.py` |
| 叶子 `linked_to` | 软约束 | 引用合法性必须 PASS | `module_checks/thinking.py` |

### 6.4 与上游 workbench 协议的差异

- workbench 使用扁平 `active/archive/watching` 三态，无位段
- Maglev 引入 9 位段 + 房间隐喻，**仅在位段层**施加隐喻，叶子保持工程化命名
- 仅 Mermaid 静态图 + frontmatter 显式 `linked_to`，**不引入 GraphRAG / 向量检索**
- 这些增量不影响协议核心契约（统一 entity-index 类型、stats DSL、INDEX 独占写权）

### 6.5 `stats.total` 与 `child_count` 语义（thinking 模块决策）

> **决策日期**：2026-04-27
> **决策理由**：选择"所有叶子"语义可让指标诚实反映现状，避免因 frontmatter 补全工作未完成而让指标失真。frontmatter 补全（约 60 篇老叶子）独立作为 P2 卫生项推进。
> **实现状态**：✅ 已落到 `index_update.py`（commit 时间同决策日）

#### 6.5.1 `stats.total` 定义

| Scope | 计算口径 | 实现 |
|:---|:---|:---|
| `root` | **所有叶子 .md 文件递归数**（不含 INDEX.md / README.md）；不要求 frontmatter 完整性 | `compute_stats` 检测 `has_sub_dirs` 后调用 `count_leaf_files_recursive` |
| `collection` | **该 collection 下所有叶子 .md 文件递归数**（不含 INDEX.md / README.md） | 同上，作用域限于该 collection 子树 |

**反例（不允许的口径）**：
- ❌ 仅统计带完整 frontmatter 的合规叶子（会让指标随 frontmatter 补全进度跳变）
- ❌ 含 INDEX.md（指标会反映"索引数"而非"内容数"）

#### 6.5.2 `child_count` 定义

| Scope | 口径 |
|:---|:---|
| `root` | 直接子节点数（叶子 .md + 直接子目录数；不含 INDEX.md） |
| `collection` | 直接子节点数（同上） |

**注意**：`child_count` 与 `stats.total` 在含子目录的 collection 下会出现差异（`child_count` 仅一级；`stats.total` 递归全树）。例如 `60_case` 有 14 直接叶子 + 14 子目录，`child_count = 28`，`stats.total = 46`。

#### 6.5.3 修复历史

| 偏差 | 原值 | 现值 | Commit |
|:---|:---|:---|:---|
| `thinking/INDEX.md` `stats.total` | 47（合规叶子） | 107 | P1 step 2（2026-04-27） |
| `thinking/60_case/INDEX.md` `stats.total` | 28（手编） | 46 | 同上 |
| `thinking/30_philosophy` 等纯叶子 collection | 不一致 | 全树递归 | 同上 |
| `index_update.py` `child_count` 不含子目录 | mixed 错算 | 自动检测 mixed sum | 同上 |

### 6.6 保留区目录约定（`_meta/`）

模块根下下划线前缀目录为**保留区**，不计入索引、不进位段、不参与归档评估：

| 目录 | 角色 | 写入者 | 读取者 | 是否进 stats |
|:---|:---|:---|:---|:---|
| `_meta/` | 机读元数据保留区 | 脚本独占（如 `cognitive_map.py`） | 脚本 / 工具链 | 否 |

约束：
- 三脚本 + `cognitive_map.py` 在 `count_leaf_files_recursive` / `get_child_dirs` / `collect_leaves` / `os.walk dirs` 同步排除该目录名。
- 该约定由 lifecycle.md §6.1 和本节共同声明，修改一处必同步另一处。
- 当前 `_meta/` 唯一产物：`docs/<module>/_meta/knowledge_graph.json`（F8 认知地图机读输出）。
- 保留区命名规则：所有以 `_` 开头的顶层目录视为保留区，新增需先在本节登记。

