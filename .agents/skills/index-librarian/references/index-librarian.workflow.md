---
name: index-librarian-workflow
description: 索引管家工作流 — scan → verify → calibrate 三步编排
---

# Index Librarian Workflow

## 步骤链

```
scan → verify → calibrate (条件触发)
```

| 步骤 | 文件 | 何时执行 |
|:---|:---|:---|
| scan | `references/scan.md` | 始终 — 第一步 |
| verify | `references/verify.md` | scan 完成后 — 第二步 |
| calibrate | `references/calibrate.md` | verify 发现问题时 — 条件触发 |

## 路由规则

### 用户意图 → 入口步骤

| 触发词 | 入口 | 说明 |
|:---|:---|:---|
| "检查索引" / "索引巡检" / "verify" | scan | 完整流程 |
| "扫描模块" / "scan" | scan | 仅 scan，不自动 verify |
| "修复索引" / "校准" / "calibrate" | verify | 先 verify 确认问题，再 calibrate |
| "索引状态" / "status" | scan | scan --format summary |
| "初始化索引" / "init" | init | 独立流程，不经过 scan-verify-calibrate |

### 初始化流程 (独立)

当用户请求初始化时，直接调用 `index_init.py`，不经过 scan-verify-calibrate 流程。
初始化完成后，建议用户执行一次完整的 verify。

## 流程图

```
用户请求
  │
  ├─ "检查/巡检/verify" ──→ [scan] ──→ [verify] ──→ 有问题? ──→ [calibrate]
  │                                                    │
  │                                                    └─ 无问题 → ✅ 报告健康度
  │
  ├─ "扫描/scan" ──→ [scan] ──→ 展示模块地图
  │
  ├─ "修复/校准" ──→ [verify] ──→ [calibrate] ──→ re-verify
  │
  └─ "初始化/init" ──→ index_init.py ──→ 建议 verify
```

## 脚本调用约定

所有脚本路径基于:
```
SCRIPTS=".agents/skills/index-librarian/protocol/scripts"
```

JSON 输出是脚本与 AI 之间的接口契约。AI 读取 JSON 输出，不要自行计算验证数据。
