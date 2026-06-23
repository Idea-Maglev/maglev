# Intent: maglev_discipline_governance

## 一句话

为 maglev 框架增加一层"反 AI 治理惰性"强制层，让 AI 在跨平台 agent 环境中无法靠路由判断绕过框架自身的红线。

## 真实问题陈述

maglev 框架定义了一套清晰的需求收敛 → 方案设计 → 实施 → 验证主流程，但 AI 在执行任务时存在多种系统性惰性，会导致主流程在"AI 自评通过"环节失守：

1. **甩锅**：把可设计的判断包装成"Key Unknowns"丢给用户
2. **工具闲置**：声称"研究完了"实则只读了文档前 1/3
3. **绕过框架自治理**：做治理类任务时跳过框架自己的需求收敛 / 方案设计流程，用结果倒推
4. **空口完成**：crystallization 闭环靠 AI 自己说"5/5 门禁通过"，无 verifier
5. **路由黑洞**：根本不进任何主流程 skill，直接答用户，治理 skill 永远不被触发
6. **改 dist 不改 runtime-src**：明明 AGENTS.md 写了警告，AI 还是会犯
7. **类同问题不复盘**：修一个 bug 不查同类位置

这些惰性不是缺乏知识，而是缺乏"会话级强制层"。maglev 现有所有 skill 都是被动加载（AI 路由对了才生效），等于把治理"挂在墙上"。

## 元自证

**本会话本身就是最佳证据**：在做"治 AI 惰性"主题的需求收敛过程中，AI 连续犯了惰性 #1（甩锅）、#2（工具闲置）、#3（绕过框架自治理流程），全部被用户当场戳穿。

这意味着本主题的方案必须能"治 AI 自己"，且必须不依赖 AI 主动调用治理 skill — 否则陷入"AI 必须主动反对自己的惰性才能触发治理"的循环依赖。

## 为什么以前的方案不够

| 备选 | 局限 |
|------|------|
| 给 catalog 加 triggers 字段 | 仍由 AI 判断要不要触发，循环依赖未解 |
| 在每个 skill 头部加纪律提醒 | 只有路由进入该 skill 才生效，治不了"根本不路由"的惰性 |
| 写一份纪律 markdown 放 docs/ | AI 不会主动读 |
| Claude Code hook 强制注入 | 跨平台不可用（Codex/Copilot/Cursor 没有等价 hook） |

## 突破点 — D 方案的核心

借鉴 tanweai/pua 项目在非 Claude Code 平台上的做法：**所有跨平台 agent 都识别的 "always-on 系统提示词文件"**（maglev 对应物 = `AGENTS.md`）才是真正的"准 hook 层"。

D 方案 = `AGENTS.md` 顶部强制红线触发器（会话级始终生效）+ 主流程 skill 头部引用（路由进主流程时二次激活）+ 独立 `maglev-discipline` skill 沉淀完整协议。

## 与 maglev 现有产物关系

- 与 `entry-router` 平级，但**不被 entry-router 路由** — entry-router 是分诊台，maglev-discipline 是会话级背景纪律
- 与 `reality-sync`、`spec-designer`、`context-implementer`、`integrated-validator` 是装饰关系 — 进入这些 skill 时自动叠加红线
- 与 `crystallization` 是验收关系 — crystallization 门禁应引用 maglev-discipline 的"信心门控 6 步"
- 不替换任何现有 skill
