# 技术设计: unified_doc_tree_indexer

> **版本**: v1.1
> **作者**: spec-designer (AI) + Maglev contributors (设计方向)
> **日期**: 2026-05-24
> **状态**: Draft

## 0. 设计原则

> 索引技能是通用基础能力。Maglev 体系适应索引技能，而非反过来。

## 1. 核心变更

### 1.1 类型合并

| Before | After |
|--------|-------|
| `spec-tree` (只写 YAML) | ❌ 删除 |
| `docs-tree` (代理 legacy) | ❌ 删除 |
| — | ✅ `dir-tree` (统一类型) |

`dir-tree` = 对任意目录递归生成 INDEX.md 网络的通用能力。不保留旧类型名别名，registry 直接清洗为 `dir-tree`。

`repo-entry` 和 `code-tree` 保留（它们的产物是 YAML/map，不是 INDEX.md）。

### 1.2 `dir-tree` 行为

给定 `root: X/`：
1. **递归发现**: 遍历 X/ 下所有子目录（排除 `_meta/`、dotfiles、ignore 列表）
2. **INDEX.md 生成/更新**: 每个含子内容的目录获得 INDEX.md
3. **frontmatter 标准**: 统一 entity-index schema（最小必填 + 可选扩展）
4. **child_count 自动计算**: 数文件或数子目录（由 `child_type` 配置或 auto-detect）
5. **stats 冒泡**: 子节点 stats 向上聚合到父节点
6. **已有 INDEX.md 保持兼容**: 不覆盖用户自定义字段，只更新 `child_count` / `stats` / `updated`

## 2. Registry 配置模型

### 2.1 新 registry 格式

```yaml
tracks:
  - id: specs
    type: dir-tree          # 统一类型
    root: specs/
    output: specs/_meta/index.yaml   # summary 产物（保留）
    entity_type: spec-topic          # 可选，写入 INDEX.md frontmatter
    child_type: auto                 # auto | file | directory
    max_depth: 4                     # 递归深度限制
    ignore:
      - _meta
      - context
      - ref

  - id: docs
    type: dir-tree          # 同一类型
    root: docs/
    output: docs/_meta/index.yaml
    entity_type: document
    child_type: auto
    max_depth: 4
    ignore:
      - _meta

  # 保持不变
  - id: repo-entry
    type: repo-entry
    root: .
    ...

  - id: skills
    type: repo-entry
    root: .agents/skills/
    ...
```

### 2.2 自定义目录接入

用户只需在 registry.yaml 追加一个 `dir-tree` 类型的 track 条目即可索引任意目录：

```yaml
  - id: my-notes
    type: dir-tree
    root: my-notes/
    entity_type: note
    max_depth: 3
```

无需修改任何脚本代码。

## 3. INDEX.md Schema

### 3.1 最小必填 (所有 dir-tree INDEX.md)

```yaml
---
type: entity-index
scope: root | collection    # root = track root; collection = 子目录
child_count: N              # 直接子节点数
updated: "YYYY-MM-DD"
---
```

### 3.2 可选扩展 (用户/track 配置决定)

```yaml
entity_type: "spec-topic"     # 从 track config 或已有 INDEX.md 继承
index_protocol_version: "2.0" # root scope 可声明
child_type: directory          # auto-detected or explicit
stats:
  total: N                     # 递归叶子数或子目录数
stats_schema: {...}            # 用户可自定义分桶规则
segments: [...]                # 用户可定义位段描述
table_columns: [...]           # 用户可定义 body table 格式
```

### 3.3 auto-detect 逻辑

`child_type: auto` 时：
- 目录下只有文件（无子目录）→ `file`
- 目录下只有子目录（无叶子文件）→ `directory`
- 混合 → `mixed`

## 4. 脚本变更

### 4.1 `track_scan.py` — 新增 `_scan_dir_tree()`

```python
def _scan_dir_tree(track: dict) -> int:
    """
    通用目录树扫描器。
    1. 递归遍历 track.root 下所有目录
    2. 对每个目录生成/更新 INDEX.md (frontmatter + body)
    3. 写 summary YAML 到 track.output
    """
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        return 0

    max_depth = track.get("max_depth", 4)
    ignore = set(track.get("ignore", ["_meta"]))
    entity_type = track.get("entity_type", "document")
    child_type_cfg = track.get("child_type", "auto")

    # Phase 1: 递归收集目录结构
    dirs_to_index = _discover_indexable_dirs(root_dir, ignore, max_depth)

    # Phase 2: 对每个目录生成/更新 INDEX.md
    for dir_path in reversed(dirs_to_index):  # bottom-up
        _generate_or_update_index_md(
            dir_path, root_dir, entity_type, child_type_cfg, ignore
        )

    # Phase 3: 写 summary YAML (保留旧行为兼容)
    _write_summary_yaml(track, root_dir, repo_root, dirs_to_index)

    return 0
```

