# skill结构性升级 skill-squadron 关系图预演 v1

> 状态：进行中
> 作用：基于当前 `.agents/private-catalog.yaml`，预演一次 `skill-squadron` 的对象图构建结果，验证当前治理对象分组是否合理。

## 1. 预演范围

本次预演只读取已登记到项目级治理对象清单中的 `active` 对象，不把文件系统中的所有 skill / workflow 机械纳入关系图。

当前预演对象数：

- `19` 个 active 能力对象

当前运行面命名状态：

- `active_legacy_name`：`12` 个
- `canonical_name_active`：`7` 个

## 2. 当前分组结果

### Group 1：体系级与后段闭环组

包含：

- `crystallization`
- `knowledge-check`
- `maglev-bootstrapper`
- `maglev-legacy-adopter`
- `maglev-librarian`
- `maglev-map-maker`
- `maglev-reverse-spec`
- `maglev-updater`
- `skill-scout`
- `skill-squadron`

当前判断：

- 这组基本符合“体系级能力簇 + 后段闭环”视角
- 内部主要由三类对象构成：
  - `整体接入`
  - `能力进化`
  - `现状表达 / 现实结晶 / 知识沉淀`

### Group 2：主流程前中段组

包含：

- `entry-router`
- `maglev-create-spec`
- `maglev-cross-validate`
- `maglev-quick-dev`
- `maglev-standup`
- `requirement-convergence`

当前判断：

- 这组基本符合“主流程前中段”视角
- 内部已形成较稳定的链路：
  - `entry-router -> requirement-convergence -> 方案设计 / 上下文实施 / 综合验证`
- 这组也是当前旧运行名最集中的一组，需要在巡逻时额外关注命名状态是否持续制造理解成本

### Group 3：质量层组

包含：

- `spec-audit-surface`
- `review-validation-surface`
- `test-design-surface`

当前判断：

- 这组三面已经能在关系图中自然连通
- 内部对应当前质量层的三面结构：
  - 输入层审计
  - 结果层审查
  - 测试设计
- `maglev-cross-validate` 继续保留在主流程组，作为跨组汇聚点而不是质量层本体

## 3. 预演结论

本次预演得到两个直接结论：

1. 当前 catalog 已足以支撑 `skill-squadron` 构建一张有意义的对象图
2. 当前对象图自然分裂成三大组：
   - 主流程前中段
   - 体系级与后段闭环
   - 质量层
3. `runtime_name_status` 已经成为有效的巡逻输入：
   - 主流程组需要重点关注旧运行名是否继续制造理解成本
   - 质量层和后段闭环组当前以正式对象名运行为主

这与当前 `5+3` 顶层能力骨架和双视图结构模型基本一致。

## 4. 本次发现并已修正的问题

### 4.1 非对象数据文件被误建成关系目标

预演中发现：

- `skill-scout`
- `skill-squadron`

都曾将 `.agents/private-catalog.yaml` 作为 `relations.target` 写入。

这会导致：

- 在 `skill-squadron` 图模型中形成悬空引用
- 把“数据资产”误当成“能力对象”

当前已修正：

- 将这两条关系从 `.agents/private-catalog.yaml` 中移除

处理原则：

- `private-catalog` 是项目级治理资产
- 它可以被对象消费，但不应进入对象关系图节点

## 5. 当前建议

下一步不需要立即扩更多对象，而更适合继续做三件事：

1. 继续补稳主流程组与后段闭环组内部的关系表达
2. 把质量层三面作为现役治理对象纳入默认编队
3. 在真正执行 `skill-squadron` 巡逻前，优先复用当前三组作为默认巡逻切片
4. 在巡逻执行层显式区分三组的默认检查重点，而不是只按对象类型做统一扫描
5. 在巡逻报告中显式展示 `runtime_name_status`，避免结构动作名与运行面名字再次混淆

## 6. 当前结论

当前 `skill-squadron` 的关系图输入面已经从“设计推测”进入“可预演验证”阶段。

后续如果继续推进，应优先基于这三个对象组做真实巡逻，而不是再回到全量对象散点分析。
