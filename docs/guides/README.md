# Maglev 指南

> 这里汇总 Maglev 的使用手册、概念说明、生态对比与进阶话题。

## 如果你只想知道先看什么

第一次接触 Maglev，建议先看：

1. [快速开始](./20_operations/maglev_distribution_quickstart.md)
2. [初始化使用手册](./20_operations/maglev_init_manual.md)
3. [更新与同步手册](./20_operations/maglev_update_manual.md)
4. [多入口使用说明](./20_operations/maglev_entrypoints.md)
5. [角色与流程翻译](./20_operations/maglev_role_flow_translation.md)

如果你已经在维护 Maglev 本身，且想先理解最近这一轮 skill 结构升级与命名调整后的项目现状，建议补看：

1. [Maglev 当前定位](../../internal Reality/positioning.md)
2. [交付运行时 Reality](../../internal Reality/delivery-runtime/README.md)
3. Active Evolution Index

如果你更关心“这套东西为什么这样设计”，再看：

1. [Maglev 协议白皮书](./10_concepts/maglev_paradigm_architecture.md)
2. [AI 代理权模型](./10_concepts/ai_agency_model.md)
3. [效率矩阵设计](./10_concepts/efficiency_matrix_design.md)

如果你是在评估老项目接入路径，建议先看：

1. [项目启动手册](./00_start/project_startup_manuals.md)
2. [遗留项目接入指南](./00_start/legacy_project_adoption.md)

如果你在公司私域环境中使用 Maglev，请先阅读对应私域指南，再回到这里查通用操作手册：

1. [私域文档入口](../private deployment context/INDEX.md)

## 目录说明

| 目录                                   | 作用                         |
| :------------------------------------- | :--------------------------- |
| [`00_start/`](./00_start/)             | 启动、接入与团队落地         |
| [`10_concepts/`](./10_concepts/)       | 核心概念与方法论解释         |
| [`20_operations/`](./20_operations/)   | 日常操作、安装、更新、排障   |
| [`30_comparisons/`](./30_comparisons/) | 和相邻方法、产品、范式的对比 |
| `90_advanced/`       | 高级配置与进阶治理议题       |

## 00_start

- [project_startup_manuals.md](./00_start/project_startup_manuals.md)
  - 新项目和老项目的两条启动路径。
- [legacy_project_adoption.md](./00_start/legacy_project_adoption.md)
  - 存量项目如何渐进式接入 Maglev。
- [maglev_traditional_team_kickoff.md](./00_start/maglev_traditional_team_kickoff.md)
  - 面向传统团队的温和 kickoff 话术与引导。

## 10_concepts

- [maglev_paradigm_architecture.md](./10_concepts/maglev_paradigm_architecture.md)
  - Maglev 的总体范式与核心结构。
- [ai_agency_model.md](./10_concepts/ai_agency_model.md)
  - AI 在不同阶段的自主边界与责任划分。
- [efficiency_matrix_design.md](./10_concepts/efficiency_matrix_design.md)
  - Spec、Code、Bug、Case、Design、Platform 的效率闭环。
- [role_personas.md](./10_concepts/role_personas.md)
  - AI 时代研发铁三角的角色画像。
- [maglev_organization_architecture.md](./10_concepts/maglev_organization_architecture.md)
  - Maglev 对研发组织结构的影响。
- [role_models_analysis.md](./10_concepts/role_models_analysis.md)
  - Copilot、Agent、Partner 等角色模型比较。
- [maglev_self_healing.md](./10_concepts/maglev_self_healing.md)
  - 如何通过验证闭环发现和修正偏差。

## 20_operations

当前最推荐的操作链路：

1. [maglev_distribution_quickstart.md](./20_operations/maglev_distribution_quickstart.md)
2. [maglev_init_manual.md](./20_operations/maglev_init_manual.md)
3. [maglev_update_manual.md](./20_operations/maglev_update_manual.md)
4. [maglev_entrypoints.md](./20_operations/maglev_entrypoints.md)
5. [maglev_role_flow_translation.md](./20_operations/maglev_role_flow_translation.md)
6. [maglev_distribution_troubleshooting.md](./20_operations/maglev_distribution_troubleshooting.md)
7. [maglev_release_manual.md](./20_operations/maglev_release_manual.md)

当前主流程的项目级理解口径是：

1. `现状同步（reality-sync，兼容入口：/standup）`
2. `方案设计（spec-designer，兼容入口：/create-spec）`
3. `上下文实施（context-implementer，兼容入口：/quick-dev）`
4. `综合验证（integrated-validator，兼容入口：/validate-all）`

如果你是维护者，准备修改 Maglev 本身并执行版本发布，建议追加阅读：

7. [maglev_development_release_workflow.md](./20_operations/maglev_development_release_workflow.md)

其他操作文档：

- [逆向现状重建使用手册](./20_operations/reverse_reality_manual.md)
  - 面向其他项目，从一手材料重建现状并完成现实资料准入。
- [collaboration_playbook.md](./20_operations/collaboration_playbook.md)
  - 团队协作与 Git / Review 基本约定。
- [human_fallback_protocol.md](./20_operations/human_fallback_protocol.md)
  - AI 不可用时的人类接管方案。
- [minimalist_toolchain.md](./20_operations/minimalist_toolchain.md)
  - 极简工具链建议。
- [user_manual_atlas.md](./20_operations/user_manual_atlas.md)
  - 安装后如何理解 Maglev 的常见工作方式与导航思路。
- [maglev_role_flow_translation.md](./20_operations/maglev_role_flow_translation.md)
  - 用传统项目角色和阶段语言理解 Maglev 主流程对象。
- [transition_guide.md](./20_operations/transition_guide.md)
  - 传统角色向 AI 原生协作方式迁移的建议。
- [maglev_development_release_workflow.md](./20_operations/maglev_development_release_workflow.md)
  - 面向维护者的开发、版本管理与发布主路径。

## 30_comparisons

- [maglev_vs_bmad.md](./30_comparisons/maglev_vs_bmad.md)
- [maglev_vs_openspec.md](./30_comparisons/maglev_vs_openspec.md)
- [maglev_vs_gsd.md](./30_comparisons/maglev_vs_gsd.md)
- [maglev_vs_harness_engineering.md](./30_comparisons/maglev_vs_harness_engineering.md)
- [maglev_vs_kiro.md](./30_comparisons/maglev_vs_kiro.md)
- [maglev_vs_sdd.md](./30_comparisons/maglev_vs_sdd.md)
- [vibekanban_integration_analysis.md](./30_comparisons/vibekanban_integration_analysis.md)
- [maglev_universality_analysis.md](./30_comparisons/maglev_universality_analysis.md)
- [toolchain_adversarial_analysis.md](./30_comparisons/toolchain_adversarial_analysis.md)

## 90_advanced

- ai_native_config_templates.md
  - AI 原生项目的配置模板。
- governance_adapter_design.md
  - 不同 IDE 和工具环境下的治理适配。
