# submodule pointer sync execution

> **状态**：✅ Archived (2026-05-18, #22)
>
> 作用：在 `submodule_adoption_model` 已封板的前提下，单独处理"是否以及如何执行 submodule pointer 同步"的高风险实现问题。

## 主入口

- `00_intent.md`
- `00_context.md`
- `01_requirements.md`
- `02_design.md`
- `03_plan.md`
- `04_decision_v1.md`
- `05_execution_spec_v1.md`

## 当前说明

本主题不重新讨论：

1. submodule 是否值得作为可选模式
2. `clone / submodule` 双模式是否成立

这些已经在：

- `../archive/submodule_adoption_model/`

里收口。

本主题只处理：

1. pointer sync 是否允许执行
2. 通过什么触发
3. 执行前如何阻断风险
4. 执行后如何提示用户提交 pointer 变化

当前首版决策已经形成：

- 第一层结论：`Explicit Only`
- 第二层结论：首轮只考虑 `sync-to-recorded`

当前已经进入 execution spec 阶段，但仍未进入真实实现：

- 首轮只为 `sync-to-recorded` 定义触发、阻断和结果解释
- `sync-to-latest` 继续留在范围外

## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality/distribution_runtime.md §2.1 + §4](../../../10_reality/distribution_runtime.md)
- **关键结论**：
  - installer 端实现 `--sync-submodules` 顶层 CLI（决策形态 A），同时在 init / 已有 `.git` 两条路径上自动拦截 submodule pointer drift；
  - 阻断 6 项 + Explicit Only + 仅 sync-to-recorded 三层保护全部落地；
  - 对抗审查发现并修复 `os.path.isdir('.git')` 在 git worktree 下误判 → 改 `os.path.exists`；
  - v0.4.1 发版承载该能力。
- **执行经验**：
  - active 在主题间停留接近 1 个月，跨越 feishu_companion + docs_knowledge_archival 两次结晶；2026-05-18 做 reality recheck 确认核心方案未漂移再启动编码，避免基于陈旧 spec 实施；
  - 真实 fixture（`/tmp/maglev_sync_fixture/`）的 5 场景行为矩阵 + 端到端 execute 是发现 worktree 兼容 bug 的关键证据；
  - npm publish 是 `maglev_release.py` 之外的手工动作，发版 SOP 已在 `docs/thinking/70_retrospective/release_0_3_3_execution_lessons.md` 沉淀。
- **测试证据**：
  - `tests/test_maglev_submodule_status.py`
  - `specs/20_evolution/active/submodule_pointer_sync_execution/06_implementation_plan_v1.md`（T1–T10 实测证据 + 与 spec 对照矩阵）
- **时间线**：2026-04-20 启动 → 2026-05-18 归档
