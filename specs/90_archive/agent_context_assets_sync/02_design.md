# Design

## 1. 设计判断

`AGENTS.md` 与 `llms.txt` 应被视为：

- AI runtime context assets

而不是普通 README 类文档，也不应被当成可直接原样下发的通用发行文件。

它们和 `.agents/`、`.maglev/` 的关系更接近“运行时认知层”，因此更适合进入 init / update 的正式检查面。

## 2. 检查能力落点

最适合承接这项能力的不是新的一级显性 skill，而是：

1. `maglev-bootstrapper`
   - 负责 `init` 后的 AI context readiness check
2. `maglev-updater`
   - 负责 `update` 前后的 AI context drift check

不建议由 `knowledge-check` 承接，原因是：

1. 它偏向知识沉淀收尾
2. 不是初始化 / 升级时的运行时健康检查
3. 容易把“知识是否落盘”和“AI 是否能正确理解项目”混在一起

需要特别区分两层职责：

1. `maglev-bootstrapper` / `maglev-updater`
   - 负责把检查纳入 init / update 的能力定义、用户解释和结果语义
2. `maglev_installer.py`
   - 负责在实际 `init` / `update` 执行面运行检查逻辑

也就是说，skill 负责承接与解释，installer 负责真实执行。

## 3. 检查目标

自检至少要回答三件事：

1. 是否存在
   - 有没有 `AGENTS.md`
   - 有没有 `llms.txt`
2. 是否充分
   - 是否足以帮助 AI 理解当前项目
   - 是否足以帮助 AI 理解 Maglev 操作方式
3. 是否漂移
   - 是否仍停留在旧 runtime name
   - 是否混淆 workflow 入口和 skill runtime name
   - 是否含有明显只属于上游 Maglev 仓库的私有上下文

## 4. 最小检查项

首轮至少检查以下 5 类内容：

### A. 文件存在性

1. `AGENTS.md` 是否存在
2. `llms.txt` 是否存在

### B. 项目理解能力

1. 是否说明项目目标、关键目录或主要任务入口
2. 是否足以帮助 AI 在项目里快速找到方向

### C. Maglev 理解能力

1. 是否反映当前主流程 skill runtime name
2. 是否说明兼容 workflow 入口
3. 是否说明 init / update 等关键操作入口

### D. 规则约束能力

1. 是否提供必要语言与文档写作约束
2. 是否会错误指引 AI 使用旧名或错误入口

### E. 上游私有内容污染

1. 是否含有明显只属于 Maglev 源仓库自身的私有现实
2. 是否会误导用户项目把上游项目现状当成本项目现状

## 5. 输出形式

首轮不要求自动重写文件。

更合理的输出是统一检查结果，例如：

1. `present / missing`
2. `sufficient / insufficient`
3. `aligned / drifted`

并附最小补齐建议。

## 6. 接入层建议

这项能力至少会影响两层：

1. `maglev-bootstrapper`
   - 在初始化完成后做 readiness check
2. `maglev-updater`
   - 在 `dry-run` 或正式更新前后做 drift check

首轮不要求改 release / manifest 的资产下发逻辑。

但可以在 installer 执行面补入最小检查实现，用来承接 init / update 的真实结果。

## 7. 验收信号

满足以下条件时，认为这项能力成立：

1. 新项目初始化后，Maglev 能判断 `AGENTS.md` / `llms.txt` 是否达到最小可用标准
2. 已接入项目升级前，Maglev 能判断这两个文件是否已和当前能力结构漂移
3. 检查结果能指出缺什么，而不是泛化提醒
4. 不再默认把复制上游文件当成解决方案
