# AI 上下文数据区（context/ 目录约定扩展）

## 问题陈述

在 v2.15 Cover Page 特性的归档审查中发现：执行者在 `active/feat_xxx/` 下自建了深层嵌套的个人工作区（`workflow-zx/context/`），用于存放字段规则 CSV、可见性映射、代码结构分析等半结构化数据。

这些数据是**AI 协作中合理且必要的上下文投喂**，但 Maglev 当前框架中缺少标准化的存放位置。现有 `context/` 目录仅被定义为存放 `input_facts.md`（方案设计的输入事实基准），不覆盖更广泛的 AI 上下文需求。

结果是执行者自创目录结构，产生个人命名空间 + 深层嵌套 + 偏离标准的反模式。

## 触发来源

- `docs/component-level-spec-decomposition-antipattern.md`（modelconfig 项目归档审查）
- 建议 2：明确「AI 上下文数据区」

## 期望结果

- Maglev spec 生命周期中有标准化的 context/ 目录约定
- 执行者知道 AI 协作时的半结构化数据应该放在哪里
- context/ 与 ref/ 的边界清晰
- context/ 随 spec 归档时自动搬迁

## 状态

- [x] 需求收敛
- [ ] 方案设计
- [ ] 编码实施
- [ ] 综合验证
- [ ] 结晶归档
