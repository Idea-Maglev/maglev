#!/usr/bin/env python3
"""Archive trigger detector for docs/thinking/ leaf files.

Implements the three triggers from spec AC-F6-1:
  1. time_window: file untouched (no git commit) for >= M months
  2. supersede:   frontmatter has `superseded_by:` pointing to another doc
  3. orphan:      no inbound reference from anywhere in repo, AND
                  git age >= N months

Outputs candidate list. Does NOT auto-migrate by default (use --apply).

See specs/20_evolution/active/docs_knowledge_archival_methodology/
01_requirements.md F6 for the contract.

Exit codes:
  0  scan completed (regardless of how many candidates found)
  1  scan error (e.g., not a git repo, missing module)

Usage:
  python3 archive_triggers.py                       # default: thinking module, 12mo window, 6mo orphan
  python3 archive_triggers.py --time-window-months 6
  python3 archive_triggers.py --output json
  python3 archive_triggers.py --apply               # actually git mv to 90_archive/<segment>/
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parents[5]
MODULE_DEFAULT = "thinking"
ARCHIVE_DIRNAME = "90_archive"


@dataclass
class Candidate:
    path: str
    triggers: list[str] = field(default_factory=list)
    last_commit: str | None = None
    age_months: float | None = None
    superseded_by: str | None = None
    inbound_count: int | None = None
    status: str | None = None
    protected_lpm: bool = False


def run(cmd: list[str], cwd: Path = REPO_ROOT) -> str:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        return ""
    return r.stdout


def parse_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def collect_leaf_files(module_root: Path) -> list[Path]:
    leaves = []
    for p in module_root.rglob("*.md"):
        if p.name in ("INDEX.md", "README.md"):
            continue
        rel_parts = p.relative_to(module_root).parts
        # exclude already-archived
        if ARCHIVE_DIRNAME in rel_parts:
            continue
        # exclude machine-readable meta (lifecycle.md §6, 3-state revision)
        if "_meta" in rel_parts:
            continue
        if any(part.startswith(".") for part in rel_parts):
            continue
        leaves.append(p)
    return sorted(leaves)


def get_last_commit_date(path: Path) -> datetime | None:
    out = run(["git", "log", "-1", "--format=%cI", "--", str(path.relative_to(REPO_ROOT))])
    out = out.strip()
    if not out:
        return None
    try:
        return datetime.fromisoformat(out)
    except ValueError:
        return None


def months_between(then: datetime, now: datetime) -> float:
    delta = now - then
    return delta.days / 30.4375


def build_inbound_index(leaf_files: list[Path]) -> dict[str, int]:
    """For each leaf file, count how many other files in repo reference it.

    Reference detection (best-effort):
      - by stem (filename without .md extension)
      - by relative path segment (e.g. 'docs/thinking/30_philosophy/foo.md')
    Excludes self-references and INDEX.md auto-generated tables.
    """
    stems: dict[str, list[Path]] = {}
    for lf in leaf_files:
        stems.setdefault(lf.stem, []).append(lf)

    # Build a single grep -r for all stems
    inbound: dict[str, int] = {str(lf.relative_to(REPO_ROOT)): 0 for lf in leaf_files}

    # Collect candidate referrer files (whole repo .md/.yaml/.py)
    cmd = [
        "git", "ls-files",
        "*.md", "*.yaml", "*.yml", "*.py", "AGENTS.md", "README.md",
    ]
    out = run(cmd)
    candidate_files = [REPO_ROOT / line for line in out.splitlines() if line]

    for cand in candidate_files:
        try:
            text = cand.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lf in leaf_files:
            if cand == lf:
                continue
            # Skip auto-generated INDEX.md body table references
            if cand.name == "INDEX.md" and cand.parent == lf.parent:
                continue
            rel = str(lf.relative_to(REPO_ROOT))
            stem = lf.stem
            # Match either stem (with .md or as bare word) or relative path
            if rel in text or f"{stem}.md" in text:
                inbound[rel] += 1

    return inbound


def detect_triggers(
    module_root: Path,
    time_window_months: int,
    orphan_age_months: int,
) -> list[Candidate]:
    leaves = collect_leaf_files(module_root)
    now = datetime.now(timezone.utc)

    inbound = build_inbound_index(leaves)

    candidates: list[Candidate] = []
    for lf in leaves:
        rel = str(lf.relative_to(REPO_ROOT))
        last_dt = get_last_commit_date(lf)
        age = months_between(last_dt, now) if last_dt else None
        meta = parse_frontmatter(lf)
        superseded = meta.get("superseded_by")
        in_count = inbound.get(rel, 0)

        triggers: list[str] = []

        # Trigger 1: time window
        if age is not None and age >= time_window_months:
            triggers.append(f"time_window>={time_window_months}mo")

        # Trigger 2: supersede
        if superseded:
            triggers.append(f"superseded_by={superseded}")

        # Trigger 3: orphan
        if (
            in_count == 0
            and age is not None
            and age >= orphan_age_months
        ):
            triggers.append(f"orphan(age>={orphan_age_months}mo,inbound=0)")

        if triggers:
            status = (meta.get("status") or "draft").lower()
            # AC-F1-7: LPM protection — crystallized never auto-archives
            # except via explicit superseded_by (which the author wrote manually)
            is_lpm = status == "crystallized"
            has_explicit_supersede = bool(superseded)
            protected = is_lpm and not has_explicit_supersede

            candidates.append(Candidate(
                path=rel,
                triggers=triggers,
                last_commit=last_dt.date().isoformat() if last_dt else None,
                age_months=round(age, 1) if age is not None else None,
                superseded_by=superseded,
                inbound_count=in_count,
                status=status,
                protected_lpm=protected,
            ))

    return candidates


def derive_segment(rel_path: str, module_root: Path) -> str | None:
    """Extract segment id (e.g., '30_philosophy') from a leaf path."""
    p = Path(rel_path)
    try:
        relative = p.relative_to(module_root.relative_to(REPO_ROOT))
    except ValueError:
        return None
    parts = relative.parts
    if not parts:
        return None
    # First part is segment dir (e.g., '30_philosophy')
    if re.match(r"^\d{2}_[a-z_]+$", parts[0]):
        return parts[0]
    return None


def apply_archive(
    candidates: list[Candidate],
    module_root: Path,
    dry_run: bool = True,
) -> list[dict]:
    """Move candidates to docs/thinking/90_archive/<segment>/ via git mv.

    AC-F6-2: target = 90_archive/<original_segment>/
    AC-F6-3: must use git mv to preserve history.
    AC-F1-7: LPM (status=crystallized) protected — skipped unless author
             has explicitly set superseded_by.
    """
    archive_root = module_root / ARCHIVE_DIRNAME
    moved = []
    for cand in candidates:
        if cand.protected_lpm:
            moved.append({
                "path": cand.path,
                "status": "skipped_lpm_protected",
                "note": "crystallized; manual git mv required",
            })
            continue
        seg = derive_segment(cand.path, module_root)
        if seg is None:
            moved.append({"path": cand.path, "status": "skipped_no_segment"})
            continue
        if seg == ARCHIVE_DIRNAME:
            moved.append({"path": cand.path, "status": "already_archived"})
            continue
        src = REPO_ROOT / cand.path
        dst_dir = archive_root / seg
        dst = dst_dir / src.name

        if dst.exists():
            moved.append({"path": cand.path, "status": "skipped_dst_exists"})
            continue

        if dry_run:
            moved.append({
                "path": cand.path,
                "status": "would_move",
                "dst": str(dst.relative_to(REPO_ROOT)),
            })
        else:
            dst_dir.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(
                ["git", "mv", str(src.relative_to(REPO_ROOT)),
                 str(dst.relative_to(REPO_ROOT))],
                cwd=REPO_ROOT, capture_output=True, text=True,
            )
            if r.returncode == 0:
                moved.append({
                    "path": cand.path,
                    "status": "moved",
                    "dst": str(dst.relative_to(REPO_ROOT)),
                })
            else:
                moved.append({
                    "path": cand.path,
                    "status": "git_mv_failed",
                    "stderr": r.stderr,
                })
    return moved


def format_table(candidates: list[Candidate]) -> str:
    if not candidates:
        return "No archive candidates found.\n"
    lines = [
        "Path | Status | LPM | Age (mo) | Inbound | Triggers",
        "-----|--------|-----|----------|---------|---------",
    ]
    for c in candidates:
        triggers = "; ".join(c.triggers)
        age = f"{c.age_months}" if c.age_months is not None else "?"
        lpm = "🔒" if c.protected_lpm else ""
        st = c.status or "?"
        lines.append(f"{c.path} | {st} | {lpm} | {age} | {c.inbound_count} | {triggers}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect archive candidates for docs/thinking/ leaf files (F6).",
    )
    parser.add_argument("--module", default=MODULE_DEFAULT, help="Module name (default: thinking)")
    parser.add_argument(
        "--time-window-months", type=int, default=12,
        help="Trigger 1 threshold: M months without commit (default: 12)",
    )
    parser.add_argument(
        "--orphan-age-months", type=int, default=6,
        help="Trigger 3 threshold: orphan + age >= N months (default: 6)",
    )
    parser.add_argument(
        "--output", choices=["table", "json"], default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Actually git mv candidates to 90_archive/<segment>/ (default: dry-run)",
    )
    args = parser.parse_args()

    module_root = REPO_ROOT / "docs" / args.module
    if not module_root.is_dir():
        print(f"ERROR: module path not found: {module_root}", file=sys.stderr)
        return 1

    candidates = detect_triggers(
        module_root,
        time_window_months=args.time_window_months,
        orphan_age_months=args.orphan_age_months,
    )

    if args.output == "json":
        out = {
            "module": args.module,
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "thresholds": {
                "time_window_months": args.time_window_months,
                "orphan_age_months": args.orphan_age_months,
            },
            "candidates": [c.__dict__ for c in candidates],
        }
        if args.apply or candidates:
            out["actions"] = apply_archive(candidates, module_root, dry_run=not args.apply)
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(format_table(candidates))
        if args.apply:
            print("\n--- Applying migrations ---")
            actions = apply_archive(candidates, module_root, dry_run=False)
            for a in actions:
                print(f"  {a['status']:20s} {a['path']} -> {a.get('dst', '-')}")
        elif candidates:
            print("\n(use --apply to actually move; or use git mv manually for fine control)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
