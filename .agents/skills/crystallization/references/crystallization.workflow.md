---
name: crystallization
description: 在完整 Reality Projection 验证后完成准入、active 收口与可发现性回填
output_folder: .agents/skills/crystallization
---

# Crystallization Workflow

**Goal**: 在主流程后段完成事实状态闭环，把已成立结果沉淀为新的项目现实。

## 流程 (Process)

1. 结晶条件确认
2. 现实回写判定
3. active 状态收口
4. 可发现性回填
5. 结构化归档（仅当 Step 3 判定 close 时）

## 进入条件 (Entry Conditions)

- 当前主题已完成主要实施
- 已能在隔离分支形成完整 Reality Projection，并可创建独立验证 worktree
- 需要判断 Reality 回写、active 收口或可发现性回填
- 已有逆向 Work Contract、Module Map、Gate A/B 和逐模块语义包，或明确记录本主题不经过逆向链

## 退出条件 (Exit Conditions)

满足以下任一条件即可结束本次结晶：

1. 明确给出 Reality 回写、active 状态和可发现性回填结论
2. 明确给出 `not_ready_to_crystallize` 与阻塞项，停止继续结晶

## 最小产物 (Minimum Deliverables)

- 结晶条件结果
- 写回范围判断
- active 状态结论
- 回填动作清单

## 步骤架构

- **Micro-Steps**: 严格遵循 `step-*.md`
- **Isolation**: 内存中只加载当前步骤

## 初始化

1. 读取 Reality Profile，把成立事实与既有 Reality 合并到同一受控分支；
   Admission 不再代替 Producer 写入。
2. 若当前结果来自逆向链，先核对 Gate A 的模块边界和依赖顺序、Gate B 的项目级入口页面与首个模块
   纵切片，以及后续逐模块语义包；任何缺失都在 Step 1 标为 `not_ready_to_crystallize`，
   不能用“已有页面”替代。
3. 阅读 `references/step-01-confirm-readiness.md`

## 跨会话交接纪律

当一个会话只完成了部分结晶时，交接产物必须包含以下四项：

1. **进度清单**：哪些模块/结构单元已完成、哪些待做
2. **约束清单**：目录结构、命名规范、标记格式等已确立的规则
3. **质量标杆引用**：指定一个已完成模块作为参照（具体文件路径 + 期望信息密度）
4. **验证清单**：后续会话完成新模块后必须执行的检查项

> ⚠️ 缺少质量标杆引用 = 下一会话大概率产出质量不一致产物。
