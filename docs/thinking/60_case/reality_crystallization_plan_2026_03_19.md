# Maglev Iteration to Reality Crystallization Plan

> **日期**: 2026-03-19
> **目标**: 重新定义“需求归档到 Reality”应达到的粒度，并形成后续可重复执行的沉淀计划。

## 1. 背景

本轮围绕分发、安装、同步、`standup`、`.agents` 迁移做了大量真实落地工作，但将需求“归档到 Reality”时，容易退化成：

- 在 `specs/10_reality/01_requirements.md` 写几条结论
- 在 `specs/10_reality/repository_map.md` 补几个目录说明

这类做法有两个问题：

1. **信息过粗**：只能表达“做过了”，不能表达“现在系统到底长什么样”。
2. **无法驱动后续工作**：`standup`、`map-maker`、发布检查、后续迭代都无法仅依赖这类粗粒度文字获得足够准确的现状。

因此，Maglev 需要的不是“任务结论写进 Reality”，而是把 **迭代结果转化为可消费、可校验、可导航的现状结构**。

## 2. 对 Maglev 而言，Reality 应该是什么

结合以下既有判断：

- [maglev_reality_definition.md](./maglev_reality_definition.md)
- [maglev_reality_repair_plan.md](./maglev_reality_repair_plan.md)
- [.agents/skills/reality-sync/SKILL.md](../../.agents/skills/reality-sync/SKILL.md)
- [.maglev/protocols/specs_lifecycle.md](../../.maglev/protocols/specs_lifecycle.md)

可以得出一个更准确的定义：

### 2.1 Reality 不是复述源码

Reality 不应该重复：

- 每个 Skill 的具体 Prompt
- 每个脚本的逐行实现
- 每份文档已经写清的正文

这些都已经有自己的 SSOT。

### 2.2 Reality 是“元信息层”

Reality 应该回答那些散落在各处、但后续协作一定会反复追问的问题：

1. **当前真正生效的主路径是什么**
2. **哪些资产已经是正式运行时结构**
3. **哪些实现是主实现，哪些只是包装层或镜像**
4. **哪些旧概念已经被吸收、废弃或迁移**
5. **用户当前应该如何安装、更新、验证**
6. **哪些事实已经落地，哪些仍是已知缺口**

### 2.3 Reality 对 Maglev 至少要丰富到 4 个维度

#### A. Runtime Reality

当前运行时到底由什么构成：

- `.agents/`
- `.maglev/`
- `dist/`
- `packages/maglev-cli/dist/`
- `sync_state.json`

#### B. Execution Reality

当前真实执行链路是什么：

- 用户安装入口
- 用户更新入口
- 底层执行核心
- 发布构建链路

#### C. Product Reality

当前对用户生效的产品口径是什么：

- 安装前入口
- 安装后交互层
- 不再推荐的旧路径
- 当前文档主入口

#### D. Gap Reality

不是简单写“后续再说”，而是明确哪些能力：

- 当前不存在
- 为什么不存在
- 会影响什么
- 是否阻断发布

## 3. 本轮暴露出的 Reality 不足

本轮已经暴露出 `10_reality` 仍然偏粗的问题：

### 3.1 缺少“主路径状态”

例如：

- 当前安装主路径已切到 `npm / npx`
- `curl | bash` 被降级为未来公开分发能力

这类变化不仅是“需求完成”，更是 **现状边界改变**。

### 3.2 缺少“结构迁移状态”

例如：

- `.agent/` 已迁移到 `.agents/`
- `dist/manifest.json` 与 `packages/maglev-cli/dist/manifest.json` 已同步迁移

这不是普通需求描述，而是 **运行时结构事实**。

### 3.3 缺少“产物层现状”

例如：

- `dist/` 是仓库内发行快照
- `.maglev_build/` 是本轮构建沙箱
- `packages/maglev-cli/dist/` 是 npm 包内镜像

这些关系不进入 Reality，后续很容易再次混淆。

### 3.4 缺少“需求 -> 现状”的映射格式

现在还没有一个明确的模板，告诉维护者：

- 一个需求完成后，应该把哪些结论写进 `10_reality`
- 应该写到什么粒度
- 应该避免什么冗余

## 4. 未来的正确做法：迭代结果如何转为 Reality

以后每轮迭代完成，不应直接把任务摘要塞进 Reality，而应做一次 **Reality Crystallization**，分四步：

