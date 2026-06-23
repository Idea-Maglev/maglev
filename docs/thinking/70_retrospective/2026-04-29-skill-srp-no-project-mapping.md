# Skill 不应持有项目映射 —— SRP 在治理层的应用

- 日期：2026-04-29
- 类别：Retrospective / Skill 治理边界
- 触发场景：artifact-purity-keeper 解耦过程中的职责切分对话

## 1. 现象

`artifact-purity-keeper` 是分发到下游的 user_visible skill。审视其 `audience-rules.md` 时发现：

- "判断算法"段直接列举 `specs/10_reality/`、`specs/20_evolution/active/<spec>/02_design.md`、`plan.md` 等路径作为受众层级的判定依据
- "边界场景"段引用 `specs/.../00_intent.md`、`issues/active/`、`contributors/`、`archive/starter-kit_legacy/` 等仓库特定目录
- `rules.yaml` 默认 `exclude_paths` 含 `.maglev_build/`、`archive/starter-kit_legacy/`
- 反例文档使用 `reality-sync`、`/standup`、`specs/10_reality/README.md` 这种本仓专名

下游接入时这些内容会造成两类问题：

1. **目录不匹配**：下游项目的目录结构与本仓不同，路径硬编码不适用
2. **反向误导**：下游用户看到 `archive/starter-kit_legacy/` 这种本仓历史目录，可能误以为这是 skill 的标准约定

## 2. 第一次的方案与被推翻

最初的方案（方案 A）是"skill 内置默认映射 + 下游可覆盖"——保留路径硬编码作为默认值，新增配置文件让下游声明自己的映射。

被推翻的理由（用户原话提炼）：**"项目以自己的规则机制驱动清理技能做判断，而不是清理技能自己构建当前项目的判断机制。"**

这句话切中了问题本质：skill 不应该回答"在 X 项目里 Y 路径属于什么层级"。这是项目语境问题，应由项目持有；skill 只持有"层级本身的语义"。

## 3. 修正后的边界

| 谁的责任 | 内容 |
|---|---|
| **skill 持有**（通用、可携带） | ① 受众分级的本质特征定义（external/handoff/session 各自的语义边界）<br>② 痕迹识别规则（scanner + rules.yaml 的 pattern）<br>③ 各层级对应的 severity 处置策略<br>④ scanner CLI 接口 |
| **调用方持有**（项目特定） | ① 本项目里"哪些路径是哪个层级"的判断<br>② 调用 scanner 时显式选 severity 档位（external→info / handoff→hard / session→不扫）<br>③ 通过 `--exclude` 或自定义规则集追加项目特定排除路径 |

## 4. 一般化原则：通用 skill 的 SRP 红线

把这次的判断升华为可复用的红线，供未来评估其他 user_visible skill 时使用：

- **红线 1：通用 skill 不持有项目特定路径硬编码**。即使作为"默认值 + 可覆盖"也应警惕——默认值会变成下游用户的隐式期望，反向锚定他们的目录结构。
- **红线 2：通用 skill 持有的是"概念的本质特征"，不持有"具体语境下的实例化判断"**。"什么是 external 受众" 是本质；"specs/10_reality 是 external" 是实例化判断。后者属于调用方。
- **红线 3：skill 内的反例 / 举例应使用占位符或泛化描述**，避免下游读者误把举例当成约定。例如 `<new-name>`、`<legacy-entry>`、`<project-internal-path>` 比 `reality-sync`、`/standup`、`specs/20_evolution/` 更好。
- **红线 4：skill 提供"接口"而非"决策"**。调用方决定"用什么档位扫这个文件"；skill 决定"这个档位对应哪些规则被触发"。

## 5. 反向：什么时候 skill 可以有项目假设？

不是所有 skill 都必须项目无关。判断阈值：

- `distribution_scope: runtime_internal` 的 skill（仅本仓使用）：可以持有本仓约定，不强求项目无关
- `distribution_scope: user_visible` 的 skill（会下发给下游）：必须项目无关，或显式将项目假设隔离到可替换的输入面

artifact-purity-keeper 是 user_visible，所以适用红线。

## 6. 关联

- 解耦实施：commit `3b9d808` (`refactor(skill/purity-keeper): decouple from Maglev project specifics`)
- 涉及文件：`.agents/skills/artifact-purity-keeper/{SKILL.md, references/audience-rules.md, references/finding-interpretation.md, references/rules-extension.md, scripts/rules.yaml, scripts/scanner.py}`
- skill-squadron 后续巡逻应将红线 1-4 纳入 user_visible skill 的检查项
