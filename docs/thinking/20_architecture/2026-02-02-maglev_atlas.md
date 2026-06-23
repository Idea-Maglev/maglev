# Maglev Atlas: 分形地图与状态感知 (The Fractal Map)

> **Date**: 2026-02-02
> **Topic**: State Awareness & Navigation
> **Status**: Crystallized

## 1. 核心理念 (Concept)
Maglev 不应强制用户记忆 "技能列表"，而应提供 "定位服务"。
**Maglev Atlas** 是一个多层级 (Multi-Scale)、分形 (Fractal) 的动态地图系统，用于回答三个终极问题：
1.  **Where am I?** (当前处于生命周期的哪个阶段？)
2.  **What's missing?** (缺少了 Design？还是 Test？)
3.  **Where to go?** (下一步该调用什么技能？)

---

## 2. 三层比例尺 (Three Scales)

### 🌍 Scale 1: 世界地图 (World Map) - 战略视图 (Time)
*   **对象**: 项目生命周期
*   **节点**: `Idea` -> `MVP` -> `PMF` -> `Growth`
*   **用途**: 判断当前所处的"时间阶段"。

### 🏔️ Scale 1.5: 地形地图 (Terrain Map) - 结构视图 (Space)
*   **对象**: `specs/10_reality/` (Reality Layer)
*   **内容**: 系统上下文 (System Context) 或 领域模型 (Domain Model)。
*   **呈现**: Mermaid C4-Context 或 Class Diagram。
*   **用途**: 回答 "这个系统长什么样？有哪些模块？" (Structure)。
*   **更新源**: 扫描 `10_reality/` 下的架构与模型文件。

### 🏙️ Scale 2: 城市地图 (City Map) - 战术视图
*   **对象**: 特性流水线 (`specs/20_evolution/`)
*   **节点**: `Inbox` (20个意图) -> `Active` (3个进行中) -> `Review` (1个验收中)
*   **呈现**: Mermaid Kanban / Class Diagram
*   **用途**: 资源分配。识别瓶颈 (e.g., Inbox 堆积，Active 阻塞)。

### 🛣️ Scale 3: 街道地图 (Street Map) - 执行视图
*   **对象**: 单个特性 (`specs/20_evolution/active/{slug}/`)
*   **节点**: `Reqs` -> `Design` -> `Plan` -> `Code` -> `Verify`
*   **呈现**: Mermaid Flowchart
*   **用途**: 具体的技能导航 (Next Best Action)。

---

## 3. 更新机制：解耦 vs 联动 (Decoupled vs Coupled)

用户之问：*地图的更新是跟其他技能联动，还是单独总结？*

**决策：Artifact-Driven State Inference (ADSI) —— 彻底解耦**

### 为什么不联动 (Anti-Coupling)？
如果我们要求 `quick-spec` 跑完后去回调 `update-map`，或者 `quick-dev` 跑完后去通知 `update-map`:
1.  **脆弱**: 任何一个技能挂了，地图就不同步了。
2.  **入侵性**: 每个新技能都要写 "汇报逻辑"，开发者体验极差。
3.  **不真实**: "汇报" 可能是假的。

### 也就是 "Observer Pattern" (观察者模式)
Maglev Atlas 应该像一个 **雷达 (Radar)**，它**只扫描产物 (Artifacts)**：
*   *"我看到了 `02_ui_design.md` 文件存在 => 所以当前状态包含 Design"*。
*   *"我扫描到 `src/` 下有新代码，但没有 `test/` => 所以当前状态是 Unverified Code"*。

**结论**: 地图由 `maglev-map-maker` 技能**独立扫描生成**。它反映的是 **客观事实 (Reality)**，而不是 **流程状态 (Process)**。

---

## 4. 技能设计: `maglev-map-maker`

*   **Role**: The Cartographer (制图师)
*   **Input**: 文件系统扫描 (`ls -R specs/`, `ls src/`)
*   **Logic**:
    *   Load Rules: `.maglev/rules/atlas_rules.md` (定义什么文件代表什么状态)
    *   Infer State: 推导当前 Phase。
    *   Draw: 生成中文 Mermaid 代码。
*   **Output**:
    *   `docs/maps/world_map.mmd`
    *   `docs/maps/pipeline_map.mmd`
    *   `docs/maps/{slug}_street_map.mmd`
    *   `README.md` (Update dashboard section)
