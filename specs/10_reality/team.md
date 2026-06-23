---
team:
  vo: { name: "", title: "Value Owner (产品经理)" }
  tp: { name: "", title: "Tech Pilot (技术领航者)" }
  xg: { name: "", title: "Experience Guardian (测试工程师)" }
---

# 团队配置

> 此文件用于 `project-board` Skill 的角色-人员映射。
> 填写 name 字段后，看板将展示具体人员名称而非仅角色代号。

## 使用说明

1. 在上方 YAML frontmatter 的 `name` 字段中填入对应人员姓名
2. `title` 字段仅供阅读参考，不影响看板输出
3. 若某个需求的角色分配与项目级不同，在该 spec 目录下创建 `team.yaml` 覆盖

## 角色定义

详见 [角色画像与人才选拔指南](../../docs/guides/10_concepts/role_personas.md)

| 角色 | 职责 |
|------|------|
| VO (Value Owner) | 价值定义者——需求定义、验收红线和业务决策 |
| TP (Tech Pilot) | 技术领航者——架构设计、代码实施和 AI 协作 |
| XG (Experience Guardian) | 体验捍卫者——质量验证、交互测试和体验把关 |
