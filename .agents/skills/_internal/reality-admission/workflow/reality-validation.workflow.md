---
name: reality-validation
description: Committed Reality projection validation handoff
---

# Reality Validation Provider

独立 Validation Provider 验证一个 **已提交的完整 Reality 投影**，而不是独立候选
目录。Coordinator 传递以下结构化值即可，不要求创建 Validation Request 文件：

- repository；
- `base_commit`；
- `candidate_commit`；
- Reality root；
- 模板登记入口、模板包标识和模板包摘要；
- Reverse Work Contract、Module Map、Gate A/B 和逐模块 Semantic Review Package；
- 本轮选定页面及中间复验记录；
- projection / Reality / change digest；
- intended use。

Validator 必须在 checkout `candidate_commit` 的独立 worktree 或等价只读上下文中：

1. 读取同一模板登记入口、登记清单、方法论、适用页面契约、正向示例和模板审阅项；
2. 读取 Work Contract、Module Map、Gate A/B 和中间复验记录，核对流程、页面和逐模块结论；
3. 读取完整仓库代码与完整 `specs/10_reality`；
4. 按模板逐页核对最终页面结构、来源角色、适用性、未知/阻断表达和深挖链接；
5. 逐模块核对目标、入口、边界、依赖、证据和模块间关系；
6. 分别输出 structure、content、confidence 三层 findings；content 必须覆盖 UIUX/前端适用
   时的用户任务、路由、视图/组件、状态、前端源文件和 API/数据连接；
7. 确认所有 Evidence Ref 都可从 candidate commit 读取，而非仅存在于本机或
   ignored 目录；
8. 检查既有 Reality 与本次变化合并后是否一致、无冲突、无退化；
9. 检查 `base_commit → candidate_commit` 的 Reality diff；
10. 覆盖 `explain`、`locate`、`verify` 场景；
11. 返回绑定同一模板包、中间复验、projection、commit、digest 和三层 review result 的
    Validation Result。

Validator 不修改 Reality，不依赖 Producer transcript，也不得只审新增页面而忽略既有
Reality。结果优先通过 Agent/Task 原生返回通道交给 Coordinator；仅当运行载体要求
时才序列化为 JSON/YAML。

输入和输出契约：

- `../protocol/reality_projection.schema.json`
- `../protocol/validation_result.schema.json`
- `../protocol/reality_contract.yaml`
- `../../../maglev-reverse-spec/protocol/work_contract.schema.json`
- `../../../maglev-reverse-spec/protocol/semantic_review_package.schema.json`
- `../../../maglev-reverse-spec/protocol/reverse_review_result.schema.json`

存在模板登记不一致、流程不完整、任一 review 层质量问题、旧事实冲突、缺失证据、
commit/digest 不匹配或阻断性未知时返回 `fail` 或 `blocked`，不得伪造 `pass`。结构通过不能
覆盖内容或置信度失败。

角色边界：`reality_contract.yaml` 与 Admission 脚本只承载机器可追溯性校验（身份字段、
证据存在性、摘要与提交一致性），不规定页面章节、标题、措辞或篇幅。页面结构、写法与
质量结论全部以本轮模板包和 Validation Provider 的三层 review 为准；发现结构或内容
问题时，修复路径是回到模板包对照反思并返工页面，而不是把内容改写成脚本检查项期望
的形状。占位符类残留只会以非阻断 `WARN` 提示出现。
