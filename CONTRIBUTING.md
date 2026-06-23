# Contributing to Maglev / 参与 Maglev 贡献

Thank you for helping improve Maglev.

感谢你参与 Maglev 的改进。

## Before you start / 开始前

- Read `README.md` and the relevant guide under `docs/guides/`.
- Check whether your change affects documentation, runtime assets, release behavior, or community policy.
- Keep public-facing English and Chinese documents aligned when the change affects user-facing concepts.

- 先阅读 `README.md` 和 `docs/guides/` 下的相关指南。
- 判断你的改动影响的是文档、运行资产、发布行为还是社区政策。
- 如果改动影响用户面概念，需要同步中英文表达。

## Contribution types / 贡献类型

Good first contribution areas:

- documentation clarity;
- bilingual terminology alignment;
- examples and tutorials;
- issue reproduction notes;
- release checks;
- community templates.

适合作为首次贡献的方向：

- 文档清晰度；
- 双语术语一致性；
- 示例和教程；
- issue 复现信息；
- 发布检查；
- 社区模板。

## Pull request expectations / PR 要求

Before opening a pull request:

- explain the user-facing impact;
- link related issues or docs;
- keep sensitive or organization-specific context out of public files;
- do not commit npm tokens or credentials;
- verify package `publishConfig` still points to `https://registry.npmjs.org/` with public access;
- run the most relevant checks you can.

提交 PR 前：

- 说明对用户面的影响；
- 链接相关 issue 或文档；
- 不把敏感信息或组织特定上下文写入公开文件；
- 不提交 npm token 或任何凭据；
- 确认包的 `publishConfig` 仍指向 `https://registry.npmjs.org/` 且 access 为 public；
- 运行你能覆盖的相关检查。

## Sensitive information / 敏感信息

Public docs should describe public behavior and user value. Do not publish private repository paths, company URLs, personal operating notes, credentials, or unverified release claims.

公开文档应描述公开行为和用户价值。不要发布私有仓库路径、公司侧 URL、个人运营笔记、凭据或未验证发布声明。
