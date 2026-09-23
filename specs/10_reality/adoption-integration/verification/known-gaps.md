---
reality_id: adoption-integration.verification.known-gaps
title: 接入与集成已知缺口
owner_domain: adoption-integration
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 本域当前查过且无法证明的点：运行证据缺失、适配层陈旧与零测试、Profile 登记滞后
  excludes:
    - 已证明的实现与契约事实（属 capability/implementation/interfaces 页面）
---
# 接入与集成已知缺口

登记原则：只登记"查过且无法证明"的项；未查过的对象不进入本页。

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 运行证据缺失 | capability/overview、interfaces/cli | 接入能力的"触发→结果"只能是契约级，非运行级 | open |
| 适配层质量 | implementation/claude-code-adapter | 适配层陈旧、零测试、双标题为已知形态 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 四个接入能力对象只有契约文本，无运行记录 | 本仓无日志、产物样本或回执类证据源（触发、六阶段流转、Gate A/B 裁决） | 契约文本只能证明"规定了什么"，不能证明"这样运行过" | 接入能力不得宣称运行效果 | `implementation/claude-code-adapter.md` |
| 适配层陈旧：`.claude/skills/superpowers-bridge` 快照的源目录已删除 | 生成器只新增/覆盖、无删除分支；CLAUDE.md 口径依赖人工重新生成 | 无自动同步机制 | 消费者可能用到失效技能引用 | `implementation/claude-code-adapter.md` |
| 适配层相对引用不可达 | 43 个条目每条仅含 SKILL.md；`convertSkill` 只写单文件 | 源技能 `references/*.md` 不随适配复制 | 适配层内引用断链 | `implementation/claude-code-adapter.md` |
| 适配层双标题（`# maglev-tutor` + `# Maglev Tutor`） | `convertSkill` 剥离 frontmatter 后仅去空行，原一级标题保留 | 转换逻辑未修正，也无"已知接受形态"决策记录 | 适配层可读性 | `implementation/claude-code-adapter.md` |
| 生成器零测试保护 | package.json `test` 脚本为 `echo "No tests yet" && exit 0` | 无任何断言 | 适配行为回归无保护 | `implementation/claude-code-adapter.md` |
| README 与实现的 `--dry-run` 语义偏差 | README 写"预览生成内容"，实现仅打印将创建路径 | 二者不一致 | 使用者预期偏差 | `interfaces/cli.md` |
| `peerDependencies @idea-maglev/maglev-cli >=0.5.0` 无代码耦合点 | bin 与 lib 源码均未 import 该包 | 声明意图无记录 | 依赖语义不明 | `implementation/claude-code-adapter.md` |
| bootstrapper AI-context-check 真实执行面未核对 | step-04 指向 `packages/maglev-cli/dist/maglev_installer.py`，该文件不在本轮来源白名单 | 无法核对实现与 step-04 口径一致 | init 注入行为是转述非核对 | `capability/overview.md` |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 无运行记录 | "bootstrapper/tutor 已在真实项目运行" | 无带时间戳会话记录或产物样本不得宣称 | ✗"SKILL.md 存在所以运行过" |
| 适配层陈旧 | "适配层与源技能始终同步" | 生成器无删除分支 + 已观察陈旧条目 | ✗"头部说每次重新生成所以是新的" |
| 消费者边界 | "消费者项目会得到 Maglev 的 Reality" | 与 bootstrapper 契约相反（只读接入） | ✗"接入即获得完整 Reality 层" |
| 适配器验证 | "适配器行为已验证" | 零测试、无运行记录 | ✗"生成成功即验证通过" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 无运行记录 | 带时间戳的真实接入/逆向/教学会话记录或产物样本（repositories.md、Admission Receipt、ATLAS 生成记录）入库 | 契约文本、SKILL 更新 | `../capability/overview.md` |
| 适配层陈旧 | 生成器补清理逻辑并带测试，或一次重新生成后差集核对记录入库 | 手工删除单个快照 | `../implementation/claude-code-adapter.md` |
| 引用不可达 | 适配层复制引用资产，或转换时改写为源路径引用 | 仅修改单个 SKILL.md | `../implementation/claude-code-adapter.md` |
| 双标题 | 转换修正带断言测试，或"已知接受形态"决策记录入库 | 口头约定 | `../implementation/claude-code-adapter.md` |
| 零测试 | 覆盖 convertSkill/loadConfig/冲突提示分支的测试入库 | echo 占位脚本 | `../implementation/claude-code-adapter.md` |
| dry-run 偏差 | README 更新或实现补内容预览，二者一致 | 单边修改 | `../interfaces/cli.md` |
| peerDependencies | 依赖用途说明或移除声明决策记录入库 | 保留声明不说明 | `../implementation/claude-code-adapter.md` |
| 执行面未核对 | 允许读取 maglev-cli 包的轮次核对 installer 实现并回填锚点 | 继续转述 step-04 | `../capability/overview.md` |

> 证据口径说明：`CLAUDE.md` 与 `.claude/skills/` 为生成器产出的本地生成物（本仓不入库），其行为证据绑定生成器源码；本页对生成物当前内容的观察属于作者工作区时点记录，不作为仓库证据。
