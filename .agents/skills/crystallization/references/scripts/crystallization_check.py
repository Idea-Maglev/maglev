#!/usr/bin/env python3
"""crystallization_check.py — 结晶产物自检脚本

用法:
    maglev-python crystallization_check.py <reality_dir> [--json]

退出码:
    0  无 FAIL
    1  存在 FAIL
    2  参数/路径错误

基于通用结构信号自适配检查，不硬编码特定目录名。
检查项以注册式组织，可扩展。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import importlib.util
from pathlib import Path
from typing import List, Tuple

import yaml

# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"
BLOCKED = "BLOCKED"

Result = Tuple[str, str, str]  # (level, check_name, detail)


def _load_reality_admission():
    internal_root = Path(__file__).resolve().parents[3] / "_internal" / "reality-admission"
    module_path = internal_root / "core.py"
    spec = importlib.util.spec_from_file_location("maglev_reality_admission_core", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load Reality Admission core: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(spec.name, module)
    spec.loader.exec_module(module)
    return module


reality_admission = _load_reality_admission()


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _collect_md_files(root: Path) -> List[Path]:
    """Recursively collect all .md files under root."""
    return sorted(root.rglob("*.md"))


def _non_blank_line_count(path: Path) -> int:
    """Count non-blank lines in a file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    return sum(1 for line in text.splitlines() if line.strip())


def _is_inside_code_fence(lines: List[str], target_idx: int) -> bool:
    """Check if a line index is inside a fenced code block."""
    inside = False
    for i, line in enumerate(lines):
        if i == target_idx:
            return inside
        if line.strip().startswith("```"):
            inside = not inside
    return inside


# ---------------------------------------------------------------------------
# Universal checks (always run)
# ---------------------------------------------------------------------------

def check_placeholder_free(root: Path) -> List[Result]:
    """Check for placeholder text outside code fences."""
    results: List[Result] = []
    pattern = re.compile(r"\b(TODO|TBD|FIXME)\b|待补充|^\.{3}$")
    for md in _collect_md_files(root):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        found = False
        for i, line in enumerate(lines):
            if pattern.search(line) and not _is_inside_code_fence(lines, i):
                results.append((FAIL, "placeholder_free",
                                f"{md.relative_to(root)}:{i+1}"))
                found = True
        if not found:
            results.append((PASS, "placeholder_free",
                            str(md.relative_to(root))))
    return results


def check_mermaid_fence_balanced(root: Path) -> List[Result]:
    """Check that ```mermaid fences are properly closed."""
    results: List[Result] = []
    for md in _collect_md_files(root):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        open_line = None
        has_mermaid = False
        fence_depth = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("```mermaid"):
                has_mermaid = True
                if fence_depth == 0:
                    open_line = i + 1
                fence_depth += 1
            elif stripped == "```" and fence_depth > 0:
                fence_depth -= 1
                open_line = None
        rel = str(md.relative_to(root))
        if fence_depth > 0:
            results.append((FAIL, "mermaid_fence_balanced",
                            f"{rel}:{open_line} (unclosed fence)"))
        elif has_mermaid:
            results.append((PASS, "mermaid_fence_balanced", rel))
    return results


def check_internal_links_reachable(root: Path) -> List[Result]:
    """Check that relative markdown links point to existing files."""
    results: List[Result] = []
    link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    for md in _collect_md_files(root):
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rel_path = md.relative_to(root)
        all_ok = True
        for match in link_pattern.finditer(text):
            target = match.group(2)
            # Skip external links, anchors, and absolute paths
            if target.startswith(("http://", "https://", "#", "/")):
                continue
            # Strip anchor
            target_path = target.split("#")[0]
            if not target_path:
                continue
            resolved = (md.parent / target_path).resolve()
            if not resolved.exists():
                results.append((FAIL, "internal_links_reachable",
                                f"{rel_path} -> {target_path} (not found)"))
                all_ok = False
        if all_ok and link_pattern.search(text):
            results.append((PASS, "internal_links_reachable", str(rel_path)))
    return results


