# skill结构性升级 非主干 Skill 保留与清理决议 v1

> 状态：进行中
> 作用：为当前不在 `5+3` 主干骨架中的 skill 提供第一版保留、豁免、延后内部化与清理决议，避免后续再按“感觉”逐个判断。

## 1. 决议目标

这份决议回答的是：

1. 当前哪些非主干 skill 可以直接清理
2. 哪些虽然不在主干上，但仍有保留价值
3. 哪些对象当前不能删除，因为仍被主干对象直接引用

本文件不负责立即执行删除，而负责先固定判断依据。

## 2. 当前决议判据

一个非主干 skill 若要进入清理候选，至少应同时满足：

1. 不再被当前主干 skill 直接引用
2. 不承接 `5+3` 骨架中的稳定职责
3. 不是当前运行链路的必要内部模块
4. 其价值可由更上层对象、通用工具或普通协作动作替代
5. 保留它会继续制造入口噪音、边界歧义或维护负担

补充规则：

- 仅仅“不在当前升级主干上”，不能构成删除理由
- 只要仍被主干对象直接引用，就只能先做“内部化 / 降显性”，不能直接删除
- 团队现实协作约束可以构成保留理由，不能只按结构纯化做拍板

## 3. 当前决议结果

### A. 已执行清理

#### `contribute_methodology`

当前结论：

- 已完成清理

清理理由：

1. 不在当前 `5+3` 主干骨架内
2. 没有被当前主干 skill 直接引用
3. 更接近仓库内部的方法论文档辅助，而不是 Maglev 运行时必须能力
4. 继续保留会制造一个难以向用户解释的旁支入口

当前建议动作：

- 已删除 `.agents/skills/contribute_methodology/SKILL.md`
- 当前仓库内不存在现役 workflow 包装
- 后续仅在历史归档或贡献记录中保留其客观痕迹

### B. 保留并豁免清理

#### `mermaid-expert`

当前结论：

- 保留
- 命名收口已完成

保留理由：

1. 当前 AI 在 Mermaid 生成与修复时仍频繁出现语法错误
2. 该对象承担的是明确的通用图示纠错职责
3. 删除它不会改善主干结构，反而会损失当前可用的实际修复工具

当前问题：

1. 当前保留价值明确，但命名需要与现役 skill 标准一致
2. 已切换为 kebab-case 口径

当前建议动作：

- 继续保留
- 已改名为 `mermaid-expert`
- 不把它误提升为主流程对象

### C. 吸收后删除

#### `maglev-create-prd`

当前结论：

- 已完成吸收方向确认
- 当前进入删除回合

删除前提已满足：

1. 前段“稳定需求产物输出”已转入 `requirement-convergence`
2. 当前删除不会再让需求产物漂移问题失去承接对象
3. 独立 `maglev-create-prd` 继续存在只会制造并列入口和错误路由

删除理由：

1. 它不属于当前主流程骨架中的稳定一级对象
2. 继续和 `requirement-convergence`、`maglev-create-spec` 并列存在，会继续制造前段三入口并存
3. 它的结构职责已被 `requirement-convergence` 内化，不再需要独立一级能力

当前建议动作：

1. 删除 `.agents/skills/maglev-create-prd/`
2. 删除 `.agents/workflows/create-prd.md`
3. 统一现役文档口径为：稳定需求产物输出属于 `requirement-convergence`
4. 历史 `archive/scout` 保留为客观决策痕迹，不再作为现役运行口径

补充文档：

- `design/03au_maglev_create_prd_transition_plan_v1.md`

### D. 已完成物理内部化并退出运行面

#### `maglev-spec-ingest`
#### `maglev-spec-draft`
#### `maglev-spec-crystallize`
#### `maglev-validate-spec-context`

当前结论：

- 已完成物理内部化
- 现役独立目录已删除

完成依据：

1. `ingest` / `validate-context` 已并入 `maglev-create-spec/references/pipeline/`
2. `draft` / `crystallize` 已并入 `.agents/skills/_internal/spec-pipeline/`
3. `maglev-create-spec` / `maglev-reverse-spec` 的活引用已切换到新路径
4. 旧的四个独立 skill 目录已删除，且未打断当前主链路

当前建议动作：

1. 后续只维护新 internal / private pipeline 目录
2. 不再恢复旧独立 skill 目录
3. 若后续再调结构，应在新主题中继续推进，而不是回退到旧独立对象

## 4. 当前最小执行顺序

如果后续进入实际清理，当前更合理的顺序是：

1. `contribute_methodology` 已清理完成
2. `mermaid-expert` 命名收口已完成
3. 删除 `maglev-create-prd` 现役 skill 与 workflow
4. 已完成 `maglev-spec-*` 与 `maglev-validate-spec-context` 的物理内部化与移除

## 5. 当前结论

到这一版为止，当前已完成清理的对象是：

- `contribute_methodology`

其余非主干对象中：

- `mermaid-expert` 属于保留豁免
- `maglev-create-prd` 已吸收到 `requirement-convergence`，现役对象进入删除回合
- `maglev-spec-*` 与 `maglev-validate-spec-context` 已完成物理内部化并退出运行面
