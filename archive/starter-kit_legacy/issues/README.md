# 🎯 意图收件箱 (Intent Inbox)

> **Role**: **Pre-Spec Staging Area**. 原始意图的缓冲区。
> **Input**: 用户在这里提交模糊的想法、Bug 描述或功能请求。
> **Output**: 被 `maglev-spec-ingest` 摄入并转化为 `specs/` 或 `docs/`。

## 📥 这里放什么？(What goes here?)

这里是 **Atomizer** 的输入队列。当你有一个想法但还没准备好写正式 Spec 时，在这里创建一个 Markdown 文件。

- **Feature Ideas**: `active/feat-add-login.md`
- **Bug Reports**: `active/bug-crash-on-payment.md`
- **Questions**: `active/q-how-to-deploy.md`

### 💡 小贴士：附件放哪里？(Where to put valid files?)
如果你有巨大的 PDF PRD、会议录音或设计稿原件：
1.  **Storage**: 将文件放入 `specs/20_evolution/intake/`。
2.  **Trigger**: 在本目录建一个 Issue，并在其中引用该文件路径。
    > "请基于 `specs/20_evolution/intake/v2_prd.pdf` 开始设计。"

## 🔄 生命周期 (Lifecycle)

1.  **Stage (暂存)**: 你创建一个 Issue 文件。
2.  **Route (路由)**: Atomizer 扫描此目录，建议下一步：
    - Feature -> 推荐 `/maglev-quick-spec`
    - Bug -> 推荐 `/maglev-quick-dev`
3.  **Ingest (摄入)**: 技能运行后，会将 Issue 的内容提取到 `specs/` 中。
4.  **Archive (归档)**: 处理完的 Issue 会被移动到 `closed/`。

## 📝 快速模板

```markdown
# 意图标题

## 现状 (Context)
说明当前遇到的问题或背景...

## 期望 (Intent)
希望达成什么效果...

## 原始材料 (Raw Material)
(粘贴日志、截图链接或会议记录)
```
