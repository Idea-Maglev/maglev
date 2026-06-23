# Requirements: AI 上下文文件整合

## R1: 消除三文件重叠

AGENTS.md、llms.txt、core_rules.md 中重复的内容应只保留在一个文件中：

- 语言规则 → AGENTS.md（唯一来源）
- 目录/文件体系 → AGENTS.md（已有速查表）
- 命令入口 → llms.txt（保留其"AI 快速上手"定位）
- Runtime names → AGENTS.md（已有，llms.txt 中删除重复段）

## R2: core_rules.md 退役

core_rules.md 的 12 条指令经核查：
- 4 条与 AGENTS.md/llms.txt 重复（BOOTSTRAP, TRUTH_FIRST, LANGUAGE, DASHBOARD）
- 4 条已被现有 skill 覆盖（EVIDENCE→reverse-spec, TRACEABILITY→integrated-validator, INDEXING→maglev-librarian, CAPTURE→knowledge-check）
- 2 条引用不存在的文件（LOGGING→docs/dev_log.md, USER_FOCUS→.maglev/user.yaml）
- 2 条理念有价值但实现路径过时（COLLAB, CUSTODIAN）

处理方式：
1. 不原样搬运——避免双重指令和引用不存在的路径
2. 从中提炼 2-3 条仍有价值且未被覆盖的原则，以适配当前仓库现状的方式写入 AGENTS.md
3. core_rules.md 标记 deprecated 后删除
4. 更新 llms.txt 中对 core_rules.md 的引用

## R3: 项目宪法定位（取消）

经核查，不需要单独的"项目宪法"文件：
- `specs/00_vision.md` §3 已有北极星原则（Spec First, Observe Before Act, Think Before Code, Verify Before Closeout）
- 操作级治理已由 skill 层覆盖
- 8 条规则中无内容需要新的承载位置

## R4: llms.txt 精简

去除与 AGENTS.md 重复的内容后，llms.txt 应保持"AI 快速入口"定位：
- 关键命令（slash commands）
- 文件体系概览（可精简，不与 AGENTS.md 表格重复）
- 分发入口与操作手册链接
- 删除 §2 "核心法则"段落（不再引用 core_rules.md）
- 删除 §5 "AI 上下文资产"段落（AGENTS.md 已覆盖）