### 4.2 INDEX.md 生成/更新策略

```python
def _generate_or_update_index_md(dir_path, root_dir, entity_type, child_type_cfg, ignore):
    index_path = dir_path / "INDEX.md"

    if index_path.exists():
        # 已有 INDEX.md → 只更新 child_count / stats / updated
        # 保留用户定义的 stats_schema / segments / table_columns / 自定义字段
        existing = parse_file(index_path)
        metadata = existing.metadata
        metadata["child_count"] = _count_children(dir_path, child_type_cfg, ignore)
        metadata["stats"] = _compute_stats(dir_path, metadata.get("stats_schema"))
        metadata["updated"] = today()
        write_frontmatter(index_path, metadata)
    else:
        # 新建 INDEX.md → 最小 frontmatter + 简单 body
        scope = "root" if dir_path == root_dir else "collection"
        child_count = _count_children(dir_path, child_type_cfg, ignore)
        metadata = {
            "type": "entity-index",
            "scope": scope,
            "entity_type": entity_type,
            "child_count": child_count,
            "updated": today(),
            "stats": {"total": _recursive_leaf_count(dir_path, ignore)},
        }
        body = _generate_default_body(dir_path, ignore)
        write_new_index_md(index_path, metadata, body)
```

### 4.3 `track_verify.py` — 统一 `_verify_dir_tree()`

```python
def _verify_dir_tree(track: dict) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    issues = []

    # 1. 产物存在性检查
    output_path = repo_root / track.get("output", "")
    if output_path.name and not output_path.exists():
        issues.append(f"scan output missing: {track['output']}")

    # 2. INDEX.md 存在性检查 (每个子目录应有)
    ignore = set(track.get("ignore", ["_meta"]))
    max_depth = track.get("max_depth", 4)
    for dir_path in _discover_indexable_dirs(root_dir, ignore, max_depth):
        if not (dir_path / "INDEX.md").exists():
            rel = dir_path.relative_to(repo_root)
            issues.append(f"missing INDEX.md: {rel}/")

    # 3. INDEX.md frontmatter 校验 (必填字段)
    for dir_path in _discover_indexable_dirs(root_dir, ignore, max_depth):
        idx = dir_path / "INDEX.md"
        if idx.exists():
            result = parse_file(idx)
            if not result.is_valid:
                issues.append(f"invalid frontmatter: {idx.relative_to(repo_root)}")
            elif result.metadata.get("type") != "entity-index":
                issues.append(f"wrong type field: {idx.relative_to(repo_root)}")

    if issues:
        print(f"[track-verify] dir-tree {track['id']}: {len(issues)} issue(s)")
        for s in issues[:10]:
            print(f"  - {s}")
        return 1
    print(f"[track-verify] dir-tree {track['id']}: ok")
    return 0
```

### 4.4 DISPATCH 表 (无别名，干净映射)

```python
DISPATCH = {
    "dir-tree": _scan_dir_tree,
    "repo-entry": _scan_repo_entry,
    "code-tree": _scan_code_tree,
}
```

旧的 `spec-tree` / `docs-tree` 不再识别。如果 registry 中残留旧类型名，脚本应 error 并提示迁移。

## 5. legacy 脚本处理

### 5.1 保留但降级

| 脚本 | 处置 |
|------|------|
| `index_scan.py` | 保留，但 `track_scan.py` 不再代理它 |
| `index_verify.py` | 保留，但 `track_verify.py` 不再代理它 |
| `index_update.py` | **复用核心逻辑**：`_generate_or_update_index_md` 提取自此脚本 |
| `index_init.py` | 保留，低优先级；track_scan 首次运行即等同 init |
| `cognitive_map.py` | 保留，`track_map.py` 的 dir-tree 路径调用它 |
| `archive_triggers.py` | 保留，`track_archive_triggers.py` 的 dir-tree 路径调用它 |

### 5.2 从 `index_update.py` 提取的核心函数

