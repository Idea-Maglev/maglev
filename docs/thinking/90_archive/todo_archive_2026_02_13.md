# Archived TODOs - 2026-02-13

Following items were moved from `TODO.md`.

- [x] **开发文档逆向引导 Skill (Software Archaeologist)**
    - **来源**: 遗留项目接入讨论 (Step 794)
    - **背景**: 针对 "高负债" 代码 (Legacy Projects)，单纯靠文档 `legacy_project_adoption.md` 可能不够。负责人面对庞大的旧代码库时，需要一个交互式的 AI 助手来引导他一步步做“划界”、“逆向”和“存证”。
    - **目标**: 创建一个 `.agents/skills/reverse_engineer_guide`，不仅提供 Prompt 模板，还能主动询问用户“你想先动哪个模块？”，并生成对应的 `specs/reverse/` 文件结构。
    - **Status**: 已创建于 `solutions/skills/reverse_engineer_guide/SKILL.md`（产品交付物）。

- [x] **开发方法论构建 Skill (Methodology Architect)**
    - **来源**: 思考模式复用讨论 (Step 936/957)
    - **背景**: 用户希望将 Maglev 自身“从辩证思考到文档落库”的**元方法论 (Meta-Methodology)** 沉淀为 Skill，用于指导后续对 Maglev 体系本身的贡献。
    - **目标**: 创建 `solutions/skills/contribute_methodology`，固化 Thinking -> Solution -> Index -> Log 的产出闭环。
    - **Status**: 已创建于 `solutions/skills/contribute_methodology/SKILL.md`（产品交付物）。

- [x] **Maglev 生产与验证体系 (Phase 1 & 2)**
    - **来源**: 产物标准与稳定性讨论 (Session 88ff5dcc)
    - **Phase 1: 交付物标准 (The Standards)**
        - **Status**: [x] 完成。已建立 `specs/10_reality/` 和 `specs/20_evolution/` 标准结构，并由 `maglev-audit-spec` 强制执行。
    - **Phase 2: 交叉验证 (The Matrix)**
        - **Status**: [x] 完成。已发布 `maglev-cross-validate` 技能，支持 "Spec vs Code" 和 "PRD vs Spec" 的双向一致性扫描。

- [x] **Maglev Atlas 导航体系 (Project Navigation)**
    - **来源**: 技能膨胀与迷航问题 (Session 2026-02-02)
    - **背景**: 随着技能数量突破 20+，用户不知道"现在该用哪个技能"。
    - **目标**: 从 "工具箱" (Toolbox) 转变为 "驾驶舱" (Cockpit)。
    - **Status**: [x] 已发布。
        - 产出 `maglev-map-maker`: 自动生成 World/Terrain/City/Street 四层地图。
        - 重构 `README.md`: 引入 Dashboard 和魔法指令 (`/maglev-map-maker`)。
        - 文档体系: 统一 `docs/thinking/` 路径，发布 `user_manual_atlas.md`。

- [x] **Deep Mode 技能深化 (Skill Evolution)**
    - **来源**: 技能空心化问题 (Session 2026-02-02)
    - **背景**: 生成的脚本缺乏 BMM (Brain-Machine-Mind) 的深度，偏向 rote execution。
    - **目标**: 引入 "Facilitator" 角色和 "Socratic Questioning"。
    - **Status**: [x] **已完成**。
        - [x] Phase 0: 创建 `deep-mode-interview.template.md` 通用模板。
        - [x] Phase 1: `maglev-quick-spec` 升级为 Product Architect。
        - [x] Phase 2: `maglev-design-ux` 升级为 Empathetic Design Partner。
        - [x] Phase 3: `maglev-research` 升级为 Research Lead。
