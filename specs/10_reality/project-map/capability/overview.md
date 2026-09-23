---
reality_id: project-map.capability.overview
title: 项目地图能力
owner_domain: project-map
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - docs/ATLAS.md 唯一人读地图的确定性生成、指纹新鲜度校验与置信度分级的当前事实
  excludes:
    - 索引引擎与目录盘点（属 machine-index-engine 域）
    - 看板扫描语义（属 collaboration-lifecycle 域）
---
# 项目地图能力

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 新加入的贡献者 | 快速获得唯一的人读项目入口 | `docs/ATLAS.md`（Reality + 看板 + Git 结构的确定性合成） | `.agents/skills/maglev-map-maker/scripts/generate_atlas.py`（`render_atlas`） |
| 维护者 | 校验地图未漂移 | `--check` 指纹比对（tracked path 集 + 治理源内容 sha256），不写盘 | `generate_atlas.py`（`check`、`_source_digest`） |
| 消费自动化 | 获得结构化生成证据 | `.maglev/temp/atlas-snapshot.json`（gitignored 运行时产物，不作证据绑定） | `generate_atlas.py`（`generate`） |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 显式生成动作 | 在 Git 仓库内运行 | 整文件覆写 ATLAS.md；先写 snapshot 再写地图 | 生成架构 | established | supported |
| `--check` | ATLAS frontmatter 携带 source_digest | 指纹一致/漂移报告，不写盘 | 生成架构 | established | supported |
| 治理源缺席 | 候选源文件不存在 | 跳过读取不阻断；置信度降级标注 | 生成架构（`_confidence`） | established | supported |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 不承诺 | 初始化/日常 reality-sync 自动写地图 | 写盘始终是显式动作 | `.agents/skills/maglev-map-maker/SKILL.md` |
| 不承诺 | 输入缺失时猜测补齐 | 按输入可用性降级置信度（High/Medium/Low） | 生成架构 |
| 范围外 | 索引导航与目录盘点 | 属 machine-index-engine 域 | `../machine-index-engine/capability/overview.md` |
| 范围外 | 看板扫描语义 | 属 collaboration-lifecycle 域 | `../collaboration-lifecycle/capability/overview.md` |

## 4. 事实与深挖

- 生成架构、构件、数据、依赖、配置
- [已知缺口](../verification/known-gaps.md)、Claim 登记册
