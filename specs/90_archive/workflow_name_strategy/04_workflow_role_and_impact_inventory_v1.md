# workflow role and impact inventory v1

> 状态：已完成首轮盘点
> 作用：盘点四个兼容 workflow 入口当前承担的角色、影响面与 rename 风险。

## 1. 当前对象

本轮只看四个 workflow：

1. `standup.md`
2. `create-spec.md`
3. `quick-dev.md`
4. `validate-all.md`

它们当前分别对应：

1. `/standup` -> `reality-sync`
2. `/create-spec` -> `spec-designer`
3. `/quick-dev` -> `context-implementer`
4. `/validate-all` -> `integrated-validator`

## 2. 当前结构事实

当前四个 workflow 都已经退化为：

1. 一个很薄的启动包装层
2. 一个兼容入口说明

它们不再承担复杂编排逻辑，主要作用是：

1. 保留低摩擦 slash 入口
2. 将旧用户习惯映射到新 skill runtime name
3. 作为教学与文档中的“可执行入口名”

## 3. 当前引用面

### A. 用户指南与 Reality

当前仍直接使用这些 workflow 入口的现役文档包括：

1. `docs/guides/20_operations/maglev_entrypoints.md`
2. `docs/guides/20_operations/user_manual_atlas.md`
3. `docs/guides/20_operations/maglev_role_flow_translation.md`
4. `specs/10_reality/01_requirements.md`
5. `specs/10_reality/distribution_runtime.md`

判断：

- 它们不是偶然残留，而是当前显性用户入口的一部分

### B. 教学与引导

当前仍直接教授 slash workflow 入口的对象包括：

1. `maglev-tutor/references/step-02-curriculum.md`

判断：

- tutor 仍把 `/quick-dev`、`/create-spec` 一类命令当成用户学习路径的一部分

### C. 发行与排障说明

当前仍把 workflow 文件名和 slash 入口当成实际维护对象的文档包括：

1. `docs/guides/20_operations/maglev_release_manual.md`
2. `docs/guides/20_operations/maglev_distribution_troubleshooting.md`

判断：

- workflow 文件名仍影响构建镜像与排障说明

## 4. workflow rename 的主要风险

如果直接把四个 workflow 文件名一起 rename，当前至少会带来三类影响：

1. 用户学习成本上升
   - 现在用户已经开始按 `/standup`、`/quick-dev` 记忆入口
2. 教学与文档统一成本上升
   - guides、tutor、Reality 都要同步重写
3. 命名收益未必对等
   - `validate-all.md` 本来就不是对象名直译，改成形式整齐不一定更好懂

## 5. 首轮判断

当前更稳的判断不是“立即进入 workflow 物理 rename”，而是：

- `默认保留`

原因：

1. skill runtime name 已经承担了结构规范化
2. workflow 仍主要承担用户入口与兼容职责
3. 当前没有证据表明 workflow 旧文件名已经形成显著使用阻力

## 6. 当前仍需回答的问题

若后续要继续推进，还需要明确：

1. `/standup` 这种短命令是否比 `/reality-sync` 更符合人类使用习惯
2. `create-spec` / `quick-dev` 是否比新动作名更贴近团队口语
3. workflow 层是否应该长期允许“入口名”和“运行名”分离
