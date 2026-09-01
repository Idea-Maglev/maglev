---
description: 确定性项目地图生成工作流
metadata:
  formal_action_name: 项目地图生成
  object_kind: workflow_reference
  output_map: '{project-root}/docs/ATLAS.md'
---

# Map Maker Workflow

```mermaid
flowchart LR
    A[确认 Git 根目录] --> B[读取 Reality 仓库清单与 Profile]
    B --> C[读取项目看板]
    C --> D[扫描 Git tracked tree]
    D --> E[生成结构化 snapshot]
    E --> F[渲染 docs/ATLAS.md]
    F --> G[运行 --check]
```

## 执行步骤

1. 若本次由结晶触发，先确认 `project-board` 已更新。
2. 执行 `scripts/generate_atlas.py --root .`。
3. 执行同一脚本的 `--check` 模式。
4. 报告置信度、来源路径和输出路径。

脚本失败时展示原始错误，不得用手工编写 Atlas 伪装成功。
