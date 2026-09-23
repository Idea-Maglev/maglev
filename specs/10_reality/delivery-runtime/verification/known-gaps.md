---
reality_id: delivery-runtime.verification.known-gaps
title: 交付运行时已知缺口
owner_domain: delivery-runtime
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 当前查过、无法在本轮闭环的缺口及其关闭条件
  excludes:
    - 已建立事实（属各页面）
---
# 交付运行时已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 扩展状态 | implementation/extension-distribution | 下游项目扩展状态只能表述为生成机制，不能表述为当前值 | open |
| 扩展验证 | implementation/extension-distribution | 生命周期验证只能引 archive 摘要，非 Testbed 原始记录 | open |
| 退役保护 | implementation/installer | `--force` 交互未穷尽审计，保护承诺有边界 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| `.maglev/extensions.lock` 与 `extensions.sources.yaml` 当前状态无直接证据 | 两文件是下游项目产物，本仓库不持有（目录核查） | 本仓无法证明"任意下游项目的当前状态" | 扩展状态只能讲机制 | `../implementation/extension-distribution.md` |
| 扩展生命周期验证证据（Testbed）在仓库外 | 本仓只有 archive 中验证报告摘要 | 无 commit 级锚点的原始记录 | 验证声称只能到摘要粒度 | `../implementation/extension-distribution.md` |
| `--force` 不绕过退役保护的穷尽路径清单 | installer 源码 force 分支与退役判定交互未逐路径审计 | 保护承诺未穷尽验证 | `--force` 行为承诺有边界 | `../implementation/installer.md` |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 扩展状态文件 | "扩展状态文件存在于项目中" | 在本仓库为假；只能表述为"下游项目由安装器生成" | ✗"lock 在仓库里" |
| Registry 技能验证 | "第三方 Registry 技能已全部验证" | 只有 Testbed 记录覆盖的步骤被验证；凭证相关运行状态 `not_run` | ✗"验证报告存在即全验证" |
| 退役保护 | "`--force` 在所有路径下不绕过保护" | 未逐分支审计 | ✗"文档说了所以穷尽" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 扩展状态 | 一个真实下游项目安装后的 lock 文件入库（digest 绑定） | 在本仓创建示例文件 | `../implementation/extension-distribution.md` |
| Testbed 证据 | Testbed 记录入库，或摘要补充 commit 级锚点 | 再次转述摘要 | `../implementation/extension-distribution.md` |
| `--force` 审计 | 逐分支审计写入 implementation/installer.md，或降级删除该承诺 | 抽样确认 | `../implementation/installer.md` |
