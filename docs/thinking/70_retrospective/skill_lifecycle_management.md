# Maglev Skill 更新与生命周期管理方案 (RFC)

> **Status**: Draft
> **Author**: Maglev AI
> **Date**: 2026-02-13

## 1. 背景与挑战
当前 Maglev 的 Skill (如 `spec-designer`，历史运行名：`maglev-create-spec`) 是以源码形式散落在 `.agents/skills` 目录下的。
用户面临的痛点：
1. **获取难**: 不知道官方什么时候更新了新技能。
2. **升级难**: 手动复制粘贴文件容易出错，且容易覆盖用户的自定义配置。
3. **环境杂**: 用户分布在 Mac, Windows, Linux，且技术水平参差不齐。

## 2. 用户分层与场景分析

我们不应该用一套方案强塞给所有人，建议采用 **"分层交付策略"**。

### Level 1: The Consumer (拿来即用型)
*   **特征**: 不懂 Git，不想看 Python 代码，只希望在 Cursor/VSCode 里输入 `/` 就能用。
*   **OS**: Windows 用户居多，其次是 Mac。
*   **痛点**: "环境配置" 是最大的拦路虎 (Python 版本、依赖包)。
*   **策略**: **"无感更新" (Seamless Update)** via Workflow.

### Level 2: The Tinkerer (配置玩家)
*   **特征**: 会修改 `PROMPT.md`，会调整一些参数，但不动核心 Python 逻辑。
*   **OS**: Mac/Linux 居多。
*   **痛点**: 官方更新后，自己的 Prompt 修改被覆盖。
*   **策略**: **"配置分离" (Config Separation)**. 代码与配置解耦。

### Level 3: The Contributor (魔改大神)
*   **特征**: 直接修改 Python 源码，甚至重写 Logic。
*   **痛点**: Merge Conflict。
*   **策略**: **Git-Native Flow**.

## 3. 核心方案：The "Maglev Manager" (M-CLI)

建议引入一个轻量级的 **Python 脚本 (`manage.py` 或 `m`)** 作为统一入口，屏蔽 OS 差异。

### 3.1 为什么是 Python?
*   **跨平台**: Windows/Mac/Linux 通吃 (只要有 Python)。
*   **Maglev 依赖**: Maglev 的 Skill 本身就依赖 Python 运行环境，由于用户已经在运行 Skill，说明 Python 环境已就绪。
*   **能力强**: 处理文件操作、网络请求、Git 调用比 Shell/Bat 更稳健。

### 3.2 交互设计

#### 方案 A: 适合 L1 用户的 "AI 代理模式"
用户不需要打开终端，直接在 Chat 框输入：
```
User: /update-skills
AI: 检测到 'spec-designer' 有新版本 (v2.1)。
    更新内容: 修复了 Windows 下的路径分隔符问题。
    正在为您下载并应用补丁...
    [执行 python manage.py upgrade spec-designer]
    更新完成！
```

#### 方案 B: 适合 L2/L3 的 "CLI 模式"
```bash
# Windows (Powershell) / Mac / Linux
python manage.py list       # 列出可更新的 Skills
python manage.py upgrade    # 更新所有
python manage.py restore    # 恢复出厂设置 (当玩坏了时)
```

## 4. 针对不同 OS 的 "最后一公里" (Bootstrapping)

为了让用户能跑起来 `python manage.py`，我们需要提供极简的引导脚本。

| OS | 引导脚本 | 作用 |
| :--- | :--- | :--- |
| **Mac/Linux** | `maglev.sh` | 检查 Python -> 建立 venv -> 运行 manage.py |
| **Windows** | `maglev.bat` | 检查 Python -> 建立 venv -> 运行 manage.py |

**关键假设**: 我们假设用户机器上至少安装了 Python。如果连 Python 都没有，建议提供一个 "One-Line Installer" (如 `curl ... | bash` 或 Powershell 命令)。

## 5. 解决 "覆盖冲突" 的策略

为了满足 L2 (配置玩家) 的需求，Skill 结构需要标准化改造：

```text
.agents/skills/spec-designer/
├── SKILL.md          # [Core] 指令入口 (只读，由官方更新)
├── src/              # [Core] 代码实现 (只读，由官方更新)
├── config/           # [User] 用户配置 (如 prompt_templates, settings.yaml)
│   ├── default.yaml  # 默认配置
│   └── user.yaml     # 用户覆盖配置 (.gitignore)
└── REVISION          # 版本号文件
```

**更新逻辑**:
1. `updater` 下载最新的 `src/` 和 `SKILL.md`，强制覆盖。
2. `config/default.yaml` 覆盖更新。
3. `config/user.yaml` **保留不动**。
4. 运行时，程序优先读取 `user.yaml`，缺省值回退到 `default.yaml`。

## 6. 总结建议

1.  **统一内核**: 开发 `manage.py` 处理核心更新逻辑。
2.  **分层入口**:
    *   **Dashboard**: 提供 `/update` Workflow 供 AI 调用。
    *   **CLI**: 提供 `maglev.bat` / `maglev.sh` 供终端调用。
3.  **安全网**: 引入版本控制文件 `REVISION` 和配置分离，防止用户修改丢失。

---
**Decision Needed**:
您是否同意以 **Python (`manage.py`)** 为核心，辅以 **Shell/Bat 引导脚本** 的技术路线？
这将作为我们后续开发 "Maglev Skill Package Manager" 的基础。
