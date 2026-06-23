# 状态: submodule_pointer_sync_execution

> 最后更新: 2026-05-18T23:30:00+08:00

## 意图

定义 Maglev 是否应支持 submodule pointer 的显式同步，以及如果支持，应以什么方式安全执行。

## 流程进度

⏳ 需求收敛 → ⏳ 方案设计 → ⏳ 编码实施 → ⬜ 综合验证 → ⬜ 结晶归档

## 当前主阶段

编码实施 (in progress, 待综合验证)

## 证据

| 阶段 | 状态 | 关键证据 |
|------|------|---------|
| 需求收敛 | ⏳ | 意图文档: 有目标定义；需求文档: 有决策/安全/语义/运行面要求 |
| 方案设计 | ⏳ | 决策文档 v1 (Explicit Only) + v2 (CLI 形态 A + 行为矩阵)；执行规格 v1 (sync-to-recorded) |
| 编码实施 | ⏳ | `06_implementation_plan_v1.md` + `maglev_installer.py` T1–T10 已落地；fixture 五场景实测通过；端到端 ready→executed 实测把 HEAD 从 3784741 拉回 recorded 975d14e |
| 综合验证 | ⬜ | 待发起 |
| 结晶归档 | ⬜ | — |

## 角色状态

| 角色 | 人员 | 状态 |
|------|------|------|
| VO | (未配置) | 已完成 |
| TP | (未配置) | 主导中 |
| XG | (未配置) | 待介入 |

## 已知阻塞

- （已解除）实施未启动 — 2026-05-18 已启动并完成 T1–T10
- 综合验证未跑：跨真实多 submodule 项目的回归留待下一会话

## 决策修订记录

### 2026-05-18 — Reality Recheck (pending 约 26 天后)

主题在 active 中停留接近 1 个月，跨越了两个大改动（feishu_companion_integration、docs_knowledge_archival_methodology 结晶），需要核对核心方案是否仍与 reality 一致。

**结论：核心决策仍然成立，不推翻**：

- ✅ Explicit Only (拒绝 Default in Update) — 不变
- ✅ 首轮只做 sync-to-recorded — 不变
- ✅ 实施落点 = `maglev_installer.py` — installer 仍存在
- ✅ 阻断条件 6 项 — 全部仍然有效
- ✅ `.maglev/config.json` + `.gitmodules` 二源探测 — 当前 installer 仍是这条路径

**轻量更新**（已合入 master !5）：

- `00_context.md` 新增 §1.5 漂移记录
- `05_execution_spec_v1.md` §3 补充命令侧 A/B 选择
- `05_execution_spec_v1.md` 新增 §12 "已有起点"

### 2026-05-18 — 编码实施启动（本会话）

- 通过 v2 决策 (`04_decision_v2.md`) 敲定 CLI 形态 A（顶层 `--sync-submodules` flag）
- 完成 T1–T10 切片实施（详见 `06_implementation_plan_v1.md`）
- 在 `/tmp/maglev_sync_fixture/` 完成五场景 plan + 行为矩阵 + 端到端真实执行实测
- 对抗审查发现 1 项修复：`os.path.isdir(.git)` → `os.path.exists(...)`（兼容 git worktree）
- 待综合验证：跨真实多 submodule 项目回归

