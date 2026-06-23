#!/usr/bin/env python3
"""
index_scan.py — Registry health check.

Reads registry.yaml, checks each module's path existence and protocol declarations.
Outputs a JSON module map.

Exit codes:
  0 — all modules healthy
  1 — some modules have issues
  2 — script error (registry not found)
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent to path for common imports
sys.path.insert(0, str(Path(__file__).parent))
from common.frontmatter import parse_file, parse_any_frontmatter
from common.logger import IndexLogger

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

SCRIPT_DIR = Path(__file__).parent
PROTOCOL_DIR = SCRIPT_DIR.parent
REGISTRY_PATH = PROTOCOL_DIR / "registry.yaml"


def find_repo_root() -> Path:
    """Walk up from script location to find .git directory."""
    current = PROTOCOL_DIR
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def load_registry(registry_path: Path) -> dict:
    """Load and parse registry.yaml."""
    if not registry_path.exists():
        return {}
    text = registry_path.read_text(encoding="utf-8")
    return yaml.safe_load(text) or {}


def scan_module(repo_root: Path, module: dict) -> dict:
    """Scan a single module for health status."""
    name = module["name"]
    root_path = repo_root / module["root_path"]
    root_index = repo_root / module["root_index"]
    issues = []

    # Check path existence
    if not root_path.exists():
        return {
            "name": name,
            "root_path": module["root_path"],
            "root_index": module["root_index"],
            "management_level": module.get("management_level", "unknown"),
            "status": "missing",
            "issues": [f"Module directory not found: {module['root_path']}"],
        }

    # Check root index existence
    if not root_index.exists():
        issues.append(f"Root index not found: {module['root_index']}")

    # If index exists, check protocol declarations
    if root_index.exists():
        result = parse_file(root_index)
        if not result.is_valid:
            issues.extend(result.errors)
        else:
            meta = result.metadata
            if "index_protocol_version" not in meta:
                issues.append("Missing index_protocol_version")
            if "stats_schema" not in meta:
                issues.append("Missing stats_schema")
    elif (root_path / "README.md").exists():
        # Fallback: check README.md for protocol compatibility
        readme = parse_any_frontmatter(root_path / "README.md")
        if readme.metadata.get("type") != "entity-index":
            issues.append("README.md type is not entity-index (migration needed)")
        if "index_protocol_version" not in readme.metadata:
            issues.append("Missing index_protocol_version in README.md")

    # Determine status
    mgmt = module.get("management_level", "managed")
    if mgmt == "bootstrap":
        status = "bootstrap"
    elif not issues:
        status = "ready"
    else:
        status = "incomplete"

    return {
        "name": name,
        "root_path": module["root_path"],
        "root_index": module["root_index"],
        "management_level": mgmt,
        "entity_type": module.get("entity_type", ""),
        "status": status,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description="Index Protocol — Module Scanner")
    parser.add_argument(
        "--format",
        choices=["json", "summary"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--registry",
        type=str,
        default=None,
        help="Override registry.yaml path",
    )
    args = parser.parse_args()

    logger = IndexLogger("scan", args=sys.argv[1:])

    # Load registry
    reg_path = Path(args.registry) if args.registry else REGISTRY_PATH
    registry = load_registry(reg_path)

    if not registry or "modules" not in registry:
        print(
            json.dumps({"error": f"Registry not found or empty: {reg_path}"}),
            file=sys.stderr,
        )
        logger.finalize(exit_code=2, summary={"error": "registry_not_found"})
        sys.exit(2)

    repo_root = find_repo_root()
    modules_config = registry["modules"]
    logger.set_input(
        registry_path=str(reg_path),
        protocol_version=registry.get("protocol_version", "unknown"),
        modules_count=len(modules_config),
    )

    # Scan each module
    results = []
    for mod in modules_config:
        result = scan_module(repo_root, mod)
        results.append(result)
        logger.add_execution(mod["name"], {"status": result["status"], "issues": result["issues"]})

    # Compute summary
    total = len(results)
    ready = sum(1 for r in results if r["status"] == "ready")
    incomplete = sum(1 for r in results if r["status"] == "incomplete")
    missing = sum(1 for r in results if r["status"] == "missing")
    bootstrap = sum(1 for r in results if r["status"] == "bootstrap")

    summary = {
        "total": total,
        "ready": ready,
        "incomplete": incomplete,
        "missing": missing,
        "bootstrap": bootstrap,
    }

    exit_code = 0 if (incomplete == 0 and missing == 0) else 1

    output = {
        "timestamp": logger.timestamp,
        "registry_path": str(reg_path),
        "protocol_version": registry.get("protocol_version", "1.0"),
        "modules": results,
        "summary": summary,
    }

    if args.format == "json":
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        # Summary format
        print(f"\n📊 模块扫描结果 ({logger.timestamp})\n")
        print(f"| 模块 | 状态 | 说明 |")
        print(f"|:---|:---|:---|")
        status_icons = {"ready": "🟢", "incomplete": "🔴", "missing": "⚫", "bootstrap": "🟡"}
        for r in results:
            icon = status_icons.get(r["status"], "❓")
            desc = "; ".join(r["issues"]) if r["issues"] else "协议已就绪"
            print(f"| {r['name']}/ | {icon} {r['status']} | {desc} |")
        print(f"\n共 {total} 个模块: {ready} ready, {incomplete} incomplete, {bootstrap} bootstrap, {missing} missing")

    log_path = logger.finalize(exit_code=exit_code, summary=summary)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
