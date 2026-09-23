---
reality_id: session-reality-sync.verification.known-gaps
title: 会话同步已知缺口
owner_domain: session-reality-sync
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 静态无法证明的同步能力事实
  excludes:
    - 已证明事实（属 test-matrix / static-coverage）
---

# 会话同步已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 运行时行为 | 本页组全部 capability 页 | 同步输出质量结论 | open |
| 输出模板完整性 | business-rules / workflows | Mode 节形态 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 同步输出的真实质量无法静态证明 | SKILL.md 契约 + 本轮会话实操一次 | 契约证明"会输出什么"，不证明"输出得准不准"；准确性依赖当次索引与仓库状态 | 消费方应把同步输出视为起点假设而非结论 | 观测类主题 |
| `[Mode]` 输出节形态未知 | SKILL.md 交互示例只含四节 | 定义四类同步的文本未规定第五节如何呈现 | 输出解析器不能假设固定五节 | 补充交互样例 |
| 无运行记录机制 | 全仓无会话级遥测 | 静态盘点未见任何记录设施 | 无法统计触发频率与失败率 | 观测类主题 |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 无运行记录 | "同步质量 X%"类任何统计 | 无数据源不得产出统计 | ✗"契约齐全所以质量可靠" |
| Mode 节未知 | "五节输出"表述 | 未定位的输出形态不得计入分母 | ✗"四类同步必有五个输出节" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 运行时质量 | 带时间戳的会话同步样本记录 + 与仓库状态的人工比对结论 | 单次无对照的使用感受 | static-coverage |
| Mode 节 | SKILL.md 或交互示例中出现 Mode 节明文 | 推测性描述 | workflows 步骤表 |
