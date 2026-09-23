#!/usr/bin/env python3
"""Generate Wiki navigation surfaces from a human-approved structure plan.

The generator never creates content pages or infers information architecture.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import sys
from datetime import date, datetime
from pathlib import Path

from wiki_config import CONFIG_TEMPLATE, load_and_validate
from wiki_content import load_wiki_plan, validate_plan_approval

WIKI_ROOT_RELATIVE = Path("docs/wiki")
TEMPLATE_DIR = Path(__file__).resolve().parent / "wiki_templates"
WIKI_PACK_REGISTRY_RELATIVE = Path("templates/wiki-packs/registry.yaml")


def sha256_of(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:{}".format(digest.hexdigest())


def mtime_date(path):
    return datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()


def resolve_fact_binding(root, fact_roots):
    for fact_root in fact_roots:
        fact_dir = root / fact_root
        if not fact_dir.is_dir():
            continue
        for name in ("INDEX.md", "README.md"):
            candidate = fact_dir / name
            if candidate.is_file():
                return "{}/{}".format(fact_root.rstrip("/"), name), sha256_of(candidate)
    return None


def render_template(name, **fields):
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8").format(**fields)


def resolve_pack_registry(root):
    registry = root / WIKI_PACK_REGISTRY_RELATIVE
    return registry.resolve() if registry.is_file() else None


def render_framework_surface(root, dimensions, binding_date):
    from wiki_config import finding

    registry_path = resolve_pack_registry(root)
    if registry_path is None:
        return {}, []
    registry_label = registry_path.relative_to(root.resolve()).as_posix()
    try:
        from wiki_pack import WikiPackError, resolve_methodology, resolve_pack

        pack = resolve_pack(registry_path)
        methodology = resolve_methodology(pack)
        body = methodology.path.read_text(encoding="utf-8")
        if body.startswith("---"):
            parts = body.split("---", 2)
            if len(parts) == 3:
                body = parts[2].lstrip()
    except WikiPackError as error:
        return {}, [finding("WIKI_FRAMEWORK_RENDER_BLOCKED", registry_label, f"wiki pack rejected: {error.code}:{error.location}:{error.detail}")]
    except (OSError, UnicodeDecodeError) as error:
        return {}, [finding("WIKI_FRAMEWORK_RENDER_BLOCKED", registry_label, f"read_failed:{error}")]
    dimension_lines = "\n".join(
        "- `{}`（{}）— {}".format(item["id"], item["audience"], item["purpose"])
        for item in dimensions
    )
    pack_relative_root = pack.manifest_path.parent.relative_to(root.resolve()).as_posix()
    header = (
        "---\n"
        'title: "Wiki 写作指导"\n'
        "dimension: guidance\n"
        'audience: contributor\n'
        "source_bindings:\n"
        "  - path: {source}\n"
        "    digest: {digest}\n"
        "    role: fact\n"
        'last_updated: "{date}"\n'
        "generator: wiki_generate.py\n"
        "---\n\n"
        "> 本文件从模板包 `{pack}` 投影。模板只提供约束、建议和示例，不决定项目页面数量或内容规模。\n\n"
        "# 当前批准结构\n\n"
        "{dimensions}\n\n---\n\n"
    ).format(
        source="{}/{}".format(pack_relative_root, methodology.public_path),
        digest=methodology.digest,
        date=binding_date or date(1970, 1, 1).isoformat(),
        pack="{}/{}".format(pack.pack_id, pack.version),
        dimensions=dimension_lines,
    )
    return {WIKI_ROOT_RELATIVE / "FRAMEWORK.md": header + body}, []


def planned_dimension_pages(dimension, dimension_dir):
    pages = []
    for aspect in dimension.get("aspects", []):
        for page in aspect.get("pages", []):
            target = str(page["path"])
            link = posixpath.relpath(target, start=dimension_dir.as_posix())
            pages.append((link, str(page["title"])))
    return pages


def collect_dimension_pages(dimension_dir):
    pages = []
    if not dimension_dir.is_dir():
        return pages
    for markdown in sorted(dimension_dir.rglob("*.md")):
        if markdown.name in {"INDEX.md", "README.md"}:
            continue
        pages.append((markdown.relative_to(dimension_dir).with_suffix("").as_posix(), extract_page_title(markdown)))
    return pages


def render_dimension_overviews(dimensions):
    lines = []
    wiki_root = WIKI_ROOT_RELATIVE.as_posix()
    for dimension in dimensions:
        dimension_id = str(dimension["id"])
        dimension_link = posixpath.relpath(f"{wiki_root}/{dimension_id}/README.md", start=wiki_root)
        lines.extend([
            f"### [{dimension['title']}]({dimension_link})",
            "",
            f"> {dimension['purpose']}（面向 {dimension['audience']}）",
            "",
        ])
        for aspect in dimension.get("aspects", []):
            lines.append(f"**{aspect['title']}**：{aspect['reader_need']}")
            for page in aspect.get("pages", []):
                page_path = str(page["path"])
                page_link = posixpath.relpath(page_path, start=wiki_root)
                reader_task = str(page.get("reader_task", ""))
                purpose = str(page.get("purpose", ""))
                lines.append(f"- [{page['title']}]({page_link})：{reader_task} {purpose}")
            lines.append("")
    return "\n".join(lines).rstrip()

def render_dimension_flow(dimensions):
    lines = ["flowchart LR"]
    for index, dimension in enumerate(dimensions):
        node_id = str(dimension["id"]).replace("-", "_")
        title = str(dimension["title"]).replace('"', "'")
        lines.append(f'    {node_id}["{title}"]')
        if index:
            previous = str(dimensions[index - 1]["id"]).replace("-", "_")
            lines.append(f"    {previous} --> {node_id}")
    return "\n".join(lines)

def render_overview(wiki_meta):
    overview = wiki_meta.get("overview", {}) if isinstance(wiki_meta, dict) else {}
    core_problem = str(overview.get("core_problem") or wiki_meta.get("description", "")).strip()
    system_role = str(overview.get("system_role") or wiki_meta.get("description", "")).strip()
    lifecycle = overview.get("lifecycle", [])
    flow_lines = ["flowchart LR"]
    lifecycle_lines = ["| 阶段 | 读者应理解什么 |", "|---|---|"]
    previous = None
    if isinstance(lifecycle, list):
        for item in lifecycle:
            if not isinstance(item, dict):
                continue
            node_id = str(item.get("id", "step")).replace("-", "_")
            title = str(item.get("title", "")).replace('"', "'")
            description = str(item.get("description", ""))
            flow_lines.append(f'    {node_id}["{title}"]')
            if previous:
                flow_lines.append(f"    {previous} --> {node_id}")
            previous = node_id
            lifecycle_lines.append(f"| {title} | {description} |")
    boundaries = overview.get("boundaries", [])
    boundary_lines = []
    if isinstance(boundaries, list):
        boundary_lines = [f"- {item}" for item in boundaries if isinstance(item, str) and item.strip()]
    return {
        "core_problem": core_problem,
        "system_role": system_role,
        "flow": "\n".join(flow_lines),
        "lifecycle": "\n".join(lifecycle_lines) if len(lifecycle_lines) > 2 else "",
        "boundaries": "\n".join(boundary_lines) or "- 具体边界以当前事实和页面来源为准。",
    }

def generate(root, config_path=None, plan_path=".maglev/wiki/wiki-plan.yaml", dry_run=False):
    config, findings = load_and_validate(root, config_path)
    plan, plan_findings = load_wiki_plan(root, plan_path)
    findings.extend(plan_findings)
    if config is None or plan is None or findings:
        return [], findings, CONFIG_TEMPLATE if config is None else None
    findings.extend(validate_plan_approval(root, plan, config["source_policy"]))
    if findings:
        return [], findings, None

    wiki_meta = config["wiki"]
    dimensions = plan["dimensions"]
    binding = resolve_fact_binding(root, config["source_policy"].get("fact_roots", []))
    binding_date = mtime_date(root / binding[0]) if binding else None
    files = {}
    framework_files, framework_findings = render_framework_surface(root, dimensions, binding_date)
    files.update(framework_files)
    findings.extend(framework_findings)
    links = []
    for dimension in dimensions:
        relative = WIKI_ROOT_RELATIVE / dimension["id"]
        approved_pages = planned_dimension_pages(dimension, relative)
        page_links = "\n".join(f"- {title}" for link, title in approved_pages) or "（该维度没有批准的正文页面。）"
        files[relative / "README.md"] = render_template(
            "dimension_readme.md",
            dimension_title=dimension["title"],
            dimension_id=dimension["id"],
            dimension_audience=dimension["audience"],
            dimension_description=dimension["purpose"],
            audience_label=dimension["audience"],
            page_links=page_links,
            last_updated=binding_date or date(1970, 1, 1).isoformat(),
        )
        links.append(f"- [{dimension['title']}]({dimension['id']}/README.md)：{dimension['purpose']} — 面向{dimension['audience']}")
    dimension_overviews = render_dimension_overviews(dimensions)
    overview = render_overview(wiki_meta)
    policy = config["source_policy"]
    configured_roots = list(policy.get("fact_roots", []))
    fact_roots = "、".join(root for root in configured_roots if "docs" not in root and "guide" not in root) or "未配置"
    guide_roots = "、".join([root for root in configured_roots if "docs" in root or "guide" in root] + policy.get("material_roots", []) + policy.get("operation_roots", [])) or "未配置"
    files[WIKI_ROOT_RELATIVE / "WIKI.md"] = render_template(
        "WIKI.md",
        project_title=wiki_meta["title"],
        wiki_description=wiki_meta["description"].strip(),
        dimension_count=len(dimensions),
        dimension_links="\n".join(links),
        dimension_overviews=dimension_overviews,
        dimension_flow=render_dimension_flow(dimensions),
        fact_roots=fact_roots,
        guide_roots=guide_roots,
        overview_core_problem=overview["core_problem"],
        overview_system_role=overview["system_role"],
        overview_flow=overview["flow"],
        overview_lifecycle=overview["lifecycle"],
        overview_boundaries=overview["boundaries"],
    )
    if dry_run:
        return sorted(str(path) for path in files), findings, None
    for relative, content in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return sorted(str(path) for path in files), findings, None


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate Wiki navigation from an approved structure plan.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--config", default=None)
    parser.add_argument("--plan", default=".maglev/wiki/wiki-plan.yaml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    files, findings, guidance = generate(root, args.config, args.plan, args.dry_run)
    payload = {
        "ok": not findings,
        "blocked": bool(findings),
        "dry_run": args.dry_run,
        "files": files,
        "findings": findings,
        "next_step": "Write the approved pages, then run frontmatter, structure, drift, readability, and reader-task review checks." if not findings else "Resolve plan or configuration findings before writing Wiki content.",
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if guidance:
            print(guidance, file=sys.stderr)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