以下函数直接复用（不重写）：
- `get_child_dirs()` / `get_child_files()`
- `count_leaf_files_recursive()`
- `compute_stats()`
- `generate_body_table()`
- `collect_children_metadata()`
- frontmatter 解析/写入 (`common/frontmatter.py`)

## 6. 具体实例: specs/ 索引后的样子

```
specs/
├── INDEX.md                    ← 新 (root, child_count=4, lists 10_reality/20_evolution/90_archive/README.md)
├── _meta/index.yaml            ← 保留 (summary YAML)
├── 10_reality/
│   └── INDEX.md                ← 新 (collection, child_count=6)
├── 20_evolution/
│   ├── INDEX.md                ← 新 (collection)
│   └── active/
│       └── INDEX.md            ← 新 (collection, currently empty)
└── 90_archive/
    └── INDEX.md                ← 新 (collection, child_count=23)
```

## 7. 具体实例: docs/ 索引后的样子

```
docs/
├── INDEX.md                    ← 新 (root, child_count=5)
├── thinking/
│   └── INDEX.md                ← 已有（保持不变，只更新 child_count/stats/updated）
│   └── 00_meta/INDEX.md        ← 已有
│   └── ...
├── guides/
│   ├── INDEX.md                ← 新 (collection)
│   ├── 00_start/INDEX.md       ← 新
│   ├── 10_concepts/INDEX.md    ← 新
│   ├── 20_operations/INDEX.md  ← 新
│   └── 30_comparisons/INDEX.md ← 新
├── marketing/
│   └── INDEX.md                ← 新
├── releases/
│   └── INDEX.md                ← 新
└── evaluation/
    └── INDEX.md                ← 新
```

## 8. verify 产物存在性修复 (所有 track 通用)

在 `track_verify.py` 的 main 入口统一添加产物检查：

```python
def main():
    ...
    track = _track_resolver.resolve(args.track_id)

    # 通用产物存在性门禁 (P4 修复)
    output = track.get("output")
    if output:
        output_path = _find_repo_root() / output
        if not output_path.exists():
            print(f"[track-verify] WARN: output {output} not found — run scan first")
            # 不 fail（scan 可能未运行），但必须报告

    handler = DISPATCH.get(track["type"])
    ...
```

## 9. 实施步骤

| # | 任务 | 依赖 |
|---|------|------|
| C1 | 提取 `index_update.py` 核心函数到 `common/index_gen.py` | 无 |
| C2 | 实现 `_scan_dir_tree()` (新 scan 逻辑) | C1 |
| C3 | 实现 `_verify_dir_tree()` (新 verify 逻辑) | C1 |
| C4 | 更新 DISPATCH 表 (`dir-tree` only，旧类型 error) | C2, C3 |
| C5 | 清洗 `registry.yaml`: type 全改 `dir-tree`，删 modules 段 | C4 |
| C6 | 首次运行: 对 specs/ 和 docs/ 生成 INDEX.md | C5 |
| C7 | 验证: 已有 docs/thinking/ INDEX.md 未被破坏 | C6 |
| C8 | 更新 `index-schema.md` / `SKILL.md` / registry 注释 | C7 |

## 10. 风险与缓解

| 风险 | 严重度 | 缓解 |
|------|--------|------|
| 已有 INDEX.md frontmatter 被意外覆盖 | 🔴 | update-only 模式：只改 child_count/stats/updated |
| body table 格式不兼容 | 🟡 | 已有 INDEX.md 的 body 不重写，只有新建的才生成默认 body |
| 大仓库递归爆炸 | 🟡 | max_depth 限制 + ignore 配置 |
| legacy 脚本行为退化 | 🟡 | 保留 legacy 脚本物理文件，不删除 |
| 残留旧 type 配置未迁移 | 🟢 | DISPATCH 遇到未知 type 直接 error 并提示 |

## 11. DoD (完成标准)

1. `track_scan --track-id specs` → specs/ 下每个子目录有 INDEX.md
2. `track_scan --track-id docs` → docs/ 下每个子目录有 INDEX.md
3. `track_verify --track-id specs` → exit 0，检查 INDEX.md 存在 + frontmatter 合法
4. `track_verify --track-id docs` → exit 0
5. `docs/thinking/INDEX.md` 已有 frontmatter 未被覆盖（segments / stats_schema 保留）
6. 任意新目录通过 registry 配置可接入（只需 type: dir-tree）
7. 所有 track 的 verify 能检测产物缺失
8. registry.yaml 中无任何 `spec-tree` / `docs-tree` 残留
