#!/usr/bin/env python3
"""Public Maglev release builder.

Builds a local release payload in `.maglev_build/` and mirrors it into
`packages/maglev-cli/dist/` for npm packaging. This public builder does not
push git branches, create tags, or publish to npm.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / ".maglev_build"
NPM_DIST_DIR = ROOT / "packages/maglev-cli/dist"
VERSION_FILE = ROOT / "release.version.json"
CLI_PACKAGE_FILE = ROOT / "packages/maglev-cli/package.json"
VERSION_MANAGER = ROOT / "scripts/maglev_version.py"
CATALOG = ROOT / ".agents/private-catalog.yaml"
PUBLIC_REGISTRY = "https://registry.npmjs.org/"
PUBLIC_PACKAGE = "@idea-maglev/maglev-cli"
PUBLIC_PACKAGE_FILES = ["README.md", "bin/", "dist/"]

MAGLEV_WHITELIST = ["rules/", "protocols/", "knowledge_base/", "config/core_rules.md"]
PROTOCOL_ROOT = ".agents/skills/_internal"
EXCLUDE_DIR_NAMES = {".git", "__pycache__", ".pytest_cache", "node_modules"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".DS_Store"}
DIST_EXCLUDE_SCOPES = {"private", "private_only", "external_optional"}
DIST_REQUIRED_SKILL_SCOPES = {"user_visible", "runtime_internal"}
CATALOG_KEEP_SCOPES = {"user_visible"}
TEXT_EXTENSIONS = {".json", ".md", ".py", ".sh", ".txt", ".yaml", ".yml"}
# Hex markers keep public source free of recognizable private endpoints/scopes
# while still letting the release gate block them in generated npm dist files.
DIST_FORBIDDEN_MARKER_HEX = [
    "6769742e6e6576696e742e636f6d",
    "6e6576696e74",
    "6e706d6d6972726f72",
    "6e696f696e74",
    "5f61757468546f6b656e",
    "406e696f2d66652f",
]
DIST_FORBIDDEN_TEXT_PATTERNS = [
    re.compile(
        "|".join(re.escape(bytes.fromhex(marker).decode("ascii")) for marker in DIST_FORBIDDEN_MARKER_HEX),
        re.I,
    )
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_version() -> str:
    if not VERSION_FILE.exists():
        raise SystemExit("missing release.version.json")
    version = str(read_json(VERSION_FILE).get("version", ""))
    if not version:
        raise SystemExit("release.version.json missing version")
    package = read_json(CLI_PACKAGE_FILE)
    if package.get("name") != PUBLIC_PACKAGE:
        raise SystemExit(f"unexpected package name: {package.get('name')}")
    if package.get("version") != version:
        raise SystemExit(
            f"version mismatch: release.version.json={version}, package.json={package.get('version')}"
        )
    return version


def verify_public_package_metadata() -> None:
    package = read_json(CLI_PACKAGE_FILE)
    expected_publish_config = {"registry": PUBLIC_REGISTRY, "access": "public"}
    if package.get("name") != PUBLIC_PACKAGE:
        raise SystemExit(f"unexpected package name: {package.get('name')}")
    if package.get("publishConfig") != expected_publish_config:
        raise SystemExit(
            "package publishConfig must be "
            + json.dumps(expected_publish_config, sort_keys=True)
        )
    if package.get("files") != PUBLIC_PACKAGE_FILES:
        raise SystemExit(f"package files must be {PUBLIC_PACKAGE_FILES}")


def run_version_check() -> None:
    result = subprocess.run(
        [sys.executable, str(VERSION_MANAGER), "check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode:
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
        raise SystemExit(result.returncode)


def extract_catalog_entries(catalog: Any) -> List[Dict]:
    """Match the private release compiler's catalog entry extraction."""
    if isinstance(catalog, list):
        return [e for e in catalog if isinstance(e, dict) and "name" in e]
    if isinstance(catalog, dict):
        for key in ("skills", "objects", "entries", "items"):
            value = catalog.get(key)
            if isinstance(value, list):
                return [e for e in value if isinstance(e, dict) and "name" in e]
        for value in catalog.values():
            if isinstance(value, list) and value and isinstance(value[0], dict) and "name" in value[0]:
                return [e for e in value if isinstance(e, dict) and "name" in e]
    return []


