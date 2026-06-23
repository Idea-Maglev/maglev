---
name: step-calibrate
description: 索引管家 - 校准步骤，修复验证发现的问题并 re-verify
next_step: null
---

# Step: Calibrate (校准)

## 目标

根据 verify 步骤发现的问题，分类执行修复，然后 re-verify 直到全部通过。

## 输入

来自 verify 步骤的 issues 列表 (JSON):

```json
{
  "issues": [
    {
      "id": "L02",
      "severity": "error",
      "path": "meetings/2026/04/INDEX.md",
      "fix_hint": "recount"
    }
  ]
}
```

## 修复分类

| fix_hint | 执行方式 | 说明 |
|:---|:---|:---|
| `recount` | 脚本 (index_update.py) | 重计 child_count 和 stats |
| `refresh_updated` | 脚本 (index_update.py) | 刷新 updated 字段 |
| `add_row` | 脚本 (如有 table_columns) 或 AI | 表格缺行 |
| `remove_row` | 脚本 (如有 table_columns) 或 AI | 表格多余行 |
| `fix_link` | AI | 修复断链 |
| `generate_index` | 脚本 (index_init.py) | 生成缺失的 INDEX.md |
| `manual` | AI + 用户确认 | 需要人工判断 |

## 动作

### 1. 对问题分组

将 issues 按修复方式分为两组:
- **脚本可修**: recount, refresh_updated, add_row (有 table_columns), generate_index
- **需 AI 介入**: fix_link, remove_row (无 table_columns), manual

### 2. 执行脚本修复

对脚本可修的路径，批量调用 update:

```bash
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/index_update.py \
  --path meetings/2026/04/ --path comms/groups/ --full
```

### 3. 执行 AI 修复

对需 AI 介入的问题:
1. 向用户展示每个问题的上下文
2. 提出修复建议
3. 用户确认后执行修改
4. 修改后标记为已处理

### 4. Re-verify (必须)

修复完成后，必须重新执行 verify:

```bash
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/index_verify.py \
  --path {所有修复过的路径} --level local --format json
```

### 5. 循环直到通过

```
WHILE verify exit code != 0:
  展示剩余问题
  执行修复
  re-verify
```

**最大迭代**: 3 轮。如果 3 轮后仍未全部通过:
- 展示剩余问题列表
- 建议用户手动介入
- 不要无限循环

## 展示修复结果

```
🔧 校准完成

修复了 2 个问题:
  ✅ L02: meetings/2026/04/INDEX.md — child_count 18→20
  ✅ L07: comms/groups/INDEX.md — updated 刷新

Re-verify: 🟢 100% (47/47 通过)
```

## 规则

- **用户确认**: 任何修改在执行前必须获得用户确认
- **Re-verify 是硬性要求**: 不 re-verify 就不能声明校准完成
- **不猜测**: 如果不确定修复方式，展示问题上下文并询问用户
- **日志**: 每次 calibrate 的 update 调用都会自动记录到 .index-logs/

## 状态流转

- re-verify exit code 0 → ✅ 流程结束
- 达到最大迭代次数 → 展示剩余问题，建议手动修复
