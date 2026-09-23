# 步骤 3：审核结构充分性

1. 校验 Source Universe 是否完整覆盖当前来源策略，并校验 Challenge Receipt、Blind Challenge 和 Producer Plan；
2. 由不同于 Producer 和 Challenger 的 Integrator 比较 concerns 与 Plan，生成 `.maglev/wiki/wiki-divergence.yaml`；
3. 每项 concern 必须记录 `covered`、`merged`、`deferred`、`not_applicable` 或 `blocked`，并提供依据和关联页面；`deferred` 与 `blocked` 必须进入 `residual_risks`；
4. Divergence 必须记录 Integrator 标识和独立执行依据；
5. 运行 `wiki_content.py validate-open-world`；
6. 运行 `wiki_content.py render-plan`，生成固定路径 `.maglev/wiki/wiki-plan.md`；该页面必须展示来源依据、隔离与集成记录、差异处置、替代方案和剩余风险；
7. 人类审核该 Markdown；Producer Plan 保持 `pending`，不得自行写成批准；
8. 人类明确批准后，单独生成 `.maglev/wiki/wiki-plan-approval.yaml`，绑定 Plan、Source Universe、Challenge、Divergence 和 Markdown 摘要。

以下情况阻断正文生成：

- Source Universe 缺少策略内来源或混入策略外来源；
- 挑战输入收据包含 Plan、审批、历史 review、临时审阅物或现有 Wiki；
- Challenge 任意层级携带页面结构；
- concern 未处置，或未登记剩余风险与独立 Integrator；
- 任一摘要不一致；
- 固定 Markdown 不是当前开放世界资产的确定性渲染；
- 缺少独立人类审批收据。

仓库收据只能提供可审计声明，不能认证会话历史或人类身份；拥有同等写权限的恶意执行者仍可伪造收据。审批真实性依赖 Agent 只在用户明确批准后签发，充分性保持 `provisional`；需要抵抗恶意写入时必须接入仓库外可信验证器。
