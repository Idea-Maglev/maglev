# Handoff Transfer Checklist

## 目标
把本次在业务项目中收敛完成的 `maglev-reverse-spec` 相关成果，稳定传回 Maglev 项目。

## 推荐回传顺序

### 1. 回传 skill 主体
将以下目录整体带回：

- `.agents/skills/maglev-reverse-spec/`

这是最核心的回传对象，包含：
- 最新 `SKILL.md`
- 最新 `references/`
- 最新 `templates/`
- `mri_scanner.py`

### 2. 回传方法论文档
建议同时带回：

- `methodology/reverse_minimum_standard.md`
- `methodology/reverse_module_taxonomy.md`

这两份文档对应“逆向结果最低标准”和“模块分类法”，适合给后续 skill 或 workflow 继续复用。

### 3. 回传评审工具
建议带回：

- `review_tools/reverse_review_scorecard.md`
- `review_tools/reverse_review_result_template.md`
- `review_tools/reverse_skill_genericity_checklist.md`
- `review_tools/reverse_stability_checklist.md`
- `review_tools/reverse_stability_quickcheck.md`
- `review_tools/reverse_recheck_entry_guide.md`
- `review_tools/maglev_reverse_spec_final_review.md`

这些文档适合作为后续验证、review 和演进的配套工具。

### 4. 选择性回传样例
按需带回：

- `samples/memory_center_standard/`
- `samples/memory_center_deep/`
- `samples/tasks_management_standard/`

这些样例是当前业务项目语境下的验证材料，不是 skill 本体。
如果 Maglev 主仓只想要方法论和 skill，不一定需要全部回传。

## 本次回传必须确认的新增约束

1. `reverse` 过程默认禁止业务修复
2. `reverse / reality` 产物默认以中文为主

如果目标仓已有旧版 `maglev-reverse-spec`，请确认这两条约束不会在合并时被覆盖掉。

## 回传时要同步处理的删除项

如果 Maglev 主仓还保留以下旧文件，建议删除：

- `references/step-01-scope-lock.md`
- `references/step-02-strata-analysis.md`
- `references/step-03-reconstruction.md`
- `references/legacy-tech-spec-template.md`
- `references/review-adversarial-reverse.xml`

这些文件在本轮已经确认属于旧流程残留。

## 回传后建议做的验证

1. 确认 `.agents/skills/maglev-reverse-spec/` 中所有 reference 都能在目标仓找到
2. 确认删除项不再被引用
3. 确认 `Module Partition` 已接入主流程，且 reality 按 `module_slug` 单独落盘
4. 确认“禁止业务修复”与“默认中文产物”已在目标仓 skill 中保留
5. 任选一个存量模块，跑一轮 `maglev-reverse-spec`
6. 用 `reverse_review_scorecard.md` 做一次结果审查
7. 再用 `reverse_stability_quickcheck.md` 做一次快速稳定性判断

## 最小回传集

如果你时间有限，只传这一组就够了：

1. 当前仓库中的 `.agents/skills/maglev-reverse-spec/`
2. `methodology/reverse_minimum_standard.md`
3. `review_tools/reverse_review_scorecard.md`
4. `review_tools/reverse_stability_checklist.md`
5. `skill_change_manifest.md`

## 当前结论

本次 handoff 已经收敛到：

- 可以回传
- 可以在 Maglev 主仓作为逆向主 skill 的候选基线
- 不再依赖当前 MPX 业务上下文
