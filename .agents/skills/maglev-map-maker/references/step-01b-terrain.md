---
name: step-01b-terrain
description: 仓库结构与 Reality 拓扑的数据契约
---

# Step 1b: 仓库结构与 Reality 拓扑

- 仓库结构来自 Git tracked tree，固定排除管理目录、生成目录和依赖目录。
- Reality 拓扑来自 `specs/10_reality/00_profile.yaml`。
- 两个视图均由 `generate_atlas.py` 确定性渲染。
