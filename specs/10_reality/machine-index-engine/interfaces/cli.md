---
reality_id: machine-index-engine.interfaces.cli
title: 索引引擎 CLI 与导航收据契约
owner_domain: machine-index-engine
owner_slot: interfaces
fact_type: cli_contract
knowledge_status: established
scope:
  includes:
    - track_scan / track_verify / task_navigate 三个脚本的命令行契约
    - 导航收据 JSON 的 status 语义
  excludes:
    - maglev-cli 发行产品命令（属 delivery-runtime 域）
    - 脚本内部实现（属 implementation/index-engine.md）
---

# 索引引擎 CLI 与导航收据契约

## 1. Synopsis 与命令范围

| 入口 | 类型 | 调用方/场景 | 意图来源 | 注册锚点 |
| --- | --- | --- | --- | --- |
| `track_scan.py --track-id <id>\|--all` | 协议脚本 | 维护者/技能流程刷新索引产物 | registry.yaml 头注释（维护: index-librarian / track_*.py） | track_scan.py `main()` argparse |
| `track_verify.py --track-id <id>\|--all` | 协议脚本 | 启动 preflight / 索引巡检 | registry.yaml 头注释 | track_verify.py `main()` argparse |
| `task_navigate.py --intent <文本>` | 协议脚本 | 受控阶段的任务上下文查询 | task_navigate.py 模块 docstring | task_navigate.py `main()` argparse |

## 2. 命令与选项

| 命令/Job | 参数或选项 | 必填/默认事实 | 处理器 | 状态 |
| --- | --- | --- | --- | --- |
| `track_scan.py` | `--track-id` 与 `--all`（互斥，必选其一）；`--debug` | `--debug` 打印 track JSON | `DISPATCH` 按 `track.type` 分派 dir-tree/repo-entry/code-tree | established |
| `track_verify.py` | `--track-id` 与 `--all`（互斥，必选其一）；`--debug` | 同上 | `DISPATCH` 分派；未登记 type 打印 warn 并跳过 | established |
| `task_navigate.py` | `--intent`（必填）；`--root`（默认 `.`）；`--known-source`（可追加）；`--missing-question`（可追加）；`--top-k`（默认 5）；`--receipt-out <path>`；`--validate-receipt <path>` | `--receipt-out` 落盘收据；`--validate-receipt` 复验已有收据 | `navigate` → `_apply_escalation` → `build_receipt` | established |
| `task_navigate.py`（升级链） | `--escalation-step`（限 `refine_scope/reuse_hint/ask_user_hint/controlled_deep_scan`）；`--escalation-attempt`；`--scope-hint`；`--known-source-hint`；`--escalation-note`；`--exhausted` | 仅当结果为 `insufficient` 且提供 `--escalation-step` 时生效；`--exhausted` 将状态置为 `exhausted` | `_apply_escalation` | established |

## 3. 输入、静态可知输出与退出分支

| 入口 | 输入约束 | 静态可知输出/副作用 | exit/失败分支 | 证据 |
| --- | --- | --- | --- | --- |
| `track_scan.py` | track 须在 registry 登记 | dir-tree：`[track-scan] dir-tree <id>: N dirs (created=X, updated=Y, pruned=Z) → <output>`；repo-entry：`wrote N anchors → <output>`；code-tree：`wrote N anchors + radar_summary=ok\|skipped → <output>`；root 缺失打印 `skip: ... not found` | 常规进程语义：handler 返回 0（含 root 缺失跳过）；exit 取各 handler 最大值 | track_scan.py 三 handler 与 `main()` |
| `track_verify.py` | 同上 | 通过：`[track-verify] <type> <id>: ok (N dirs checked)`；失败：`N issue(s)` + 逐条清单（最多打印 15 条）；repo-entry pattern 未命中为 informational，不算失败 | exit = 各 handler 返回值最大值：0=全部通过，1=任一 handler 报告失败 | track_verify.py `_verify_dir_tree` 等 |
| `task_navigate.py` | `--intent` 必填 | stdout 打印收据 JSON（`indent=2`）；`--receipt-out` 追加落盘；`--validate-receipt` 打印 `{"receipt_status": "valid\|stale"}` | `status ∈ {insufficient, exhausted}` → exit 1，否则 exit 0 | task_navigate.py `main()` 返回语句 |

