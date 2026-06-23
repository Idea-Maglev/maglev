# Index Verify Rules — 验证规则定义

> 设计权威: 本文件定义验证检查项、分级和报告格式。
> 执行权威: `scripts/index_verify.py` — 如有矛盾以脚本实际行为为准。
> 来源: spec 02_design.md §4 + spec 04 §3.1 + spec 04 D4

---

## 1. Local Checks (L01-L07)

逐节点检查，每个 INDEX.md 独立验证。

| ID | 名称 | 规则 | 严重度 |
|:---|:---|:---|:---|
| L01 | INDEX 存在 | child_count >= 3 的目录必须有 INDEX.md | error |
| L02 | child_count 一致 | `frontmatter.child_count == actual_children_count` | error |
| L03 | stats.total 一致 | `frontmatter.stats.total == actual_total` | error |
| L04 | 分桶求和 | `sum(stats.buckets) == stats.total` (互斥分桶) | error |
| L05 | 表格行数 | body_table_rows == child_count (底层) 或 == 子索引数 (非底层) | warning |
| L06 | 链接有效性 | body table 中每个链接指向存在的路径 | error |
| L07 | updated 新鲜度 | `updated >= max(children.modified_date) - 14 days` | warning |

### L01 详细规则

- 检查对象: 已注册模块下的所有目录
- 判断条件: 直接子目录数 >= 3 且该目录无 INDEX.md
- 排除: 叶子实体目录（通过 registry 中的 `child_type` 判断）

### L04 详细规则

- 仅检查 stats_schema 中标记为互斥的分桶
- `type: computed` 的 `total` 不参与求和检查（它本身就是和）
- 如果 stats_schema 未声明分桶关系，L04 跳过

### L05 详细规则

- 有 `table_columns` → 严格检查行数
- 无 `table_columns` → 尽力检查（允许表格包含说明文字行）

### L07 详细规则

- 14 天容差窗口：如果子节点 14 天内有变更但 INDEX.md 未更新，报 warning
- 通过比较 `updated` 字段与子目录文件系统 mtime 实现

## 2. Global Checks (X02-X03)

跨模块一致性检查。

| ID | 名称 | 规则 | 严重度 |
|:---|:---|:---|:---|
| X02 | 无孤儿 | 每个叶子实体都能从 root 通过 index chain 到达 | error |
| X03 | 无幽灵 | INDEX.md 中引用的每个路径在文件系统中存在 | error |

### X02 详细规则

1. 从模块 root INDEX.md 开始，递归遍历所有子索引
2. 收集所有被索引覆盖的叶子路径
3. 扫描文件系统中实际存在的叶子目录
4. 差集 = 孤儿 (存在于 FS 但不在索引中)

### X03 详细规则

1. 遍历所有 INDEX.md 的 body table 链接
2. 检查每个链接目标路径是否存在
3. 不存在的 = 幽灵引用

## 3. Custom Checks

由模块在 root INDEX.md 的 `custom_checks` 中声明，实现位于 `scripts/module_checks/{module}.py`。

```yaml
# 示例: meetings 模块
custom_checks:
  - id: "M01"
    name: "系列包含于时间"
    description: "series/ 下每个系列引用的会议都必须在 month/ 时间索引中存在"
    scope: "module"
    severity: "warning"
    implementation: "script"
    script_function: "check_series_in_time"
```

执行流程:
1. 核心检查 (L01-L07) 先执行
2. 全局检查 (X02-X03) 后执行
3. 读取各模块 root INDEX.md 的 `custom_checks`
4. 自动加载 `module_checks/{module}.py` 中对应函数
5. 执行 custom check → 结果合并到总报告

## 4. 报告格式

### JSON 输出 Schema

```json
{
  "timestamp": "ISO 8601",
  "scope": {
    "modules": ["meetings", "comms"],
    "level": "local|global"
  },
  "nodes_checked": 47,
  "results": {
    "passed": 45,
    "failed": 2,
    "warnings": 1,
    "health_pct": 96
  },
  "issues": [
    {
      "id": "L02|X02|M01",
      "severity": "error|warning",
      "path": "相对路径",
      "check": "检查项名称",
      "expected": "期望值",
      "actual": "实际值",
      "fix_hint": "recount|refresh_updated|fix_link|generate_index|manual"
    }
  ],
  "passed_checks": [
    {"id": "L01", "path": "...", "check": "..."}
  ]
}
```

### Exit Codes

| Code | 含义 |
|:---|:---|
| 0 | 全部通过 |
| 1 | 有 error 级问题 |
| 2 | 脚本自身错误 (registry 不存在、Python 版本不满足等) |

## 5. 验证级别

```bash
--level local    # 仅 L01-L07 (快速)
--level global   # L01-L07 + X02-X03 + custom_checks (完整)
```

## 6. 纪律保障

`index_verify.py` 是 commit 前的硬性 gate:
- 它不依赖 AI 的诚实性 — 它自己数、自己比、自己判
- exit code 1 = 阻断，必须修复后再检查
- 任何技能的 persist 步骤最后都应调用 verify 确认
