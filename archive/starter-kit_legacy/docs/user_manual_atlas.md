# Maglev Atlas: 用户导航手册 (User Manual)

> **Motto**: "Stop memorizing tools. Start using the map."

## 1. 核心理念 (Philosophy)
在 Maglev 2.0 中，我们不再强调 "调用技能"，而是强调 **"状态感知"**。
你不需要知道 `maglev-cross-validate` 是干嘛的，你只需要看一眼地图，发现 **"Quality Gate: Blocked"**，然后点击修复即可。

## 2. 三大魔法指令 (Magic Commands)

### `/maglev-map-maker` (The GPS)
*   **何时用**: 每次你迷失方向，或者想向老板汇报进度时。
*   **它做什么**:
    1.  扫描你的 `specs/` 和 `src/`。
    2.  推断你现在的真实状态 (e.g. "Dev Completed, Test Missing")。
    3.  更新 `README.md` 中的可视化地图。

### `/maglev-standup` (The Morning Coffee)
*   **何时用**: 每天早上第一件事。
*   **它做什么**:
    1.  读取 `repository_map.md` (物理空间)。
    2.  读取 `thinking/` (最近决策)。
    3.  告诉 AI："嘿，我们昨天干到这儿了，别失忆。"

### `/maglev` (The Atomizer)
*   **何时用**: 当你有明确意图时 (e.g. "修个 Bug", "做个设计")。
*   **它做什么**: 自动路由到背后那 26 个复杂的原子技能。

## 3. 地图图例 (Map Legend)

### 🌍 世界地图 (World)
*   **Incubation**: 还在写 PPT/Spec 阶段。
*   **Growth**: 疯狂写代码阶段。
*   **Stable**: 修 Bug 阶段。

### 🏔️ 地形图 (Terrain)
*   展示你的 `10_reality` 系统架构 (C4 Context)。如果这里是空的，说明你还在为了写代码而写代码，没有顶层设计。

### 🏙️ 城市地图 (Pipeline)
*   **Inbox**: 你的想都在这。
*   **Draft**: AI 正在写的 Spec。
*   **Active**: 正在被编码的 Spec。
*   **Landed**: 已经上线的 Feature。

## 4. 最佳实践 (Best Practices)
1.  **Don't Touch Active**: 不要手动去改 `specs/20_evolution/active/` 下的文件，那是 AI 的领地。
2.  **Use Intake**: 有想法？丢个文件到 `specs/evolution/intake/`，然后叫 AI "Ingest this"。
3.  **Trust the Map**: 如果地图显示状态不对 (e.g. 明明写了测试却显示未测试)，请检查你的文件存放路径是否符合 Maglev 标准。
