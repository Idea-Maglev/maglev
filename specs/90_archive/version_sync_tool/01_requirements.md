---
title: "Version Sync Tool - Requirements"
status: "Superseded"
---

# 01 Requirements: 功能边界与规约 (Ready-to-Code)

> 本组 Spec 已被 `specs/20_evolution/active/maglev_distribution/` 吸收，以下内容仅作为历史约束来源保留，不再作为现行入口要求。

## 1. 核心能力诉求 (In-Scope Capabilities)

### 1.1 轻量级无痕执行 (Zero-Dependency Execution)
*   **形态**: 必须支持通过纯 Python (>= 3.8) 标准库直接运行，不依赖 `requests`、`PyYAML` 等必须通过 pip 安装的第三方库。
*   **入口**: 历史方案曾设想以单文件脚本（例如 `maglev_sync.py`）作为入口；当前该能力已并入统一的 `maglev_installer.py`。

### 1.2 高保真安全状态同步 (High-Fidelity Safe Sync)
该工具不仅负责“下载”，更负责“安全仲裁”。它必须覆盖以下四个核心文件级同步场景：
1.  **新增 (Addition)**: 远端上游拥有新的 Skill 或 Protocol，本地不存在。-> **Action**: 自动下载放至对应的本地目录。
2.  **静默更新 (Silent Update)**: 上游文件有更新，且用户在本地**从未修改**过该文件（比对本地与本地基线 Hash 相等）。-> **Action**: 覆盖更新为官方最新版。
3.  **魔改避险备份 (Modified Backup & Overwrite)**: 上游文件有更新，但用户在本地**修改**了该文件（比对本地 Hash 与基线 Hash 不一致）。-> **Action**:
    *   将用户修改版文件（如 `maglev-quick-dev/SKILL.md`）原址重命名备份为 `maglev-quick-dev/SKILL.local_backup_<timestamp>.md`。
    *   下载并放置官方最新版本到原路经。
    *   收集此事件，最终在终端输出显眼的冲突红名单。
4.  **配置合并 (Incremental Merge)** (MVP Phase 暂不实现深度 AST 合并，以基准 JSON/Dict 处理为主): 对于 `.maglev/` 下的配置元数据集，尽量执行增量 KV 合并而非全量覆盖；遇到同 Key 冲突，永远以用户本地的 Key 为尊。

### 1.3 版本宣告与自愈烙印 (Version Provenance & Reporting)
1.  **打入烙印**: 所有被这个工具同步拉取下来的 Maglev 规范或核心技能中（如果是 Markdown 或 JSON 且支持 Frontmatter/Metadata），应当隐式挂载 `_maglev_engine_version: "vX.Y.Z"` 标记，以便未来审计。
2.  **强制播报 (Changelog Broadcast)**: 工具拉取成功后，必须从上游下载当次更新的 `CHANGELOG.md` 并在终端以格式化的形式（纯文本高亮）向执行人播报。

## 2. 交互与用户体验 (UX & CLI Definition)

### 2.1 终端指令输出预期
历史方案中，用户输入 `python .maglev/maglev_sync.py`（或包装好的 `/maglev-update` 命令）时，标准输出流程应当包含：
1.  **Init**: `🔍 正在解析本地状态基线...`
2.  **Fetch**: `📡 正在连接 Maglev 星环... 发现新版本: v2.1.0 -> v2.2.0`
3.  **Process**:
    *   `[+] 下载新文件: .agents/skills/maglev-research/SKILL.md`
    *   `[~] 覆盖旧文件: .agents/skills/maglev-create-spec/SKILL.md`
    *   `[!] 冲突避险触发: 本地 .agents/skills/maglev-quick-dev/SKILL.md 已被修改。`
        *   `-> 本地修改已备份为: SKILL.local_backup_171000.md`
        *   `-> 官方新版本已放入原位，请视需手工 Diff。`
4.  **Finish**: 在末尾打印最新 Changelog 的前 N 行。

## 3. 验收标准 (Acceptance Criteria)

- **AC-1 (本地状态溯源)**: 运行完毕后，必定会在 `.maglev/sync_state.json` 中存储刚刚被干预过的所有文件的最新官方 Hash 值。这是下次迭代的判据基石。
- **AC-2 (断网与重试)**: 若远端 Upstream 不可达，工具必须要在 3 秒内超时并抛出优雅的断网提示，不能导致工作区文件被删改了一半的“破损态 (Corrupted State)”。
- **AC-3 (幂等性)**: 如果在同一个版本（Upstream Version = Local Version）连跑两次 Sync，第二次必须极速结束并提示 “当前已被完全覆盖，无需更新”，不引发多余的网络下载。

## 4. 排除事项 (Out-of-Scope)
- 不去处理 Maglev 核心框架 (`.agents/`、`.maglev/`) 以外的用户业务代码库。
- MVP 阶段不提供复杂的交互式终端选择器（如：让用户按空格键挑选取舍哪个文件），全部采用“全量备份+全量强拉”的傻瓜式策略。
