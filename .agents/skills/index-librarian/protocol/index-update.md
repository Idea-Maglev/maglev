# Index Update Protocol — 更新协议定义

> 设计权威: 本文件定义索引更新的触发时机、冒泡规则和写入规则。
> 执行权威: `scripts/index_update.py` — 如有矛盾以脚本实际行为为准。
> 来源: spec 02_design.md §3 + spec 04 §3.2 + spec 05 §1

---

## 1. 触发时机

任何技能的 persist/archive 步骤完成文件写入后，必须触发索引更新。

### 1.1 嵌入方式

在各技能的 persist 步骤中添加:

```
### N. 更新索引 (Index Protocol)

调用:
  ./scripts/maglev-python .agents/skills/_internal/index-protocol/scripts/index_update.py \
    --path {本步骤写入的文件路径}

输入: 本步骤写入/修改/删除的所有文件路径
输出: 更新后的 INDEX.md 文件列表
```

### 1.2 AI 调用流程

```
1. AI 调用: index_update.py --path {paths} --dry-run
   → 预览将要修改哪些 INDEX.md

2. AI 调用: index_update.py --path {paths}
   → 脚本更新 frontmatter (child_count, stats, updated)
   → 脚本返回 body_tables_needing_ai_update 列表

3. AI 更新 body tables (需要语义理解的部分)
   → 仅对无 table_columns 的节点

4. AI 调用: index_verify.py --path {affected_indexes} --level local
   → exit code 0 → ✅ 索引更新完成
   → exit code 1 → ❌ 修复后重试
```

## 2. 冒泡规则

```
FUNCTION update_index(written_path):
  1. current_dir = parent_dir(written_path)
  2. WHILE current_dir has INDEX.md with type: entity-index:
       a. scan current_dir for children
       b. recount stats from children frontmatter
       c. update INDEX.md frontmatter (child_count, stats, updated)
       d. IF table_columns defined: regenerate body table
       e. current_dir = parent_dir(current_dir)
  3. STOP when reaching module root (scope:root) — root 也更新，但不继续向上
```

## 3. 写入规则

| 字段 | 更新方式 |
|:---|:---|
| `child_count` | 重新计数直接子目录/文件 |
| `stats.total` | = `child_count` (底层) 或 `sum(children.stats.total)` (非底层) |
| `stats.{bucket}` | 按 `stats_schema` 中的 `rule` 重新计算 |
| `updated` | = today |
| body table | 有 `table_columns` → 脚本重生成; 无 → 返回 `body_tables_needing_ai_update` |

## 4. Body Table 排序

排序由模块 root INDEX.md 的 `sort_key` 和 `sort_order` 声明决定:
- 子索引继承父索引的 sort 配置，除非自身显式覆盖
- 无 sort 声明时默认: `sort_key: "name", sort_order: "asc"`

## 5. 脚本接口

```bash
# 单路径冒泡
./scripts/maglev-python index_update.py --path meetings/2026/04/17-1400-team-weekly/

# 多路径批量
./scripts/maglev-python index_update.py --path path1/ --path path2/

# Dry-run (预览，不写入)
./scripts/maglev-python index_update.py --path ... --dry-run

# 全量重算 (不看增量)
./scripts/maglev-python index_update.py --module meetings --full
```

### 5.1 脚本职责边界

| 能做 | 不能做 |
|:---|:---|
| 更新 frontmatter 数值字段 | 创建不存在的 INDEX.md |
| 向上冒泡到 root | 决定新 INDEX.md 的结构 |
| 有 table_columns 时重生成 body table | 无 table_columns 时生成 body 内容 |
| 重排 body table 行序 | 修改人写的 README.md |

## 6. 幂等性

多次对同一路径执行 update，frontmatter 值不变（因为总是从实际状态计算）。
