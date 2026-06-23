"""
index_gen.py — Shared INDEX.md generation utilities for dir-tree type.

Provides directory discovery, child counting, and INDEX.md creation/update
functions used by track_scan (dir-tree) and potentially index_update.

Design authority: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path
from typing import Any

from .frontmatter import parse_file, parse_any_frontmatter, write_frontmatter


# ─── Directory Discovery ─────────────────────────────────────────────

def discover_indexable_dirs(
    root_dir: Path,
    ignore: set[str],
    max_depth: int,
) -> list[Path]:
    """Recursively find all directories that should get an INDEX.md.

    Returns list sorted deepest-first (bottom-up) for safe processing.
    Root dir itself is included (last in the returned list after reversing).
    """
    results: list[Path] = []

    def _walk(current: Path, depth: int) -> None:
        results.append(current)
        if depth >= max_depth:
            return
        for child in sorted(current.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith("."):
                continue
            if child.name in ignore:
                continue
            _walk(child, depth + 1)

    if root_dir.is_dir():
        _walk(root_dir, 0)

    # Return bottom-up (deepest dirs first) so children are processed before parents
    results.reverse()
    return results


# ─── Child Type Detection ─────────────────────────────────────────────

def detect_child_type(directory: Path, ignore: set[str]) -> str:
    """Auto-detect child type: 'file', 'directory', or 'mixed'."""
    has_dirs = False
    has_files = False
    for child in directory.iterdir():
        if child.name.startswith("."):
            continue
        if child.name in ignore:
            continue
        if child.name in ("INDEX.md", "README.md"):
            continue
        if child.is_dir():
            has_dirs = True
        elif child.is_file():
            has_files = True
        if has_dirs and has_files:
            return "mixed"
    if has_dirs and not has_files:
        return "directory"
    if has_files and not has_dirs:
        return "file"
    return "mixed" if (has_dirs or has_files) else "directory"


# ─── Counting ─────────────────────────────────────────────────────────

def count_children(directory: Path, child_type: str, ignore: set[str]) -> int:
    """Count direct children based on child_type."""
    count = 0
    for child in directory.iterdir():
        if child.name.startswith("."):
            continue
        if child.name in ignore:
            continue
        if child.name in ("INDEX.md", "README.md"):
            continue
        if child_type == "file" and child.is_file():
            count += 1
        elif child_type == "directory" and child.is_dir():
            count += 1
        elif child_type == "mixed":
            if child.is_file() or child.is_dir():
                count += 1
    return count


def recursive_leaf_count(directory: Path, ignore: set[str]) -> int:
    """Recursively count all leaf files (non-INDEX, non-README, non-dotfile)."""
    total = 0
    for root, dirs, files in os.walk(directory):
        # Filter dirs in-place
        dirs[:] = [
            d for d in sorted(dirs)
            if not d.startswith(".") and d not in ignore
        ]
        for f in files:
            if f.startswith("."):
                continue
            if f in ("INDEX.md", "README.md"):
                continue
            total += 1
    return total


# ─── INDEX.md Generation / Update ────────────────────────────────────

def generate_or_update_index(
    dir_path: Path,
    root_dir: Path,
    entity_type: str,
    child_type_cfg: str,
    ignore: set[str],
) -> bool:
    """Generate new or update existing INDEX.md for a directory.

    Returns True if file was written/modified, False if skipped.
    """
    index_path = dir_path / "INDEX.md"

    # Resolve effective child_type
    if child_type_cfg == "auto":
        effective_child_type = detect_child_type(dir_path, ignore)
    else:
        effective_child_type = child_type_cfg

    child_count = count_children(dir_path, effective_child_type, ignore)
    total = recursive_leaf_count(dir_path, ignore)
    today = date.today().isoformat()

    if index_path.exists():
        # UPDATE mode: only touch child_count, stats.total, updated
        result = parse_any_frontmatter(index_path)
        meta = result.metadata

        if not meta:
            # File exists but no frontmatter — add minimal frontmatter, preserve body
            scope = "root" if dir_path == root_dir else "collection"
            meta = {
                "type": "entity-index",
                "scope": scope,
                "entity_type": entity_type,
                "child_count": child_count,
                "child_type": effective_child_type,
                "stats": {"total": total},
                "updated": today,
            }
            # Preserve original body content
            body = result.content if result.content else ""
            write_frontmatter(index_path, meta, body)
            return True

        meta["child_count"] = child_count
        if "stats" not in meta or not isinstance(meta["stats"], dict):
            meta["stats"] = {}
        meta["stats"]["total"] = total
        meta["updated"] = today

        # Preserve body content entirely
        write_frontmatter(index_path, meta, result.content)
        return True
    else:
        # CREATE mode: minimal frontmatter + default body
        scope = "root" if dir_path == root_dir else "collection"
        meta: dict[str, Any] = {
            "type": "entity-index",
            "scope": scope,
            "entity_type": entity_type,
            "child_count": child_count,
            "child_type": effective_child_type,
            "stats": {"total": total},
            "updated": today,
        }

        body = _generate_default_body(dir_path, ignore, effective_child_type)
        write_frontmatter(index_path, meta, body)
        return True


def _generate_default_body(
    directory: Path,
    ignore: set[str],
    child_type: str,
) -> str:
    """Generate a simple default body listing children as links."""
    lines: list[str] = []
    lines.append(f"\n# {directory.name}\n")

    children: list[tuple[str, bool]] = []  # (name, is_dir)
    for child in sorted(directory.iterdir()):
        if child.name.startswith("."):
            continue
        if child.name in ignore:
            continue
        if child.name in ("INDEX.md", "README.md"):
            continue
        if child.is_dir():
            children.append((child.name, True))
        elif child.is_file() and child_type in ("file", "mixed"):
            children.append((child.name, False))

    if children:
        lines.append("")
        lines.append("| 名称 | 类型 |")
        lines.append("|:---|:---|")
        for name, is_dir in children:
            if is_dir:
                lines.append(f"| [{name}](./{name}/) | 📁 |")
            else:
                lines.append(f"| [{name}](./{name}) | 📄 |")
    else:
        lines.append("\n（空目录）\n")

    lines.append("")
    return "\n".join(lines)


# ─── Summary YAML ────────────────────────────────────────────────────

def build_summary(
    track: dict[str, Any],
    root_dir: Path,
    repo_root: Path,
    dirs: list[Path],
) -> dict[str, Any]:
    """Build summary YAML data for the track output file."""
    items: list[dict[str, Any]] = []
    for d in dirs:
        rel = d.relative_to(repo_root).as_posix()
        index_exists = (d / "INDEX.md").exists()
        items.append({
            "path": rel,
            "has_index": index_exists,
        })

    return {
        "track_id": track["id"],
        "track_type": track["type"],
        "root": track["root"],
        "dir_count": len(dirs),
        "items": items,
    }
