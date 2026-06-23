---
name: step-verify
description: 索引管家 - 验证步骤，调用 index_verify.py 执行检查清单
next_step: references/calibrate.md
---

# Step: Verify (验证)

## 目标

调用 `index_verify.py` 对注册模块执行检查清单 (L01-L07 + X02-X03 + custom_checks)，向用户展示验证报告。

## 动作

### 1. 确定验证范围

根据 scan 步骤的模块地图，确定验证范围:

- **全局验证** (默认): `./scripts/maglev-python ... --level global --format full`
- **单模块验证**: `./scripts/maglev-python ... --module meetings --level local`
- **单目录快速检查**: `./scripts/maglev-python ... --path meetings/2026/04/`

### 2. 调用验证脚本

```bash
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/index_verify.py \
  --level global --format full
```

### 3. 解读 JSON 输出

```json
{
  "timestamp": "...",
  "scope": {"modules": [...], "level": "global"},
  "nodes_checked": 47,
  "results": {
    "passed": 45,
    "failed": 2,
    "warnings": 1,
    "health_pct": 96
  },
  "issues": [
    {
      "id": "L02",
      "severity": "error",
      "path": "meetings/2026/04/INDEX.md",
      "check": "child_count 一致",
      "expected": 20,
      "actual": 18,
      "fix_hint": "recount"
    }
  ]
}
```

### 4. 展示验证报告

```
# 索引巡检报告

## 健康度: 🟢 96% (45/47 通过)

## 问题 (2)

| # | 位置 | 检查项 | 问题 | 修复建议 |
|:---|:---|:---|:---|:---|
| 1 | meetings/2026/04/INDEX.md | L02 | child_count=18, 实际=20 | 重计数 |
| 2 | comms/groups/INDEX.md | L07 | updated 过期 14+ 天 | 刷新 updated |

执行校准修复上述问题？
```

## Exit Code 处理

| Code | 含义 | AI 动作 |
|:---|:---|:---|
| 0 | 全部通过 | 展示 ✅ 100% 报告，流程结束 |
| 1 | 有 error 级问题 | 展示报告，询问是否进入 calibrate |
| 2 | 脚本自身错误 | 展示错误信息，引导用户排查 |

## 规则

- **禁止自行判断数值**: 不要自己数 child_count 或计算 stats — 这是脚本的职责
- **原样展示**: 脚本报告中的 expected/actual 值直接展示，不做二次计算
- **severity 分级**: error 必须修复，warning 建议修复但不阻断

## 状态流转

- exit code 0 → 流程结束，展示健康报告
- exit code 1 + 用户确认修复 → 进入 `calibrate.md`
- exit code 1 + 用户拒绝修复 → 记录问题，流程结束
- exit code 2 → 停止，排查脚本错误
