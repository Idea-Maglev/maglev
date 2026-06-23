# Requirements

## 1. 决策要求

本主题至少要给出一个明确结论：

1. `Reject`
2. `Explicit Only`
3. `Default in Update`

当前默认假设应偏向 `Explicit Only`，除非有足够强的反证。

## 2. 安全要求

如果允许执行 pointer sync，必须至少说明：

1. 哪些情况阻断执行
2. 执行前是否需要确认
3. 执行后是否必须提示提交 wrapper 变化

## 3. 语义要求

必须明确回答：

1. 同步到当前 pointer 期望 revision
2. 同步到远端最新分支

这两种语义不能混写成一个“同步”。

## 4. 运行面要求

如果后续进入实现，必须明确落在哪一层：

1. `maglev-updater`
2. installer
3. 独立 workflow / CLI flag

不能停留在抽象说明。
