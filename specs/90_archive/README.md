# specs archive index

> 项目编年史：记录已完成需求的结晶状态、关键结论和执行经验。
> 日常运作中偏忽略，仅在分析、溯源和复盘时读取。

## 归档口径

归档条目满足以下条件：
1. 已完成结晶 — 结论已写入 `10_reality`
2. 已填写归档日志 — 包含结晶状态、关键结论、执行经验、时间线
3. 不再作为当前活跃工作面

## 归档条目

| # | 主题 | 结晶状态 | 关键结论 | 归档时间 |
|---|------|---------|---------|---------|
| 1 | [skill_structural_upgrade](./skill_structural_upgrade/) | ⚠️ 历史条目 | — | pre-v2 |
| 2 | [spec_pipeline_internalization](./spec_pipeline_internalization/) | ⚠️ 历史条目 | — | pre-v2 |
| 3 | [runtime_name_strategy](./runtime_name_strategy/) | ⚠️ 历史条目 | — | pre-v2 |
| 4 | [runtime_rename_migration](./runtime_rename_migration/) | ⚠️ 历史条目 | — | pre-v2 |
| 5 | [runtime_rename_execution_preflight](./runtime_rename_execution_preflight/) | ⚠️ 历史条目 | — | pre-v2 |
| 6 | [runtime_rename_execution](./runtime_rename_execution/) | ⚠️ 历史条目 | — | pre-v2 |
| 7 | [runtime_rename_post_cleanup](./runtime_rename_post_cleanup/) | ⚠️ 历史条目 | — | pre-v2 |
| 8 | [workflow_name_strategy](./workflow_name_strategy/) | ⚠️ 历史条目 | — | pre-v2 |
| 9 | [runtime_naming_governance](./runtime_naming_governance/) | ⚠️ 历史条目 | — | pre-v2 |
| 10 | [agent_context_assets_sync](./agent_context_assets_sync/) | ⚠️ 历史条目 | — | pre-v2 |
| 11 | [submodule_adoption_model](./submodule_adoption_model/) | ⚠️ 历史条目 | — | pre-v2 |
| 12 | [lifecycle_closure_disambiguation](./lifecycle_closure_disambiguation/) | ✅ → 10_reality §2.10 | 后段技能路由消歧 + 归档门禁机制 + 生命周期边界形式化 | 2026-04-11 |
| 13 | [archive_mechanism_redesign](./archive_mechanism_redesign/) | ✅ → 10_reality §2.10 | crystallization 5 步流程 + Step 5 门禁 + 90_archive 结构化索引 | 2026-04-11 |
| 14 | [context_file_consolidation](./context_file_consolidation/) | ✅ → 10_reality §2.11 | 三文件→两文件 + core_rules 退役 + 不需要项目宪法 | 2026-04-11 |
| 15 | [main_flow_quality_gates](./main_flow_quality_gates/) | ✅ → 15 个 skill 文件 | 审批门禁 + 结构化 AC + AC 追溯链 + 设计模板标准化 + 任务依赖图 + 审计评分 + 验证层前端能力 | 2026-04-14 |
| 16 | [spec_document_architecture](./spec_document_architecture/) | ✅ → 8 文件 + glossary.md | 交互文档模板 + 术语表机制 + 文档互联互验 | 2026-04-14 |
| 17 | [ai_context_data_area](./ai_context_data_area/) | ✅ → collaboration.md §3 + specs_lifecycle §2 + step-01-split-files | context/ 目录约定标准化 + context/ vs ref/ 区分规则 + 禁止 backup 和个人命名空间 | 2026-04-22 |
| 18 | [project_board_skill](./project_board_skill/) | ✅ → 10_reality §2.4 + repository_map §4.4 | 标准 Skill `project-board` 建立 + board.md 总看板 + status.md 子看板 + 证据驱动阶段判断 + cache 契约守护 | 2026-04-23 |
| 19 | [runtime_distribute_project_index_protocol](./runtime_distribute_project_index_protocol/) | ✅ → 10_reality §2.4 + distribution_runtime §2.3 | docs-index-protocol v2.0 multi-track + index-librarian D27 报告契约 + maglev-librarian 物理废弃 + release.py distribution_scope 校验与 dist catalog 拆分 | 2026-04-29 |
| 20 | [feishu_companion_integration](./feishu_companion_integration/) | ✅ → repository_map §1 第 10 行 | 三套飞书工具合一为私域 skill `feishu-companion` + 三处反混淆基线 + 私域 skill 治理面统一承载于 `.agents/private-catalog.yaml` | 2026-04-29 |
| 21 | [docs_knowledge_archival_methodology](./docs_knowledge_archival_methodology/) | ✅ → repository_map §1 行 13 + §2 工具层 | docs/thinking 9 位段化结构 + collection INDEX 网络 + F1/F6/F8 协议骨架（lifecycle/archive_triggers/cognitive_map）+ schema 计数语义 + maglev-librarian → index-librarian 接力 | 2026-05-18 |
| 22 | [submodule_pointer_sync_execution](./submodule_pointer_sync_execution/) | ✅ → distribution_runtime.md §2.1 + §4 | installer `--sync-submodules` CLI（形态 A）+ init / 已有 .git 双路径自动拦截 submodule pointer drift + Explicit Only + 仅 sync-to-recorded + worktree 兼容修复（v0.4.1 承载） | 2026-05-18 |
| 23 | [maglev_discipline_governance](./maglev_discipline_governance/) | ✅ → 10_reality §2.8 | 反 AI 惰性治理 `maglev-discipline` skill + 三层防御（L1 AGENTS.md / L2 主流程引用 / L3 完整 skill）+ skills track + drift sentinel | 2026-05-24 |
| 24 | [superpowers_integration](./superpowers_integration/) | ✅ → 10_reality §2.3 + positioning.md §4 | 代码执行委托 `superpowers-bridge` skill + context-implementer 退出代码执行 + Skill 优先级协议 + SP 不是终态的架构灵活性 | 2026-06-01 |
| 25 | [version_json_flag](./version_json_flag/) | ✅ → distribution_runtime.md §2.2 | CLI `version --json` 子命令，输出结构化版本信息 | 2026-06-01 |
| 26 | [evolution_observatory](./evolution_observatory/) | ✅ → 10_reality §2.8 + competitive_registry.yaml | 持续进化观测 skill + 竞品 Registry + 6 Phase 工作流 + Insight Schema v2 + 9 项功能路线图 | 2026-06-01 |
| 27 | [unified_doc_tree_indexer](./unified_doc_tree_indexer/) | ✅ → index-librarian 脚本层 | spec-tree/docs-tree 统一为 dir-tree + common/index_gen.py 提取 + verify 产物存在性检查 + 任意目录通过 registry 配置接入 | 2026-06-01 |

## 当前进行中主题

→ [20_evolution/active/README.md](../20_evolution/active/README.md)
