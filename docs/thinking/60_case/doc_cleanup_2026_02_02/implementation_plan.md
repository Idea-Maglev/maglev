# Maglev 文档重构计划

## 目标
治理日益膨胀的 `docs/thinking/` (20+ 文件) 和 `solutions/guides/` (24+ 文件) 目录，建立清晰的、基于 Johnny Decimal 思想的分类体系，提升文档的可发现性。

## 原则
1.  **关注点分离 (Separation of Concerns)**:
    *   `docs/thinking/`: **Why & What** (哲学、架构、批判、决策记录)。
    *   `solutions/guides/`: **How** (手册、Playbooks、具体操作指南)。
2.  **可扩展性 (Scalability)**: 使用数字前缀 (e.g., `00_`, `10_`) 预留扩展空间。
3.  **可发现性 (Discoverability)**: 区分 "红药丸 (Red Pill)" 与 "说明书 (Instruction Manual)"。

---

## 建议结构: `docs/thinking/` (The "Why")

现状：混杂了逻辑推演、批判反思和架构决策的扁平列表。

### `00_meta/` (元理论 & 哲学)
*   Maglev 的基石理论。
*   *候选文件*: `meta_paradigm_analysis.md`, `atomizer_uncertainty_principle.md`, `transparency_as_feature.md`, `spec_as_universal_ir.md`

### `10_critique/` (批判与反思)
*   自我反思、红队测试、风险分析。
*   *候选文件*: `defense_completeness_myth.md`, `fleet_vision_critique.md`, `tech_generation_critique.md`, `2026-02-02-maglev_vs_bmm_critique.md`, `reflection_phase1_risks.md`

### `20_architecture/` (架构设计)
*   具体的系统设计与关键决策。
*   *候选文件*: `atomic_spec_architecture.md`, `2026-02-02-maglev_atlas.md`, `visual_verification_strategy.md`, `tech_robustness_gap_analysis.md`, `skill_safety_analysis.md`

### `90_archive/` (归档)
*   过往的任务清单或已过时的推演。
*   *候选文件*: `deep_mode_rollout_2026_02_02/`, `reverse_spec_redesign_2026_02_01/`, `skill_extension_2026_02_01/`

---

## 建议结构: `solutions/guides/` (The "How")

现状：宏观对比与微观手册混杂。

### `00_start/` (启动与接入)
*   新手入门、安装引导、Kickoff。
*   *候选文件*: `project_startup_manuals.md`, `maglev_traditional_team_kickoff.md`, `quick_start.md`, `legacy_project_adoption.md`

### `10_concepts/` (核心概念)
*   理解角色、组织与模型。
*   *候选文件*: `role_personas.md`, `role_models_analysis.md`, `maglev_organization_architecture.md`, `maglev_paradigm_architecture.md`, `efficiency_matrix_design.md`

### `20_operations/` (日常与操作)
*   项目运行、协作SOP、工具链。
*   *候选文件*: `collaboration_playbook.md`, `human_fallback_protocol.md`, `minimalist_toolchain.md`, `user_manual_atlas.md`

### `30_comparisons/` (生态对比)
*   Maglev 与其他范式的定位差异。
*   *候选文件*: `maglev_vs_bmad.md`, `maglev_vs_openspec.md`, `maglev_vs_sdd.md`, `vibekanban_integration_analysis.md`

### `90_advanced/` (进阶话题)
*   小众或深度的定制话题。
*   *候选文件*: `governance_adapter_design.md`, `ai_native_config_templates.md`

---

## 执行步骤
1.  **从头创建**：建立新的目录结构。
2.  **物理迁移**：移动文件 (保留 Git 历史)。
3.  **更新索引**：修正 `README.md` 和 `INDEX.md` 中的链接。
