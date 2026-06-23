# Intent

## 1. 当前目标

定义 Maglev 是否应支持 submodule pointer 的显式同步，以及如果支持，应以什么方式安全执行。

## 2. 这个主题只回答什么

1. 是否引入显式 pointer sync
2. 是独立命令、独立 flag，还是独立 workflow
3. 哪些情况必须阻断
4. pointer 变化后，如何提示用户处理 wrapper 项目提交

## 3. 这个主题不回答什么

1. submodule 是否可选
2. `init` 是否支持 submodule
3. `update` 是否继续保留观察层

这些问题已由上游主题固定。
