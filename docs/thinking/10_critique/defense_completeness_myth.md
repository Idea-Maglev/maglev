# Defense: The Completeness Fallacy (完整性谬误)

> **Context**: Sceptic challenge. "Maglev 是否要求所有内容必须非常严谨和完整？如果是，很难落地。"
> **Answer**: **NO.** Maglev 恰恰是反"大而全"的。

## 1. The Myth of "Perfect Spec" (完美文档的迷思)
传统瀑布流要求 "PRD 必须完美才能开发"。结果是 PRD 写了一个月，开发时发现全是错的。
**Maglev 也就是为了解决这个问题而生的。**

## 2. Maglev 的核心机制：JIT Rigor (即时严谨)

Maglev 不要求 *Start* 状态是严谨的，只要求 *Conversion* (转化) 的瞬间是严谨的。

*   **Intake 是宽容的**:
    *   我们在 `specs_lifecycle.md` 定义了 `05_raw_ideas`。你可以只扔一句话："我想做个积分系统，像星巴克那样。" -> **这完全合法。**
*   **Process 是渐进的 (Progressive)**:
    *   Atomizer 拿到这句话，不会因"不严谨"而报错。
    *   它会发起 **Reflection**: "好的积分系统。是指'消费积星'吗？还是'充值送分'？"
    *   **严谨性是在对话中"生长"出来的**，而不是预先"定义"好的。
*   **Correction 是常态**:
    *   代码写出来了，发现不好用？走 `Correction Stream`。我们允许 Spec 出错，只要能快速修正。

## 3. The "Good Enough" Principle (够用原则)

Maglev 的 `Complexity Tier` (分级制度) 就是为了防止过度严谨。
*   **Tier 1 (Hotfix)**: 不需要改为完美的 Spec。直接修代码，AI 自动帮你补一句 Spec 备注就行。
*   **Tier 3 (Arch)**: 只有核心架构才需要 13-Point Checklist。

## 4. 结论
质疑者把 Maglev 误解成了 "AI 时代的瀑布流"。
实际上，Maglev 是 **"AI 时代的敏捷 (Agile)"**。
我们用 AI 极高的生成速度，来**对抗**需求的不确定性，而不是试图用文档**封锁**不确定性。
Spec 不是挡箭牌，Spec 是脚手架。
