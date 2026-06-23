# context check integration spec v1

> 状态：已形成首版接入规格
> 作用：明确 `AGENTS.md` / `llms.txt` 的 AI 上下文自检能力如何接入 `maglev-bootstrapper` 与 `maglev-updater`。

## 1. 接入对象

### A. `maglev-bootstrapper`

接入位置：

- 初始化完成后的后置检查阶段

目标：

- 判断新接入项目是否具备最小 AI context readiness

输出：

1. `AGENTS.md` 是否存在
2. `llms.txt` 是否存在
3. 是否达到最小可用标准
4. 若不足，给出最小补齐建议

说明：

- `maglev-bootstrapper` 承接这项能力的用户语义
- 真实执行面由 installer 负责

### B. `maglev-updater`

接入位置：

- `dry-run` 前后解释阶段
- 正式 `update` 后的检查建议阶段

目标：

- 判断现有项目的 AI context 是否已与当前 Maglev 能力结构漂移

输出：

1. 是否仍停留在旧 runtime name
2. 是否混淆 skill runtime name 与 workflow 兼容入口
3. 是否缺少对 init / update / 关键主流程入口的说明
4. 是否混入明显上游私有内容

说明：

- `maglev-updater` 承接这项能力的用户语义
- 真实执行面由 installer 负责

## 2. 首轮统一检查结果结构

首轮建议统一成四段：

1. `存在性`
2. `充分性`
3. `漂移风险`
4. `最小补齐建议`

## 3. 首轮最小实现方式

首轮不要求新增复杂模板系统。

更合理的最小实现是：

1. 在 `maglev-bootstrapper` / `maglev-updater` 的 references 中新增检查步骤
2. 基于本地文件读取和规则判断输出结果
3. 先以检查和提示为主，不直接自动重写文件

## 4. 当前不做

首轮不做：

1. release 构建纳入 `AGENTS.md` / `llms.txt`
2. manifest 增加这两个文件
3. installer 原样下发这两个文件
4. 自动 merge 或自动覆盖

## 5. 当前实现状态

首轮最小实现已按下面方式落地：

1. `maglev-bootstrapper` 已接入 `step-04-ai-context-check.md`
2. `maglev-updater` 已接入 `references/ai-context-drift-check.md`
3. `packages/maglev-cli/dist/maglev_installer.py` 已实现最小检查逻辑，并在 `init` / `update` 结束时输出结果
4. 已提供最小草稿参考模板，用于承接“最小补齐建议”

当前职责分层：

1. skill / workflow：负责承接与解释
2. installer：负责真实执行

## 6. 首轮验收标准

首轮实现完成时，至少应满足：

1. `maglev-init` 结束时会告诉用户项目 AI 上下文是否达到最小可用标准
2. `update --dry-run` 或 `maglev-updater` 会告诉用户这两个文件是否已漂移
3. 检查结果能明确指出：
   - 缺文件
   - 旧 runtime name
   - 入口说明缺失
   - 上游私有内容污染
