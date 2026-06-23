# Plan

## 1. 当前步骤

1. 固化上游主题的已知前提
2. 明确 pointer sync 的决策问题
3. 区分 `sync-to-recorded` 与 `sync-to-latest`
4. 输出正式决策文档
5. 输出 `sync-to-recorded` execution spec
6. 再决定是否进入真实实现

## 2. 本轮预期输出

- 一份新主题骨架
- 一份当前设计入口
- 一组明确的比较维度
- 一份首版决策文档
- 一份首轮 execution spec

## 3. 当前不做

- 不直接在 installer 里加入 pointer sync 命令
- 不直接新增 `update --sync-submodules`
- 不直接修改 `maglev-updater` 的现役实现
