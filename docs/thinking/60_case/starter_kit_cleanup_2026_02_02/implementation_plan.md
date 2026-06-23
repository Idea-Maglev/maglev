# Starter Kit Cleanup Plan (起步套件清理计划)

## 目标 (Goal)
确保 `solutions/starter-kit` 与主仓库的最新架构 (JD 目录、Deep Mode、Atlas) 保持完全一致，消除死链和过时概念。

## 变更范围 (Scope)

### 1. 链接修复 (Link Fixes)
*   **`.maglev/protocols/specs_lifecycle.md`**:
    *   移除或修正指向 `johnny_decimal_theory.md` 和 `maglev_product_lifecycle.md` 的死链。
    *   建议指向 `docs/thinking/00_meta/meta_paradigm_analysis.md` 或直接引用通用概念。
*   **`README.md`**:
    *   将 `docs/user_manual_atlas.md` 修正为部署后的实际路径 (用户初始化后通常在 `docs/20_operations/user_manual_atlas.md`，或者直接指向 Guide 目录)。
    *   *Note*: Starter Kit 的 README 是用户项目的根 README。用户初始化后，`solutions/guides` 会被复制哪里？
    *   *Check*: `maglev_init_guide.md` 并没有说要复制 `solutions/guides` 到用户项目。它只复制 `.agents` 和 `.maglev` 和 `issues/README.md`。
    *   *Correction*: Starter Kit 的 README 引用了 `docs/user_manual_atlas.md`，这意味着 `user_manual_atlas.md` 应该存在于用户的 `docs/` 下。需要确认 Init Guide 是否搬运了这个文件。如果没有，应该修正为指向 Online Doc 或建议用户创建。

### 2. Atlas 对齐 (Atlas Alignment)
*   **Map Maker Skill**: 确认 Starter Kit 中的 `maglev-map-maker` SKILL.md 是否已包含 "Unified ATLAS.md" 的变更。
*   **README Dashboard**: 更新 Mermaid 占位符，提示用户运行 `/maglev-map-maker` 生成 `docs/ATLAS.md`。

### 3. Init Guide 修正
*   `maglev_init_guide.md`: 检查是否需要更新以支持 Johnny Decimal 结构的创建 (如 `docs/thinking/00_meta` 等)。

## 执行计划
1.  修正 `specs_lifecycle.md`。
2.  修正 `starter-kit/README.md`。
3.  检查 `maglev-map-maker` 内容。
4.  检查 `maglev_init_guide.md` 目录创建逻辑。