def rebuild_catalog_with_entries(source_catalog: Any, entries: List[Dict]) -> Any:
    if isinstance(source_catalog, list):
        return entries
    if isinstance(source_catalog, dict):
        for key in ("skills", "objects", "entries", "items"):
            if isinstance(source_catalog.get(key), list):
                output = dict(source_catalog)
                output[key] = entries
                return output
        for key, value in source_catalog.items():
            if isinstance(value, list) and value and isinstance(value[0], dict) and "name" in value[0]:
                output = dict(source_catalog)
                output[key] = entries
                return output
    return entries


def load_catalog() -> Any:
    if not CATALOG.exists():
        return {}
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    return yaml.safe_load(CATALOG.read_text(encoding="utf-8")) or {}


def parse_catalog_blocks() -> Tuple[List[Dict], Set[str]]:
    catalog = load_catalog()
    if catalog is None:
        raise SystemExit("PyYAML is required to parse .agents/private-catalog.yaml")
    entries = extract_catalog_entries(catalog)
    hidden_paths = {
        str(entry["path"]).rstrip("/")
        for entry in entries
        if entry.get("distribution_scope") in DIST_EXCLUDE_SCOPES
        and str(entry.get("path", "")).startswith(".agents/")
    }
    return entries, hidden_paths


def render_public_catalog() -> str:
    catalog = load_catalog()
    if catalog is None:
        raise SystemExit("PyYAML is required to render the public catalog")
    entries = extract_catalog_entries(catalog)
    hidden_names = {entry.get("name") for entry in entries if entry.get("distribution_scope") != "user_visible"}
    cleaned = []
    for entry in entries:
        if entry.get("distribution_scope") != "user_visible":
            continue
        projected = dict(entry)
        relations = projected.get("relations") or []
        if isinstance(relations, list):
            kept = [rel for rel in relations if not (isinstance(rel, dict) and rel.get("target") in hidden_names)]
            if kept != relations:
                projected["relations"] = kept
        cleaned.append(projected)
    output = rebuild_catalog_with_entries(catalog, cleaned)
    try:
        import yaml  # type: ignore
    except ImportError:
        raise SystemExit("PyYAML is required to render the public catalog")
    header = (
        "# Auto-generated by maglev_release.py public catalog split\n"
        "# Source: .agents/private-catalog.yaml\n"
        "# Contains user_visible entries only.\n\n"
    )
    return header + yaml.safe_dump(output, allow_unicode=True, sort_keys=False)


def should_skip_source(path: Path, hidden_paths: Set[str]) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIR_NAMES:
        return True
    if path.name in EXCLUDE_SUFFIXES or any(path.name.endswith(s) for s in EXCLUDE_SUFFIXES):
        return True
    rel_path = rel(path)
    for hidden in hidden_paths:
        if rel_path == hidden or rel_path.startswith(hidden + "/"):
            return True
    return False


def copy_tree_filtered(src_root: Path, dst_root: Path, hidden_paths: Set[str]) -> None:
    for src in src_root.rglob("*"):
        if not src.is_file():
            continue
        if should_skip_source(src, hidden_paths):
            continue
        copy_file(src, dst_root / src.relative_to(src_root))


def is_public_workflow(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:15]
    except OSError:
        return True
    return not any("distribution:" in line and "private" in line.lower() for line in head)


def public_skill_paths(entries: List[Dict]) -> List[Path]:
    paths = []
    for entry in entries:
        if entry.get("object_kind") != "skill":
            continue
        if entry.get("status", "active") != "active":
            continue
        if entry.get("distribution_scope") != "user_visible":
            continue
        path = ROOT / str(entry.get("path", "")).rstrip("/")
        if path.is_dir():
            paths.append(path)
    return paths


