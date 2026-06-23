# skill结构性升级 未来显性 Skill 清单 v1

> 状态：进行中
> 作用：基于当前统一判据，给出未来 Maglev 应显性保留、补位、降显性和协作承接的第一版清单。

## 1. 使用方式

这份清单回答的不是“当前仓库里有什么”，而是：

1. 未来哪些对象值得继续作为显性 skill 被用户或系统直接感知
2. 哪些对象更适合继续存在，但不再作为并列显性 skill 理解
3. 哪些能力当前应先以 workflow 或能力面形式存在

补充原则：

- 未来显性 skill 名称，不需要继续拟合历史 skill 名
- 未来显性 skill 名称，也不需要强行与正式动作名完全一致
- 后续应优先选择最能提示对象职责、分发边界和使用场景的 skill 名称

## 2. 清单分层

当前显性与非显性对象，先分成四层：

1. 用户显性主流程 skill
2. 体系显性能力簇
3. 非显性但稳定存在的内部承接对象
4. 当前缺口或待补位对象

## 3. 用户显性主流程 Skill

这层是未来最值得被用户直接感知的主心智。

| 未来主流程能力 | 当前承接对象 | 当前判断 | 后续建议 |
| :--- | :--- | :--- | :--- |
| `现状同步` | `maglev-standup` | 保留 | 保留对象，对外优先按“现状同步 / 会话启动同步”解释 |
| `需求收敛` | `requirement-convergence` | 保留 | 已补位，继续观察前段三段式是否稳定 |
| `方案设计` | `maglev-create-spec` | 保留 | 保留对象，对外优先按“方案设计”解释 |
| `上下文实施` | `maglev-quick-dev` | 保留 | 保留对象，但后续需继续压低“quick”语义 |
| `综合验证` | `maglev-cross-validate` | 保留 | 保留对象，继续作为主流程汇聚点 |

### 当前结论

未来用户显性主流程层，当前更接近：

1. `maglev-standup`
2. `requirement-convergence`
3. `maglev-create-spec`
4. `maglev-quick-dev`
5. `maglev-cross-validate`

补充说明：

- `需求收敛` 当前已形成真实 skill：
  - `.agents/skills/requirement-convergence/`
- `.agents/workflows/requirement-convergence.md` 继续作为调用入口包装

## 4. 体系显性能力簇

这层需要显性存在，但不适合误收成单点总 skill。

| 体系级能力 | 当前承接对象 | 当前判断 | 后续建议 |
| :--- | :--- | :--- | :--- |
| `整体接入` | `maglev-bootstrapper` / `maglev-legacy-adopter` / `maglev-reverse-spec` | 协作承接 | 保持能力层显性、对象层协作承接 |
| `能力进化` | `skill-scout` / `skill-squadron` | 协作承接 | 保持能力簇，不急于总 skill 化 |
| `现状表达` | `10_reality` / `maglev-map-maker` / `maglev-librarian` | 协作承接 | 保持底层长期能力，不提升为用户主流程入口 |

### 当前结论

这层未来应继续作为“体系显性能力簇”被表达，而不是变成 3 个并列大而全 skill。

## 5. 非显性但稳定存在的内部承接对象

这类能力应继续存在，但不应再作为未来用户心智中的并列一级 skill。

### A. Internal Modules

spec pipeline 四件套已完成物理内部化，当前由以下目录继续承接：

- `maglev-create-spec/references/pipeline/ingest/`
- `maglev-create-spec/references/pipeline/validate-context/`
- `.agents/skills/_internal/spec-pipeline/draft/`
- `.agents/skills/_internal/spec-pipeline/crystallize/`

### B. Quality Surfaces

- `spec-audit-surface`
- `review-validation-surface`
- `test-design-surface`

当前方向：

- 作为现役三面保留

已退出运行面的历史碎片对象：

- `maglev-audit-prd`
- `maglev-audit-spec`
- `maglev-code-review-backend`
- `maglev-code-review-frontend`
- `maglev-plan-unit-tests-backend`
- `maglev-plan-unit-tests-frontend`
- `maglev-create-test-cases`

### C. Specialized Support

- `maglev-content-sync`
- `maglev-design-ux`
- `maglev-tutor`
- `maglev-changelog-generator`
- `mermaid-expert`

当前方向：

- 继续保留为专项支持对象
- 不提升为主流程显性 skill

## 6. 当前需继续观察与收束的对象

这层是后续升级最值得优先关注的对象。

### A. `需求收敛`

当前方向：

- `Keep`

最小结构：

1. `入口分流`
2. `需求定义`
3. `Ready Gate`

当前落地：

- `.agents/skills/requirement-convergence/`
- `.agents/workflows/requirement-convergence.md`

### B. `现实结晶`

当前方向：

- `Keep`

最小结构：

1. 结晶条件确认
2. 现实回写判定
3. active 状态收口
4. 索引与可发现性回填

当前落地：

- `.agents/skills/crystallization/`
- `.agents/workflows/crystallization.md`

### C. `思考沉淀`

当前方向：

- 不提升为用户显性主流程 skill
- 继续作为知识资产链存在

## 7. 已移除旧对象与正式替代

| 对象 | 当前方向 | 说明 |
| :--- | :--- | :--- |
| `atomizer` | `Removed` | 入口路由语义已由 `entry-router` 接管 |
| `maglev_archival_check` | `Removed` | 知识沉淀检查语义已由 `knowledge-check` 接管 |

其中 `atomizer` 当前已出现正式替代对象：

- `.agents/skills/entry-router/`

当前处理原则是：

- `entry-router` 作为正式入口对象继续推进
- `atomizer` 不再保留在运行面

其中 `maglev_archival_check` 当前已出现正式替代对象：

- `.agents/skills/knowledge-check/`

当前处理原则是：

- `knowledge-check` 作为正式知识沉淀检查对象继续推进
- `maglev_archival_check` 不再保留在运行面

## 8. 当前最重要的清单结论

如果只看未来显性 skill 体系，当前最关键的 5 个判断是：

1. 未来用户主流程层应保持精简，不应再次膨胀成大量并列 skill
2. `需求收敛` 已完成第一轮 skill 化补位，但仍需继续观察其前段三段式稳定性
3. 体系级能力更适合能力簇，不适合单点总 skill
4. 质量层应以能力面存在，不应以碎片 skill 平铺
5. 已判定误导性强的旧对象应直接移除，不再占用运行面语义入口

## 9. 当前结论

这份清单 v1 的作用，不是立刻推动所有对象重写，而是先给出未来显性 skill 体系的大致边界：

- 什么应该继续显性存在
- 什么应该协作承接
- 什么应该降显性
- 什么当前仍是缺口
