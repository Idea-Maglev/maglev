#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Maglev Distribution Engine - Installer
实现零依赖的 Python 3.6+ 分发安装与更新引擎。
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone


DEFAULT_UPSTREAM = os.environ.get("MAGLEV_UPSTREAM_URL", "https://raw.githubusercontent.com/Idea-Maglev/maglev/release")
MAGLEV_DIR = ".maglev"
STATE_FILE = os.path.join(MAGLEV_DIR, "sync_state.json")
CONFIG_FILE = os.path.join(MAGLEV_DIR, "config.json")
MANIFEST_NAME = "manifest.json"
CURRENT_RUNTIME_NAMES = [
    "reality-sync",
    "spec-designer",
    "context-implementer",
    "integrated-validator",
]
LEGACY_RUNTIME_NAMES = [
    "maglev-standup",
    "maglev-create-spec",
    "maglev-quick-dev",
    "maglev-cross-validate",
]
WORKFLOW_ENTRYPOINTS = [
    "/standup",
    "/create-spec",
    "/quick-dev",
    "/validate-all",
]
PRIVATE_CONTAMINATION_MARKERS = [
    "specs/20_evolution/active/",
    "runtime_naming_governance",
    "task_ai_tooling_compatibility_followup",
    "task_public_distribution_channel",
    ".maglev_build",
]

# Discipline injection markers and content
DISCIPLINE_MARKER_START = "<!-- maglev:managed:discipline -->"
DISCIPLINE_MARKER_END = "<!-- /maglev:managed:discipline -->"
DISCIPLINE_BLOCK = """\
<!-- maglev:managed:discipline -->
# 🔴 会话纪律（maglev-discipline）

> 本区块为 Maglev 框架的会话级强制层，所有 agent 在本项目工作时必须遵循。

## 三条不可灰度红线

1. **闭环验证**：交付前必须用证据（命令输出、文件 diff、可观察事实）说话，禁止用"已完成/已修复"代替证据
2. **事实驱动**：声明任何状态前必须有工具验证依据，禁止凭记忆/印象下结论
3. **穷尽方法**：宣告无法解决前必须走完 maglev-discipline 通用 5 步方法论

## 强制读取

进入任何主流程（`reality-sync` / `spec-designer` / `context-implementer` / `integrated-validator`）或本项目治理任务前，必须读取 `.agents/skills/maglev-discipline/SKILL.md`，并将其红线协议作为本会话默认背景纪律。

---
<!-- /maglev:managed:discipline -->
"""
DISCIPLINE_LLMS_LINE = "> 🔴 会话纪律：进入主流程前必须读取 `.agents/skills/maglev-discipline/SKILL.md` 并遵循其红线协议。"


class Colors:
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_info(msg):
    print(f"{Colors.OKCYAN}{msg}{Colors.ENDC}")


def print_success(msg):
    print(f"{Colors.OKGREEN}✅ {msg}{Colors.ENDC}")


def print_warning(msg):
    print(f"{Colors.WARNING}⚠️  {msg}{Colors.ENDC}")


def print_error(msg):
    print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")


