#!/usr/bin/env python3
"""
track_verify.py — Generic per-track health check dispatcher.

Per type:
  - dir-tree    → verify INDEX.md existence + frontmatter validity
  - repo-entry  → verify all declared anchor patterns hit at least once
  - code-tree   → verify root exists
  - removed     → error with migration hint

Design authority: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md
Execution authority: THIS FILE.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import _track_resolver  # noqa: E402
from common.index_gen import discover_indexable_dirs  # noqa: E402
from common.frontmatter import parse_file  # noqa: E402


def _find_repo_root() -> Path:
    return _track_resolver._find_repo_root()


# ---------- dir-tree ----------

def _verify_dir_tree(track: dict[str, Any]) -> int:
    """Verify dir-tree: INDEX.md existence + frontmatter validity."""
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-verify] dir-tree {track['id']}: root {track['root']} not found")
        return 1

    issues: list[str] = []

    # 1. Output file existence
    output = track.get("output")
    if output:
        output_path = repo_root / output
        if not output_path.exists():
            issues.append(f"scan output missing: {output} (run scan first)")

    # 2. Discover dirs and check INDEX.md existence
    ignore = set(track.get("ignore") or ["_meta"])
    max_depth = track.get("max_depth", 4)
    dirs = discover_indexable_dirs(root_dir, ignore, max_depth)

    for dir_path in dirs:
        idx = dir_path / "INDEX.md"
        if not idx.exists():
            rel = dir_path.relative_to(repo_root)
            issues.append(f"missing INDEX.md: {rel}/")
            continue

        # 3. Frontmatter validation (relaxed: just check type field)
        result = parse_file(idx)
        if not result.is_valid:
            rel = idx.relative_to(repo_root)
            # Only report critical errors, not missing optional fields
            critical = [e for e in result.errors if "type must be" in e or "No YAML" in e or "YAML parse" in e]
            if critical:
                issues.append(f"invalid frontmatter: {rel} ({critical[0]})")

    if issues:
        print(f"[track-verify] dir-tree {track['id']}: {len(issues)} issue(s)")
        for s in issues[:15]:
            print(f"  - {s}")
        return 1
    print(f"[track-verify] dir-tree {track['id']}: ok ({len(dirs)} dirs checked)")
    return 0


# ---------- repo-entry ----------

def _verify_repo_entry(track: dict[str, Any]) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        return 0

    patterns = track.get("patterns") or []
    misses = [pat for pat in patterns if not any(root_dir.glob(pat))]
    if misses:
        print(
            f"[track-verify] repo-entry {track['id']}: {len(misses)} pattern(s) "
            f"matched zero files (informational, not a failure)"
        )
        for m in misses:
            print(f"  - {m}")
    print(f"[track-verify] repo-entry {track['id']}: ok")
    return 0


# ---------- code-tree ----------

def _verify_code_tree(track: dict[str, Any]) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-verify] code-tree {track['id']}: root {track['root']} not found")
        return 1
    print(f"[track-verify] code-tree {track['id']}: ok")
    return 0


_REMOVED_TYPES = {
    "docs-tree": "dir-tree",
    "spec-tree": "dir-tree",
}

DISPATCH = {
    "dir-tree": _verify_dir_tree,
    "repo-entry": _verify_repo_entry,
    "code-tree": _verify_code_tree,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track-id", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    track = _track_resolver.resolve(args.track_id)
    if track is None:
        return 0

    track_type = track["type"]
    handler = DISPATCH.get(track_type)

    if handler is None:
        if track_type in _REMOVED_TYPES:
            new_type = _REMOVED_TYPES[track_type]
            print(
                f"[track-verify] ERROR: type '{track_type}' has been removed. "
                f"Migrate registry.yaml to type: {new_type}",
                file=sys.stderr,
            )
            return 2
        print(f"[track-verify] warn: no dispatch for type {track_type!r}, skip")
        return 0
    return handler(track)


if __name__ == "__main__":
    sys.exit(main())
