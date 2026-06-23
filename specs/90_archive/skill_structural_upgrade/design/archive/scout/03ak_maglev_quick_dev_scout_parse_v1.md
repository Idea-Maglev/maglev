# `maglev-quick-dev` Scout 需求解析 v1

> 状态：已确认
> 作用：为 `maglev-quick-dev` 的重判与可能重命名补齐标准 `skill-scout` 的 `parse` 产物。

## SearchIntent

```yaml
search_intent:
  capability_type: 主流程 / 实施能力
  target_scenario: 在方案依据清楚后完成受控编码、自检与对抗性审查
  constraints:
    - 不能继续让 “quick” 成为默认价值承诺
    - 必须保留实施、自检、对抗性审查三段闭环
    - 必须与需求收敛、方案设计、综合验证保持边界
    - 当前优先回答是否需要正式改名，而不是立即替换运行面
  raw_description: 重新判断 maglev-quick-dev 的对象定位、命名准备度与后续改名路径。
  confirmed: true
```

## 当前问题

1. `quick-dev` 这个名字同时混入了速度承诺和实施语义。
2. 当前结构动作名已经收敛到 `上下文实施`，但物理 skill 名还没有正式重判。
3. 本轮需要通过正式 Scout 证据链判断：
   - 是否现在就该改名
   - 还是先保留旧名，仅固定结构动作名
