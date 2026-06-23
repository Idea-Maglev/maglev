#!/usr/bin/env python3
"""
track_archive_triggers.py — Generic per-track archive-candidate finder.

Per type:
  - dir-tree    → delegate to legacy archive_triggers.py for docs/ track
  - repo-entry  → no-op (anchors don't archive)
  - code-tree   → no-op (use radar for dead-code)

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


def _find_repo_root() -> Path:
    return _track_resolver._find_repo_root()


# ---------- dir-tree ----------

def _archive_dir_tree(track: dict[str, Any]) -> int:
    """dir-tree archive: delegates to legacy archive_triggers.py for docs/ track."""
    if track["id"] == "docs":
        legacy = SCRIPT_DIR / "archive_triggers.py"
        if legacy.is_file():
            return subprocess.run([sys.executable, str(legacy)], cwd=_find_repo_root()).returncode
    print(f"[track-archive] dir-tree {track['id']}: no archive triggers configured")
    return 0


# ---------- repo-entry / code-tree ----------

def _archive_noop(track: dict[str, Any]) -> int:
    print(f"[track-archive] {track['type']} {track['id']}: no archive triggers (by design)")
    return 0


def _archive_code_tree(track: dict[str, Any]) -> int:
    print(
        f"[track-archive] code-tree {track['id']}: no archive triggers "
        f"(use radar unused for dead-code analysis instead)"
    )
    return 0


DISPATCH = {
    "dir-tree": _archive_dir_tree,
    "repo-entry": _archive_noop,
    "code-tree": _archive_code_tree,
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
        print(f"[track-archive] warn: no dispatch for type {track['type']!r}, skip")
        return 0
    return handler(track)


if __name__ == "__main__":
    sys.exit(main())
