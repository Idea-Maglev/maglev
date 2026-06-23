# Requirements

## 1. 决策要求

本主题至少要给出一个明确结论：

1. `Reject`
2. `Optional / Recommended`
3. `Default`

不能停留在“可以考虑支持 submodule”这种模糊口径。

## 2. 影响面要求

如果决定保留或引入 submodule 模型，必须至少说明以下 5 个影响面：

1. `init`
2. `update`
3. `.maglev/config.json`
4. `specs/10_reality/repository_map.md`
5. 用户协作 / 文档说明

## 3. 工程现实要求

新的判断必须正面回答 submodule 的现实摩擦，而不是只讲好处：

1. detached HEAD
2. recursive clone / update
3. pointer 变更如何提交
4. 团队成员如何获得一致环境

## 4. 与旧决策的关系要求

如果当前结论与 `docs/thinking/20_architecture/adoption_model_evolution.md` 相冲突，必须明确写出：

1. 哪些前提已经变化
2. 为什么旧反对理由现在不再构成阻断
3. 哪些风险仍然成立
