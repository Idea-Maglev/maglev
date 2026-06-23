# Design

## 1. 当前问题

当前存在一个故意保留的不一致：

1. skill runtime name 已切到新名
2. workflow 文件名仍保留旧入口名

这并不一定是错误，但需要明确判断它是否仍有价值。

## 2. 判断维度

本主题至少要回答：

1. 旧 workflow 文件名是否仍有真实使用价值
2. 它们是否承担“低门槛入口”或“历史兼容入口”的角色
3. 如果做 workflow rename，会影响哪些文档、路由、教学和用户习惯
4. workflow 层是否也应该采用“双写兼容 -> 物理切换”的策略

## 3. 预期输出

1. 一份 workflow rename / retain 决策
2. 一份影响面 inventory
3. 若需要，再进入单独 execution 主题
