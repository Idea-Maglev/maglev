#!/usr/bin/env python3
"""
index_verify.py — Index verification engine.

Implements L01-L07 local checks, X02-X03 global checks, and custom_checks.
Outputs JSON report with issues, health percentage, and fix hints.

Exit codes:
  0 — all checks passed
  1 — has error-level issues
  2 — script error
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common.frontmatter import parse_file, parse_any_frontmatter
from common.logger import IndexLogger

try:
    import yaml
except ImportError:
    print("Error: pyyaml required.", file=sys.stderr)
    sys.exit(2)

SCRIPT_DIR = Path(__file__).parent
PROTOCOL_DIR = SCRIPT_DIR.parent
REGISTRY_PATH = PROTOCOL_DIR / "registry.yaml"
FRESHNESS_DAYS = 14


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
    """Get direct child directories (excluding hidden, _meta)."""
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

    Excludes INDEX.md / README.md, dotfiles, and _meta/ subtree. Mirrors
    index_update.count_leaf_files_recursive. See lifecycle.md §6.
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


def get_child_count(directory: Path, child_type: str = "directory") -> int:
    """Get child count based on child_type.

    Auto-detects mixed: if directory has both sub-dirs and leaf files,
    sum both regardless of declared child_type. See index-schema.md §6.5.
    """
    has_sub_dirs = len(get_child_dirs(directory)) > 0
    has_leaf_files = len(get_child_files(directory)) > 0
    if has_sub_dirs and has_leaf_files:
        return len(get_child_dirs(directory)) + len(get_child_files(directory))
    if child_type == "file" or (has_leaf_files and not has_sub_dirs):
        return len(get_child_files(directory))
    if child_type == "mixed":
        return len(get_child_dirs(directory)) + len(get_child_files(directory))
    return len(get_child_dirs(directory))


def get_child_index_files(directory: Path) -> list[Path]:
    """Get INDEX.md files in direct child directories."""
    return [
        d / "INDEX.md" for d in get_child_dirs(directory) if (d / "INDEX.md").exists()
    ]


def find_index_nodes(repo_root: Path, module_root: str) -> list[Path]:
    """Recursively find all INDEX.md files under a module."""
    module_path = repo_root / module_root
    nodes = []
    for root, dirs, files in os.walk(module_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        if "INDEX.md" in files:
            nodes.append(Path(root) / "INDEX.md")
    return sorted(nodes)


# --- Check implementations ---

def check_L01(directory: Path, repo_root: Path) -> list[dict]:
    """L01: INDEX must exist for directories with >= 3 children."""
    issues = []
    child_dirs = get_child_dirs(directory)
    if len(child_dirs) >= 3 and not (directory / "INDEX.md").exists():
        issues.append({
            "id": "L01",
            "severity": "error",
            "path": str(directory.relative_to(repo_root)),
            "check": "INDEX 存在",
            "expected": "INDEX.md should exist (child_count >= 3)",
            "actual": "INDEX.md not found",
            "fix_hint": "generate_index",
        })
    return issues


def check_L02(index_path: Path, repo_root: Path) -> list[dict]:
    """L02: child_count matches actual children."""
    result = parse_file(index_path)
    if not result.is_valid:
        return []

    declared = result.metadata.get("child_count")
    if declared is None:
        return []

    parent_dir = index_path.parent
    child_type = result.metadata.get("child_type", "directory")
    actual = get_child_count(parent_dir, child_type)

    if int(declared) != actual:
        return [{
            "id": "L02",
            "severity": "error",
            "path": str(index_path.relative_to(repo_root)),
            "check": "child_count 一致",
            "expected": actual,
            "actual": int(declared),
            "fix_hint": "recount",
        }]
    return []


def check_L03(index_path: Path, repo_root: Path) -> list[dict]:
    """L03: stats.total is consistent."""
    result = parse_file(index_path)
    if not result.is_valid:
        return []

    meta = result.metadata
    stats = meta.get("stats", {})
    declared_total = stats.get("total")
    if declared_total is None:
        return []

    scope = meta.get("scope")
    parent_dir = index_path.parent

    # For bottom-level scopes (month, collection with leaf children),
    # total = recursive leaf count. For upper levels with INDEX.md children,
    # also use recursive count when sub-dirs exist (some sub-dirs may lack
    # their own INDEX.md). See index-schema.md §6.5.
    child_indexes = get_child_index_files(parent_dir)
    has_sub_dirs = len(get_child_dirs(parent_dir)) > 0
    has_leaf_files = len(get_child_files(parent_dir)) > 0

    # If this directory contains leaf files (with or without sub-dirs),
    # stats.total = recursive leaf count.
    if has_leaf_files:
        actual_total = count_leaf_files_recursive(parent_dir)
    elif child_indexes and has_sub_dirs:
        # Pure aggregator: sum children, but also account for sub-dirs
        # without INDEX.md via recursive leaf count override.
        actual_total = count_leaf_files_recursive(parent_dir)
    elif child_indexes:
        # Sum children's stats.total, respecting no_aggregate flag
        actual_total = 0
        for ci in child_indexes:
            cr = parse_file(ci)
            if cr.is_valid and not cr.metadata.get("no_aggregate"):
                actual_total += cr.metadata.get("stats", {}).get("total", 0)
    else:
        # Bottom level: count matching entities
        child_type = meta.get("child_type", "directory")
        entity_type = meta.get("entity_type")
        if child_type == "file":
            actual_total = get_child_count(parent_dir, child_type)
        elif child_type == "mixed":
            actual_total = get_child_count(parent_dir, "mixed")
        elif entity_type:
            # Count only child dirs whose frontmatter type matches entity_type
            count = 0
            for d in get_child_dirs(parent_dir):
                for fname in ["INDEX.md", "README.md"]:
                    fp = d / fname
                    if fp.exists():
                        cr = parse_any_frontmatter(fp)
                        if cr.metadata.get("type") == entity_type:
                            count += 1
                        break
            actual_total = count
        else:
            actual_total = get_child_count(parent_dir, child_type)

    if int(declared_total) != actual_total:
        return [{
            "id": "L03",
            "severity": "error",
            "path": str(index_path.relative_to(repo_root)),
            "check": "stats.total 一致",
            "expected": actual_total,
            "actual": int(declared_total),
            "fix_hint": "recount",
        }]
    return []


def check_L04(index_path: Path, repo_root: Path) -> list[dict]:
    """L04: bucket sum equals total (only for disjoint partition sets).

    Skips the check if stats_schema contains overlapping categories
    (i.e., non-partition buckets). Only triggers when explicitly
    complementary buckets are detected (e.g., field=='x' + field!='x').
    """
    result = parse_file(index_path)
    if not result.is_valid or not result.is_root:
        return []

    stats = result.metadata.get("stats", {})
    total = stats.get("total")
    if total is None:
        return []

    stats_schema = result.metadata.get("stats_schema", {})
    bucket_sum = 0
    bucket_names = []
    has_overlap_risk = False

    for name, schema in stats_schema.items():
        if name == "total":
            continue
        if isinstance(schema, dict) and schema.get("type") == "computed":
            continue
        # Check if bucket is marked as partition member
        if isinstance(schema, dict) and not schema.get("partition", False):
            has_overlap_risk = True
        val = stats.get(name)
        if isinstance(val, (int, float)):
            bucket_sum += int(val)
            bucket_names.append(name)

    # Skip L04 if buckets are likely overlapping (no partition markers)
    if has_overlap_risk:
        return []

    if bucket_names and bucket_sum != int(total):
        return [{
            "id": "L04",
            "severity": "error",
            "path": str(index_path.relative_to(repo_root)),
            "check": "分桶求和",
            "expected": f"sum({', '.join(bucket_names)}) == {int(total)}",
            "actual": bucket_sum,
            "fix_hint": "recount",
        }]
    return []


def check_L05(index_path: Path, repo_root: Path) -> list[dict]:
    """L05: body table row count matches expected."""
    result = parse_file(index_path)
    if not result.is_valid:
        return []

    content = result.content
    child_count = result.metadata.get("child_count", 0)

    # Count table rows (lines starting with |, excluding header and separator)
    import re
    table_lines = [
        line for line in content.split("\n")
        if line.strip().startswith("|") and not re.match(r"^\|[\s:-]+\|", line.strip())
    ]
    # Remove header row (first table row)
    data_rows = max(0, len(table_lines) - 1) if table_lines else 0

    if data_rows > 0 and data_rows != int(child_count):
        return [{
            "id": "L05",
            "severity": "warning",
            "path": str(index_path.relative_to(repo_root)),
            "check": "表格行数",
            "expected": int(child_count),
            "actual": data_rows,
            "fix_hint": "add_row" if data_rows < int(child_count) else "remove_row",
        }]
    return []


def check_L06(index_path: Path, repo_root: Path) -> list[dict]:
    """L06: all links in body table point to existing paths."""
    result = parse_file(index_path)
    if not result.is_valid:
        return []

    import re
    link_re = re.compile(r"\[.*?\]\((\./[^)]+)\)")
    issues = []

    for m in link_re.finditer(result.content):
        link_target = m.group(1)
        resolved = (index_path.parent / link_target).resolve()
        if not resolved.exists():
            issues.append({
                "id": "L06",
                "severity": "error",
                "path": str(index_path.relative_to(repo_root)),
                "check": "链接有效性",
                "expected": f"path exists: {link_target}",
                "actual": "not found",
                "fix_hint": "fix_link",
            })
    return issues


def check_L07(index_path: Path, repo_root: Path) -> list[dict]:
    """L07: updated field freshness."""
    result = parse_file(index_path)
    if not result.is_valid:
        return []

    updated_str = str(result.metadata.get("updated", ""))
    try:
        updated_date = datetime.strptime(updated_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return []

    # Check children modification times
    parent_dir = index_path.parent
    child_type = result.metadata.get("child_type", "directory")
    latest_child_mtime = None

    if child_type == "file":
        children = get_child_files(parent_dir)
    else:
        children = get_child_dirs(parent_dir)

    for child in children:
        mtime = datetime.fromtimestamp(child.stat().st_mtime)
        if latest_child_mtime is None or mtime > latest_child_mtime:
            latest_child_mtime = mtime

    if latest_child_mtime:
        threshold = latest_child_mtime - timedelta(days=FRESHNESS_DAYS)
        if updated_date < threshold:
            return [{
                "id": "L07",
                "severity": "warning",
                "path": str(index_path.relative_to(repo_root)),
                "check": "updated 新鲜度",
                "expected": f">= {threshold.strftime('%Y-%m-%d')}",
                "actual": updated_str,
                "fix_hint": "refresh_updated",
            }]
    return []


def check_L08(repo_root: Path, module_root: str) -> list[dict]:
    """L08 (warning): leaf frontmatter status field validation.

    See lifecycle.md §6 (3-state revision, 2026-04-27):
      - status field is optional (default = 'active')
      - if present, must be one of: active / crystallized / archived
      - position-status invariant:
          * 90_archive/* must be 'archived'
    """
    issues = []
    valid_statuses = {"active", "crystallized", "archived"}
    module_path = repo_root / module_root

    for p in module_path.rglob("*.md"):
        if p.name in ("INDEX.md", "README.md"):
            continue
        rel_parts = p.relative_to(module_path).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        # Skip _meta (no validation; machine-readable reserved area)
        if "_meta" in rel_parts:
            continue

        meta = parse_any_frontmatter(p).metadata
        status = meta.get("status")

        # Position invariant: 90_archive
        if "90_archive" in rel_parts:
            if status and status != "archived":
                issues.append({
                    "id": "L08",
                    "severity": "warning",
                    "path": str(p.relative_to(repo_root)),
                    "check": "status 字段位置不变量 (90_archive 应 archived)",
                    "expected": "archived",
                    "actual": status,
                    "fix_hint": "set_status_archived",
                })
            continue

        # Active segment: validate enum
        if status is not None and status not in valid_statuses:
            issues.append({
                "id": "L08",
                "severity": "warning",
                "path": str(p.relative_to(repo_root)),
                "check": "status 枚举",
                "expected": f"one of {sorted(valid_statuses)}",
                "actual": status,
                "fix_hint": "fix_status_enum",
            })

    return issues


def check_X02(repo_root: Path, module_root: str) -> list[dict]:
    """X02: no orphans — every leaf entity reachable from index chain."""
    issues = []
    module_path = repo_root / module_root

    # Collect all paths referenced in INDEX.md files
    indexed_dirs = set()
    for index_file in find_index_nodes(repo_root, module_root):
        parent = index_file.parent
        for child in get_child_dirs(parent):
            indexed_dirs.add(child)

    # Find actual leaf directories (no INDEX.md inside = leaf)
    for root, dirs, files in os.walk(module_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "_meta"]
        root_path = Path(root)
        if root_path == module_path:
            continue
        # Skip _meta subtree entirely
        rel_parts = root_path.relative_to(module_path).parts
        if "_meta" in rel_parts:
            continue
        # A directory is a potential leaf if it has README.md but no INDEX.md
        if "README.md" in files and "INDEX.md" not in files:
            if root_path not in indexed_dirs:
                issues.append({
                    "id": "X02",
                    "severity": "error",
                    "path": str(root_path.relative_to(repo_root)),
                    "check": "无孤儿",
                    "expected": "reachable from index chain",
                    "actual": "orphan (not indexed)",
                    "fix_hint": "manual",
                })
    return issues


def check_X03(repo_root: Path, module_root: str) -> list[dict]:
    """X03: no phantoms — every indexed path exists in filesystem."""
    import re
    issues = []

    for index_file in find_index_nodes(repo_root, module_root):
        result = parse_file(index_file)
        if not result.is_valid:
            continue

        link_re = re.compile(r"\[.*?\]\((\./[^)]+)\)")
        for m in link_re.finditer(result.content):
            link_target = m.group(1)
            resolved = (index_file.parent / link_target).resolve()
            if not resolved.exists():
                issues.append({
                    "id": "X03",
                    "severity": "error",
                    "path": str(index_file.relative_to(repo_root)),
                    "check": "无幽灵",
                    "expected": f"exists: {link_target}",
                    "actual": "phantom reference",
                    "fix_hint": "fix_link",
                })
    return issues


def load_module_checks():
    """Dynamically load module check functions from module_checks/ directory."""
    checks_dir = SCRIPT_DIR / "module_checks"
    registry = {}

    if not checks_dir.exists():
        return registry

    for py_file in checks_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        module_name = py_file.stem
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                f"module_checks.{module_name}", py_file
            )
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                # Register all check_* functions
                for attr_name in dir(mod):
                    if attr_name.startswith("check_"):
                        registry[attr_name] = getattr(mod, attr_name)
        except Exception:
            pass

    return registry


def main():
    parser = argparse.ArgumentParser(description="Index Protocol — Verifier")
    parser.add_argument("--module", type=str, help="Verify specific module only")
    parser.add_argument("--path", type=str, help="Verify specific path only")
    parser.add_argument("--level", choices=["local", "global"], default="global")
    parser.add_argument("--format", choices=["json", "summary", "full"], default="json")
    parser.add_argument("--check", type=str, help="Run specific check only (e.g., L02)")
    parser.add_argument("--registry", type=str, default=None)
    args = parser.parse_args()

    logger = IndexLogger("verify", args=sys.argv[1:])
    repo_root = find_repo_root()

    reg_path = Path(args.registry) if args.registry else REGISTRY_PATH
    registry = load_registry(reg_path)

    if not registry or "modules" not in registry:
        print(json.dumps({"error": f"Registry not found: {reg_path}"}), file=sys.stderr)
        logger.finalize(exit_code=2)
        sys.exit(2)

    # Filter modules
    modules = registry["modules"]
    if args.module:
        modules = [m for m in modules if m["name"] == args.module]

    all_issues = []
    all_passed = []
    nodes_checked = 0

    for mod in modules:
        mgmt = mod.get("management_level", "managed")
        if mgmt == "bootstrap":
            continue

        module_root = mod["root_path"]

        if args.path:
            # Single path mode
            index_path = repo_root / args.path / "INDEX.md"
            if not index_path.exists():
                index_path = repo_root / args.path
            index_nodes = [index_path] if index_path.exists() else []
        else:
            index_nodes = find_index_nodes(repo_root, module_root)

        for index_path in index_nodes:
            nodes_checked += 1
            node_checks = {}

            # Run local checks
            checks_to_run = [
                ("L01", lambda ip=index_path: check_L01(ip.parent, repo_root)),
                ("L02", lambda ip=index_path: check_L02(ip, repo_root)),
                ("L03", lambda ip=index_path: check_L03(ip, repo_root)),
                ("L04", lambda ip=index_path: check_L04(ip, repo_root)),
                ("L05", lambda ip=index_path: check_L05(ip, repo_root)),
                ("L06", lambda ip=index_path: check_L06(ip, repo_root)),
                ("L07", lambda ip=index_path: check_L07(ip, repo_root)),
            ]

            if args.check:
                checks_to_run = [(cid, fn) for cid, fn in checks_to_run if cid == args.check]

            for check_id, check_fn in checks_to_run:
                issues = check_fn()
                if issues:
                    all_issues.extend(issues)
                    node_checks[check_id] = {"status": "fail"}
                else:
                    all_passed.append({
                        "id": check_id,
                        "path": str(index_path.relative_to(repo_root)),
                        "check": check_id,
                    })
                    node_checks[check_id] = {"status": "pass"}

            logger.add_execution(
                str(index_path.relative_to(repo_root)), node_checks
            )

        # Global checks
        if args.level == "global" and not args.path:
            all_issues.extend(check_X02(repo_root, module_root))
            all_issues.extend(check_X03(repo_root, module_root))
            if not args.check or args.check == "L08":
                all_issues.extend(check_L08(repo_root, module_root))

    # Custom checks
    if args.level == "global" and not args.check:
        custom_check_fns = load_module_checks()
        for mod in modules:
            root_index = repo_root / mod["root_index"]
            if not root_index.exists():
                continue
            result = parse_file(root_index)
            if not result.is_valid:
                continue
            for cc in result.metadata.get("custom_checks", []):
                fn_name = cc.get("script_function")
                if fn_name and fn_name in custom_check_fns:
                    try:
                        custom_issues = custom_check_fns[fn_name](
                            str(repo_root / mod["root_path"]),
                            {"repo_root": str(repo_root)},
                        )
                        all_issues.extend(custom_issues or [])
                    except Exception:
                        pass

    # Compute results
    errors = sum(1 for i in all_issues if i.get("severity") == "error")
    warnings = sum(1 for i in all_issues if i.get("severity") == "warning")
    passed = nodes_checked * 7 - len(all_issues)  # approximate
    health_pct = int((passed / max(passed + len(all_issues), 1)) * 100)

    summary = {
        "nodes_checked": nodes_checked,
        "passed": passed,
        "failed": errors,
        "warnings": warnings,
        "health_pct": health_pct,
    }

    exit_code = 1 if errors > 0 else 0

    output = {
        "timestamp": logger.timestamp,
        "scope": {
            "modules": [m["name"] for m in modules],
            "level": args.level,
        },
        "nodes_checked": nodes_checked,
        "results": summary,
        "issues": all_issues,
        "passed_checks": all_passed[:20],  # Truncate for readability
    }

    if args.format in ("json", "full"):
        print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.format in ("summary", "full"):
        print(f"\n🔍 索引验证报告 ({logger.timestamp})")
        print(f"   健康度: {'🟢' if exit_code == 0 else '🔴'} {health_pct}% ({passed} passed, {errors} errors, {warnings} warnings)")
        if all_issues:
            print(f"\n| # | 位置 | 检查项 | 问题 | 修复 |")
            print(f"|:---|:---|:---|:---|:---|")
            for i, issue in enumerate(all_issues, 1):
                print(f"| {i} | {issue['path']} | {issue['id']} | {issue.get('check', '')} | {issue.get('fix_hint', '')} |")

    log_path = logger.finalize(exit_code=exit_code, summary=summary)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
