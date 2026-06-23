# `maglev-create-prd` Scout 需求解析 v1

> 状态：已确认
> 作用：为 `maglev-create-prd` 的保留、吸收与后续并入 `requirement-convergence` 补齐标准 `skill-scout` 的 `parse` 产物。

## SearchIntent

```yaml
search_intent:
  capability_type: 前段需求文档生成 / 需求收敛兼容模式
  target_scenario: 在前段需求如果只停留在松散总结就会持续漂移时，为需求收敛提供稳定、可被下游充分消费的需求文档输出模式，并判断该能力是否应继续作为独立对象存在
  constraints:
    - 不能直接删除，因为前段仍需要一个稳定需求产物输出节点
    - 不能继续作为与 requirement-convergence 并列的前段一级对象
    - 应优先判断是否可被 requirement-convergence 吸收为兼容输出模式
    - 不应并入 maglev-create-spec，避免把需求收敛与方案设计重新混在一起
    - 吸收目标必须围绕“抑制产物漂移、提升下游可消费性”，而不是仅仅兼容传统流程
    - 本轮需要补齐实际联网检索证据后，才能继续进入 evaluate / adapt
  raw_description: 重新判断 maglev-create-prd 的对象定位、保留必要性，以及它后续并入 requirement-convergence 并解决前段产物漂移问题的合理方式。
  confirmed: true
```

## 当前问题

1. `maglev-create-prd` 当前有真实问题承接价值，但不在 `5+3` 主干骨架中。
2. 如果继续与 `requirement-convergence`、`maglev-create-spec` 并列存在，会继续制造前段多入口并存。
3. 本轮需要通过正式 Scout 证据链回答：
   - 它是否仍应保留
   - 它保留的理由是“目标节点仍需要稳定需求产物”还是仅仅“协作兼容”
   - 它后续更适合并入哪个对象