### Step 1. 提炼“现状变化点”

先从本轮迭代里只提炼那些会改变系统现状的问题：

- 主入口变化
- 主实现变化
- 运行时结构变化
- 用户路径变化
- 已知缺口变化

### Step 2. 选择写回位置

不同类型的事实写回不同位置：

- `specs/10_reality/01_requirements.md`
  - 写能力现状、主路径、缺口
- `specs/10_reality/repository_map.md`
  - 写结构现状、关键目录关系、主资产位置
- 需要时新增专题 Reality 文档
  - 例如 `specs/10_reality/distribution_runtime.md`
  - 用来承载复杂子系统的结构事实

### Step 3. 写“元信息”而不是写“工作日志”

Reality 中应该写：

- 当前唯一推荐入口是什么
- 当前唯一主实现是什么
- 当前哪些产物是正式发行层

Reality 中不应该写：

- “这次我改了 A/B/C 文件”
- “我做了哪些操作步骤”
- “我先这样然后那样”

这些应该留在：

- issue
- closeout
- thinking

### Step 4. 执行一次 Reality Gate

归档前至少问 4 个问题：

1. `standup` 能否只读 Reality 就说对当前主线？
2. `map-maker` 能否从 Reality 看懂主结构？
3. 新维护者是否能仅靠 Reality 知道当前主入口？
4. 是否把未来计划误写成了当前事实？

## 5. 对当前分发主题，Reality 应该丰富到什么程度

对于 `maglev_distribution` 这条主线，Reality 至少应表达以下内容：

### 5.1 分发主链路

- 用户安装主路径：`npm / npx`
- 用户更新主路径：`npm / npx` + installer 核心
- Shell / curl 当前不是正式对外主路径

### 5.2 执行与包装分层

- `dist/maglev_installer.py` 是统一执行核心
- `packages/maglev-cli/` 是用户入口包装
- `scripts/maglev_release.py` 是上游构建器

### 5.3 运行时结构

- 正式运行目录是 `.agents/`
- 正式状态目录是 `.maglev/`
- `dist/` 与 `packages/maglev-cli/dist/` 当前都已对齐到 `.agents`

### 5.4 用户工程边界

- 根目录不再下发 `install.sh`
- 根目录不再下发 `maglev_installer.py`
- 初始化会补最小 `.gitignore`

### 5.5 交互层事实

- `standup` 已升级为会话启动器
- AI 更新入口尚未产品化

### 5.6 已知缺口

- 公开 OSS / CDN 分发未完成
- 版本治理尚未统一

## 6. 后续执行计划

### Phase 1. 建立 Reality 模板

目标：

- 为未来所有迭代定义统一的“现状沉淀模板”

建议新增：

- `specs/10_reality/README.md`

模板内容至少包括：

- 能力现状
- 结构现状
- 主路径
- 主实现
- 已知缺口

### Phase 2. 为复杂子系统增加专题 Reality

目标：

- 避免把 `01_requirements.md` 塞成大杂烩

建议优先补：

- `specs/10_reality/distribution_runtime.md`

用于承接：

- 分发主链路
- 发行物关系
- 运行时目录
- 包装层关系

### Phase 3. 建立“需求归档到 Reality”的操作协议

目标：

- 让每轮迭代结束时，知道该怎么把结果转成现状

建议内容：

- 什么写进 Reality
- 什么留在 issue / closeout / thinking
- 谁负责检查
- 归档前最小核对项

### Phase 4. 将归档动作接入 Skill

目标：

- 让 `maglev_archival_check` 不只检查“有没有记录”，还检查“有没有正确转成 Reality”

可扩展方向：

- 增加 `Reality Delta` 检查项
- 增加 `Reality 位置选择` 检查项
- 增加 `Future vs Current` 混写检查项

## 7. 本次建议结论

本轮最大的收获不是“又补了一条 Reality 文本”，而是确认了：

> **Maglev 的 Reality 必须从“任务结论摘要”升级为“运行时与产品现状的元信息层”。**

因此，后续正确的方向不是继续在 `01_requirements.md` 里堆 bullet，而是：

1. 建立 Reality 模板
2. 为复杂子系统建立专题 Reality
3. 把“需求 -> 现状”的沉淀过程变成可执行协议

---
*Planned for Maglev Reality Crystallization*
