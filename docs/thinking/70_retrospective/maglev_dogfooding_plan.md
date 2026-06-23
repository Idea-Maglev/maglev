# Maglev 自举计划 (Project Ouroboros)

> **目标**: 使用 Maglev 自带的 `maglev-bootstrapper` 技能对自己进行初始化，从而确立 Maglev 项目自身的 "单一真理来源" (Single Source of Truth)。

## 1. 现状分析
*   **当前状态**: 项目中包含 `.agents/` 和一些 `specs/` (可能是之前步骤生成的 `maglev_system/`)。
*   **目标**: 运行标准的 `maglev-init` 流程，将 `<private-repo-path-redacted>/my/maglev` 视为我们正在构建的"产品"。

## 2. 初始化策略 (Bootstrapping Strategy)

### 步骤 1: 飞行前检查 (Pre-Flight Check)
*   验证 `solutions/starter-kit/.agents/skills/maglev-bootstrapper/` 是否为最新版本。
*   确认我们处于 **Adoption Mode (存量接入模式)** 而非 Template Mode。

### 步骤 2: 执行初始化 (The "Init")
执行 `maglev-bootstrapper`，并输入以下信息：
*   **项目名称**: "Maglev OS"
*   **愿景**: "一个 AI 原生的工程化操作系统，通过铁三角协议将意图转化为可靠的软件。"
*   **仓库类型**:
    *   `./`: **Monorepo** (核心系统)
    *   `./solutions/starter-kit`: **Product** (分发包)
    *   `./.agents`: **Engine** (运行时引擎)

### 步骤 3: Spec 生成
引导程序将触发生成以下文件：
1.  **`specs/01_requirements.md`**:
    *   *输入*: Maglev 的核心价值主张 (来自 `README.md` & `llms.txt`)。
    *   *输出*: Maglev 自身的结构化 PRD。
2.  **`specs/02_design.md`** (或 `architecture.md`):
    *   *输入*: 当前目录结构分析。
    *   *输出*: `Thinking`, `Solutions`, `Specs`, `Standards` 的架构映射。

### 步骤 4: 整合 (Integration)
*   将之前手动创建的 `specs/maglev_system/` 合并到由引导程序生成的官方 `specs/` 结构中。
*   `maglev_system` 可能会被移动到 `specs/20_evolution/feature_maglev_manager/`，或者作为核心模块 Spec 保留。

## 3. 验证标准 (Verification)
*   **成功标准**:
    *   `specs/01_requirements.md` 存在且准确描述了 Maglev。
    *   `specs/10_reality/repository_map.md` 准确反映了 `maglev` 仓库结构。
    *   `task.md` 已更新为 "Evolution Phase" 任务。

## 4. 风险与缓解
*   **风险**: 覆盖现有的 `README.md` 或配置。
*   **缓解**: 引导程序在检出文件前应询问。我们将仔细审查 diff。

---
*Created by Maglev Spec Architect*
