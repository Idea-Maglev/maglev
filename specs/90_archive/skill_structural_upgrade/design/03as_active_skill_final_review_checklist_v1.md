# skill结构性升级 现役 Skill 最终复核清单 v1

> 状态：进行中
> 作用：给出当前现役 skill 的最终复核视图，区分哪些已可接受、哪些仍需收口、哪些可暂缓处理。

## 1. 使用方式

这份清单回答的不是“仓库里有哪些 skill”，而是：

1. 哪些现役对象已经达到当前可接受状态
2. 哪些对象仍需要继续收口
3. 哪些对象当前可以暂缓，不作为本轮收口前置条件

判断口径优先基于：

- 当前运行面对象
- `.agents/private-catalog.yaml`
- `5+3` 顶层能力骨架
- 已完成的 `skill-scout` 与治理收口结果

## 2. 已可接受

这些对象当前已达到“可继续运行、可进入后续维护”的状态，不再作为本轮主线阻塞项。

### A. 新骨架对象

- `entry-router`
- `knowledge-check`
- `requirement-convergence`
- `crystallization`
- `spec-audit-surface`
- `review-validation-surface`
- `test-design-surface`

### B. 治理底座对象

- `skill-scout`
- `skill-squadron`

### C. 体系级现役对象

- `maglev-bootstrapper`
- `maglev-legacy-adopter`
- `maglev-reverse-spec`
- `maglev-map-maker`
- `maglev-librarian`

### D. 本轮已完成收口的补充对象

- `maglev-standup`
- `maglev-create-spec`
- `maglev-quick-dev`
- `maglev-cross-validate`
- `maglev-updater`
- `maglev-content-sync`
- `maglev-design-ux`
- `maglev-tutor`

本轮完成依据：

1. `SKILL.md` 最小 metadata 已补齐
2. formal action name、runtime name status 与分发范围已和运行面说明对齐
3. 对象边界已在技能正文内显式写清，不再只靠历史讨论维持
4. 需要进入治理视图的对象已与 `.agents/private-catalog.yaml` 对齐

## 3. 还需收口

这些对象当前能用，但还不能视为“本轮彻底定稿”。

当前对象级复核后，原先列入“还需收口”的对象已不再构成本轮阻塞项。

剩余未收口内容已收缩为文档级事项：

1. 是否需要单独产出主流程核心对象的最终 rename 策略说明
2. 本主题退出条件与封板标准是否要再单列一份 closeout 文档
3. 后续是否让更多专项支持对象进入治理清单，应按新回合再判断

## 4. 可暂缓处理

这些对象当前不应成为本轮 `skill结构性升级` 的收口阻塞项。

### A. Creator / 私有维护对象

- `maglev-changelog-generator`

### B. 仍未进入治理主线的专项对象

- `mermaid-expert`

当前补充决议：

1. `mermaid-expert`
   - 当前给予保留豁免，命名收口已完成

## 5. 已退出运行面的对象

以下对象当前不再作为现役对象参与复核：

- `contribute_methodology`
- `maglev-create-prd`
- `maglev-spec-ingest`
- `maglev-spec-draft`
- `maglev-spec-crystallize`
- `maglev-validate-spec-context`
- `atomizer`
- `maglev_archival_check`
- `maglev-skill-forge`
- 旧质量碎片对象：
  - `maglev-audit-prd`
  - `maglev-audit-spec`
  - `maglev-code-review-backend`
  - `maglev-code-review-frontend`
  - `maglev-plan-unit-tests-backend`
  - `maglev-plan-unit-tests-frontend`
  - `maglev-create-test-cases`

## 6. 当前结论

当前更准确的进度判断是：

- **已可接受**：新骨架对象、治理底座、体系级现役对象
- **还需收口**：主流程核心对象、少数私有与专项支持对象
- **可暂缓处理**：Creator 对象、专项支持对象、内部原子模块

因此，本轮对象级“最终复核”已经基本完成，后续真正需要继续推进的是：

- 命名策略文档化
- 退出条件与封板标准收口
- 新回合对象是否进入治理清单的门槛治理
