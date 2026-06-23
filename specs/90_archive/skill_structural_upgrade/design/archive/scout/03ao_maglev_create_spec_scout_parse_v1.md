# `maglev-create-spec` Scout 需求解析 v1

> 状态：已确认
> 作用：为 `maglev-create-spec` 的重判与可能重命名补齐标准 `skill-scout` 的 `parse` 产物。

## SearchIntent

```yaml
search_intent:
  capability_type: 主流程 / 方案设计能力
  target_scenario: 在需求边界稳定后，通过结构化流程形成可执行、可验证的技术方案
  constraints:
    - 不能继续吞并需求收敛
    - 必须保留追问、摄入、起草、落盘的端到端方案设计链
    - 必须与上下文实施、综合验证保持边界
    - 当前优先回答是否需要正式改名，而不是立即替换运行面
  raw_description: 重新判断 maglev-create-spec 的对象定位、命名准备度与后续改名路径。
  confirmed: true
```

## 当前问题

1. `create-spec` 这个名字容易把需求澄清、文档生成和方案设计混成一个入口。
2. 当前结构动作名已经收敛到 `方案设计`，但物理 skill 名还没有正式重判。
3. 本轮需要通过正式 Scout 证据链判断：
   - 是否现在就该改名
   - 还是先保留旧名，仅固定结构动作名
