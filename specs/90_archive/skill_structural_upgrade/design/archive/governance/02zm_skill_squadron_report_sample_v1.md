# skill结构性升级 skill-squadron 默认巡逻报告样例 v1

> 状态：样例
> 作用：给出当前 Maglev 项目在现有治理对象图下，一份可直接参考的 `skill-squadron` 报告写法。

## 1. 使用边界

这份样例用于固定当前项目的报告表达习惯，不用于替代 `step-05-report.md` 的通用模板。

适用前提：

- 使用当前 `.agents/private-catalog.yaml`
- 采用当前三组默认巡逻切片
- 输出目标是让维护者快速判断：
  - 哪一组在巡逻
  - 这组的主要风险是什么
  - 下一步该先看哪里

## 2. 当前项目推荐摘要结构

报告优先按以下层次展开：

1. 总体摘要
2. 分组摘要
3. 组内对象状态
4. 关键风险 / 关键机会
5. 下一步建议

不建议一开始就铺大量逐对象明细。

## 3. 当前样例

```md
📊 Squadron Report - Maglev 默认巡逻报告

**生成时间**：{generated_at}
**总体摘要**：
当前对象图分为 3 个稳定巡逻组：
- 主流程前中段组
- 体系级与后段闭环组
- 质量层组

本轮重点关注：
- 主流程前段是否重新混写
- 后段闭环与知识沉淀是否重新缠绕
- 体系级对象之间是否出现关系断裂
- 运行面仍保留旧名的核心对象是否继续制造理解成本
- 不同分发范围的对象是否被错误推成同一层入口

═══════════════════════════════════════

## Group 1: 主流程前中段组 [组级评分: {group_value_score}]

**对象**：
- `entry-router`
- `maglev-standup`
- `requirement-convergence`
- `maglev-create-spec`
- `maglev-quick-dev`
- `maglev-cross-validate`

**本组重点**：
- 入口是否正确路由
- `requirement-convergence` 是否仍保持三段式
- `方案设计 -> 上下文实施 -> 综合验证` 是否衔接顺滑
- 是否重新出现阶段语义吞并

### 巡逻结论

- `entry-router`：{status_summary}
- `maglev-standup`：{status_summary}（运行面命名状态：{runtime_name_status}）
- `maglev-standup`：{status_summary}（运行面命名状态：{runtime_name_status}，分发范围：{distribution_scope}）
- `requirement-convergence`：{status_summary}
- `maglev-create-spec`：{status_summary}（运行面命名状态：{runtime_name_status}，分发范围：{distribution_scope}）
- `maglev-quick-dev`：{status_summary}（运行面命名状态：{runtime_name_status}，分发范围：{distribution_scope}）
- `maglev-cross-validate`：{status_summary}（运行面命名状态：{runtime_name_status}，分发范围：{distribution_scope}）

### 本组关键风险

- {risk_1}
- {risk_2}

### 本组下一步建议

1. {next_action_1}
2. {next_action_2}

═══════════════════════════════════════

## Group 2: 体系级与后段闭环组 [组级评分: {group_value_score}]

**对象**：
- `crystallization`
- `knowledge-check`
- `maglev-bootstrapper`
- `maglev-updater`
- `maglev-legacy-adopter`
- `maglev-reverse-spec`
- `maglev-map-maker`
- `maglev-librarian`
- `skill-scout`
- `skill-squadron`

**本组重点**：
- `crystallization` 与 `knowledge-check` 是否仍保持分离
- `整体接入` 能力簇是否仍协作清楚
- `现状表达` 与 `能力进化` 是否能正确闭环
- `map-maker / librarian` 是否仍挂在闭环末端
- `runtime_internal` 与 `private_only` 对象是否被错误推成用户默认入口

### 巡逻结论

- `crystallization`：{status_summary}
- `knowledge-check`：{status_summary}
- `maglev-bootstrapper / maglev-updater / maglev-legacy-adopter / maglev-reverse-spec`：{status_summary}
- `maglev-map-maker / maglev-librarian`：{status_summary}
- `skill-scout / skill-squadron`：{status_summary}

### 本组关键风险

- {risk_1}
- {risk_2}

### 本组下一步建议

1. {next_action_1}
2. {next_action_2}

═══════════════════════════════════════

## Group 3: 质量层组 [组级评分: {group_value_score}]

**对象**：
- `spec-audit-surface`
- `review-validation-surface`
- `test-design-surface`

**本组重点**：
- 输入审计、结果审查、测试设计三面是否仍边界清晰
- 三面是否重新混写
- `maglev-cross-validate` 是否仍保持主流程汇聚验证，而没有重新吞并质量层

### 巡逻结论

- `spec-audit-surface`：{status_summary}
- `review-validation-surface`：{status_summary}
- `test-design-surface`：{status_summary}

### 本组关键风险

- {risk_1}
- {risk_2}

### 本组下一步建议

1. {next_action_1}
2. {next_action_2}

═══════════════════════════════════════

## 总结建议

本轮更建议优先处理：
1. {top_priority_1}
2. {top_priority_2}
3. {top_priority_3}
```

## 4. 当前项目表达偏好

当前项目的 `skill-squadron` 报告应优先做到：

- 先说组语义，再说对象状态
- 先说结构风险，再说单对象优化机会
- 先给下一步建议，再展开长明细

不建议：

- 把所有对象逐个平铺成同权重列表
- 不区分“主流程问题”和“体系级问题”
- 一上来就铺满 Patrol 原始细节

## 5. 与通用模板的关系

关系如下：

- `step-05-report.md`
  - 提供通用输出骨架
- 本文件
  - 提供当前 Maglev 项目的默认写法样例

当对象图分组明显变化时，应优先更新本文件，而不是直接改写通用模板。
