# runtime name 主流程核心对象 rename readiness assessment v1

> 状态：已完成
> 作用：基于当前仓库运行面、文档面与治理面的现状，判断主流程核心四对象是否已经具备进入物理 rename 回合的条件。

## 1. 评估对象

本次只评估以下四个对象：

1. `maglev-standup`
2. `maglev-create-spec`
3. `maglev-quick-dev`
4. `maglev-cross-validate`

## 2. 当前证据面

### A. Catalog 与元数据面

当前 `.agents/private-catalog.yaml` 已稳定表达：

- 四对象都处于 `active_legacy_name`
- `formal_action_name` 已可作为正式结构语言使用

判断：

- 命名治理字段已具备
- 不构成当前阻塞

### B. Workflow 与运行入口面

当前 `.agents/workflows/` 中仍以历史运行名暴露入口：

- `standup.md`
- `create-spec.md`
- `quick-dev.md`
- `validate-all.md`

同时 workflow 描述仍直接要求启动：

- `maglev-standup`
- `maglev-create-spec`
- `maglev-quick-dev`
- `maglev-cross-validate`

判断：

- 运行入口仍明确绑定旧名
- 若直接物理 rename，会立即影响当前使用路径与教程口径

### C. 主流程技能协作面

当前 `entry-router`、`requirement-convergence`、`skill-squadron` 等协作对象仍以历史运行名作为路由与协作对象标识。

判断：

- 主流程协作面仍未完成对正式动作名的双写兼容
- 若直接 rename，内部协作口径会先出现断层

### D. Reality 与结构文档面

`specs/10_reality/01_requirements.md` 已经开始采用：

- `现状同步（历史入口：maglev-standup）`
- `方案设计（历史入口：maglev-create-spec）`
- `上下文实施（历史入口：maglev-quick-dev）`
- `综合验证（历史入口：maglev-cross-validate）`

判断：

- 结构文档面已经进入推荐双写状态
- 这部分已达到预期方向

### E. 对外说明与营销文档面

当前 `docs/marketing/assets/` 下大量文档仍以：

- `maglev-standup`（会话启动器）
- `maglev-create-spec`（需求转 Spec）
- `maglev-quick-dev`（快速开发闭环）
- `maglev-cross-validate`（交叉验证）

为主要表达方式。

判断：

- 对外文档仍以旧运行名为主
- 还没有普遍切到“正式动作名优先、旧名兼容”的统一写法

## 3. readiness 结论

当前四对象都：

1. 已具备正式动作名
2. 已具备治理字段
3. 已具备文档先行与双写兼容基础

但当前仍不具备进入物理 rename 回合的条件，原因是：

1. workflow 与 skill 入口仍强绑定旧名
2. 主流程协作对象仍以旧名做路由与 handoff
3. 对外说明面尚未完成正式动作名优先的双写统一
4. 物理 rename 的真实影响面还未被单独盘清

因此当前结论是：

> `runtime_name_strategy` 主题可以封板到“策略明确、readiness 已判定”的状态，但不应直接进入物理 rename。

## 4. 当前最合理的下一步

如果后续继续推进，下一轮应新开独立主题，而不是在本主题内直接改名。

建议下一轮主题目标：

1. 盘清 workflow / 入口 / 教程 / capability snapshot / reality / catalog 的 rename 影响面
2. 明确哪些地方先做双写统一
3. 决定物理 rename 是只改 skill，还是 skill 与 workflow 一起改
4. 形成一份单独的 migration checklist

## 5. 当前不建议的动作

当前不建议：

1. 直接修改四个 skill 目录名
2. 直接修改四个 workflow 文件名
3. 把历史运行名从用户文档与协作文档中一次性移除
4. 把 readiness 主题错误推进成 rename 执行主题
