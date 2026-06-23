# 📋 runtime_distribute_project_index_protocol

- **状态**: Archived
- **类型**: Protocol / Skill / Release Tooling
- **负责人**: Creator
- **最后更新**: 2026-04-29

## 导航

| 文件 | 说明 |
|------|------|
| [00_intent.md](00_intent.md) | 意图与问题陈述 |
| [01_requirements.md](01_requirements.md) | 功能需求 |
| [02_design.md](02_design.md) | 技术设计 (v5.2) — 含 §5 行为对等性矩阵 + §6 AC 矩阵 |
| [status.md](status.md) | Step 4 验证记录 + integrated-validator 综合验证报告 |

## 归档日志

- **结晶状态**：✅ 已完成 → `specs/10_reality/01_requirements.md` §2.4（`index-librarian` 条目改述为 multi-track v2.0），`specs/10_reality/distribution_runtime.md` §2.3（补充 `distribution_scope` 校验 + dist catalog 拆分 + `check_runtime_distribution.py` CI 脚本）
- **关键结论**：
  - `docs-index-protocol` 升级为 v2.0 multi-track（4 track type：spec-tree / docs-tree / repo-entry / code-tree），`registry.yaml` 默认含 3 实例（specs / docs / repo-entry），`code-tree` 由用户按需启用
  - 新增 `_track_resolver.py` + 4 个 generic 入口（`track_scan` / `track_map` / `track_verify` / `track_archive_triggers`） + `_code_tree_helpers.py`（含 anchors 抽取 + radar 委派降级）
  - 4 个 `registry.example.<type>.yaml` 模板覆盖全部 track 类型，用户加 track 走 `references/track-extension.md`
  - `index-librarian/SKILL.md` v2.0：D27 报告契约（radar_summary 纪律 + 多 track 状态模板，含 ok/partial/skipped/failed 4 态枚举）+ 委派 radar 边界（不重复 hotspot 算法）
  - `maglev-librarian` 物理废弃：skill 目录 / workflow / `smart_map.py` 全部删除，catalog 整段移除 + `replaces` 关系边保留作 historical trace
  - `scripts/maglev_release.py` 新增 `step1b_verify_distribution_scope`（catalog scope 枚举校验）+ `step3b_split_catalog`（dist 仅含 user_visible 条目 + dangling relations 清洗）+ runtime_internal 资产显式纳入；`scripts/check_runtime_distribution.py` 独立 CI 脚本守护边界
  - 上游主题 `docs_knowledge_archival_methodology` 的 K2 决策（仅覆盖 Track B docs/）已加 2026-04-28 范围修订标注，本主题完成 Track A/C 的同等替代与物理退役
- **执行经验**：
  - 行为对等性矩阵（3 default × 4 维度 = 12 格）作为 D15 强制 Gate，比纯 AC 复核更能保证"换底盘不退化"
  - catalog `distribution_scope` 枚举包含 `private_only`（实战值不在原 spec D11/D12 列举中），spec 与现网枚举对齐应在 step1b 前拉一遍真值
  - 14 个 runtime_internal skill 通过现存 `_is_public()` 关键字过滤侥幸不分发；step3b 用 catalog SSOT 收紧后边界明确
  - radar binary 不在 PATH 时 D26 兜底降级写 `{skipped: True, reason}`，冒烟全程未中断
  - 在源仓库做 step1b/step3b 单元冒烟足够；端到端 dry-run install 留给 release pipeline 真发版前
- **测试证据**：
  - 无正式 `tests/` 文件；证据链由以下三类构成
  - **冒烟**：`track_scan/verify` × 3 default tracks 全 exit 0（status.md §B 12 格记录）
  - **CI 脚本**：`scripts/check_runtime_distribution.py`（当前 repo exit 0；故意构造泄漏 dist exit 1）
  - **AC 矩阵**：26 项 AC 25✅+1⚠️ Minor，记录于 `status.md` 综合验证报告段
- **已知限制**（不阻塞归档，作为后续演进输入）：
  - U-V5-1：radar binary 在 maglev 安装链路中的可用性保障（首次发版前补）
  - U-V5-2：`radar_summary.max_output_lines=200` 默认值缺实战 benchmark
  - AC-F6 dry-run install 端到端验证：留给 release pipeline 首次真发版前执行
- **时间线**：2026-04-27 启动 → 2026-04-29 归档
