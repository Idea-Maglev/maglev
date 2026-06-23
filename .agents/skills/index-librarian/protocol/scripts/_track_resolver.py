"""
Track Resolver — 读 registry.yaml / schema 校验 / 返回 track config

Design authority: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md
Execution authority: THIS FILE.

Used by: track_scan.py / track_verify.py / track_archive_triggers.py / track_map.py
Schema:
  必填: id (str) / type (str, enum: dir-tree/repo-entry/code-tree) / root (str)
  可选: output (str) / entity_type (str) / child_type (str) / max_depth (int)
        / ignore (list[str]) / patterns (list[str]) / thresholds (dict)
        / depth_limit (int) / radar_summary (dict)

Behavior on errors:
  - registry.yaml not found / unparseable → exit code 2 + JSON error
  - track_id not found → return None (caller decides exit 0 vs error)
  - schema invalid (missing required / unknown type) → return None + warn log
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

import yaml

REGISTRY_REL_PATH = ".agents/skills/index-librarian/protocol/registry.yaml"

REQUIRED_FIELDS = ("id", "type", "root")
KNOWN_TYPES = frozenset({"dir-tree", "repo-entry", "code-tree"})


def _find_repo_root(start: Optional[Path] = None) -> Path:
    """Walk up from given path (or cwd) to find .git directory."""
    current = (start or Path.cwd()).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def _load_registry(registry_path: Optional[Path] = None) -> dict[str, Any]:
    """Load registry.yaml. Returns parsed dict; exits with code 2 on hard errors."""
    if registry_path is None:
        registry_path = _find_repo_root() / REGISTRY_REL_PATH

    if not registry_path.is_file():
        print(
            f"[track-resolver] error: registry.yaml not found at {registry_path}",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        with registry_path.open("r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp) or {}
    except yaml.YAMLError as exc:
        print(
            f"[track-resolver] error: failed to parse {registry_path}: {exc}",
            file=sys.stderr,
        )
        sys.exit(2)

    if not isinstance(data, dict):
        print(
            f"[track-resolver] error: registry.yaml top level must be a mapping",
            file=sys.stderr,
        )
        sys.exit(2)

    return data


def _validate_track(track: Any, *, log_prefix: str = "[track-resolver]") -> bool:
    """Return True if track passes schema check; print warn and return False otherwise."""
    if not isinstance(track, dict):
        print(f"{log_prefix} warn: track entry not a mapping, skipped: {track!r}")
        return False

    for field in REQUIRED_FIELDS:
        if field not in track or track[field] in (None, ""):
            print(
                f"{log_prefix} warn: track {track.get('id', '?')!r} missing required "
                f"field {field!r}, skipped"
            )
            return False

    track_type = track["type"]
    if track_type not in KNOWN_TYPES:
        print(
            f"{log_prefix} warn: track {track['id']!r} has unknown type {track_type!r} "
            f"(known: {sorted(KNOWN_TYPES)}), skipped"
        )
        return False

    return True


def list_tracks(registry_path: Optional[Path] = None) -> list[dict[str, Any]]:
    """Return all valid tracks from registry.yaml. Invalid entries are skipped with warn."""
    data = _load_registry(registry_path)
    raw_tracks = data.get("tracks") or []
    if not isinstance(raw_tracks, list):
        print("[track-resolver] warn: 'tracks' field is not a list, treating as empty")
        return []
    return [t for t in raw_tracks if _validate_track(t)]


def resolve(
    track_id: str,
    *,
    registry_path: Optional[Path] = None,
) -> Optional[dict[str, Any]]:
    """Return validated track config for track_id, or None if not found / invalid.

    Caller convention:
      - None → caller should exit 0 (skip gracefully); user error or absent track is not fatal
      - dict → caller proceeds with track-specific scan
    """
    for track in list_tracks(registry_path):
        if track["id"] == track_id:
            return track

    print(f"[track-resolver] info: track {track_id!r} not found in registry.yaml, skip")
    return None


def get_modules(registry_path: Optional[Path] = None) -> list[dict[str, Any]]:
    """Legacy accessor: return modules: field for docs-tree backing scripts.

    Used by docs-tree backing scripts (cognitive_map / archive_triggers etc.) to keep
    backward compatibility with v1 registry layout.
    """
    data = _load_registry(registry_path)
    modules = data.get("modules") or []
    return modules if isinstance(modules, list) else []


if __name__ == "__main__":
    # Diagnostic CLI: python _track_resolver.py [<track-id>]
    if len(sys.argv) == 1:
        tracks = list_tracks()
        print(f"found {len(tracks)} valid tracks:")
        for t in tracks:
            print(f"  - {t['id']:<16} type={t['type']:<12} root={t['root']}")
        sys.exit(0)

    track_id = sys.argv[1]
    track = resolve(track_id)
    if track is None:
        sys.exit(0)
    import json

    print(json.dumps(track, indent=2, ensure_ascii=False))
