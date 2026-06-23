#!/usr/bin/env python3
"""
track_map.py — Generic per-track cognitive/structural map dispatcher.

Per type:
  - dir-tree    → INDEX.md network IS the map; optionally runs cognitive_map
  - repo-entry  → repo entry map (smart_map.py 行为合并)
  - code-tree   → anchor navigation markdown

Design authority: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md
Execution authority: THIS FILE.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import _track_resolver  # noqa: E402
import _code_tree_helpers as cth  # noqa: E402


def _find_repo_root() -> Path:
    return _track_resolver._find_repo_root()


# ---------- dir-tree ----------

def _map_dir_tree(track: dict[str, Any]) -> int:
    """dir-tree map: optionally runs cognitive_map for docs/ track."""
    repo_root = _find_repo_root()
    # cognitive_map only applies to docs/ (thinking notes with links)
    if track["id"] == "docs":
        legacy = SCRIPT_DIR / "cognitive_map.py"
        if legacy.is_file():
            result = subprocess.run([sys.executable, str(legacy)], cwd=repo_root)
            if result.returncode == 0:
                print(f"[track-map] dir-tree {track['id']}: cognitive_map ok")
                return 0
            else:
                print(f"[track-map] dir-tree {track['id']}: cognitive_map exit {result.returncode}")
                return result.returncode
    print(f"[track-map] dir-tree {track['id']}: INDEX.md network is the navigational map")
    return 0


# ---------- repo-entry (D10: smart_map.py 行为合并) ----------

def _map_repo_entry(track: dict[str, Any]) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-map] skip: root {track['root']} not found")
        return 0

    # repo-entry 的 map 走 smart_map.py 移植行为：浅扫 + 锚点导航
    structure = cth.walk_with_anchors(
        root_dir,
        ignore_dirs=frozenset(track.get("ignore") or cth.DEFAULT_IGNORE_DIRS),
        anchor_files=frozenset(track.get("anchor_files") or cth.DEFAULT_ANCHOR_FILES),
        max_depth=cth.DEFAULT_MAX_DEPTH,
        max_lines=cth.DEFAULT_MAX_LINES,
    )
    markdown = cth.format_repo_map_markdown(structure, max_lines=cth.DEFAULT_MAX_LINES)

    out_rel = track.get("output") or ".agents/_meta/repo-map.md"
    out_path = repo_root / out_rel
    if out_path.suffix in (".yaml", ".yml"):
        # 若用户用了 yaml 后缀，改写到同目录的 .md
        out_path = out_path.with_name("repo-map.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(
        f"[track-map] repo-entry {track['id']}: wrote {len(structure)} entries "
        f"→ {out_path.relative_to(repo_root)}"
    )
    return 0


# ---------- code-tree ----------

def _map_code_tree(track: dict[str, Any]) -> int:
    """code-tree 的 map = 锚点导航 markdown（不含 radar 摘要，摘要在 track_scan 段）"""
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-map] skip: root {track['root']} not found")
        return 0

    structure = cth.walk_with_anchors(
        root_dir,
        ignore_dirs=frozenset(track.get("ignore") or cth.DEFAULT_IGNORE_DIRS),
        anchor_files=frozenset(track.get("anchor_files") or cth.DEFAULT_ANCHOR_FILES),
        max_depth=int(track.get("depth_limit", cth.DEFAULT_MAX_DEPTH)),
        max_lines=cth.DEFAULT_MAX_LINES,
    )
    markdown = cth.format_repo_map_markdown(structure, max_lines=cth.DEFAULT_MAX_LINES)

    out_rel = track.get("output") or f"{track['root'].rstrip('/')}/_meta/code-map.md"
    out_path = repo_root / out_rel
    if out_path.suffix in (".yaml", ".yml"):
        out_path = out_path.with_name("code-map.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(
        f"[track-map] code-tree {track['id']}: wrote {len(structure)} entries "
        f"→ {out_path.relative_to(repo_root)}"
    )
    return 0


DISPATCH = {
    "dir-tree": _map_dir_tree,
    "repo-entry": _map_repo_entry,
    "code-tree": _map_code_tree,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track-id", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    track = _track_resolver.resolve(args.track_id)
    if track is None:
        return 0

    handler = DISPATCH.get(track["type"])
    if handler is None:
        print(f"[track-map] warn: no dispatch for type {track['type']!r}, skip")
        return 0
    return handler(track)


if __name__ == "__main__":
    sys.exit(main())
