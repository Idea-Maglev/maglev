# 10 Reality

> **Purpose**: `10_reality` 是 Maglev 当前已落地事实的 SSOT，不是任务总结，也不是源码复述。

## 1. 这层应该写什么

`10_reality` 只写 **元信息层事实**，也就是那些会被后续协作反复追问，但无法靠单一源码文件直接回答的问题：

- 当前唯一推荐主路径是什么
- 当前唯一主实现是什么
- 当前运行时结构是什么
- 当前哪些包装层 / 镜像 / 发行物是正式生效的
- 当前哪些能力已经真实落地
- 当前有哪些已知缺口，但尚未阻断系统运行

## 2. 这层不应该写什么

不要把以下内容直接塞进 Reality：

- 逐文件修改清单
- 一轮迭代的执行步骤
- issue closeout 摘要
- Skill / Script 已经自描述过的细节正文

这些应分别留在：

- `issues/`
- `docs/thinking/`
- 各 `SKILL.md`
- 各实现文件本身

## 3. 当前推荐结构

- [01_requirements.md](./01_requirements.md)
  - 记录“当前已经满足的能力现状”和“已知缺口”
- [repository_map.md](./repository_map.md)
  - 记录当前关键目录、资产关系与运行时分层
- [distribution_runtime.md](./distribution_runtime.md)
  - 记录分发、安装、更新链路这一复杂子系统的专题现状

## 4. 归档到 Reality 的最小步骤

每次一轮迭代完成后，先做一次 `Reality Crystallization`：

1. 提炼本轮真正改变了哪些“现状”
2. 判断这些变化属于：
   - 能力现状
   - 结构现状
   - 运行时现状
   - 已知缺口
3. 选择正确落点：
   - `01_requirements.md`
   - `repository_map.md`
   - 某个专题 Reality 文档
4. 执行一次自检：
   - `现状同步（当前通常由 standup 承接）` 能否只读 Reality 说清主线
   - 新维护者能否只读 Reality 找到主入口
   - 是否把未来计划误写成当前事实

## 5. 对分发主题的特殊要求

对于分发、安装、更新相关迭代，Reality 至少要覆盖：

- 用户安装主路径
- 用户更新主路径
- 执行核心与包装层关系
- 运行时目录结构
- 发行物与包内镜像关系
- 下游项目边界
- 当前未完成但已确认的缺口

---
*Reality is not a changelog. Reality is the operating dashboard.*
