# SDD 执行工具全景与 Maglev 桥接灵活性

> **日期**: 2026-05-31
> **触发**: Superpowers 集成完成后的战略反思
> **位段**: 20_architecture (架构判断)

## 背景

Maglev 在 v0.4.5 完成了与 Superpowers 的深度整合（`superpowers-bridge` skill）。整合后需要回答：如果未来 SP 不再是最佳选择，替换成本是多少？当前设计是否有锁定风险？

## 三工具对比

| 维度 | Superpowers | Spec Kit | OpenSpec |
|------|-------------|----------|----------|
| 维护者 | Jesse Vincent (obra) | GitHub 官方 | Fission AI |
| Stars | ~5K | 107K | 52K |
| 核心哲学 | 严格 TDD + subagent 自主执行 | Spec 即可执行规范 | 轻量灵活、先对齐再写 |
| 流程 | brainstorm→plan→subagent→TDD→review | specify→plan→tasks→implement | propose→apply→archive |
| 安装 | 各平台 plugin 系统 | `uv tool install specify-cli` | `npm install -g @fission-ai/openspec` |
| TDD | **强制**（铁律级） | 可选 | 可选 |
| Subagent 并行 | ✅ 核心特性 | ❌ | ❌ |
| 两阶段 Review | ✅ (spec 合规 + 代码质量) | ❌ | ❌ |
| Git Worktree | ✅ | ❌ | ❌ |
| 自有 Spec 层 | ❌ (依赖外部) | ✅ (完整) | ✅ (完整) |

## 与 Maglev 的互补度判断

**Superpowers — 互补度最高**：
SP 完全不做上游（需求收敛、spec 设计），只做代码执行。Maglev 完全不做代码执行，只做上游和验证。两者是"上游-下游"关系，零重叠。

**Spec Kit — 互补度中等**：
SpecKit 自带完整的 spec 层（/speckit.specify + /speckit.plan），与 Maglev 的 requirement-convergence + spec-designer 存在功能重叠。若集成 SpecKit，要么禁用其 spec 层只用执行层，要么让 Maglev 退出 spec 环节（不可接受）。

**OpenSpec — 互补度中等**：
类似 SpecKit，OpenSpec 也有 /opsx:propose 做 spec。但 OpenSpec 强调"轻量灵活"，其 spec 层更像快速草案而非 Maglev 的结构化产出。集成时可以跳过 propose 直接用 /opsx:apply，但需要格式适配。

## 当前桥接架构耦合度分析

```
superpowers-bridge SKILL.md 构成拆分：

通用逻辑 (~60%)                    SP 特有 (~40%)
├── delivery_type 路由判断          ├── 启动指令模板 (~15 行措辞)
├── 安装检测模式 (接口)             ├── 检测路径 (skills/writing-plans/...)
├── 结果回收接口 (diff+test)        ├── 跳过规则 ("skip brainstorming")
├── 优先级协议骨架                  ├── SP skill 名引用
└── 混合交付物串行处理              └── finishing-a-development-branch 假设
```

**替换成本评估**：
- 换到 SpecKit: ~2h（改模板+检测路径+跳过规则）
- 换到 OpenSpec: ~2h（类似）
- 泛化为多后端: ~4h（抽象接口+配置注册）

## 决策结论

1. **当前设计不过度抽象** — 40% 工具特有内容的替换成本（~2h）远低于预防性抽象的维护成本。遵循 YAGNI。
2. **SP 仍是最优选择** — 因为零 spec 层重叠 + 强制 TDD + subagent 并行。
3. **保留灵活性** — 如果 SP 项目停滞或出现更好选择，重写 bridge 的 40% 内容即可迁移。
4. **不强制团队绑定** — `superpowers-bridge` 有"SP 未安装时回退到 CI"的逻辑，用户可选择不安装 SP。

## 延伸：何时应该重新评估

- SP 项目 6 个月无更新
- SpecKit/OpenSpec 新增"无 spec 层纯执行模式"
- 出现新工具同时满足：无 spec 重叠 + 强 TDD + subagent 支持
- 团队反馈 SP 的 TDD 铁律过于严格影响效率
