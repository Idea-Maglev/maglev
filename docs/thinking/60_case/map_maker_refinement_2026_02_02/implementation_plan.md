# Maglev Map Maker Refinement Plan (地图绘制技能优化计划)

## 目标 (Goal)
解决 `maglev-map-maker` 生成独立的 `.mmd` 文件导致在 IDE/CLI 中难以预览的问题。
将地图直接嵌入 Markdown 文件 (`docs/ATLAS.md`)，利用 Markdown 的 Mermaid 渲染能力实现 "所见即所得" 的仪表盘效果。

## 核心变更 (Core Changes)

1.  **统一输出目标 (Unified Output)**
    *   不再生成 `docs/maps/*.mmd`。
    *   统一生成/更新 `docs/ATLAS.md` (Maglev Atlas)。
    *   可选：将核心的 "Project Status" 地图同步更新到根目录 `README.md`。

2.  **技能步骤调整 (Skill Steps Update)**
    *   **Step 1 (World)**: 在 `ATLAS.md` 顶部绘制 "世界状态图" (State Diagram)。
    *   **Step 1b (Terrain)**: 在 `ATLAS.md` 中绘制 "系统地形图" (C4 Context/Class)。
    *   **Step 2 (City)**: 在 `ATLAS.md` 中绘制 "资产流动图" (Flowchart)。
    *   **Step 3 (Street)**: 在 `ATLAS.md` 中绘制 "活跃特性执行图" (V-Model)。

3.  **技术实现 (Implementation)**
    *   使用 `multi_replace_file_content` 或 `write_to_file` (overwrite) 模式。
    *   确保 Mermaid 代码块被正确包裹在 \`\`\`mermaid ... \`\`\` 中。

## 新版 `ATLAS.md` 结构示例

```markdown
# 🗺️ Maglev Atlas (项目全景地图)

> Last Updated: 2026-02-02

## 1. 🌍 World Map (战略层)
[Mermaid Chart]

## 2. 🏔️ Terrain Map (地形层)
[Mermaid Chart]

## 3. 🏙️ City Map (管线层)
[Mermaid Chart]

## 4. 🛣️ Street Map (执行层)
[Feature X Status Chart]
```

## 执行步骤
1.  更新 `SKILL.md` 定义输出目标。
2.  更新 `references/step-*.md` 指令，明确 "Embed in Markdown" 的要求。
3.  创建 `docs/ATLAS.md` 模板（如果是首次运行）。
