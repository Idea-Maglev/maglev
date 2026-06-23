# Maglev 存量接入计划 (Project Ouroboros)

> **目标**: 将标准的 "Legacy Adopter" 工作流应用于 Maglev 仓库本身，基于现有的 `starter-kit` 代码库建立真实的 `10_reality` 基线。

## 1. 背景与理念 (Context & Philosophy)
*   **主体**: `<private-repo-path-redacted>/my/maglev` (The Repository).
*   **源码**: `solutions/starter-kit/` (Distributable Source).
*   **策略**: **Flattening / Reshoring (扁平化归位)**。消除嵌套，让根目录即为代码主目录。
*   **标准**: 严格遵循 `maglev-legacy-adopter` 协议。

## 2. 接入工作流 (Adoption Workflow)

### 阶段 0: 源码归位 (Reshoring - The Move)
> **Goal**: 消除 "Project Root" 与 "Starter Kit Root" 的二义性。让 Maglev 根目录直接承载核心源码。

*   **Action**: 将 `solutions/starter-kit/` 下的核心目录安全迁移至项目根目录。
    *   `solutions/starter-kit/.agents/` -> `.agents/` (Merge)
    *   `solutions/starter-kit/.maglev/` -> `.maglev/` (Merge)
    *   `solutions/starter-kit/specs/` -> 暂不覆盖，保持手动管理的 `specs/` 为主，逐步合并。
    *   `solutions/starter-kit/docs/` -> `docs/` (Merge)
*   **Outcome**: `<private-repo-path-redacted>/my/maglev` 成为真正的 Monorepo，不再有 "Project inside Project" 的结构。

### 阶段 1: MRI 扫描 (现状诊断)
*   **目标**: 识别归位后的 Skill 代码库。
*   **动作**: 扫描根目录 `.agents/skills/`，生成 **Feature Map**。
*   **产出**: 更新 `specs/10_reality/repository_map.md`。

### 阶段 2: Spec 归位 (Lift & Shift) 🆕
> **Goal**: 优先迁移已有高质量文档，仅对黑盒代码使用逆向。

*   **Audit**: 许多核心 Skill (`bootstrapper`, `create-spec`) 已包含 `SKILL.md` (Manifest) 和 `references/` (Design Steps)。
*   **Refactor Strategy**:
    *   **Level 1 (Well-Documented)**: 直接提取 `SKILL.md` 为 `01_requirements.md`，提取 `references/` 为 `02_design.md`。这保留了原始设计意图。
    *   **Level 2 (Code-Only)**: 仅对缺乏文档的脚本使用 `maglev-reverse-spec`。
*   **Validation**: 确保提取后的 Spec 与代码逻辑一致。

### 阶段 3: 差异分析 (Gap Analysis)
*   **目标**: 比较 `10_reality` (我们拥有的) 与 `20_evolution` (我们想要的)。

## 3. 执行步骤
1.  **Preparation**: 备份根目录现有配置。
2.  **Reshore**: 执行 `cp -R solutions/starter-kit/.agents .agents` 及相关迁移命令。
3.  **Scan**: 扫描 `.agents/skills` 确认迁移完整性。
4.  **Extract**: 手动提取 `bootstrapper` 的现有文档为标准 Spec。

## 4. 为什么这样做有效？
大部分 Maglev Skill 其实文档健全。与其让 AI 重新猜测并可能产生幻觉（逆向），不如直接**承认现有文档的权威性**并将其标准化。这既节省精力，又避免了信息丢失。

---
*Planned by Maglev Legacy Adopter*
