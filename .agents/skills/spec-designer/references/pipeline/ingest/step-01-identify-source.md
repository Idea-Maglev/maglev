---
name: 'step-01-identify-source'
description: '识别用户输入类型并获取原始素材'
nextStepFile: './step-02-map-skeleton.md'
---

# 步骤 1: 识别源头 (Identify Source)

## 目标
确定用户想要摄入的信息类型，并收集原始指针。

## 交互流程

### 1. 意图输入检查 (Intent Input Check)
**优先动作**: 使用当前用户已明确的任务描述作为 Raw Intent。
*   **Case A: 已有明确意图**
    *   读取用户输入作为 `intent`。
    *   设置 `slug`，并将 `source` 记录为当前会话或用户提供的相对路径。
*   **Case B: 意图仍不明确**
    *   询问用户："请告诉我想要改变什么，以及这次变更的标题。"
    *   在获得明确意图前不进入方案设计。

### 2. Spec-First Check (Spec 优先检查)
*   **Action**: 检查目录 `{project-root}/specs/20_evolution/active/{slug}` 是否存在。
*   **Logic**:
    *   **If Exists**:
        *   告诉用户: "发现现有 Spec！我们将基于它进行增量开发。"
        *   设置 `ingest_manifest.has_spec = true`。
        *   设置 `ingest_manifest.complexity = "incremental"`。
        *   **Skip**: 直接跳过后续扫描，跳转到 `step-03-zoom-extract.md` (并在那里做特殊处理)。
    *   **If Not Exists**:
        *   继续执行下一步 (Source Identification)。

### 3. Complexity Classification (复杂度判断)
**仅当没有 Spec 时执行**:
根据 Intent 判断复杂度：
*   **Simple**: 纯UI修改、文案修改、小Bug修复 -> 设置 `complexity = "low"`。
*   **Complex**: 涉及逻辑变更、新功能、重构 -> 设置 `complexity = "high"`。

### 4. 识别源头 (Source Identification)
**仅当 Complexity = High 且没有 Spec 时执行**:
"看起来这是一个全新的复杂任务。请告诉我输入类型：
1. **Docs**: 已有文档路径
2. **Legacy**: 存量代码目录"

(如果 Complexity = Low，自动跳过此步，直接进入 Fast Track)

### 5. 构建 `ingest_manifest`
```json
{
  "slug": "{slug}",
  "intent": "{intent}",
  "has_spec": true/false,
  "complexity": "low/high/incremental",
  "source": "{source}",
  "type": "idea/doc/legacy"
}
```

### 6. 前进
*   如果 `has_spec == true` OR `complexity == "low"` -> 跳转 `step-03-zoom-extract.md` (Fast Track)。
*   否则 -> 跳转 `step-02-map-skeleton.md` (Full Scan)。