收据字段集（`schema_version`/`status`/`task_fingerprint`/`query`/`sources`/`candidates`/
`missing_categories`/`events`/`created_at`，升级态含 `escalation`）的字段级契约见
`../machine-index-engine/implementation/data.md`；本页只登记 CLI 行为面。

## 4. 导航收据 status 语义

| status | 含义 | 产生条件（代码事实） | 附加字段 |
| --- | --- | --- | --- |
| `not_needed` | 调用方已声明足够来源，无需导航补充 | 提供了 `--known-source` 且未提供 `--missing-question` | 空 `candidates` |
| `queried` | 查到相关权威记录，返回有限、可解释候选 | 打分后有候选，取 `top_k` | `candidates`（含 `score`/`adjusted_score`/`reasons`/`confidence`） |
| `insufficient` | 无相关权威来源，需升级 | 打分后无候选 | `missing_categories`（当前唯一类别：`relevant_authoritative_source`） |
| `escalated` | 在 `insufficient` 基础上进入受控补救动作 | `--escalation-step` 提供且未加 `--exhausted` | `escalation`（step/attempt/basis[/note]） |
| `exhausted` | 补救动作已标记穷尽 | `--escalation-step` + `--exhausted` | `escalation` + `missing_categories` |

消费边界：收据是 index-librarian 与实施能力之间的机器契约。context-implementer
step-02 在 glob/grep 前先取收据并按状态分流：`queried` 围绕候选定位文件、`not_needed`
说明理由后继续、`insufficient`/`escalated`/`exhausted` 不得静默跳过或恢复全域搜索，
须走消费方侧升级纪律（升级链设计文档已失效，见 R1，当前以测试断言与 step-02 现行文本为准）。
`confidence` 限定为 `navigation_confidence`，不作业务证据消费。

### 调用场景与实现锚点

| 入口 | 调用场景 | 实现链 | 测试/验证 | 边界 |
| --- | --- | --- | --- | --- |
| `track_verify.py --track-id skills` | reality-sync 启动 preflight（reality-sync SKILL.md "启动期漂移哨兵"段） | `main()` → resolve → `_verify_dir_tree` 等 handler → exit | `../machine-index-engine/verification/test-matrix.md`（verify handler 无专项测试，见未覆盖表） | 不证明消费方的失败处置行为 |
| `track_scan.py --track-id <id>\|--all` | 维护者/技能流程在结构变更后刷新索引 | `main()` → `DISPATCH` → 各 `_scan_*` | `../machine-index-engine/verification/test-matrix.md`（经 `generate_or_update_index` 间接覆盖） | 不证明部分失败的 track 级路由 |
| `task_navigate.py --intent ...` | context-implementer step-02 上下文收集（glob/grep 前先取收据） | `navigate` → `_apply_escalation` → `build_receipt` → stdout/`--receipt-out` | `tests/test_index_librarian_navigation.py` 收据与升级用例 | 不证明升级链在真实会话中的执行质量 |

## 5. 未知项与深挖

| 项目 | 未知原因 | 已查材料 | 深挖 |
| --- | --- | --- | --- |
| `--help` 文本与国际化输出 | argparse 自动生成，未作为契约登记 | 三个脚本 argparse 段 | `../machine-index-engine/implementation/components.md` |
| `--receipt-out` 写盘失败（路径不可写）的退出分支 | 脚本未定义该分支的显式处理 | task_navigate.py 落盘段 | `../machine-index-engine/operations/errors.md` |
| scan 的 exit 1/2 在当前 handler 实现中的实际触发路径 | 三个 dir-tree/repo-entry/code-tree handler 均返回 0；非 0 退出语义是 SKILL 层 exit 约定 | track_scan.py handler 返回值 | `../machine-index-engine/operations/errors.md` |