def runtime_internal_paths(entries: List[Dict]) -> List[Path]:
    paths = []
    seen = set()
    for entry in entries:
        if entry.get("distribution_scope") != "runtime_internal":
            continue
        if entry.get("status") == "deprecated":
            continue
        if entry.get("runtime_distribution") is False:
            continue
        raw_path = str(entry.get("path", "")).rstrip("/")
        if not raw_path or raw_path in seen:
            continue
        path = ROOT / raw_path
        if path.exists():
            paths.append(path)
            seen.add(raw_path)
    return paths


def public_workflow_paths() -> List[Path]:
    workflow_root = ROOT / ".agents/workflows"
    if not workflow_root.exists():
        return []
    return sorted(path for path in workflow_root.iterdir() if path.is_file() and path.suffix == ".md" and is_public_workflow(path))


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def build_payload(version: str) -> List[Dict]:
    entries, hidden_paths = parse_catalog_blocks()
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)

    # Mirror the private release compiler: assemble explicit runtime assets, not
    # broad repository roots. Public projection only changes visibility/sanitizing.
    for skill_path in public_skill_paths(entries):
        copy_tree_filtered(skill_path, BUILD_DIR / rel(skill_path), hidden_paths)

    for workflow_path in public_workflow_paths():
        copy_file(workflow_path, BUILD_DIR / rel(workflow_path))

    for whitelist_item in MAGLEV_WHITELIST:
        src = ROOT / ".maglev" / whitelist_item
        dst = BUILD_DIR / ".maglev" / whitelist_item
        if src.is_dir():
            copy_tree_filtered(src, dst, hidden_paths)
        elif src.is_file() and not should_skip_source(src, hidden_paths):
            copy_file(src, dst)

    for runtime_path in runtime_internal_paths(entries):
        dst = BUILD_DIR / rel(runtime_path)
        if runtime_path.is_dir():
            copy_tree_filtered(runtime_path, dst, hidden_paths)
        elif runtime_path.is_file() and not should_skip_source(runtime_path, hidden_paths):
            copy_file(runtime_path, dst)

    protocol_root = ROOT / PROTOCOL_ROOT
    if protocol_root.is_dir():
        copy_tree_filtered(protocol_root, BUILD_DIR / PROTOCOL_ROOT, set())

    if entries:
        catalog_out = BUILD_DIR / ".agents/private-catalog.yaml"
        catalog_out.parent.mkdir(parents=True, exist_ok=True)
        catalog_out.write_text(render_public_catalog(), encoding="utf-8")

    for runtime_name in ["maglev_installer.py", "install.sh"]:
        src = ROOT / "packages/maglev-cli/runtime-src" / runtime_name
        if src.exists():
            copy_file(src, BUILD_DIR / runtime_name)

    changelog = BUILD_DIR / "CHANGELOG.md"
    changelog.write_text(
        f"# Maglev {version}\n\nPublic release payload generated at {datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )

    files = []
    for path in sorted(BUILD_DIR.rglob("*")):
        if not path.is_file() or path.name == "manifest.json":
            continue
        files.append({"path": rel(path.relative_to(BUILD_DIR) if False else path), "sha256": sha256(path)})

    # Convert paths from repository-relative to payload-relative.
    payload_files = []
    for path in sorted(BUILD_DIR.rglob("*")):
        if not path.is_file() or path.name == "manifest.json":
            continue
        payload_files.append({"path": path.relative_to(BUILD_DIR).as_posix(), "sha256": sha256(path)})

    manifest = {
        "version": version,
        "package": PUBLIC_PACKAGE,
        "registry": PUBLIC_REGISTRY,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "files": payload_files,
    }
    write_json(BUILD_DIR / "manifest.json", manifest)
    return payload_files


def sync_npm_dist() -> None:
    if NPM_DIST_DIR.exists():
        shutil.rmtree(NPM_DIST_DIR)
    shutil.copytree(BUILD_DIR, NPM_DIST_DIR, ignore=shutil.ignore_patterns(".git"))


def scan_dist_for_forbidden_text() -> List[str]:
    hits = []
    for path in NPM_DIST_DIR.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
            continue
        rel_path = path.relative_to(NPM_DIST_DIR).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), 1):
            for pattern in DIST_FORBIDDEN_TEXT_PATTERNS:
                match = pattern.search(line)
                if match:
                    hits.append(f"{rel_path}:{line_no}:{match.group(0)}")
    return hits


