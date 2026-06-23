# Security Policy / 安全政策

## Reporting a vulnerability / 报告漏洞

Please do not disclose security issues publicly before maintainers have had a chance to review them.

在维护者完成评估前，请不要公开披露安全问题。

For now, open a private security advisory if available on GitHub, or contact the repository maintainers through the support channel listed in `SUPPORT.md`.

当前请优先使用 GitHub private security advisory（如可用），或通过 `SUPPORT.md` 中的支持渠道联系维护者。

## npm token safety / npm token 安全

- Do not commit persistent npm auth config; use npm login, CI secrets, trusted publishing, or temporary local config for releases.
- Token literals must never be committed.
- Release logs should not print token values.
- Public npm release verification must use `https://registry.npmjs.org/`.

- 不要提交持久 npm 认证配置；发布时使用 npm login、CI secret、trusted publishing 或临时本地配置。
- 不得提交 token 明文。
- 发布日志不应打印 token 值。
- 公开 npm 发布验证必须使用 `https://registry.npmjs.org/`。

## Sensitive information / 敏感信息

Reports involving private URLs, internal automation, or personal operating assets should be redacted before being shared in public issues.

涉及私有 URL、内部自动化或个人运营资产的报告，在公开 issue 中分享前应先脱敏。
