# Plan

## 1. 当前步骤

1. 固化必要性与资产分层判断
2. 明确 bootstrapper / updater 两层接入点
3. 明确 init / update / dry-run 的检查行为
4. 将最小检查契约接入现役 skill / workflow
5. 将最小检查逻辑接入 installer 执行面
6. 再决定是否进入更深的自动修复 implementation

## 2. 本轮预期输出

- 一份 AI context check 规格
- 一份接入层判断
- 一版现役技能接入说明
- 一版 installer 最小实现
- 一组最小草稿参考模板

## 3. 当前不做

- 不直接改 installer 资产下发逻辑
- 不直接改 release 打包逻辑
- 不直接改用户项目里的 `AGENTS.md` / `llms.txt`
