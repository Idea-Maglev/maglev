#!/usr/bin/env python3
"""
cognitive_map.py — F8 认知地图生成器。

职责：
  - 扫描指定模块的全部叶子 .md（排除 INDEX/README/_meta/.dotfile）
  - 聚合两类边：
      1) markdown 跨位段链接（`../<segment>/xxx.md`）
      2) frontmatter `linked_to: [path, ...]` 显式声明（AC-F8-2）
  - 节点 = 位段目录（如 `30_philosophy`）；边 = 跨位段引用 ≥ 1 建立
  - 缺失或 `active` / `crystallized` 的文档全部入图（lifecycle 3 态修订，2026-04-27）
  - `archived` 文档仍排除以避免噪声（与 archive_triggers 一致）
  - 输出：
      a) Mermaid 节点图（stdout 或 --emit-mermaid <file>）
      b) docs/<module>/_meta/knowledge_graph.json（机读，含节点/边/边权）
      c) 可选 --inject 把 Mermaid 块写回 root INDEX.md 的 <!-- COGNITIVE_MAP --> 标记之间

Exit codes:
  0 — generated successfully
  1 — markers missing on --inject
  2 — script error

不在 P0 范围：
  - librarian navigate 子命令（AC-F8-3）
  - 概念向量检索
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common.frontmatter import parse_any_frontmatter

REPO_ROOT = Path(__file__).resolve().parents[5]

SKIP_NAMES = {"INDEX.md", "README.md"}
SKIP_DIRS = {"_meta"}  # 3-state revision (2026-04-27): _drafts removed

# 跨段引用正则：匹配 ../<digits>_<name>/xxx.md 或 /<segment>/xxx.md
SEG_RE = re.compile(r"^(\d{2}_[a-zA-Z0-9_-]+)$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+\.md)\)")


@dataclass
class Edge:
    src: str  # segment name
    dst: str
    weight: int = 0
    samples: list[str] = field(default_factory=list)  # up to 3 sample edges (src_file -> dst_file)


def is_segment_dir(name: str) -> bool:
    return bool(SEG_RE.match(name))


def collect_leaves(module_path: Path) -> list[Path]:
    leaves = []
    for p in module_path.rglob("*.md"):
        if p.name in SKIP_NAMES:
            continue
        rel = p.relative_to(module_path)
        if any(part.startswith(".") or part in SKIP_DIRS for part in rel.parts):
            continue
        leaves.append(p)
    return leaves


def get_segment(rel_path: Path) -> str | None:
    """Return top-level segment name (e.g. '30_philosophy') or None if not under a segment."""
    if not rel_path.parts:
        return None
    top = rel_path.parts[0]
    return top if is_segment_dir(top) else None


def resolve_link(src_file: Path, link: str, module_path: Path) -> Path | None:
    """Resolve a markdown link relative to src_file, return absolute path under module_path or None."""
    # Skip external / anchor-only links
    if link.startswith(("http://", "https://", "#", "mailto:")):
        return None
    link_clean = link.split("#", 1)[0]
    if not link_clean:
        return None
    try:
        target = (src_file.parent / link_clean).resolve()
    except (OSError, ValueError):
        return None
    try:
        target.relative_to(module_path.resolve())
    except ValueError:
        return None
    return target


def build_graph(module_path: Path, include_drafts: bool = False) -> tuple[dict[str, dict], list[Edge]]:
    """Return (nodes_by_segment, edges).

    3-state revision (2026-04-27): missing status defaults to 'active' (was 'draft').
    `include_drafts` parameter retained for backward CLI compat but no longer
    materially affects behavior since 'draft' is not a valid status anymore.
    Only `archived` documents are excluded from edges (handled implicitly:
    archived docs live in 90_archive/ which is filtered upstream).
    """
    module_path = module_path.resolve()
    leaves = collect_leaves(module_path)
    nodes: dict[str, dict] = {}  # segment -> {count, files: [...]}
    edges_map: dict[tuple[str, str], Edge] = {}

    # First pass: register nodes (every segment with ≥1 leaf)
    leaf_meta: dict[Path, dict] = {}
    for leaf in leaves:
        rel = leaf.relative_to(module_path)
        seg = get_segment(rel)
        if seg is None:
            continue
        meta = parse_any_frontmatter(leaf).metadata
        leaf_meta[leaf] = meta
        node = nodes.setdefault(seg, {"count": 0, "drafts": 0, "files": []})
        node["count"] += 1
        # 'drafts' field retained for output schema stability but always 0 post-revision
        node["files"].append(str(rel))

    # Second pass: edges
    for leaf, meta in leaf_meta.items():
        rel = leaf.relative_to(module_path)
        src_seg = get_segment(rel)
        if src_seg is None:
            continue
        # 3-state: skip only explicitly archived documents
        status = meta.get("status")
        if status == "archived":
            continue

        # Source 1: markdown links in body
        try:
            content = leaf.read_text(encoding="utf-8")
        except OSError:
            continue

        targets: list[Path] = []
        for m in LINK_RE.finditer(content):
            t = resolve_link(leaf, m.group(1), module_path)
            if t and t.exists():
                targets.append(t)

        # Source 2: frontmatter linked_to
        linked_to = meta.get("linked_to") or []
        if isinstance(linked_to, str):
            linked_to = [linked_to]
        for entry in linked_to:
            if not isinstance(entry, str):
                continue
            t = resolve_link(leaf, entry, module_path)
            if t and t.exists():
                targets.append(t)

        for t in targets:
            try:
                t_rel = t.relative_to(module_path)
            except ValueError:
                continue
            dst_seg = get_segment(t_rel)
            if dst_seg is None or dst_seg == src_seg:
                continue  # only cross-segment edges count (AC-F8-1)
            key = (src_seg, dst_seg)
            edge = edges_map.get(key)
            if edge is None:
                edge = Edge(src=src_seg, dst=dst_seg)
                edges_map[key] = edge
            edge.weight += 1
            if len(edge.samples) < 3:
                edge.samples.append(f"{rel} -> {t_rel}")

    return nodes, list(edges_map.values())


def emit_mermaid(nodes: dict[str, dict], edges: list[Edge]) -> str:
    lines = ["```mermaid", "graph LR"]
    for seg in sorted(nodes.keys()):
        info = nodes[seg]
        label = f"{seg}<br/>{info['count']} files"
        if info["drafts"]:
            label += f" ({info['drafts']} draft)"
        lines.append(f'    {seg}["{label}"]')
    if not edges:
        lines.append("    %% no cross-segment edges yet (waiting for status promotion + linked_to)")
    for e in sorted(edges, key=lambda x: (x.src, x.dst)):
        lines.append(f"    {e.src} -->|{e.weight}| {e.dst}")
    lines.append("```")
    return "\n".join(lines)


def emit_json(nodes: dict[str, dict], edges: list[Edge]) -> dict:
    return {
        "nodes": [
            {"segment": seg, **info} for seg, info in sorted(nodes.items())
        ],
        "edges": [asdict(e) for e in sorted(edges, key=lambda x: (x.src, x.dst))],
    }


INJECT_BEGIN = "<!-- COGNITIVE_MAP:BEGIN -->"
INJECT_END = "<!-- COGNITIVE_MAP:END -->"


def inject_into_index(index_path: Path, mermaid_block: str) -> bool:
    try:
        content = index_path.read_text(encoding="utf-8")
    except OSError:
        return False
    if INJECT_BEGIN not in content or INJECT_END not in content:
        return False
    new_block = f"{INJECT_BEGIN}\n{mermaid_block}\n{INJECT_END}"
    pattern = re.compile(
        re.escape(INJECT_BEGIN) + r".*?" + re.escape(INJECT_END),
        re.DOTALL,
    )
    new_content = pattern.sub(new_block, content)
    if new_content != content:
        index_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description="Generate cognitive map (Mermaid + knowledge_graph.json) for a module.")
    ap.add_argument("--module", default="docs/thinking", help="Module root path relative to repo root.")
    ap.add_argument("--emit-mermaid", help="Write Mermaid to file (default: stdout).")
    ap.add_argument("--emit-json", help="Write knowledge_graph.json to file (default: <module>/_meta/knowledge_graph.json).")
    ap.add_argument("--inject", action="store_true", help="Inject Mermaid into root INDEX.md between COGNITIVE_MAP markers.")
    ap.add_argument("--include-drafts", action="store_true", help="Include draft-status leaves in edges (AC-F8-4 override).")
    ap.add_argument("--dry-run", action="store_true", help="Compute only; do not write files.")
    args = ap.parse_args()

    module_path = (REPO_ROOT / args.module).resolve()
    if not module_path.is_dir():
        print(f"error: module not found: {module_path}", file=sys.stderr)
        sys.exit(2)

    nodes, edges = build_graph(module_path, include_drafts=args.include_drafts)
    mermaid = emit_mermaid(nodes, edges)
    graph = emit_json(nodes, edges)

    summary = {
        "module": args.module,
        "nodes": len(nodes),
        "edges": len(edges),
        "total_weight": sum(e.weight for e in edges),
        "include_drafts": args.include_drafts,
    }

    # Mermaid output
    if args.emit_mermaid:
        if not args.dry_run:
            Path(args.emit_mermaid).write_text(mermaid + "\n", encoding="utf-8")
        summary["mermaid_path"] = args.emit_mermaid
    elif not args.inject:
        print(mermaid)

    # JSON output
    json_path = Path(args.emit_json) if args.emit_json else module_path / "_meta" / "knowledge_graph.json"
    if not args.dry_run:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary["json_path"] = str(json_path.relative_to(REPO_ROOT)) if json_path.is_absolute() else str(json_path)

    # Inject into root INDEX.md
    if args.inject:
        root_index = module_path / "INDEX.md"
        if not args.dry_run:
            ok = inject_into_index(root_index, mermaid)
            if not ok:
                print(f"error: COGNITIVE_MAP markers missing in {root_index}", file=sys.stderr)
                print(f"  add `{INJECT_BEGIN}` and `{INJECT_END}` to enable injection.", file=sys.stderr)
                sys.exit(1)
        summary["injected_into"] = str(root_index.relative_to(REPO_ROOT))

    print(json.dumps(summary, indent=2, ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main()
