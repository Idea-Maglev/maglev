# AI Context Drift Check

## 目标

在 `dry-run` 或正式 `update` 后，判断项目中的 `AGENTS.md` 与 `llms.txt` 是否已经和当前 Maglev 运行面发生漂移。

## 执行关系

这一步的职责是把 AI context drift check 纳入 `maglev-updater` 的更新语义。

首轮真实执行面位于：

- `packages/maglev-cli/dist/maglev_installer.py`

也就是说：

1. `maglev-updater` 负责承接、解释与结果口径
2. installer 负责在 `update` 结束时真实运行检查
3. 不在 updater skill 内部复制另一套独立判定逻辑

## 参考契约

- `../../_internal/ai-context-check/contract.md`

## 重点检查

1. 是否缺失 `AGENTS.md` 或 `llms.txt`
2. 是否仍把旧 skill runtime name 当当前真名
3. 是否缺少对兼容 workflow 入口的说明
4. 是否混淆 `skill runtime name` 与 `workflow filename / slash entry`
5. 是否继续保留已失效的上游私有现实

## 输出要求

更新流程中的 AI context 检查结果，应以四段输出：

1. `存在性`
2. `充分性`
3. `漂移风险`
4. `最小补齐建议`

## 解释原则

1. 如果文件缺失，不要把问题解释成“升级失败”；应说明这是 AI 上下文资产缺口。
2. 如果内容仍引用旧名，不要只说“文档过时”；应明确指出它会误导 AI 的运行理解。
3. 如果只是保留兼容入口名，不应误判为漂移；关键是是否把兼容入口误写成运行面真名。

## 首轮边界

首轮只检查并解释，不直接重写用户项目文件。
