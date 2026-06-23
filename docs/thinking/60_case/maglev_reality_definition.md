# 反思：什么才是 Maglev 的 "现状" (10_reality)？

> **Context**: 在 Maglev 自举过程中，`specs/10_reality/` 里只有 `01_requirements.md` 和 `repository_map.md` 两个文件。这引发了一个根本问题：**这两个文件能代表 Maglev 的现状吗？**

## 1. 诊断：当前 `10_reality` 的问题

### 1.1 `01_requirements.md` —— 抽象复述，没有新信息
这个文件用抽象术语重述了 Skills 和 Standards 已经表达过的内容。比如：
> "系统必须提供一组原子化的能力...遵循统一的 SKILL.md 描述标准"

但 `.agents/skills/` 里每个 Skill 的 `SKILL.md` 本身就是最权威的描述。再写一份 spec 去重述它，**没有任何信息增量**。这就像给字典写一份说明书说"这本字典包含了很多词条"。

### 1.2 `repository_map.md` —— 目录索引，不是现状
它列出了目录结构和 Skill 分类，但这些信息通过 `ls` 命令就能获取。**地图不是领土。** 一份文件列表不能替代对项目真实状态的理解。

### 1.3 核心矛盾
Maglev 项目实际拥有的资产极其丰富：
- **6 篇哲学原理** (00_meta): Intent → Red Team → Crystallization 范式、Spec as IR...
- **7 篇批判反思** (10_critique): 防御完备性批判、舰队愿景批判...
- **6 篇架构设计** (20_architecture): 原子化 Spec 架构、Atlas 体系...
- **3 篇核心协议**: Maglev 宣言、纠错协议、双向协议
- **3 份标准**: 协作规范、归档清单
- **29 个 Skills**: 每个都有完整的 SKILL.md
- **1 个 Starter Kit**: 完整的初始化蓝图

但 `10_reality` 对这些只字未提。它描述的是一个"空洞的框架"，而不是一个"拥有丰富积淀的方法论体系"。

## 2. 根因分析：为什么会这样？

### 2.1 `10_reality` 的定义不清晰
Maglev 标准定义了 `10_reality` 是 "现状"，但没有明确指导：
- 对于一个**代码项目**，现状 = 代码结构 + API + 数据模型 → 逆向 Spec 可以生成
- 对于一个**方法论项目** (如 Maglev 自身)，现状 = 哲学 + 标准 + 工具集 → 逆向 Spec 不适用

当前的 `maglev-reverse-spec` 是为代码项目设计的。面对 Maglev 这种"产出物本身就是文档和脚本"的项目，它无法有效工作。

### 2.2 Skill 自描述导致 Spec 冗余
每个 Skill 的 `SKILL.md` 已经包含了：使用场景、交互方式、输入输出。这本身就是一种 "Spec"。再额外生成一份 `01_requirements.md` 来复述它们，确实没有意义。

## 3. 这个问题对 Maglev 用户是否也存在？

**是的，必然存在。** 具体场景：

1. **存量项目接入时**：
   用户使用 `maglev-legacy-adopter` 或 `maglev-reverse-spec` 接入一个已有项目。如果这个项目已经有良好的文档（如 README、API Doc），那么生成的 `10_reality` Spec 就会变成一份冗余的复述。用户会困惑："我已经有文档了，为什么还要再写一份 Spec？"

2. **Skill 驱动的项目**：
   如果用户的项目本身就是 Maglev 风格的（大量 Markdown 驱动），那么 `10_reality` 几乎等同于 `ls` 的输出，没有附加价值。

3. **"现状"的边界模糊**：
   用户会问：我的 `docs/thinking/` 里已经有了设计思考，`standards/` 里有协作规范，这些算不算"现状"？如果算，那 `10_reality` 岂不是要把整个项目都复制进去？

## 4. 建议：`10_reality` 应该是什么？

对于 Maglev 这种方法论项目，`10_reality` 不应该重述已有内容，而应该提供 **元信息 (Meta-Information)** —— 即那些散布在各处、没有任何单一文件能回答的问题：

1. **状态总览**: 项目的整体健康度、成熟度评估
2. **资产索引**: 指向（而非复述）核心资产的链接地图
3. **关系图谱**: 各组件之间的依赖与调用关系
4. **已知缺口**: 明确标注缺失的部分（如"目前没有 Kernel"）

这样 `10_reality` 就变成了一个 **"仪表盘"**，而不是一份 **"复印件"**。

---
*Reflection by Maglev Self-Audit*
