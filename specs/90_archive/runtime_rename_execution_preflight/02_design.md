# runtime rename execution preflight Design

## 1. 设计目标

把真正会决定 rename execution 是否可控的最后两个问题，从“临场判断”变成“先验规格”。

## 2. 关键问题 A：迁移形态

候选只有两种：

1. `skill-only`
2. `skill + workflow`

本主题需要明确：

- 哪种更适合当前 Maglev
- 为什么另一种当前不优先

## 3. 关键问题 B：catalog relation-level checklist

catalog 不是孤立清单，而是关系图输入。

因此 checklist 必须做到：

1. 列出所有必须同步改写的 relation target
2. 区分先改对象定义，还是先改关系引用
3. 明确迁移后应如何验证一致性

## 4. 当前结论方向

本主题预期不会导出“立刻执行 rename”，而会导出：

1. 一份迁移形态决策
2. 一份 relation-level checklist
3. 一个可以交给后续 execution 主题直接消费的前置规格
