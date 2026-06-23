# Context

当前已经确认：

1. `AGENTS.md` 与 `llms.txt` 在 Maglev 化项目里不是普通说明文档，而是 AI 运行时上下文的一部分
2. 它们当前承接：
   - 语言约束
   - 文档写作约束
   - skill / workflow 导航
   - 大模型身份与交互规则
3. 现有发行构建、CLI 与 installer 主要受控下发：
   - `.agents/`
   - `.maglev/`
   - `specs/`
   - `docs/`
   - `issues/`
4. 现有发行构建、CLI 与 installer 并没有明确把这两个文件作为受控资产处理
5. 直接把 Maglev 仓库根下的 `AGENTS.md` / `llms.txt` 原样做成制品下发给用户项目并不合适
   - 因为其中混有 Maglev 仓库自身的私有上下文与阶段性现实

这意味着：

1. skill 结构已经大改，但项目根下 AI 指令文件可能继续停留在旧心智
2. 新初始化项目可能拿到过时的 AI 上下文层
3. 老项目升级后 `.agents/` 已更新，但 `AGENTS.md` / `llms.txt` 仍未同步
4. 但解决办法更适合是“检测与提示补齐”，而不是“直接复制上游文件”
