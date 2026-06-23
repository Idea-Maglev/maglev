# skill结构性升级 系统承接结构

> 状态：进行中
> 作用：承载系统承接视图，说明一级能力由哪些层次对象承接。
> 完整展开讨论：
> - `archive/02_design_full_archive.md`

## 1. 系统承接视图

当前系统承接视图继续沿用七层结构：

1. `Entry / Routing Layer`
2. `Core Flow Layer`
3. `Infrastructure Layer`
4. `Quality / Guardrail Layer`
5. `Reality / Context Layer`
6. `Evolution & Governance Layer`
7. `Specialized Support Layer`

## 2. 当前判断

这张图解决的是：

- skill、workflow、基础设施、Reality 层分别位于什么位置
- 顶层能力由什么对象和层次承接

它不直接决定：

- 顶层一级能力应该有哪些

## 3. 结晶与沉淀链路

当前需要明确区分两条链：

1. `思考归档触发链`
   - 面向知识沉淀
   - 可在需求进行中多次触发

2. `事实结晶触发链`
   - 面向 Reality 回写和生命周期收口
   - 更接近需求后段状态转换

## 4. 当前关键判断

### 4.1 现实结晶

`事实结晶` 当前更适合作为生命周期后段 workflow，而不是独立一级 skill。

当前最小步骤为：

1. 结晶条件确认
2. 现实回写判定
3. active 状态收口
4. 索引与可发现性回填

### 4.2 思考沉淀

`maglev_archival_check` 当前更偏：

- 思考归档
- 知识沉淀检查

而不是：

- 需求归档
- Reality 结晶

## 5. 当前结论

后续设计 skill 体系时，应把“能力骨架”和“系统承接”分开维护，避免再次混写。

同时需要持续保持：

- `思考沉淀` 作为知识资产链
- `现实结晶` 作为事实状态链

二者虽然相邻，但不应再共用“归档”这个默认语义入口。

质量层也应保持独立结构位，不应重新退化成：

- 主流程末端一次性检查
- 或碎片化并列 skill 列表
