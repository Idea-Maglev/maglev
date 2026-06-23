# `maglev-create-spec` Scout 评估选择 v1

> 状态：已确认
> 作用：确认 `maglev-create-spec` 的对象形态、命名准备度与是否进入正式改名。

## 输入

- [03ao_maglev_create_spec_scout_parse_v1.md](03ao_maglev_create_spec_scout_parse_v1.md)
- [03ap_maglev_create_spec_scout_search_v1.md](03ap_maglev_create_spec_scout_search_v1.md)
- [02q_formal_action_names_v1.md](02q_formal_action_names_v1.md)
- [02p_naming_readiness_matrix_v1.md](02p_naming_readiness_matrix_v1.md)

## 评估结论

### 1. 对象形态

当前仍保持为现役 `skill` 对象。

原因：

1. 它已经稳定承接主流程中的方案设计断点
2. 它不是临时 workflow，也不是内部模块
3. 其主要问题是命名和边界表达，不是对象形态错误

### 2. 结构动作名

```yaml
formal_action_name:
  value: 方案设计
  confirmed: true
  reason: 该名称能直接表达“在需求边界稳定后形成可执行方案依据”，且不会继续把需求澄清与文档生成吞进同一入口。
```

### 3. 物理 skill 名是否立即改名

```yaml
rename_decision:
  current_name: maglev-create-spec
  immediate_rename: false
  reason: 结构动作名已稳定，但新的 canonical skill name 还没有达到必须立刻替换运行面的程度。
```

### 4. 当前判断

- `create-spec` 不是理想名字
- 但当前更合理的处理是：
  - 固定结构动作名为 `方案设计`
  - 暂不立即物理改名
  - 后续如需正式改名，再进入单独的 rename/register 路径

### 5. 命名准备度

```yaml
naming_readiness:
  formal_action_name: stable
  canonical_skill_name: pending
  legacy_name_status: active_but_discouraged
```

## 当前结论

- `maglev-create-spec` 这轮 Scout 的主要结论不是“立即改名”
- 而是“正式确认其结构动作名为 `方案设计`，并把物理改名延后”
- 因此我前面做的文案收口可以保留，但不能被解释为“已经完成正式重命名”