def check_min_density(root: Path) -> List[Result]:
    """Warn about .md files with fewer than 5 non-blank lines."""
    results: List[Result] = []
    for md in _collect_md_files(root):
        count = _non_blank_line_count(md)
        rel = str(md.relative_to(root))
        if count < 5:
            results.append((WARN, "min_density",
                            f"{rel} ({count} lines)"))
        else:
            results.append((PASS, "min_density", rel))
    return results


# ---------------------------------------------------------------------------
# Versioned Reality Profile checks (only when 00_profile.yaml exists)
# ---------------------------------------------------------------------------

def _profile_path(root: Path) -> Path:
    return root / "00_profile.yaml"


def _load_profile(root: Path) -> tuple[dict | None, List[Result]]:
    path = _profile_path(root)
    if not path.exists():
        return None, []  # Shared Reality Admission reports missing Profile.
    try:
        profile = reality_admission.load_profile(path)
    except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError) as error:
        return None, [(FAIL, "profile_parseable", str(error))]
    profile_id = profile.get("profile_id", profile.get("id", "unknown"))
    version = profile.get("version", profile.get("layout_version", "unknown"))
    return profile, [(PASS, "profile_parseable", f"{profile_id}@{version}")]


def check_profile_gate(root: Path) -> List[Result]:
    """Preserve the checker-specific parseability signal; shared core owns the gate."""
    _, results = _load_profile(root)
    return results


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

UNIVERSAL_CHECKS = [
    check_placeholder_free,
    check_mermaid_fence_balanced,
    check_internal_links_reachable,
    check_min_density,
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_checks(root: Path) -> List[Result]:
    """Run all applicable checks and return results."""
    results: List[Result] = []
    results.extend(check_profile_gate(root))
    results.extend(
        (item.level, item.check, item.detail)
        for item in reality_admission.check_reality_root(root)
    )
    for check_fn in UNIVERSAL_CHECKS:
        results.extend(check_fn(root))
    return results


def _count_modules(root: Path) -> int:
    """Count profile-managed domains, falling back to top-level directories."""
    profile, _ = _load_profile(root)
    if profile and isinstance(profile.get("domains"), list):
        return sum(
            1
            for domain in profile["domains"]
            if isinstance(domain, str) and (root / domain).is_dir()
        )
    return sum(1 for path in root.iterdir() if path.is_dir() and path.name != "crosscutting")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def format_text(results: List[Result], modules_detected: int) -> str:
    """Format results as human-readable text."""
    lines: List[str] = []
    for level, name, detail in results:
        lines.append(f"[{level}] {name}   {detail}")
    lines.append("---")
    counts = {PASS: 0, WARN: 0, FAIL: 0, BLOCKED: 0}
    for level, _, _ in results:
        counts[level] = counts.get(level, 0) + 1
    lines.append(
        f"summary: pass={counts[PASS]} warn={counts[WARN]} "
        f"fail={counts[FAIL]} blocked={counts[BLOCKED]} modules_detected={modules_detected}"
    )
    return "\n".join(lines)


def format_json(results: List[Result], modules_detected: int) -> str:
    """Format results as JSON."""
    output = {
        "results": [
            {"level": level, "check": name, "detail": detail}
            for level, name, detail in results
        ],
        "summary": {
            "pass": sum(1 for r in results if r[0] == PASS),
            "warn": sum(1 for r in results if r[0] == WARN),
            "fail": sum(1 for r in results if r[0] == FAIL),
            "blocked": sum(1 for r in results if r[0] == BLOCKED),
            "modules_detected": modules_detected,
        },
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Crystallization self-check: validate reality directory structure and content."
    )
    parser.add_argument("reality_dir", help="Path to the reality directory to check")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    root = Path(args.reality_dir)
    if not root.is_dir():
        print(f"Error: '{args.reality_dir}' is not a directory", file=sys.stderr)
        return 2

    results = run_checks(root)
    modules_detected = _count_modules(root)

    if args.json:
        print(format_json(results, modules_detected))
    else:
        print(format_text(results, modules_detected))

    has_fail = any(r[0] in (FAIL, BLOCKED) for r in results)
    return 1 if has_fail else 0


if __name__ == "__main__":
    sys.exit(main())