def verify_npm_dist(version: str) -> None:
    manifest = NPM_DIST_DIR / "manifest.json"
    installer = NPM_DIST_DIR / "maglev_installer.py"
    if not manifest.exists():
        raise SystemExit("packages/maglev-cli/dist/manifest.json missing")
    if not installer.exists():
        raise SystemExit("packages/maglev-cli/dist/maglev_installer.py missing")
    data = read_json(manifest)
    if data.get("version") != version:
        raise SystemExit(f"dist manifest version mismatch: {data.get('version')} != {version}")
    entries, hidden_paths = parse_catalog_blocks()
    manifest_paths = {item.get("path", "") for item in data.get("files", [])}
    blocked_paths = []
    for path in manifest_paths:
        for hidden in hidden_paths:
            if path == hidden or path.startswith(hidden + "/"):
                blocked_paths.append(path)
                break
    if blocked_paths:
        sample = ", ".join(blocked_paths[:5])
        raise SystemExit(f"public dist contains private paths: {sample}")
    if not any(path.startswith(".agents/skills/_internal/") for path in manifest_paths):
        raise SystemExit("public dist missing required protocol root: .agents/skills/_internal/")
    for blocked_root in ("docs/", "specs/", "issues/"):
        if any(path.startswith(blocked_root) for path in manifest_paths):
            raise SystemExit(f"public dist unexpectedly contains repository root payload: {blocked_root}")
    missing_skills = []
    for entry in entries:
        if entry.get("object_kind") != "skill":
            continue
        if entry.get("status", "active") != "active":
            continue
        if entry.get("distribution_scope") not in DIST_REQUIRED_SKILL_SCOPES:
            continue
        skill_path = entry.get("path", "").rstrip("/")
        if not skill_path.startswith(".agents/skills/"):
            continue
        expected = f"{skill_path}/SKILL.md"
        if expected not in manifest_paths:
            missing_skills.append(expected)
    if missing_skills:
        sample = ", ".join(missing_skills[:8])
        raise SystemExit(f"public dist missing required runtime skills: {sample}")
    forbidden_text_hits = scan_dist_for_forbidden_text()
    if forbidden_text_hits:
        sample = ", ".join(forbidden_text_hits[:8])
        raise SystemExit(f"public dist contains private registry or upstream text: {sample}")


def build(args: argparse.Namespace) -> int:
    version = load_version()
    verify_public_package_metadata()
    run_version_check()
    payload_files = build_payload(version)
    sync_npm_dist()
    verify_npm_dist(version)
    print(f"Built Maglev {version}: {len(payload_files)} files")
    print(f"- {rel(BUILD_DIR / 'manifest.json')}")
    print(f"- {rel(NPM_DIST_DIR / 'manifest.json')}")
    if args.dry_run:
        print("Dry-run completed locally; no git push, tag, or npm publish was performed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build public Maglev release payload")
    parser.add_argument("--dry-run", action="store_true", help="build local payload only")
    parser.add_argument("--skip-audit", action="store_true", help="accepted for compatibility; no-op")
    parser.add_argument("--version", help="expected version; must match release.version.json")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    version = load_version()
    if args.version and args.version != version:
        print(f"ERROR: --version={args.version} does not match release.version.json={version}")
        return 1
    return build(args)


if __name__ == "__main__":
    sys.exit(main())
