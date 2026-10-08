#!/usr/bin/env python3
"""Generate or freshness-check the canonical human-readable project Atlas."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ATLAS_REL_PATH = Path("docs/ATLAS.md")
SNAPSHOT_REL_PATH = Path(".maglev/temp/atlas-snapshot.json")
PROFILE_REL_PATH = Path("specs/10_reality/00_profile.yaml")
REPOSITORIES_REL_PATH = Path(
    "specs/10_reality/crosscutting/repository-map/repositories.md"
)
REPOSITORY_OVERVIEW_REL_PATH = Path(
    "specs/10_reality/crosscutting/repository-map/overview.md"
)
BOARD_REL_PATH = Path("specs/20_evolution/board.md")
SOURCE_REL_PATHS = (
    PROFILE_REL_PATH,
    REPOSITORIES_REL_PATH,
    REPOSITORY_OVERVIEW_REL_PATH,
    BOARD_REL_PATH,
)
EXCLUDED_PARTS = frozenset(
    {
        ".agents",
        ".git",
        ".maglev",
        ".maglev_build",
        ".pytest_cache",
        "__pycache__",
        "build",
        "coverage",
        "dist",
        "node_modules",
        "vendor",
    }
)
ROOT_ANCHORS = frozenset(
    {
        "AGENTS.md",
        "CHANGELOG.md",
        "Dockerfile",
        "Makefile",
        "README.md",
        "go.mod",
        "llms.txt",
        "package.json",
        "pom.xml",
        "pyproject.toml",
    }
)


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )


def _git_commit(root: Path) -> str:
    result = _run_git(root, "rev-parse", "HEAD")
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def _git_dirty(root: Path) -> bool:
    result = _run_git(root, "status", "--porcelain")
    return result.returncode != 0 or bool(result.stdout.strip())


def _is_visible_tracked_path(path: str) -> bool:
    parts = Path(path).parts
    return bool(parts) and not any(part in EXCLUDED_PARTS for part in parts)


def _tracked_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "git ls-files failed; maglev-map-maker requires a Git repository"
        )
    return sorted(
        path
        for path in result.stdout.decode("utf-8").split("\0")
        if (
            path
            and path != ATLAS_REL_PATH.as_posix()
            and _is_visible_tracked_path(path)
            and (root / path).exists()
        )
    )


def _read_text(root: Path, relative_path: Path) -> str | None:
    path = root / relative_path
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def _source_contents(root: Path) -> dict[str, str]:
    sources: dict[str, str] = {}
    for relative_path in SOURCE_REL_PATHS:
        content = _read_text(root, relative_path)
        if content is not None:
            sources[relative_path.as_posix()] = content
    return sources


def _source_digest(tracked_paths: list[str], sources: dict[str, str]) -> str:
    payload = json.dumps(
        {"tracked_paths": tracked_paths, "sources": sources},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _load_profile_domains(content: str | None) -> list[dict[str, str]]:
    if not content:
        return []
    try:
        profile = yaml.safe_load(content)
    except yaml.YAMLError:
        return []
    if not isinstance(profile, dict):
        return []
    domains = profile.get("domains")
    if not isinstance(domains, list):
        return []
    result: list[dict[str, str]] = []
    for item in domains:
        if isinstance(item, str):
            result.append({"id": item, "title": item})
        elif isinstance(item, dict) and isinstance(item.get("id"), str):
            result.append(
                {
                    "id": item["id"],
                    "title": str(item.get("title") or item["id"]),
                }
            )
    return result


def _parse_repository_inventory(
    content: str | None,
) -> list[dict[str, str]]:
    if not content:
        return []
    repositories: list[dict[str, str]] = []
    for line in content.splitlines():
        if not line.startswith("|") or "---" in line or "仓库名称" in line:
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) < 2 or not cells[0] or not cells[1]:
            continue
        repositories.append({"name": cells[0], "path": cells[1]})
    return repositories


def _parse_board(content: str | None) -> dict[str, Any]:
    board: dict[str, Any] = {
        "updated_at": None,
        "active_count": 0,
        "not_started_count": 0,
        "items": [],
    }
    if not content:
        return board
    summary = re.search(
        r"最后更新:\s*([^|]+)\|\s*活跃需求:\s*(\d+)\s*\|\s*未启动:\s*(\d+)",
        content,
    )
    if summary:
        board["updated_at"] = summary.group(1).strip()
        board["active_count"] = int(summary.group(2))
        board["not_started_count"] = int(summary.group(3))

    in_active_table = False
    for line in content.splitlines():
        if line.strip() == "## 活跃需求":
            in_active_table = True
            continue
        if in_active_table and line.startswith("## "):
            break
        if not in_active_table or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if (
            len(cells) < 5
            or cells[0] in {"需求", "---"}
            or set(cells[0]) == {"-"}
        ):
            continue
        board["items"].append(
            {
                "name": cells[0],
                "intent": cells[1],
                "progress": cells[2],
                "confidence": cells[4],
            }
        )
    if not summary:
        board["active_count"] = len(board["items"])
    return board


def _structure_paths(tracked_paths: list[str], max_depth: int = 2) -> list[str]:
    visible: set[str] = set()
    for tracked_path in tracked_paths:
        path = Path(tracked_path)
        if len(path.parts) == 1 and path.name in ROOT_ANCHORS:
            visible.add(path.as_posix())
        parent_parts = path.parts[:-1]
        for depth in range(1, min(len(parent_parts), max_depth) + 1):
            visible.add("/".join(parent_parts[:depth]))
    return sorted(visible, key=lambda item: (item.count("/"), item))


def _confidence(
    has_repository_inventory: bool,
    repositories: list[dict[str, str]],
    domains: list[dict[str, str]],
    board: dict[str, Any],
) -> tuple[str, str]:
    if has_repository_inventory and repositories and domains and board["updated_at"]:
        return "High", "仓库清单、Reality Profile 与项目看板均可用。"
    if domains or board["updated_at"]:
        return "Medium", "使用当前 Git 仓库并结合部分治理事实生成。"
    return "Low", "仅能从当前 Git 结构生成，缺少 Reality 或看板事实。"


def build_snapshot(root: Path) -> dict[str, Any]:
    root = root.resolve()
    tracked_paths = _tracked_paths(root)
    sources = _source_contents(root)
    repositories = _parse_repository_inventory(
        sources.get(REPOSITORIES_REL_PATH.as_posix())
    )
    has_repository_inventory = bool(repositories)
    if not repositories:
        repositories = [{"name": root.name, "path": "."}]
    domains = _load_profile_domains(sources.get(PROFILE_REL_PATH.as_posix()))
    board = _parse_board(sources.get(BOARD_REL_PATH.as_posix()))
    confidence, confidence_reason = _confidence(
        has_repository_inventory, repositories, domains, board
    )
    return {
        "schema_version": 1,
        "source_commit": _git_commit(root),
        "source_dirty": _git_dirty(root),
        "source_digest": _source_digest(tracked_paths, sources),
        "confidence": confidence,
        "confidence_reason": confidence_reason,
        "repositories": repositories,
        "repository_structure": _structure_paths(tracked_paths),
        "reality_domains": domains,
        "board": board,
        "sources": sorted(sources),
    }


def _node_id(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}_{digest}"


def _label(value: str) -> str:
    return value.replace('"', "'").replace("\n", " ")


def _render_inventory(repositories: list[dict[str, str]]) -> list[str]:
    lines = ["flowchart LR", '    project["项目仓库"]']
    for repository in repositories:
        node = _node_id("repo", repository["name"] + repository["path"])
        label = _label(f"{repository['name']}\\n{repository['path']}")
        lines.append(f'    {node}["{label}"]')
        lines.append(f"    project --> {node}")
    return lines


def _render_structure(paths: list[str]) -> list[str]:
    lines = ["flowchart TD", '    root["仓库根目录"]']
    node_ids: dict[str, str] = {}
    for path in paths:
        node = _node_id("path", path)
        node_ids[path] = node
        lines.append(f'    {node}["{_label(path)}"]')
        parent = Path(path).parent.as_posix()
        if parent == ".":
            lines.append(f"    root --> {node}")
        elif parent in node_ids:
            lines.append(f"    {node_ids[parent]} --> {node}")
    return lines


def _render_reality(domains: list[dict[str, str]]) -> list[str]:
    lines = ["flowchart LR", '    reality["Reality 当前事实"]']
    if not domains:
        lines.append('    missing["未发现 Reality Profile"]')
        lines.append("    reality --> missing")
        return lines
    for domain in domains:
        node = _node_id("domain", domain["id"])
        lines.append(f'    {node}["{_label(domain["title"])}"]')
        lines.append(f"    reality --> {node}")
    return lines


def _render_board(board: dict[str, Any]) -> list[str]:
    lines = [
        "flowchart LR",
        f'    board["项目看板\\n活跃 {board["active_count"]} / 未启动 {board["not_started_count"]}"]',
    ]
    if not board["items"]:
        lines.append('    missing["未发现活跃 Spec 条目"]')
        lines.append("    board --> missing")
        return lines
    for item in board["items"]:
        node = _node_id("item", item["name"])
        label = _label(
            f"{item['name']}\\n{item['progress']}\\n{item['confidence']}"
        )
        lines.append(f'    {node}["{label}"]')
        lines.append(f"    board --> {node}")
    return lines


def render_atlas(snapshot: dict[str, Any], generated_at: str) -> str:
    metadata = [
        "---",
        "generated_by: maglev-map-maker",
        "schema_version: 1",
        f"generated_at: '{generated_at}'",
        f"source_commit: '{snapshot['source_commit']}'",
        f"source_dirty: {str(snapshot['source_dirty']).lower()}",
        f"source_digest: '{snapshot['source_digest']}'",
        f"confidence: {snapshot['confidence']}",
        "---",
    ]
    source_rows = [
        f"| `{source}` | 输入事实 |" for source in snapshot["sources"]
    ]
    if not source_rows:
        source_rows = ["| 当前 Git tracked tree | 结构事实 |"]
    sections = [
        *metadata,
        "",
        "# Maglev Atlas（项目全景地图）",
        "",
        f"> **Confidence**: {snapshot['confidence']} — {snapshot['confidence_reason']}",
        "",
        "## 1. 仓库范围",
        "",
        "```mermaid",
        *_render_inventory(snapshot["repositories"]),
        "```",
        "",
        "## 2. 仓库结构",
        "",
        "```mermaid",
        *_render_structure(snapshot["repository_structure"]),
        "```",
        "",
        "## 3. Reality 拓扑",
        "",
        "```mermaid",
        *_render_reality(snapshot["reality_domains"]),
        "```",
        "",
        "## 4. 演进状态",
        "",
        "```mermaid",
        *_render_board(snapshot["board"]),
        "```",
        "",
        "## 5. 证据来源",
        "",
        "| 来源 | 用途 |",
        "|:---|:---|",
        *source_rows,
        "",
        "> 此文件是派生观察视图，不替代 Reality、项目看板或业务代码事实。",
        "",
    ]
    return "\n".join(sections)


def _metadata_value(content: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*['\"]?([^'\"\n]+)", content, re.MULTILINE)
    return match.group(1).strip() if match else None


def generate(
    root: Path,
    *,
    output: Path | None = None,
    snapshot_path: Path | None = None,
    generated_at: str | None = None,
) -> int:
    root = root.resolve()
    output = output or root / ATLAS_REL_PATH
    snapshot_path = snapshot_path or root / SNAPSHOT_REL_PATH
    generated_at = generated_at or datetime.now(timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )
    snapshot = build_snapshot(root)
    snapshot["generated_at"] = generated_at
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_atlas(snapshot, generated_at), encoding="utf-8")
    print(
        f"[maglev-map-maker] wrote {output.relative_to(root)} "
        f"(confidence={snapshot['confidence']})"
    )
    return 0


def check(root: Path, *, output: Path | None = None) -> int:
    root = root.resolve()
    output = output or root / ATLAS_REL_PATH
    if not output.is_file():
        print(f"[maglev-map-maker] stale: {output.relative_to(root)} is missing")
        return 1
    existing = output.read_text(encoding="utf-8")
    recorded_digest = _metadata_value(existing, "source_digest")
    if not recorded_digest:
        print("[maglev-map-maker] stale: Atlas source_digest metadata is missing")
        return 1
    current_digest = build_snapshot(root)["source_digest"]
    if recorded_digest != current_digest:
        print("[maglev-map-maker] stale: project evidence changed; regenerate Atlas")
        return 1
    print("[maglev-map-maker] current: Atlas matches project evidence")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--generated-at")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output
    if output is not None and not output.is_absolute():
        output = root / output
    snapshot = args.snapshot
    if snapshot is not None and not snapshot.is_absolute():
        snapshot = root / snapshot
    if args.check:
        return check(root, output=output)
    return generate(
        root,
        output=output,
        snapshot_path=snapshot,
        generated_at=args.generated_at,
    )


if __name__ == "__main__":
    sys.exit(main())
