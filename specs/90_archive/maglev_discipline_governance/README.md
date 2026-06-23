# maglev_discipline_governance

> **状态**：✅ Archived (2026-05-24, #23)
>
> 作用：为 Maglev 框架增加反 AI 治理惰性的会话级强制层（maglev-discipline skill + 三层防御）。

## 主入口

- `00_index.md`
- `00_intent.md`
- `01_requirements.md`
- `02_design.md`
- `status.md`

## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality/01_requirements.md §2.8](../../../10_reality/01_requirements.md)
- **关键结论**：
  - 建立 `maglev-discipline` skill（280 行 SKILL.md + 3 references），定义 3 条红线、8 类惰性模式、L0-L4 压力升级与 Task Contract
  - 三层防御落地：L1 AGENTS.md 顶部红线区块 + L2 四主流程 SKILL.md 引用 + L3 完整 skill
  - 系统层：index-librarian 新增 skills track（4 tracks 总计）+ reality-sync 启动期 drift sentinel
  - private-catalog 登记 + maglev-librarian 引用修正
- **执行经验**：
  1. v1 设计被用户否决后 v2 全面重写，核心教训："不要 monolithic 方案，要 composable layers"
  2. 主流程 skill 引用只加一行"交互模式"引用（~15 字），实测证明够用 — 比写长段落更不易被忽略
  3. B3 fixture（drift detection for single file）暴露 repo-entry type 的局限性（只做 pattern 存在性检查），需 v3 引入 `skill-tree` type
  4. A-fixture 无法在同一会话自动化（需冷启动），确认为运营验证而非技术阻塞
  5. track_verify "ok" ≠ 索引产物已生成（只做结构校验），本次会话发现后全量补跑 track_scan + map
- **测试证据**：无 `tests/` 下正式测试文件；验证依赖 B-fixture 可重复命令：
  - `python3 .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills` → exit 0
  - `python3 .agents/skills/index-librarian/protocol/scripts/track_scan.py --track-id skills` → 29 anchors
  - `grep -c 'maglev-discipline' AGENTS.md` → 1 (红线区块存在)
  - `grep -l 'maglev-discipline' .agents/skills/*/SKILL.md` → 4 files (主流程引用)
- **时间线**：2026-05-21 启动 → 2026-05-24 归档
