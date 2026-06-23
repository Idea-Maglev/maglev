#!/usr/bin/env python3
"""
index_update.py — Bubble-up frontmatter update engine.

Takes file paths, walks up the index chain, recounts child_count and stats,
updates frontmatter, and optionally regenerates body tables (if table_columns defined).

Exit codes:
  0 — update completed
  1 — partial failure
  2 — script error
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path


class SafeEncoder(json.JSONEncoder):
    """Handle date/datetime objects in JSON output."""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

sys.path.insert(0, str(Path(__file__).parent))
from common.frontmatter import (
    parse_file,
    parse_any_frontmatter,
    write_frontmatter,
    get_nested,
)
from common.stats_dsl import evaluate_stats_schema
from common.logger import IndexLogger

try:
    import yaml
except ImportError:
    print("Error: pyyaml required.", file=sys.stderr)
    sys.exit(2)

SCRIPT_DIR = Path(__file__).parent
PROTOCOL_DIR = SCRIPT_DIR.parent
REGISTRY_PATH = PROTOCOL_DIR / "registry.yaml"


def find_repo_root() -> Path:
    current = PROTOCOL_DIR
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def load_registry(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def get_child_dirs(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(
        p for p in directory.iterdir()
        if p.is_dir() and not p.name.startswith(".")
        and p.name != "_meta"
    )


def get_child_files(directory: Path) -> list[Path]:
    """Get child .md files (excluding INDEX.md and README.md)."""
    if not directory.is_dir():
        return []
    return sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix == ".md"
        and p.name not in ("INDEX.md", "README.md")
        and not p.name.startswith(".")
    )


def count_leaf_files_recursive(directory: Path) -> int:
    """Recursively count all leaf .md files under directory.

    Excludes INDEX.md / README.md, dotfiles, and _meta/ subtree.
    See index-schema.md §6.5 and lifecycle.md §6.
    """
    if not directory.is_dir():
        return 0
    total = 0
    for p in directory.rglob("*.md"):
        if p.name in ("INDEX.md", "README.md"):
            continue
        rel_parts = p.relative_to(directory).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        if "_meta" in rel_parts:
            continue
        total += 1
    return total


def get_module_root_meta(repo_root: Path, registry: dict, directory: Path) -> dict:
    """Find the module root for a directory and return its metadata."""
    for mod in registry.get("modules", []):
        mod_path = repo_root / mod["root_path"]
        try:
            directory.relative_to(mod_path)
            root_index = repo_root / mod["root_index"]
            if root_index.exists():
                result = parse_file(root_index)
                if result.is_valid:
                    return result.metadata
            return {}
        except ValueError:
            continue
    return {}


def collect_children_metadata(directory: Path, child_type: str = "directory") -> list[dict]:
    """Collect frontmatter from direct children (dirs, files, or both)."""
    children = []
    if child_type in ("file", "mixed"):
        for child_file in get_child_files(directory):
            result = parse_any_frontmatter(child_file)
            meta = result.metadata
            meta["_dirname"] = child_file.stem
            meta["_path"] = str(child_file)
            children.append(meta)
    if child_type != "file":  # "directory", "mixed", or any other value → include dirs
        for child_dir in get_child_dirs(directory):
            # Try INDEX.md first, then README.md
            for fname in ["INDEX.md", "README.md"]:
                fpath = child_dir / fname
                if fpath.exists():
                    result = parse_any_frontmatter(fpath)
                    meta = result.metadata
                    meta["_dirname"] = child_dir.name
                    meta["_path"] = str(child_dir)
                    children.append(meta)
                    break
    return children


def compute_stats(
    directory: Path,
    stats_schema: dict,
    children_meta: list[dict],
) -> dict:
    """Compute stats values from children using stats_schema DSL.

    If children are entity-index nodes (partitions), aggregate from their
    stats instead of applying DSL rules. DSL rules only make sense when
    children are leaf entities (e.g., meeting files).

    Mixed-content collections (containing both leaf .md files AND
    sub-directories with their own INDEX.md) use recursive leaf counting
    for stats.total. See index-schema.md §6.5.
    """
    children_are_indexes = any(
        c.get("type") == "entity-index" or c.get("scope") in ("year", "month", "collection")
        for c in children_meta
    )

    has_sub_dirs = len(get_child_dirs(directory)) > 0
    has_leaf_files = len(get_child_files(directory)) > 0

    # Leaf-bearing collection (has direct leaf files, with or without sub-dirs):
    # use recursive leaf count for stats.total. See index-schema.md §6.5.
    if has_leaf_files:
        recursive_total = count_leaf_files_recursive(directory)
        if stats_schema:
            evaluated = evaluate_stats_schema(stats_schema, children_meta)
            evaluated["total"] = recursive_total
            return evaluated
        return {"total": recursive_total}

    if stats_schema and not children_are_indexes:
        return evaluate_stats_schema(stats_schema, children_meta)

    # Aggregate mode: sum children's stats (bubble-up) — but for root scope
    # over thinking-style modules, prefer recursive leaf count to capture
    # collections without an INDEX.md (see index-schema.md §6.5).
    child_indexes = [
        d / "INDEX.md" for d in get_child_dirs(directory) if (d / "INDEX.md").exists()
    ]
    if child_indexes:
        aggregated = {}
        for ci in child_indexes:
            result = parse_file(ci)
            if result.is_valid:
                # Skip children marked no_aggregate (e.g., series/)
                if result.metadata.get("no_aggregate"):
                    continue
                child_stats = result.metadata.get("stats", {})
                for key, val in child_stats.items():
                    if isinstance(val, (int, float)):
                        aggregated[key] = aggregated.get(key, 0) + val
        # Override total with full recursive leaf count when sub-dirs exist
        # without INDEX.md (otherwise stats.total under-reports).
        if has_sub_dirs:
            aggregated["total"] = count_leaf_files_recursive(directory)
        return aggregated if aggregated else {"total": count_leaf_files_recursive(directory)}
    else:
        # No child INDEX.md — count directories as leaf entities
        if stats_schema:
            return evaluate_stats_schema(stats_schema, children_meta)
        return {"total": len(get_child_dirs(directory))}


def generate_body_table(
    table_columns: list[dict],
    children_meta: list[dict],
    sort_key: str = "name",
    sort_order: str = "asc",
) -> str:
    """Generate markdown table from table_columns definition and children metadata."""
    FORMAT_HANDLERS = {
        "bool_emoji": lambda v: "✅" if v in (True, "true", "True") else "❌",
        "date_short": lambda v: str(v)[5:] if v and len(str(v)) >= 10 else str(v or ""),
    }

    # Sort children
    reverse = sort_order == "desc"
    children_meta.sort(
        key=lambda c: str(get_nested(c, sort_key, c.get("_dirname", ""))),
        reverse=reverse,
    )

    # Build header
    headers = [col["header"] for col in table_columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(":---" for _ in headers) + "|",
    ]

    # Build rows
    for idx, child in enumerate(children_meta):
        row = []
        for col in table_columns:
            source = col.get("source", "")
            fallback = col.get("fallback", "")
            fmt = col.get("format", "")

            if source.startswith("computed."):
                computed_name = source[len("computed."):]
                if computed_name == "row_number":
                    value = str(idx + 1)
                elif computed_name == "relative_link":
                    dirname = child.get("_dirname", "")
                    value = f"[→](./{dirname}/)"
                elif computed_name == "dirname":
                    value = child.get("_dirname", "")
                elif computed_name == "duration_display":
                    mins = get_nested(child, "duration_minutes")
                    value = f"{mins}min" if mins else fallback
                elif computed_name == "analysis_badge":
                    decisions = get_nested(child, "analysis.decisions")
                    value = "✅" if decisions else "⚪"
                elif computed_name == "child_scope":
                    value = str(get_nested(child, "scope", fallback))
                else:
                    value = fallback
            elif source.startswith("frontmatter."):
                field = source[len("frontmatter."):]
                value = get_nested(child, field)
                if value is None:
                    value = fallback
                else:
                    value = str(value)
            else:
                value = fallback

            # Apply format modifiers
            if fmt and value and value != fallback:
                if fmt in FORMAT_HANDLERS:
                    value = FORMAT_HANDLERS[fmt](value)
                elif fmt.startswith("truncate:"):
                    max_len = int(fmt.split(":")[1])
                    if len(str(value)) > max_len:
                        value = str(value)[:max_len] + "…"

            row.append(str(value))

        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def update_single_index(
    index_path: Path,
    repo_root: Path,
    module_root_meta: dict,
    dry_run: bool = False,
) -> dict:
    """Update a single INDEX.md file. Returns change dict."""
    result = parse_file(index_path)
    if not result.is_valid:
        return {"path": str(index_path.relative_to(repo_root)), "skipped": True, "reason": result.errors}

    meta = result.metadata
    directory = index_path.parent
    changes = {}

    # Determine child_type — per-index only, NOT inherited from module root
    # "file" = children are .md files, "mixed" = both dirs and files, default = dirs
    child_type = meta.get("child_type", "directory")

    # Recount child_count
    # Auto-detect: mixed = both sub-dirs and leaf files; else use child_type field
    # or derive from directory contents. See index-schema.md §6.5.
    has_sub_dirs = len(get_child_dirs(directory)) > 0
    has_leaf_files = len(get_child_files(directory)) > 0
    if has_sub_dirs and has_leaf_files:
        actual_child_count = len(get_child_dirs(directory)) + len(get_child_files(directory))
    elif child_type == "file" or (has_leaf_files and not has_sub_dirs):
        actual_child_count = len(get_child_files(directory))
    elif child_type == "mixed":
        actual_child_count = len(get_child_dirs(directory)) + len(get_child_files(directory))
    else:  # "directory" or any other value
        actual_child_count = len(get_child_dirs(directory))
    old_cc = meta.get("child_count", 0)
    if int(old_cc) != actual_child_count:
        changes["child_count"] = {"old": int(old_cc), "new": actual_child_count}
        meta["child_count"] = actual_child_count

    # Recompute stats
    children_meta = collect_children_metadata(directory, child_type)
    stats_schema = module_root_meta.get("stats_schema", meta.get("stats_schema", {}))
    new_stats = compute_stats(directory, stats_schema, children_meta)

    old_stats = meta.get("stats", {})
    for key, val in new_stats.items():
        if old_stats.get(key) != val:
            changes[f"stats.{key}"] = {"old": old_stats.get(key), "new": val}

    if new_stats:
        meta["stats"] = {**old_stats, **new_stats}

    # Update date
    today = date.today().isoformat()
    if meta.get("updated") != today:
        changes["updated"] = {"old": meta.get("updated"), "new": today}
        meta["updated"] = today

    # Body table
    body_table_needed = False
    table_columns_config = meta.get("table_columns") or module_root_meta.get("table_columns")

    # Determine scope-specific table_columns
    scope = meta.get("scope", "")
    if isinstance(table_columns_config, dict):
        # table_columns is scope-keyed: {month: [...], year: [...]}
        table_columns_config = table_columns_config.get(scope, table_columns_config.get("default"))
    elif isinstance(table_columns_config, list):
        pass  # Direct list
    else:
        table_columns_config = None

    if table_columns_config:
        sort_key = meta.get("sort_key", module_root_meta.get("sort_key", "name"))
        sort_order = meta.get("sort_order", module_root_meta.get("sort_order", "asc"))
        new_table = generate_body_table(table_columns_config, children_meta, sort_key, sort_order)

        # Reconstruct content with new table
        title = meta.get("entity_type", scope).title()
        stats_total = meta.get("stats", {}).get("total", 0)
        new_content = f"\n# {title}\n\n共 **{stats_total}** 个条目。\n\n## 索引\n\n{new_table}\n"
        body_table_needed = False
    else:
        new_content = result.content
        body_table_needed = True

    if not dry_run and changes:
        write_frontmatter(index_path, meta, new_content)

    output = {
        "path": str(index_path.relative_to(repo_root)),
        "changes": changes,
    }
    if body_table_needed and changes:
        output["body_table_needs_ai_update"] = True
    return output


def bubble_up(start_path: Path, repo_root: Path, registry: dict, dry_run: bool) -> list[dict]:
    """Walk up the index chain from start_path, updating each INDEX.md."""
    updates = []
    module_root_meta = get_module_root_meta(repo_root, registry, start_path)

    current = start_path if start_path.is_dir() else start_path.parent
    while True:
        index_path = current / "INDEX.md"
        if index_path.exists():
            update = update_single_index(index_path, repo_root, module_root_meta, dry_run)
            updates.append(update)

        # Check if we've reached module root
        result = parse_file(index_path) if index_path.exists() else None
        if result and result.is_valid and result.metadata.get("scope") == "root":
            break

        parent = current.parent
        if parent == current or parent == repo_root.parent:
            break
        current = parent

    return updates


def full_update(repo_root: Path, registry: dict, module_name: str, dry_run: bool) -> list[dict]:
    """Full update of all INDEX.md files in a module."""
    updates = []
    for mod in registry.get("modules", []):
        if mod["name"] != module_name:
            continue

        module_root_meta = {}
        root_index = repo_root / mod["root_index"]
        if root_index.exists():
            r = parse_file(root_index)
            if r.is_valid:
                module_root_meta = r.metadata

        module_path = repo_root / mod["root_path"]
        import os
        for root, dirs, files in os.walk(module_path):
            dirs[:] = sorted(d for d in dirs if not d.startswith("."))
            if "INDEX.md" in files:
                idx_path = Path(root) / "INDEX.md"
                update = update_single_index(idx_path, repo_root, module_root_meta, dry_run)
                updates.append(update)

    return updates


def main():
    parser = argparse.ArgumentParser(description="Index Protocol — Updater")
    parser.add_argument("--path", type=str, action="append", help="Path(s) to update from")
    parser.add_argument("--module", type=str, help="Full update for a module")
    parser.add_argument("--full", action="store_true", help="Full rescan (with --module)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only")
    parser.add_argument("--registry", type=str, default=None)
    args = parser.parse_args()

    logger = IndexLogger("update", args=sys.argv[1:])
    repo_root = find_repo_root()

    reg_path = Path(args.registry) if args.registry else REGISTRY_PATH
    registry = load_registry(reg_path)

    if not registry:
        print(json.dumps({"error": "Registry not found"}), file=sys.stderr)
        logger.finalize(exit_code=2)
        sys.exit(2)

    all_updates = []
    body_tables_needing_ai = []

    if args.module and args.full:
        all_updates = full_update(repo_root, registry, args.module, args.dry_run)
    elif args.path:
        for p in args.path:
            updates = bubble_up(repo_root / p, repo_root, registry, args.dry_run)
            all_updates.extend(updates)
    else:
        print("Error: specify --path or --module --full", file=sys.stderr)
        sys.exit(2)

    # Deduplicate by path
    seen = set()
    unique_updates = []
    for u in all_updates:
        if u["path"] not in seen:
            seen.add(u["path"])
            unique_updates.append(u)
            if u.get("body_table_needs_ai_update"):
                body_tables_needing_ai.append(u["path"])

    has_changes = any(u.get("changes") for u in unique_updates)

    output = {
        "timestamp": logger.timestamp,
        "dry_run": args.dry_run,
        "trigger_paths": args.path or [],
        "updates": unique_updates,
        "body_tables_needing_ai_update": body_tables_needing_ai,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False, cls=SafeEncoder))

    exit_code = 0
    summary = {
        "total_indexes_processed": len(unique_updates),
        "indexes_with_changes": sum(1 for u in unique_updates if u.get("changes")),
        "body_tables_needing_ai": len(body_tables_needing_ai),
    }

    log_path = logger.finalize(exit_code=exit_code, summary=summary)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
