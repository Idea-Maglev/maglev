# runtime name 策略专项收口 Design

## 1. 设计目标

这轮不是做 rename 执行，而是把 rename 从“对象级临时判断”变成“分组级固定策略”。

## 2. 当前分组

### A. 主流程核心对象

- `maglev-standup` -> `现状同步`
- `maglev-create-spec` -> `方案设计`
- `maglev-quick-dev` -> `上下文实施`
- `maglev-cross-validate` -> `综合验证`

判断：

- 这组结构动作名最稳定
- 但运行面替换风险也最高
- 应优先做“文档先行 + 双写兼容”，不直接物理改名

### B. 体系级承接对象

- `maglev-bootstrapper`
- `maglev-legacy-adopter`
- `maglev-map-maker`
- `maglev-librarian`
- `maglev-reverse-spec`
- `maglev-updater`

判断：

- 这组对象偏功能性工具
- 结构动作名虽清楚，但用户和维护者对旧名已有使用惯性
- 适合中后期进入 rename 回合

### C. 专项支持对象

- `maglev-content-sync`
- `maglev-design-ux`
- `maglev-tutor`

判断：

- 这组不是主流程阻塞项
- 可继续保留旧运行名，只在 metadata 与文档层维持正式动作名

### D. 治理底座对象

- `skill-scout`
- `skill-squadron`

判断：

- 这组名称已经兼具品牌和职责识别
- 不宜为追求“动作名一致”而强推物理 rename

## 3. 推荐策略

### Strategy 1: 文档先行，运行名暂不改

适用于：

- 主流程核心对象

动作：

1. 文档持续优先写正式动作名
2. 保留旧 skill 名作为兼容运行名
3. 未来若改，走单独迁移回合

### Strategy 2: 长期兼容保留

适用于：

- 专项支持对象
- 治理底座对象
- 多数体系级对象

动作：

1. `formal_action_name` 继续稳定
2. `runtime_name_status` 保持 `active_legacy_name`
3. 不急于进入 rename

### Strategy 3: 预备进入 rename 回合

适用于：

- 仅主流程核心四对象

前提：

1. 对外文档已完成双写兼容
2. workflow / CLI / 用户教程中的旧写法已可控
3. 迁移成本已能接受

## 4. 当前结论

当前最稳的策略不是“把所有旧名都改掉”，而是：

- 主流程核心四对象进入 rename 预备组
- 其余 `active_legacy_name` 对象保持长期兼容
- `runtime_name_status` 继续作为正式治理字段保留