def compute_sha256(file_path):
    if not os.path.exists(file_path):
        return None
    digest = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_text_if_exists(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def _minimal_agents_outline():
    return [
        "AGENTS.md 至少应包含：项目目标、关键目录、AI 协作约束、写作硬规则。",
        "可按四段来写：`项目理解`、`Maglev 使用方式`、`协作约束`、`写作与产物纯净`。",
        "在 `Maglev 使用方式` 里写清当前主流程运行名：reality-sync、spec-designer、context-implementer、integrated-validator。",
    ]


def _minimal_llms_outline():
    return [
        "llms.txt 至少应包含：项目背景、主流程 skill runtime name、兼容 workflow 入口、init/update 入口说明。",
        "如果保留 /standup、/create-spec、/quick-dev、/validate-all，请明确它们是兼容 workflow 入口。",
        "不要把 workflow 入口名写成当前 skill runtime name。",
    ]


def _minimal_agents_example():
    return "\n".join(
        [
            DISCIPLINE_BLOCK.rstrip("\n"),
            "",
            "# AGENTS.md",
            "",
            "- 默认使用简体中文回答。",
            "- 项目内引用请使用相对路径，不要写当前系统的绝对路径。",
            "",
            "## 项目理解",
            "",
            "- 本项目目标：<一句话说明项目做什么>",
            "- 关键目录：<列出 2-4 个关键目录及用途>",
            "",
            "## Maglev 使用方式",
            "",
            "- 当前主流程 skill runtime name：reality-sync、spec-designer、context-implementer、integrated-validator",
            "- 兼容 workflow 入口：/standup、/create-spec、/quick-dev、/validate-all",
            "",
            "## 协作约束",
            "",
            "- 改代码前先读相关规格和上下文。",
            "- 不要把上游 Maglev 源仓库的私有现实当成当前项目事实。",
            "",
            "## 写作与产物纯净",
            "",
            "- 面向用户的文档（README、入口页、运营正文）必须站在文档受众视角写作，",
            "  只保留对该受众有直接阅读价值的信息。",
            "- 不要把作者视角、内容治理说明、维护提示、面向内部协作的元信息混入用户文档正文，",
            "  除非用户明确要求保留。",
            "- 不在 `specs/10_reality/` 写未来计划——只写当前事实。",
            "- 不生成 `TODO` / `TBD` / `FIXME` / `<待补>` / `<占位符>` 等占位词到 spec 与 reality 文件。",
            "- 不编造 commit hash / PR 号 / 文件路径——所有引用必须先经过 `git show` 或 `ls` 验证。",
            "",
            "## Git 工作流纪律",
            "",
            "- **新需求必须新分支**：收到新需求或新功能请求时，先从主分支创建 feature 分支再开始工作，禁止直接在 main/master 上开发。",
            "- **归档操作三步走**：",
            "  1. 提取结论写入 `10_reality`（当前事实）",
            "  2. 收口 `20_evolution/active/` 中的状态",
            "  3.（可选）将过程记录归入 `90_archive`",
            "- ❌ 禁止将 `20_evolution` 内容直接搬运到 `90_archive`",
            "- 核心不变量：只看 `10_reality` 就能了解项目当前状态。",
        ]
    )


def _minimal_llms_example():
    return "\n".join(
        [
            "# llms.txt",
            "",
            DISCIPLINE_LLMS_LINE,
            "",
            "你正在一个已接入 Maglev 的项目中工作。",
            "默认使用中文回答。项目内引用使用相对路径。",
            "",
            "当前主流程 skill runtime name：",
            "- reality-sync",
            "- spec-designer",
            "- context-implementer",
            "- integrated-validator",
            "",
            "兼容 workflow 入口：",
            "- /standup",
            "- /create-spec",
            "- /quick-dev",
            "- /validate-all",
            "",
            "说明：workflow 入口是兼容入口，不等于当前 skill runtime name。",
            "初始化和升级时，请同步维护 AGENTS.md 和 llms.txt。",
            "",
            "产物纯净（前置 hint）：",
            "- 面向用户的文档以受众视角写作，避免混入维护元信息。",
            "- 10_reality 只写当前事实，不写未来计划。",
            "- 不使用 TODO/TBD/<待补> 等占位词，所有引用先验证存在。",
        ]
    )


def check_ai_context_assets(project_root="."):
    agents_path = os.path.join(project_root, "AGENTS.md")
    llms_path = os.path.join(project_root, "llms.txt")
    agents_text = _read_text_if_exists(agents_path)
    llms_text = _read_text_if_exists(llms_path)

    combined_parts = [text for text in [agents_text, llms_text] if text]
    combined_text = "\n".join(combined_parts)

    report = {
        "existence": {
            "AGENTS.md": "present" if agents_text is not None else "missing",
            "llms.txt": "present" if llms_text is not None else "missing",
        },
        "sufficiency": {"status": "insufficient", "reasons": []},
        "drift": {"status": "aligned", "reasons": []},
        "contamination": {"status": "clean", "reasons": []},
        "suggestions": [],
        "examples": {},
    }

    if not combined_text.strip():
        report["sufficiency"]["reasons"].append("未发现可用的 AI 上下文内容。")
        report["suggestions"].append("补充 AGENTS.md，说明项目目标、目录入口与 AI 行为约束。")
        report["suggestions"].extend(_minimal_agents_outline())
        report["suggestions"].append("补充 llms.txt，说明 Maglev 主流程、兼容入口与关键操作方式。")
        report["suggestions"].extend(_minimal_llms_outline())
        report["examples"]["AGENTS.md"] = _minimal_agents_example()
        report["examples"]["llms.txt"] = _minimal_llms_example()
        return report

    lower_text = combined_text.lower()
    has_project_context = any(token in combined_text for token in ["项目", "仓库", "目录", "代码库", "repo"])
    has_structure_context = any(
        token in combined_text for token in [".agents", ".maglev", "specs/", "docs/", "issues/"]
    )
    has_maglev_context = "maglev" in lower_text
    has_runtime_name = any(token in combined_text for token in CURRENT_RUNTIME_NAMES)
    has_workflow_entry = any(token in combined_text for token in WORKFLOW_ENTRYPOINTS)
    has_init_update = any(token in lower_text for token in ["init", "update", "初始化", "升级", "更新"])

    if has_project_context and has_structure_context and has_maglev_context and (has_runtime_name or has_workflow_entry):
        report["sufficiency"]["status"] = "sufficient"
    else:
        if not has_project_context:
            report["sufficiency"]["reasons"].append("缺少项目目标、仓库范围或目录入口说明。")
        if not has_structure_context:
            report["sufficiency"]["reasons"].append("缺少关键目录或治理结构说明。")
        if not has_maglev_context:
            report["sufficiency"]["reasons"].append("缺少对 Maglev 的显式说明。")
        if not (has_runtime_name or has_workflow_entry):
            report["sufficiency"]["reasons"].append("缺少主流程 skill 或兼容 workflow 入口说明。")

    legacy_hits = [token for token in LEGACY_RUNTIME_NAMES if token in combined_text]
    if legacy_hits:
        report["drift"]["status"] = "drifted"
        report["drift"]["reasons"].append("仍引用旧主流程 runtime name: " + ", ".join(legacy_hits))

    if has_workflow_entry and not has_runtime_name:
        report["drift"]["status"] = "drifted"
        report["drift"]["reasons"].append("只描述了兼容 workflow 入口，未说明当前 skill runtime name。")

    if not has_init_update:
        report["drift"]["status"] = "drifted"
        report["drift"]["reasons"].append("缺少对 init / update 或初始化升级入口的说明。")

    has_discipline = "maglev-discipline" in combined_text
    if not has_discipline:
        report["drift"]["status"] = "drifted"
        report["drift"]["reasons"].append("缺少会话纪律（maglev-discipline）引用，执行加固未激活。")

    contamination_hits = [token for token in PRIVATE_CONTAMINATION_MARKERS if token in combined_text]
    if contamination_hits:
        report["contamination"]["status"] = "contaminated"
        report["contamination"]["reasons"].append(
            "检测到可能属于上游 Maglev 源仓库的私有上下文: " + ", ".join(contamination_hits)
        )

    if report["existence"]["AGENTS.md"] == "missing":
        report["suggestions"].append("新增 AGENTS.md，写清项目约束、关键目录和 AI 协作规则。")
        report["suggestions"].extend(_minimal_agents_outline())
        report["examples"]["AGENTS.md"] = _minimal_agents_example()
    if report["existence"]["llms.txt"] == "missing":
        report["suggestions"].append("新增 llms.txt，写清主流程、兼容入口和关键命令。")
        report["suggestions"].extend(_minimal_llms_outline())
        report["examples"]["llms.txt"] = _minimal_llms_example()
    if report["drift"]["status"] == "drifted":
        report["suggestions"].append("将旧 runtime name 更新为当前运行名，并区分 skill runtime name 与 workflow 兼容入口。")
        report["examples"].setdefault("AGENTS.md", _minimal_agents_example())
        report["examples"].setdefault("llms.txt", _minimal_llms_example())
    if report["contamination"]["status"] == "contaminated":
        report["suggestions"].append("移除只属于上游 Maglev 源仓库的私有现实，改为当前项目自身上下文。")
    if report["sufficiency"]["status"] == "insufficient":
        report["suggestions"].append("至少补齐：项目目标、关键目录、主流程运行名、兼容入口与 init/update 说明。")
        report["examples"].setdefault("AGENTS.md", _minimal_agents_example())
        report["examples"].setdefault("llms.txt", _minimal_llms_example())

    deduped = []
    seen = set()
    for item in report["suggestions"]:
        if item not in seen:
            deduped.append(item)
            seen.add(item)
    report["suggestions"] = deduped
    return report


def ensure_discipline_pointer(project_root=".", dry_run=False):
    """确保 AGENTS.md 包含 discipline 管理区块，llms.txt 包含纪律行。

    策略:
    - AGENTS.md 有 marker → 更新 marker 间内容
    - AGENTS.md 无 marker → 在文件顶部注入
    - AGENTS.md 不存在 → 跳过（由 ensure_ai_context_files 负责创建）
    - llms.txt 有纪律行 → 跳过
    - llms.txt 无纪律行 → 在第一个空行后注入

    Returns: dict with 'agents_md' and 'llms_txt' status ('injected'|'updated'|'skipped')
    """
    result = {"agents_md": "skipped", "llms_txt": "skipped"}

    agents_path = os.path.join(project_root, "AGENTS.md")
    if os.path.exists(agents_path):
        with open(agents_path, "r", encoding="utf-8") as f:
            content = f.read()

        if DISCIPLINE_MARKER_START in content and DISCIPLINE_MARKER_END in content:
            start_idx = content.index(DISCIPLINE_MARKER_START)
            end_idx = content.index(DISCIPLINE_MARKER_END) + len(DISCIPLINE_MARKER_END)
            new_content = content[:start_idx] + DISCIPLINE_BLOCK.rstrip("\n") + content[end_idx:]
            if new_content != content:
                if not dry_run:
                    with open(agents_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                result["agents_md"] = "updated"
            else:
                result["agents_md"] = "skipped"
        elif "maglev-discipline" not in content:
            if not dry_run:
                with open(agents_path, "w", encoding="utf-8") as f:
                    f.write(DISCIPLINE_BLOCK + "\n" + content)
            result["agents_md"] = "injected"
        else:
            result["agents_md"] = "skipped"

    llms_path = os.path.join(project_root, "llms.txt")
    if os.path.exists(llms_path):
        with open(llms_path, "r", encoding="utf-8") as f:
            llms_content = f.read()

        if "maglev-discipline" not in llms_content:
            lines = llms_content.split("\n")
            insert_idx = 1
            for i, line in enumerate(lines):
                if i > 0 and line.strip() == "":
                    insert_idx = i + 1
                    break
            lines.insert(insert_idx, DISCIPLINE_LLMS_LINE)
            lines.insert(insert_idx + 1, "")
            if not dry_run:
                with open(llms_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
            result["llms_txt"] = "injected"

    return result


def print_ai_context_report(report, phase_label):
    print_info(f"\n[{phase_label}] 🧭 AI 上下文检查")
    existence = report["existence"]
    print(f"  AGENTS.md: {existence['AGENTS.md']}")
    print(f"  llms.txt: {existence['llms.txt']}")
    print(
        "  充分性: "
        + report["sufficiency"]["status"]
        + (f" | {'；'.join(report['sufficiency']['reasons'])}" if report["sufficiency"]["reasons"] else "")
    )
    drift_line = report["drift"]["status"]
    if report["contamination"]["status"] == "contaminated":
        drift_line += " + contaminated"
    reasons = report["drift"]["reasons"] + report["contamination"]["reasons"]
    print("  漂移: " + drift_line + (f" | {'；'.join(reasons)}" if reasons else ""))
    if report["suggestions"]:
        print("  最小补齐建议:")
        for item in report["suggestions"]:
            print(f"    - {item}")
        if report["examples"]:
            if "AGENTS.md" in report["examples"]:
                print("  AGENTS.md 最小示例:")
                for line in report["examples"]["AGENTS.md"].splitlines():
                    print(f"    {line}")
            if "llms.txt" in report["examples"]:
                print("  llms.txt 最小示例:")
                for line in report["examples"]["llms.txt"].splitlines():
                    print(f"    {line}")


def check_submodule_repos(project_root="."):
    report = {
        "status": "none",
        "registered": [],
        "reasons": [],
        "suggestions": [],
    }

    config_path = os.path.join(project_root, ".maglev", "config.json")
    if not os.path.exists(config_path):
        report["reasons"].append("未发现 .maglev/config.json，无法判断是否登记了 submodule 仓库。")
        return report

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
    except Exception as error:
        report["status"] = "unknown"
        report["reasons"].append(f"读取 .maglev/config.json 失败: {error}")
        return report

    repos = config.get("repositories", [])
    submodules = [repo for repo in repos if repo.get("management_mode") == "submodule"]
    report["registered"] = submodules

    if not submodules:
        report["reasons"].append("当前项目未登记 submodule 模式仓库。")
        return report

    gitmodules_exists = os.path.exists(os.path.join(project_root, ".gitmodules"))
    if not gitmodules_exists:
        report["status"] = "attention"
        report["reasons"].append("已登记 submodule 仓库，但根目录缺少 .gitmodules。")

    for repo in submodules:
        local_path = repo.get("local_path", "")
        abs_path = os.path.join(project_root, local_path)
        git_marker = os.path.join(abs_path, ".git")
        repo.setdefault("working_tree_state", "unknown")
        if not os.path.exists(abs_path):
            repo["working_tree_state"] = "missing"
            report["status"] = "attention"
            report["reasons"].append(f"submodule 仓库缺少工作区: {local_path}")
            continue
        if not os.path.exists(git_marker):
            repo["working_tree_state"] = "incomplete"
            report["status"] = "attention"
            report["reasons"].append(f"submodule 仓库目录存在，但未检测到 .git 标记: {local_path}")
            continue
        repo["working_tree_state"] = "ready"

    if report["status"] == "none":
        report["status"] = "ready"
        report["reasons"].append("已登记的 submodule 仓库工作区均可见。")

    if report["status"] == "attention":
        report["suggestions"].append("如需初始化已登记的 submodule 工作区，执行 `git submodule update --init --recursive`。")
        report["suggestions"].append("检查 `.gitmodules`、本地路径和 submodule pointer 是否与团队预期一致。")

    return report


def print_submodule_report(report, phase_label):
    print_info(f"\n[{phase_label}] 🔗 子仓库管理检查")
    if not report["registered"]:
        print("  已登记 submodule: 0")
        print("  状态: none" + (f" | {'；'.join(report['reasons'])}" if report["reasons"] else ""))
        return

    print(f"  已登记 submodule: {len(report['registered'])}")
    print("  状态: " + report["status"] + (f" | {'；'.join(report['reasons'])}" if report["reasons"] else ""))
    for repo in report["registered"]:
        print(
            f"    - {repo.get('name', 'unknown')} | "
            f"path={repo.get('local_path', '')} | "
            f"state={repo.get('working_tree_state', 'unknown')}"
        )
    if report["suggestions"]:
        print("  建议:")
        for item in report["suggestions"]:
            print(f"    - {item}")


# ----------------------------------------------------------------------------
# Pointer Sync (sync-to-recorded)
#
# 由 `04_decision_v1.md`(Explicit Only) + `04_decision_v2.md`(顶层 flag + 行为矩阵)
# + `05_execution_spec_v1.md` §7/§12 定义。
#
# 设计原则:
# - 只做 sync-to-recorded; 不做 sync-to-latest, 不带 --remote
# - 全程基于 wrapper 已记录 revision, 不主动推进业务代码
# - 严格阻断: 未提交改动 / .gitmodules ↔ config 不一致 / 未确认 / 工作区缺失
# - 默认交互确认; --skip-prompt 需配合 --force; --dry-run 永不动 fs
# ----------------------------------------------------------------------------

def _run_git(args, cwd=".", check=False):
    """Run git command, return (returncode, stdout, stderr). Never raises."""
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
        )
        return proc.returncode, proc.stdout.decode("utf-8", errors="replace"), proc.stderr.decode("utf-8", errors="replace")
    except FileNotFoundError:
        return 127, "", "git executable not found"
    except Exception as error:
        return 1, "", str(error)


def _submodule_has_uncommitted_changes(submodule_abs_path):
    """Return True if the submodule working tree has uncommitted changes."""
    if not os.path.isdir(submodule_abs_path):
        return False
    code, out, _ = _run_git(["status", "--porcelain"], cwd=submodule_abs_path)
    if code != 0:
        return False
    return bool(out.strip())


def _read_gitmodules_paths(project_root):
    """Parse .gitmodules and return set of submodule paths declared there.

    使用 `git config -f .gitmodules --get-regexp path` 而非自己解析,
    保持与 git 行为完全一致.
    """
    gitmodules_path = os.path.join(project_root, ".gitmodules")
    if not os.path.exists(gitmodules_path):
        return set()
    code, out, _ = _run_git(
        ["config", "-f", gitmodules_path, "--get-regexp", r"submodule\..*\.path"],
        cwd=project_root,
    )
    if code != 0:
        return set()
    paths = set()
    for line in out.splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            paths.add(parts[1].strip())
    return paths


def _read_recorded_revision(project_root, submodule_path):
    """Read the submodule SHA recorded in the wrapper repo HEAD.

    使用 `git ls-tree HEAD -- <path>` 提取 wrapper 当前记录的 commit.
    """
    code, out, _ = _run_git(
        ["ls-tree", "HEAD", "--", submodule_path],
        cwd=project_root,
    )
    if code != 0 or not out.strip():
        return None
    # 输出格式: 160000 commit <sha>\t<path>
    parts = out.split()
    if len(parts) >= 3 and parts[1] == "commit":
        return parts[2]
    return None


def _read_submodule_head(submodule_abs_path):
    """Read the current HEAD SHA inside the submodule working tree."""
    if not os.path.isdir(submodule_abs_path):
        return None
    code, out, _ = _run_git(["rev-parse", "HEAD"], cwd=submodule_abs_path)
    if code != 0:
        return None
    return out.strip() or None


def plan_sync_to_recorded(project_root):
    """Build the pointer-sync plan WITHOUT touching the filesystem.

    返回 plan dict:
    {
      "status": "no_submodules" | "all_aligned" | "blocked" | "ready" | "wrapper_not_git",
      "blocks": [{"path": str, "reason": str}, ...],
      "aligned": [{"path": str, "revision": str}, ...],
      "to_sync": [{"path": str, "current": str|None, "recorded": str}, ...],
      "config_gitmodules_mismatches": [str, ...],
      "reasons": [str, ...],
    }
    """
    plan = {
        "status": "ready",
        "blocks": [],
        "aligned": [],
        "to_sync": [],
        "config_gitmodules_mismatches": [],
        "reasons": [],
    }

    # 前提 1: wrapper 必须是 git 仓库 (用 exists 兼容 git worktree 场景, 此时 .git 是 file)
    if not os.path.exists(os.path.join(project_root, ".git")):
        plan["status"] = "wrapper_not_git"
        plan["reasons"].append("wrapper 项目根目录不是 Git 仓库, 无法进行 pointer sync.")
        return plan

    # 复用现有 check_submodule_repos 报告
    base_report = check_submodule_repos(project_root)
    if not base_report["registered"]:
        plan["status"] = "no_submodules"
        plan["reasons"].extend(base_report["reasons"])
        return plan

    config_paths = {repo.get("local_path", "") for repo in base_report["registered"] if repo.get("local_path")}
    gitmodules_paths = _read_gitmodules_paths(project_root)

    # config ↔ .gitmodules 一致性: 集合对称差作为 mismatch
    only_in_config = sorted(config_paths - gitmodules_paths)
    only_in_gitmodules = sorted(gitmodules_paths - config_paths)
    for path in only_in_config:
        plan["config_gitmodules_mismatches"].append(f"仅出现在 .maglev/config.json: {path}")
    for path in only_in_gitmodules:
        plan["config_gitmodules_mismatches"].append(f"仅出现在 .gitmodules: {path}")

    if plan["config_gitmodules_mismatches"]:
        for msg in plan["config_gitmodules_mismatches"]:
            plan["blocks"].append({"path": "<config>", "reason": msg})

    # 对每个登记的 submodule 做精细诊断
    for repo in base_report["registered"]:
        local_path = repo.get("local_path", "")
        if not local_path:
            plan["blocks"].append({"path": "<unknown>", "reason": "config 中 submodule 条目缺少 local_path."})
            continue
        abs_path = os.path.join(project_root, local_path)
        state = repo.get("working_tree_state", "unknown")

        if state in ("missing", "incomplete"):
            plan["blocks"].append({
                "path": local_path,
                "reason": f"工作区状态 {state}, 需先执行 `git submodule update --init -- {local_path}`",
            })
            continue
        if state != "ready":
            plan["blocks"].append({"path": local_path, "reason": f"工作区状态未知: {state}"})
            continue

        # ready 状态: 检查未提交改动
        if _submodule_has_uncommitted_changes(abs_path):
            plan["blocks"].append({
                "path": local_path,
                "reason": "submodule 工作区存在未提交改动, 拒绝覆盖.",
            })
            continue

        recorded = _read_recorded_revision(project_root, local_path)
        if not recorded:
            plan["blocks"].append({
                "path": local_path,
                "reason": "无法从 wrapper HEAD 读取该路径的 recorded revision.",
            })
            continue

        current = _read_submodule_head(abs_path)
        if current == recorded:
            plan["aligned"].append({"path": local_path, "revision": recorded})
        else:
            plan["to_sync"].append({
                "path": local_path,
                "current": current,
                "recorded": recorded,
            })

    # 汇总 status
    if plan["blocks"]:
        plan["status"] = "blocked"
    elif not plan["to_sync"] and plan["aligned"]:
        plan["status"] = "all_aligned"
    elif plan["to_sync"]:
        plan["status"] = "ready"
    else:
        plan["status"] = "no_submodules"

    return plan


def print_sync_plan(plan, dry_run=False):
    """Render the plan to stdout for human review."""
    header = "[SYNC] 🧭 Pointer Sync 计划" + (" (DRY-RUN)" if dry_run else "")
    print_info(f"\n{header}")
    status = plan["status"]
    print(f"  状态: {status}")

    if plan["reasons"]:
        for reason in plan["reasons"]:
            print(f"    - {reason}")

    if plan["config_gitmodules_mismatches"]:
        print("  config ↔ .gitmodules 不一致:")
        for msg in plan["config_gitmodules_mismatches"]:
            print(f"    - {msg}")

    if plan["blocks"]:
        print("  阻断项 (拒绝继续):")
        for block in plan["blocks"]:
            print(f"    - [{block['path']}] {block['reason']}")

    if plan["aligned"]:
        print(f"  已对齐 (无需 sync): {len(plan['aligned'])}")
        for item in plan["aligned"]:
            print(f"    - {item['path']} @ {item['revision'][:12]}")

    if plan["to_sync"]:
        print(f"  待 sync (恢复到 wrapper 记录): {len(plan['to_sync'])}")
        for item in plan["to_sync"]:
            cur = (item["current"] or "<missing>")[:12]
            rec = item["recorded"][:12]
            print(f"    - {item['path']}  {cur} → {rec}")


def confirm_sync_proceed(plan, args):
    """Return True if execution should proceed.

    按 04_decision_v2.md §3 行为矩阵:
    - dry_run     → False (调用方应在此前 return)
    - skip_prompt + force → True (CI 自动化)
    - skip_prompt 无 force → False + 报错 (高风险必须显式确认)
    - 默认 → 询问用户 [yes/N]
    """
    if not plan["to_sync"]:
        return False

    if getattr(args, "dry_run", False):
        return False

    skip_prompt = getattr(args, "skip_prompt", False)
    force = getattr(args, "force", False)

    if skip_prompt and not force:
        print_error(
            "Pointer Sync 是恢复性高风险动作, 必须显式确认.\n"
            "  在 --skip-prompt 模式下, 请额外提供 --force 表示已知风险且授权自动化执行."
        )
        return False

    if skip_prompt and force:
        print_warning("(--skip-prompt + --force) 已显式授权, 跳过交互确认.")
        return True

    # 交互确认
    print_warning(
        "\n  即将把以上 submodule 工作区恢复到 wrapper 当前记录的 revision.\n"
        "  这不是拉取远端最新代码, 而是覆盖本地 submodule HEAD.\n"
        "  执行后 wrapper 仓库可能出现新的 git status 变化, 需要你自行评估是否提交."
    )
    try:
        answer = input("  确认执行? [yes/N]: ").strip().lower()
    except EOFError:
        return False
    return answer in ("y", "yes")


def execute_sync_to_recorded(plan, project_root):
    """Execute sync-to-recorded for each to_sync entry.

    使用 `git submodule update --init -- <path>` (无 --remote, 无 --force).
    返回 results list: [{"path": str, "ok": bool, "message": str}, ...]
    """
    results = []
    for item in plan["to_sync"]:
        path = item["path"]
        code, out, err = _run_git(
            ["submodule", "update", "--init", "--", path],
            cwd=project_root,
        )
        if code == 0:
            results.append({"path": path, "ok": True, "message": (out or err or "ok").strip().splitlines()[-1] if (out or err) else "ok"})
        else:
            msg = (err.strip() or out.strip() or f"exit code {code}").splitlines()[-1]
            results.append({"path": path, "ok": False, "message": msg})
    return results


def print_sync_results(plan, results):
    """Render execution results."""
    print_info("\n[SYNC] ✅ Pointer Sync 执行结果")
    aligned_count = len(plan["aligned"])
    if aligned_count:
        print(f"  已对齐 (无需处理): {aligned_count}")
    success = [r for r in results if r["ok"]]
    failure = [r for r in results if not r["ok"]]
    print(f"  成功 sync: {len(success)}")
    for r in success:
        print(f"    ✓ {r['path']}: {r['message']}")
    if failure:
        print_warning(f"  失败: {len(failure)}")
        for r in failure:
            print(f"    ✗ {r['path']}: {r['message']}")
    if plan["blocks"]:
        print(f"  阻断未处理: {len(plan['blocks'])}")
    print("  下一步建议: 检查 wrapper 根目录的 `git status`, 若出现 pointer 变化请自行评估是否提交.")


def run_sync_to_recorded_flow(project_root, args):
    """Orchestrate the full sync flow. Returns exit-style int (0=ok, !=0=err)."""
    plan = plan_sync_to_recorded(project_root)
    print_sync_plan(plan, dry_run=getattr(args, "dry_run", False))

    if plan["status"] in ("no_submodules", "wrapper_not_git"):
        print_info("  无需执行 sync.")
        return 0
    if plan["status"] == "all_aligned":
        print_success("  所有已登记 submodule 均已对齐 wrapper 记录, 无需 sync.")
        return 0
    if plan["status"] == "blocked":
        print_error("  存在阻断项, 拒绝执行 sync. 请按上述提示修复后重试.")
        return 1

    # status == "ready"
    if getattr(args, "dry_run", False):
        print_warning("  [DRY-RUN] 不执行任何 fs 改动, 计划展示完毕.")
        return 0

    if not confirm_sync_proceed(plan, args):
        print_info("  用户未确认或缺少授权, 已取消 sync.")
        return 0

    results = execute_sync_to_recorded(plan, project_root)
    print_sync_results(plan, results)
    if any(not r["ok"] for r in results):
        return 1
    return 0
# ----------------------------------------------------------------------------


def _format_release_notes(text):
    return [line.rstrip() for line in text.splitlines()]


class MaglevInstaller:
    def __init__(self, args):
        self.args = args
        self.upstream_url = self.args.upstream or DEFAULT_UPSTREAM
        self.is_update = os.path.exists(STATE_FILE)
        self.manifest = None
        self.local_state = None
        self.project_config = {}
        self.repositories = []

    def _load_release_notes(self):
        if self.args.local_dist:
            changelog_path = os.path.join(self.args.local_dist, "CHANGELOG.md")
            return _read_text_if_exists(changelog_path)

        changelog_url = (self.manifest or {}).get("changelog_url")
        if not changelog_url:
            return None

        try:
            req = urllib.request.Request(changelog_url)
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode("utf-8")
        except Exception:
            return None

    def print_release_notes(self, phase_label):
        notes = self._load_release_notes()
        if not notes:
            print_warning(f"\n[{phase_label}] 未能读取本次版本说明，已跳过终端展示。")
            return

        print_info(f"\n[{phase_label}] 📣 本次版本说明")
        for line in _format_release_notes(notes):
            print(f"  {line}")

    def run(self):
        print_info(f"{Colors.BOLD}Maglev Distribution Engine{Colors.ENDC}")
        print_info("=" * 40)

        if self.args.command == "init" and self.is_update:
            print_warning("检测到已存在 .maglev/sync_state.json。将自动切换为 Update 模式。")
            self.args.command = "update"
        elif self.args.command == "update" and not self.is_update:
            print_error("未找到本地同步状态，无法执行 Update。请先执行 Init。")
            sys.exit(1)

        print_info(f"\n[1/6] 🔍 环境探测 ({self.args.command.upper()} 模式)")
        if not os.path.exists(".git") and self.args.command == "init":
            print_warning("当前目录非 Git 仓库。Maglev 建议你在 Git 仓库根目录运行。")

        self.fetch_manifest()
        if self.args.command == "init":
            self.do_init()
        else:
            self.do_update()

    def fetch_manifest(self):
        print_info("\n[2/6] 📥 获取远端分发清单")

        if self.args.local_dist:
            manifest_path = os.path.join(self.args.local_dist, MANIFEST_NAME)
            try:
                with open(manifest_path, "r", encoding="utf-8") as file:
                    self.manifest = json.load(file)
                print_success(f"成功获取本地离线清单 v{self.manifest.get('version', 'unknown')}")
                return
            except Exception as error:
                print_error(f"本地清单解析失败: {error}")
                sys.exit(2)

        manifest_url = f"{self.upstream_url}/{MANIFEST_NAME}"
        try:
            req = urllib.request.Request(manifest_url)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode("utf-8")
            self.manifest = json.loads(data)
            print_success(f"成功获取清单 v{self.manifest.get('version', 'unknown')}")
        except urllib.error.URLError as error:
            print_error(f"网络不可达 (无法连接远端): {error}")
            sys.exit(1)
        except json.JSONDecodeError as error:
            print_error(f"manifest.json 解析失败: {error}")
            sys.exit(2)

    def do_init(self):
        print_info("\n[3/6] 🚀 全量下载执行")
        files = self.manifest.get("files", [])
        success_count = 0

        for idx, item in enumerate(files, 1):
            path = item["path"]
            expected_hash = item["sha256"]
            if self.args.dry_run:
                print(f"  [DRY-RUN] Would download: {path}")
                success_count += 1
                continue
            print(f"  → 下载 {path} ({idx}/{len(files)})...", end="\r")
            if self._download_file(path, expected_hash):
                success_count += 1

        print()
        print_success(f"已下载 {success_count}/{len(files)} 个资产集。")

        print_info("\n[4/6] 🏗️ 构建目录骨架")
        self.create_skeleton_dirs()
        self.ensure_gitignore()
        self.ensure_ai_context_files()

        print_info("\n[5/6] 📝 交互式项目配置")
        self.interactive_questionnaire()
        self.gen_configs()

        print_info("\n[6/6] 💾 持久化同步状态")
        self.save_state()
        disc_result = ensure_discipline_pointer(os.getcwd(), dry_run=self.args.dry_run)
        if disc_result["agents_md"] == "injected":
            print_success("已在 AGENTS.md 顶部注入会话纪律区块。")
        elif disc_result["agents_md"] == "updated":
            print_success("已更新 AGENTS.md 中的会话纪律区块。")
        if disc_result["llms_txt"] == "injected":
            print_success("已在 llms.txt 注入纪律引用行。")
        ai_context_report = check_ai_context_assets(os.getcwd())
        print_ai_context_report(ai_context_report, "INIT")
        print_success("\n🎉 初始化成功！欢迎使用 Maglev 飞行。")

    def do_update(self):
        print_info("\n[3/6] 🔄 增量差异计算与更新")
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            self.local_state = json.load(file)

        local_version = self.local_state.get("last_synced_version")
        remote_version = self.manifest.get("version")
        if local_version == remote_version and not self.args.force:
            print_success("当前已是最新版本，无需更新。")
            disc_result = ensure_discipline_pointer(os.getcwd(), dry_run=self.args.dry_run)
            if disc_result["agents_md"] == "injected":
                print_success("已在 AGENTS.md 顶部注入会话纪律区块。")
            elif disc_result["agents_md"] == "updated":
                print_success("已更新 AGENTS.md 中的会话纪律区块。")
            if disc_result["llms_txt"] == "injected":
                print_success("已在 llms.txt 注入纪律引用行。")
            ai_context_report = check_ai_context_assets(os.getcwd())
            print_ai_context_report(ai_context_report, "UPDATE")
            submodule_report = check_submodule_repos(os.getcwd())
            print_submodule_report(submodule_report, "UPDATE")
            if getattr(self.args, "sync_submodules", False):
                run_sync_to_recorded_flow(os.getcwd(), self.args)
            return

        baselines = self.local_state.get("file_baselines", {})
        files = self.manifest.get("files", [])
        stats = {"NEW": 0, "SKIP": 0, "OVERWRITE": 0, "CONFLICT": 0}

        if self.args.dry_run:
            print_warning("  [DRY-RUN] 仅预览本次更新，不会真正写入文件。")

        for item in files:
            path = item["path"]
            remote_hash = item["sha256"]
            base_hash = baselines.get(path)
            if not base_hash:
                stats["NEW"] += 1
                print(f"  [+] NEW: {path}")
                if not self.args.dry_run:
                    self._download_file(path, remote_hash)
                continue
            if base_hash == remote_hash:
                stats["SKIP"] += 1
                continue

            current_local_hash = compute_sha256(path)
            if self.args.force or current_local_hash == base_hash or current_local_hash is None:
                stats["OVERWRITE"] += 1
                prefix = f"  [~] OVERWRITE: {path}"
                if current_local_hash is None:
                    prefix += " (Local missing)"
                print(prefix)
                if not self.args.dry_run:
                    self._download_file(path, remote_hash)
            else:
                stats["CONFLICT"] += 1
                print(f"  [!] CONFLICT: {path} (本地已修改将自动备份)")
                if not self.args.dry_run:
                    backup_path = f"{path}.local_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    shutil.copy2(path, backup_path)
                    print(f"      -> 备份至 {backup_path}")
                    self._download_file(path, remote_hash)

        print_info(
            f"\n  📊 统计: 新增 {stats['NEW']} | 覆盖更新 {stats['OVERWRITE']} | "
            f"冲突备份 {stats['CONFLICT']} | 无变化跳过 {stats['SKIP']}"
        )
        self.print_release_notes("UPDATE")
        self.save_state()
        disc_result = ensure_discipline_pointer(os.getcwd(), dry_run=self.args.dry_run)
        if disc_result["agents_md"] == "injected":
            print_success("已在 AGENTS.md 顶部注入会话纪律区块。")
        elif disc_result["agents_md"] == "updated":
            print_success("已更新 AGENTS.md 中的会话纪律区块。")
        if disc_result["llms_txt"] == "injected":
            print_success("已在 llms.txt 注入纪律引用行。")
        ai_context_report = check_ai_context_assets(os.getcwd())
        print_ai_context_report(ai_context_report, "UPDATE")
        submodule_report = check_submodule_repos(os.getcwd())
        print_submodule_report(submodule_report, "UPDATE")
        print_success(f"\n🚀 Maglev 更新完毕! 新版本 {remote_version}")
        if getattr(self.args, "sync_submodules", False):
            run_sync_to_recorded_flow(os.getcwd(), self.args)

    def _download_file(self, rel_path, expected_hash):
        local_path = os.path.join(os.getcwd(), rel_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        try:
            if self.args.local_dist:
                source_path = os.path.join(self.args.local_dist, rel_path)
                if not os.path.exists(source_path):
                    print_warning(f"\n本地离线源文件缺失: {source_path}")
                    return False
                shutil.copy2(source_path, local_path)
            else:
                full_url = f"{self.upstream_url}/{urllib.parse.quote(rel_path)}"
                req = urllib.request.Request(full_url)
                with urllib.request.urlopen(req, timeout=10) as response, open(local_path, "wb") as out_file:
                    shutil.copyfileobj(response, out_file)

            actual_hash = compute_sha256(local_path)
            if actual_hash != expected_hash:
                print_warning(f"\nHash 校验失败: {rel_path} (Expected: {expected_hash}, Got: {actual_hash})")
                return False
            if rel_path == "scripts/maglev-python":
                os.chmod(local_path, 0o755)
            return True
        except Exception as error:
            err_type = "拷贝" if self.args.local_dist else "下载"
            print_warning(f"\n{err_type}失败 {rel_path}: {error}")
            return False

    def create_skeleton_dirs(self):
        dirs = [
            "specs/00_vision",
            "specs/10_reality",
            "specs/20_evolution/active",
            "specs/90_archive",
            "docs/thinking",
            "docs/guides",
            "issues/active",
            "issues/closed",
            "tests",
            ".maglev",
        ]
        if self.args.dry_run:
            print(f"  [DRY-RUN] Will create {len(dirs)} skeleton directories.")
            return
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)
        print_success("基础领域目录结构生成完毕。")

    def ensure_gitignore(self):
        gitignore_path = ".gitignore"
        # Maglev 推荐的最小忽略集（init/update 都会保证存在）
        maglev_block_marker = "# === Maglev managed (do not edit between markers) ==="
        maglev_block_end = "# === End Maglev managed ==="
        managed_lines = [
            "# Maglev local conflict backups",
            "*.local_backup_*",
            "",
            "# Python caches (Maglev tooling)",
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "",
            "# OS / Editor noise",
            ".DS_Store",
            "",
            "# Maglev local-only state",
            ".maglev/temp/",
            ".maglev/runtime/",
        ]
        managed_block = (
            "\n".join([maglev_block_marker, *managed_lines, maglev_block_end]) + "\n"
        )

        if self.args.dry_run:
            if not os.path.exists(gitignore_path):
                print(f"  [DRY-RUN] Would create {gitignore_path} with Maglev managed block")
            else:
                print(f"  [DRY-RUN] Would ensure Maglev managed block in {gitignore_path}")
            return

        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w", encoding="utf-8") as file:
                file.write(managed_block)
            print_success("已初始化 .gitignore（包含 Maglev managed 块）。")
            return

        # 已存在：若没有 Maglev managed 块则追加，已存在则跳过
        with open(gitignore_path, "r", encoding="utf-8") as file:
            existing = file.read()

        if maglev_block_marker in existing:
            return

        if existing and not existing.endswith("\n"):
            existing += "\n"
        with open(gitignore_path, "w", encoding="utf-8") as file:
            file.write(existing + "\n" + managed_block)
        print_success("已在现有 .gitignore 中追加 Maglev managed 块。")

    def ensure_ai_context_files(self):
        """初始化阶段确保 AGENTS.md 与 llms.txt 至少存在最小骨架。

        - 已存在：保持不动（用户内容优先）
        - 不存在：写入 _minimal_*_example() 提供的最小骨架
        """
        targets = [
            ("AGENTS.md", _minimal_agents_example),
            ("llms.txt", _minimal_llms_example),
        ]
        for filename, builder in targets:
            if self.args.dry_run:
                if not os.path.exists(filename):
                    print(f"  [DRY-RUN] Would create {filename} (minimal skeleton)")
                continue
            if os.path.exists(filename):
                continue
            with open(filename, "w", encoding="utf-8") as file:
                file.write(builder())
                file.write("\n")
            print_success(f"已生成最小骨架 {filename}（请按本项目实际情况补全）。")

    def interactive_questionnaire(self):
        if self.args.skip_prompt:
            print_info("  [跳过] --skip-prompt 生效，使用默认配置。")
            self.project_config["project_name"] = os.path.basename(os.getcwd())
            self.project_config["project_description"] = ""
            return

        default_name = os.path.basename(os.getcwd())
        ans_name = input(f"{Colors.OKCYAN}  ? 项目名称 ({default_name}): {Colors.ENDC}").strip()
        self.project_config["project_name"] = ans_name if ans_name else default_name
        self.project_config["project_description"] = input(f"{Colors.OKCYAN}  ? 项目简述 (可选): {Colors.ENDC}").strip()

        while True:
            print("\n  Git 仓库导入：")
            print("  这一步用于把当前项目依赖的代码仓库登记到 Maglev。")
            print("  这样初始化后可以同时得到：")
            print("  - 初始 repository_map.md")
            print("  - 仓库来源、落地路径与管理方式记录")
            print("  - 后续 update 对 submodule 状态的解释基础")
            print("  如果你现在跳过：")
            print("  - 初始化仍会继续并成功完成")
            print("  - 只是这次不会自动导入或登记任何代码仓库")
            print("  - 后面仍可手动补仓库、重写 repository_map.md 或重新执行 init")
            print("  [1] 现在登记要接入的 Git 仓库")
            print("  [2] 跳过，稍后再补")
            choice = input(f"{Colors.OKCYAN}  ? 请选择 [1]: {Colors.ENDC}").strip()
            if not choice or choice == "1":
                self._interactive_repo_add()
                break
            if choice == "2":
                print_info("  [跳过] 本次不导入 Git 仓库；你后续仍可手动补录。")
                break

    def _interactive_repo_add(self):
        print("\n  你正在登记需要纳入当前 Maglev 工作台的 Git 仓库。")
        print("  建议只填写：")
        print("  - 你希望 AI 在当前项目里长期理解和协作的代码仓库")
        print("  - 或者你准备放到当前目录下统一管理的子仓库")
        print("  如果只是临时参考、不会纳入当前工作台，可以先不填。")
        print("  直接回车可结束登记并继续初始化。")

        while True:
            git_url = input(f"\n{Colors.OKCYAN}  ? 仓库 Git 地址（直接回车结束）: {Colors.ENDC}").strip()
            if not git_url:
                break

            repo_name = git_url.split("/")[-1]
            if repo_name.endswith(".git"):
                repo_name = repo_name[:-4]
            default_local_path = f"./{repo_name}"
            management_mode = self._prompt_repo_management_mode()
            local_path = input(f"{Colors.OKCYAN}  ? 本地落地路径 ({default_local_path}): {Colors.ENDC}").strip() or default_local_path
            desc = input(f"{Colors.OKCYAN}  ? 仓库简述（写这个仓库在项目里负责什么）: {Colors.ENDC}").strip()

            repo_entry = {
                "name": repo_name,
                "git_url": git_url,
                "local_path": local_path,
                "description": desc,
                "management_mode": management_mode,
                "repo_status": "skipped",
            }

            if self.args.dry_run:
                if management_mode == "submodule":
                    print(f"    [DRY-RUN] Would add submodule {git_url} into {local_path}")
                else:
                    print(f"    [DRY-RUN] Would clone {git_url} into {local_path}")
            elif os.path.exists(local_path):
                action = "submodule add" if management_mode == "submodule" else "clone"
                print_warning(f"    目录 {local_path} 已存在，跳过 {action}")
            else:
                try:
                    if management_mode == "submodule":
                        subprocess.run(
                            ["git", "submodule", "add", git_url, local_path],
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                        print_success(f"    Submodule {repo_name} 添加成功")
                    else:
                        subprocess.run(
                            ["git", "clone", git_url, local_path],
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                        print_success(f"    Clone {repo_name} 成功")
                    repo_entry["repo_status"] = "success"
                except subprocess.CalledProcessError as error:
                    err_msg = (error.stderr or "").lower()
                    if "permission denied" in err_msg:
                        print_warning("    权限拒绝: 请确保你对该仓库有访问权限且 SSH key 正确配置。")
                    elif "not found" in err_msg:
                        print_warning("    未找到仓库: 请检查 URL 是否正确。")
                    else:
                        action = "Submodule add" if management_mode == "submodule" else "Clone"
                        print_warning(f"    {action} 失败: {(error.stderr or '').strip()}")

            self.repositories.append(repo_entry)
            cont = input(f"\n{Colors.OKCYAN}  ? 继续添加下一个仓库？ [Y/n]: {Colors.ENDC}").strip().upper()
            if cont == "N":
                break

    def _prompt_repo_management_mode(self):
        while True:
            print("\n  仓库接入模式：")
            print("  [1] clone (默认，直接拉代码下来，最容易理解)")
            print("      适合：先把项目接起来，后面再决定是否精细治理")
            print("  [2] submodule (由当前项目记录该仓库 revision)")
            print("      适合：多仓库长期协作，需要可复现工作台")
            choice = input(f"{Colors.OKCYAN}  ? 请选择 [1]: {Colors.ENDC}").strip()
            if not choice or choice == "1":
                return "clone"
            if choice == "2":
                return "submodule"
            print_warning("    无效选择，请输入 1 或 2。")

    def gen_configs(self):
        if self.args.dry_run:
            return

        self.project_config["maglev_version"] = self.manifest.get("version")
        self.project_config["upstream_url"] = self.upstream_url
        self.project_config["repositories"] = self.repositories
        self.project_config["created_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(self.project_config, file, indent=2, ensure_ascii=False)
            file.write("\n")

        repo_map_path = "specs/10_reality/repository_map.md"
        if os.path.exists(os.path.dirname(repo_map_path)):
            with open(repo_map_path, "w", encoding="utf-8") as file:
                file.write("# Repository Map (仓库映射)\n\n")
                file.write("> 本文件记录当前 Maglev 治理范围内的所有代码仓库。\n\n")
                file.write("## 代码仓库列表\n\n")
                file.write("| 仓库名称 | 路径 | 管理方式 | 状态 | 描述 |\n")
                file.write("| :--- | :--- | :--- | :--- | :--- |\n")
                for repo in self.repositories:
                    file.write(
                        f"| {repo['name']} | `{repo['local_path']}` | "
                        f"{repo.get('management_mode', 'clone')} | "
                        f"{repo.get('repo_status', 'unknown')} | "
                        f"{repo['description']} |\n"
                    )

    def save_state(self):
        if self.args.dry_run:
            print("  [DRY-RUN] Would save state to sync_state.json")
            return

        os.makedirs(MAGLEV_DIR, exist_ok=True)
        baselines = {}
        for item in self.manifest.get("files", []):
            path = item["path"]
            local_hash = compute_sha256(path)
            if local_hash:
                baselines[path] = local_hash

        state = {
            "last_synced_version": self.manifest.get("version"),
            "last_synced_time": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "file_baselines": baselines,
        }
        with open(STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(state, file, indent=2, ensure_ascii=False)
            file.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Maglev Distribution Engine")
    parser.add_argument("command", choices=["init", "update"], help="执行的模式")
    parser.add_argument("--upstream", help="远端发布源的 Raw URL")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不执行破坏性动作")
    parser.add_argument("--force", action="store_true", help="强行覆盖所有文件，忽略本地修改；配合 --sync-submodules --skip-prompt 时表示授权 CI/自动化执行 sync")
    parser.add_argument("--skip-prompt", action="store_true", help="跳过所有交互式问答使用默认值")
    parser.add_argument("--local-dist", help="从本地发行包路径进行离线安装，跳过网络", default="")
    parser.add_argument(
        "--sync-submodules",
        action="store_true",
        help="(仅 update 生效) 将已登记的 submodule 工作区恢复到 wrapper 当前记录的 revision (sync-to-recorded)。默认交互确认；--skip-prompt 必须配合 --force 才能自动执行。",
    )

    args = parser.parse_args()

    if args.sync_submodules and args.command != "update":
        print_error("--sync-submodules 仅在 `update` 命令下生效，请改用 `maglev update --sync-submodules`。")
        sys.exit(2)

    installer = MaglevInstaller(args)
    installer.run()


if __name__ == "__main__":
    main()
