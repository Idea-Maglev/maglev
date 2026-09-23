# 步骤 2：独立推导结构与问题空间

## Source Universe

先运行 `wiki_content.py build-universe`，完整登记配置允许根目录中的实际文件与摘要、排除项、变更信号和可选 Evidence Provider。后续校验会重新枚举来源策略，缺失来源或策略外来源都会阻断。该清单只证明当前执行看过什么，不定义页面或内容目标。

## Producer Plan

生产 Agent 读取 Source Universe 和项目材料，推导维度、方面、页面、读者任务、用途、来源与合并/拆分理由，写入 `.maglev/wiki/wiki-plan.yaml`。Plan 是提案，不是内容或验收全集。

## Blind Challenge

使用独立、空白上下文的挑战 Agent。只向其提供 Source Universe、受众提示、人类可读契约和挑战协议；不得提供：

- `.maglev/wiki/wiki-plan.yaml` 或 `.maglev/wiki/wiki-plan.md`；
- `.maglev/wiki/wiki-divergence.yaml` 或审批收据；
- 现有 `docs/wiki/` 正文、历史 review 和临时审阅物；
- 生产 Agent 的推理或目录建议。

挑战 Agent 生成：

- `.maglev/wiki/wiki-challenge-receipt.yaml`：规范化实际可见输入、完整禁止输入、协议摘要、不同 Producer/Challenger 标识、隔离机制和执行证据；
- `.maglev/wiki/wiki-challenge.yaml`：读者问题、遗漏候选、风险、深度信号和来源。

Challenge 任意层级都不能出现维度、页面、页面路径或页面绑定。无法提供不同执行者和执行依据时，必须使用 `unproven`，不得声称隔离已成立。原始代码扫描和 attention map 只能作为 Provider 输入，不能直接决定页面。
