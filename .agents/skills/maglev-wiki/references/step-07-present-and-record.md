# 步骤 7：呈现结果并记录接受

生成 Markdown 成品验收简报，说明：

- 目标读者和主要阅读任务；
- Plan、Challenge、风险、变更和外部任务的覆盖情况；
- 独立挑战发现的遗漏、差异处置和剩余风险；
- 批准页面完成情况和代表性阅读路径；
- 机械观察摘要；
- 反证尝试、最可能错误的页面和仍然 blocked 的问题；
- 充分性状态：`validated` 或 `provisional`；
- 整体建议：可投入使用、需要定向修订或因证据不足阻断。

没有真实用户问题、独立业务问答，或 Blind Challenge 隔离无法证明时，充分性必须为 `provisional`，不能建议“已充分验证”。

人类明确接受后，才把简报和页面级 review ledger 写入 `.maglev/wiki/wiki-reviews/<review-id>/`。未接受时不得建立增量复用基线。
