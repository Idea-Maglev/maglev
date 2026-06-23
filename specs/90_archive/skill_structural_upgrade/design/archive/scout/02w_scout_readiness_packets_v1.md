# skill结构性升级 Scout 准备包 v1

> 状态：进行中
> 作用：为后续必须通过 `skill-scout` 机制落地的对象，提前整理标准化输入包，避免正式切换流程时重新收集上下文。

## 1. 使用方式

这份文档不直接撰写 skill，也不替代 `skill-scout`。

它只做一件事：

- 为后续要进入 `skill-scout` 的对象，准备好一组最小稳定输入

这样在真正切换到 `skill-scout` 时，可以直接把这些内容作为：

- 搜索意图
- 边界约束
- 当前判断基线

输入给正式流程。

## 2. 当前需要准备的对象

当前最明确需要进入 `skill-scout` 机制的对象有 4 个：

1. `需求收敛`
2. `现实结晶`
3. `atomizer` 的正式替代对象
4. `maglev_archival_check` 的正式改写对象

## 3. 输入包模板

后续每个对象进入 `skill-scout` 时，至少应准备：

1. `target_object`
2. `current_problem`
3. `formal_action_name`
4. `top_level_capability`
5. `object_kind_guess`
6. `lifecycle_chain`
7. `must_keep`
8. `must_not_repeat`
9. `search_focus`

## 4. 对象输入包

### A. `需求收敛`

```yaml
target_object: 需求收敛
current_problem: 当前是未来用户显性一级能力中的唯一明显缺口，但还不宜草率 skill 化
formal_action_name: 需求收敛
top_level_capability: 需求收敛
object_kind_guess: workflow-first
lifecycle_chain: main_flow
must_keep:
  - 入口分流
  - 需求定义
  - Ready Gate
  - 与方案设计的清晰接口
must_not_repeat:
  - 被 create-spec 吞并
  - 做成大而全前段总 skill
  - 只做入口聊天，没有 ready 判断
search_focus:
  - requirement convergence
  - intake triage
  - definition of ready
  - requirements clarification workflow
```

### B. `现实结晶`

```yaml
target_object: 现实结晶
current_problem: 当前是后段闭环关键动作，但更适合 workflow-first，不宜急着 skill 化
formal_action_name: 现实结晶
top_level_capability: 综合验证后段相关
object_kind_guess: workflow-first
lifecycle_chain: crystallization
must_keep:
  - 结晶条件确认
  - 现实回写判定
  - active 状态收口
  - 索引与可发现性回填
must_not_repeat:
  - 与思考沉淀混成一个归档大词
  - 被 maglev_archival_check 吞并
  - 直接做成单点大 skill
search_focus:
  - crystallization workflow
  - state closeout
  - reality writeback
  - change finalization
```

### C. `atomizer` 的正式替代对象

```yaml
target_object: atomizer replacement
current_problem: 现有对象名称和职责都在持续误导智能体，应被替换为更清晰的入口路由对象
formal_action_name: 入口路由
top_level_capability: 需求收敛前置相关
object_kind_guess: skill
lifecycle_chain: main_flow
must_keep:
  - 会话入口
  - 请求识别
  - 路由 / handoff
must_not_repeat:
  - 全能助手语义
  - 强人格化叙事
  - 吞并主流程能力本体
search_focus:
  - entry router
  - request router
  - handoff agent
  - task router
```

### D. `maglev_archival_check` 的正式改写对象

```yaml
target_object: maglev_archival_check replacement
current_problem: 当前对象保留价值存在，但名称错误占据了需求归档语义入口
formal_action_name: 知识沉淀检查
top_level_capability: 思考沉淀
object_kind_guess: skill
lifecycle_chain: thinking_archive
must_keep:
  - thinking 检查
  - solution 检查
  - references / archive 检查
  - contribution log 检查
must_not_repeat:
  - 被理解成需求归档
  - 被理解成 reality 回写
  - 被理解成 active 收口
search_focus:
  - knowledge capture
  - session closeout
  - reflection archive
  - post-task knowledge check
```

## 5. 当前结论

这份准备包的意义是：

- 当前还不进入 `skill-scout` 执行
- 但已经把最关键的 scout 输入压稳定了

后续一旦切到 `skill-scout`，不需要再重新从大量 active spec 中抽取上下文，可以直接从这里起步。
