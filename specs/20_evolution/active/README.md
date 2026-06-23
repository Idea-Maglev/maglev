# active evolution index

> 作用：只保留当前仍在推进、尚未封板的 `20_evolution` 主题。

## Spec 目录标准结构

```
active/feat_xxx/
├── 00_index.md                 # 索引与元数据
├── 00_intent.md                # 意图与问题陈述
├── 01_requirements.md          # 功能需求
├── 02_design.md                # 技术设计
├── 03_plan.md                  # 实施计划
├── context/                    # AI 上下文数据区
│   ├── input_facts.md          # [必需] 方案设计输入事实基准
│   └── {semantic_name}.*       # [可选] 字段规则、代码分析、配置快照等
├── ref/                        # 外部引用（可选）
│   └── ...                     # PRD 原稿、设计图等不可变输入
└── status.md                   # 看板状态（由 project-board 生成）
```

> `context/` 与 `ref/` 的区分规则见 `.maglev/protocols/collaboration.md` §3。

## 当前仍在进行中的主题

1. [spec-provenance-governance](./spec-provenance-governance/00_index.md)
   - Spec 来源依据、AC 上下文判定与 AI 语义变更记录治理
   - 当前阶段：validated，待人工复核 / 提交

## 搁置中的主题

1. extension_point_architecture
   - Skill 框架层与执行层分离
   - 设计方案保存在 feature 分支 `feat/extension-point-architecture`
   - 搁置原因：任务尚未成熟
   - 对应 issue 在 `issues/draft/`
   - spec 文件已从 active 目录移除

## 当前为什么没有清空 `active/`

当前 1 个主题在进行中，1 个搁置。

只要这条线还没有明确 `Reject`、正式 closeout，或真实实现落地，它就不应被挪进归档。

## 已归档主题

其余已封板主题已统一迁入：

- [../../90_archive/README.md](../../90_archive/README.md)

包括：

1. `skill_structural_upgrade`
2. `spec_pipeline_internalization`
3. `runtime_name_strategy`
4. `runtime_rename_migration`
5. `runtime_rename_execution_preflight`
6. `runtime_rename_execution`
7. `runtime_rename_post_cleanup`
8. `workflow_name_strategy`
9. `runtime_naming_governance`
10. `agent_context_assets_sync`
11. `submodule_adoption_model`
12. `lifecycle_closure_disambiguation`
13. `archive_mechanism_redesign`
14. `context_file_consolidation`
15. `main_flow_quality_gates`
16. `spec_document_architecture`
17. `ai_context_data_area`
18. `project_board_skill`
