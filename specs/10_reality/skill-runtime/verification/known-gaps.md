---
reality_id: skill-runtime.verification.known-gaps
title: 技能运行时已知缺口
owner_domain: skill-runtime
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 本域已查证据无法成立的结论、原因与关闭条件（lock/sources 缺失、CLI 输出未实测、catalog 约束冲突等）
  excludes:
    - 已绑定证据的事实（见 capability/overview、implementation/registry-mechanics、operations/extension-lifecycle）
---
# 技能运行时已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 扩展运行状态 | `.maglev/` 运行时文件、扩展生命周期 | "已启用扩展"类结论在本仓不成立 | open |
| CLI envelope | extension-manager 契约 | `maglev-extension` 输出字段只有契约级形态 | open |
| catalog 一致性 | `public capability catalog` | object_kind 约束与数据冲突；字段约束无机械强制 | open |
| managed 块同步 | `AGENTS.md` 主链路块 | 块的生成与再生成机制不成立 | open |
| 运行统计 | slot 选择与扩展管理 | 触发频率/失败率统计无数据源 | blocked-no-data |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 本仓不存在 `.maglev/extensions.lock` | 本轮 `.maglev/` 目录核查 + 全仓 find 未命中；resolver 实测返回 `pass` + 空 `candidates` + `fallback.reason=no_enabled_candidate`（exit 0） | lock 是运行时状态文件；"不存在"无法区分"从未安装"与"未提交/被清理"，且无安装历史记录 | 扩展启用结论不可宣称 | 扩展生命周期 |
| 本仓不存在 `.maglev/extensions.sources.yaml` | 本轮 `.maglev/` 目录核查 | 该文件由 `sources add` 创建；缺失时"未配置 source"与"不适用"不可区分 | Registry source 拓扑结论不成立 | 扩展生命周期 |
| `maglev-extension` CLI envelope 字段级形态只有契约级 | extension-manager SKILL.md 的 envelope 规则文本；本轮未运行该 CLI（`which` 观察属会话环境、非仓库事实） | 无真实输出样本，`result`/`issues` 实际字段不能被证实 | CLI 契约停在文本级 | 解析器机制 |
| catalog `object_kind` 约束与数据冲突 | 头注释称仅允许 `skill`/`workflow`，但 `maglev-python-runtime` 条目登记为 `script`（path `scripts/maglev-python`） | 同一权威文件内约束与数据并存冲突，无裁决规则 | catalog 约束可信度受损 | `public capability catalog` |
| catalog 字段约束是否被机械强制不成立 | 源文件内只有头注释声明约束，未定位约束校验执行器 | 声明不等于执行；无校验证据时只能视为"声明级" | 约束强度只能按声明级表述 | `public capability catalog` |
| AGENTS.md `maglev:managed` 主链路块的生成与再生成机制不成立 | 块标注"由治理注册表生成"；已读源文件内无生成器说明 | 生成器与再生成触发不在证据内 | 块与 catalog 的同步性无法证实 | 解析器机制 |
| slot 选择与扩展管理的运行质量统计不成立 | 已读源文件均为契约文本与解析脚本，无运行记录机制 | 无数据源不得产出统计 | 质量/频率统计被阻断 | 解析器机制 |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| lock 不存在 | "某扩展已在本项目启用" | lock 是运行时状态文件，本仓不存在且无安装历史 | ✗"catalog 里有 entry skill 说明已启用" |
| envelope 无样本 | "`maglev-extension` 输出字段形态已证实" | 无真实运行输出样本 | ✗"契约齐全所以运行可靠" |
| 统计无数据源 | "slot 选择/扩展管理运行质量良好（触发频率、失败率）" | 无任何运行记录机制提供可统计数据源 | ✗"resolver 单次 pass 即运行质量良好" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| lock 缺失 | 一次带输出的 `install`/`enable` 运行留档，或 lock 生成/写回行为的文档证据 | 仅修改 SKILL 文本 | 扩展生命周期 |
| sources.yaml 缺失 | `maglev-extension sources list` 的真实输出留档 | 推测默认行为 | 扩展生命周期 |
| envelope 契约级 | 真实 CLI 运行输出留档（含 `--json`） | 本机 which 观察 | 解析器机制 |
| object_kind 冲突 | 修订头注释枚举，或条目迁移/更名后消除冲突 | 在会话内解释冲突 | `public capability catalog` |
| 字段约束强制 | 约束校验行为规格或校验脚本运行证据 | 继续引用头注释 | `public capability catalog` |
| managed 块机制 | 生成器规格或运行证据 | 仅引用块内标注 | 解析器机制 |
| 运行统计 | 会话留档或审计类产物提供可统计数据源 | 单次运行结果外推 | 解析器机制 |
