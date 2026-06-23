---
name: step-scan
description: 索引管家 - 扫描步骤，调用 index_scan.py 获取模块地图
next_step: references/verify.md
---

# Step: Scan (扫描)

## 目标

调用 `index_scan.py` 获取所有注册模块的健康状态，向用户展示模块地图。

## 动作

### 1. 调用扫描脚本

```bash
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/index_scan.py --format json
```

### 2. 解读 JSON 输出

脚本返回 JSON 格式的模块地图:

```json
{
  "timestamp": "...",
  "registry_path": "...",
  "modules": [
    {
      "name": "meetings",
      "root_path": "meetings/",
      "root_index": "meetings/INDEX.md",
      "status": "ready|incomplete|missing",
      "issues": ["缺少 index_protocol_version", ...]
    }
  ],
  "summary": {
    "total": 5,
    "ready": 3,
    "incomplete": 1,
    "missing": 1
  }
}
```

### 3. 展示模块地图

向用户展示可读的模块状态表:

```
📊 模块扫描结果

| 模块 | 状态 | 说明 |
|:---|:---|:---|
| meetings/ | 🟢 ready | 协议已就绪 |
| comms/ | 🔴 incomplete | 缺少 stats_schema |
| domains/ | 🟡 bootstrap | 待接入 |
| ... | ... | ... |

共 5 个注册模块: 3 ready, 1 incomplete, 1 bootstrap
```

## Exit Code 处理

| Code | 含义 | AI 动作 |
|:---|:---|:---|
| 0 | 所有模块健康 | 展示地图，提示可进入 verify |
| 1 | 有不可用模块 | 展示地图，标注问题模块，建议先修复 |
| 2 | registry.yaml 不存在 | 提示用户先执行 init 或检查路径 |

## 状态流转

- exit code 0 或 1 → 进入 `verify.md`（用户确认后）
- exit code 2 → 停止，引导用户修复环境
- 用户仅要求 scan → 展示地图后结束
