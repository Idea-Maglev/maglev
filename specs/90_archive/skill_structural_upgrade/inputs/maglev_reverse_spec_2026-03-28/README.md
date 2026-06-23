# maglev-reverse-spec Handoff

## 目的
这是一份针对 `maglev-reverse-spec` 的收敛归档包，用于从当前业务项目回传到 Maglev 项目。

本归档包只保留两类长期有价值的内容：
- 方法论与评审工具
- 代表性逆向样例

当前业务项目中原先散落在 `tmp_reverse_samples/` 下的逆向临时产物，已经收拢到本目录，便于后续整体传递。
`maglev-reverse-spec` 的真实单一事实源保留在当前仓库：

- `.agents/skills/maglev-reverse-spec/`

## 目录结构

- `methodology/`
  - 逆向最低标准、模块分类法等方法论文档
- `review_tools/`
  - 评分表、稳定性检查、通用性审查、最终评审等工具
- `samples/`
  - `Standard / Deep` 代表性样例与对应评审结果

## 推荐传递内容

如果只想最小化回传，优先带走：

1. 当前仓库中的 `.agents/skills/maglev-reverse-spec/`
2. `methodology/reverse_minimum_standard.md`
3. `methodology/reverse_module_taxonomy.md`
4. `review_tools/reverse_review_scorecard.md`
5. `review_tools/reverse_skill_genericity_checklist.md`
6. `review_tools/reverse_stability_checklist.md`
7. `review_tools/reverse_recheck_entry_guide.md`
8. `review_tools/maglev_reverse_spec_final_review.md`

## 样例说明

- `samples/memory_center_standard/`
  - 用于展示 `Standard` 档逆向产物
- `samples/memory_center_deep/`
  - 用于展示 `Deep` 档逆向产物
- `samples/tasks_management_standard/`
  - 用于展示另一类模块的 `Standard` 档产物

这些样例属于当前业务项目语境下的演示材料，不属于 skill 本体。

## 当前结论

当前 `maglev-reverse-spec` 已达到：

- `Maglev-compatible`
- `MPX-business-neutral`
- `Generic reverse skill ready`

并额外具备两条已收敛的协议级约束：

- reverse 默认禁止越界到业务修复
- reverse / reality 产物默认以中文为主

## 维护约束

- 不再在 handoff 包中保存 `skill_snapshot` 副本，避免与仓库内真实 skill 形成双版本维护
- 若要同步到 Maglev，请直接从当前仓库 `.agents/skills/maglev-reverse-spec/` 拷贝

## 备注

当前项目里与本轮逆向沉淀相关、但已经确认冗余的旧文件已从 skill 中清理，不再需要单独归档。
