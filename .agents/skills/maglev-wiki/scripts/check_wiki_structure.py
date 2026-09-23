#!/usr/bin/env python3
"""Compare Wiki content pages with the human-approved structure plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from wiki_config import load_and_validate
from wiki_content import check_opaque_identifiers, iter_plan_pages, load_wiki_plan, validate_plan_approval
from wiki_frontmatter import parse_frontmatter, validate_frontmatter

WIKI_ROOT_RELATIVE = "docs/wiki"
FIXED_NAVIGATION_PATHS = {"docs/wiki/WIKI.md", "docs/wiki/INDEX.md", "docs/wiki/FRAMEWORK.md"}
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
CONTRACT_AUX_HEADING_RE = re.compile(r"^#{1,6}\s*(完整正向示例|模板审阅项)\s*$", re.MULTILINE)


def finding(code, path, message, severity="error"):
    return {"code": code, "severity": severity, "path": str(path), "message": message}


def wiki_markdown_pages(root: Path) -> list[Path]:
    wiki_root = root / WIKI_ROOT_RELATIVE
    return sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []


def navigation_paths(plan: dict | None = None) -> set[str]:
    paths = set(FIXED_NAVIGATION_PATHS)
    if plan is not None:
        paths.update(f"docs/wiki/{item['id']}/README.md" for item in plan.get("dimensions", []) if isinstance(item, dict) and item.get("id"))
    return paths


def content_pages(root: Path, plan: dict | None = None) -> list[Path]:
    navigation = navigation_paths(plan)
    return [path for path in wiki_markdown_pages(root) if path.name != "INDEX.md" and path.relative_to(root).as_posix() not in navigation]


def planned_pages(plan):
    result = {}
    for dimension, _, page in iter_plan_pages(plan):
        result[str(page["path"])] = {
            "page_id": str(page["id"]),
            "dimension": str(dimension["id"]),
            "audience": str(dimension["audience"]),
            "title": str(page["title"]),
        }
    return result


def check_links(root: Path) -> list[dict]:
    problems = []
    for page in wiki_markdown_pages(root):
        text = page.read_text(encoding="utf-8")
        page_relative = page.relative_to(root).as_posix()
        for match in MD_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_text, _, anchor = target.partition("#")
            if not path_text:
                continue
            resolved = (page.parent / path_text).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                problems.append(finding("WIKI_LINK_BROKEN", page_relative, f"outside_repo:{target}"))
                continue
            if not resolved.exists():
                problems.append(finding("WIKI_LINK_BROKEN", page_relative, f"missing:{target}"))
                continue
            if anchor and resolved.is_file():
                try:
                    headings = {line.strip().lstrip("#").strip() for line in resolved.read_text(encoding="utf-8").splitlines() if line.startswith("#")}
                except (OSError, UnicodeDecodeError):
                    continue
                if anchor not in headings:
                    problems.append(finding("WIKI_ANCHOR_BROKEN", page_relative, f"anchor_missing:{target}", severity="warning"))
    return problems


def check_contract_leak(root: Path) -> list[dict]:
    problems = []
    for page in content_pages(root):
        match = CONTRACT_AUX_HEADING_RE.search(page.read_text(encoding="utf-8"))
        if match:
            problems.append(finding("WIKI_GUIDANCE_LEAK", page.relative_to(root).as_posix(), f"template guidance section leaked into product page: {match.group(1)}"))
    return problems


def build_report(root: Path, config: dict, plan: dict) -> tuple[dict, list[dict]]:
    expected = planned_pages(plan)
    actual = {page.relative_to(root).as_posix(): page for page in content_pages(root, plan)}
    problems = []
    for path, item in expected.items():
        if path not in actual:
            problems.append(finding("WIKI_PLANNED_PAGE_MISSING", path, f"approved page is missing: {item['title']}"))
    for path in sorted(set(actual) - set(expected)):
        problems.append(finding("WIKI_PAGE_NOT_APPROVED", path, "content page is absent from the approved structure plan"))
    for path in sorted(set(actual) & set(expected)):
        text = actual[path].read_text(encoding="utf-8")
        meta, _, parse_findings = parse_frontmatter(text, path)
        problems.extend(parse_findings)
        if meta is not None:
            problems.extend(validate_frontmatter(meta, config, plan, path, root))
            item = expected[path]
            if meta.get("dimension") != item["dimension"]:
                problems.append(finding("WIKI_PAGE_PLAN_DIMENSION_MISMATCH", path, "page dimension differs from the approved plan"))
            if meta.get("audience") != item["audience"]:
                problems.append(finding("WIKI_PAGE_PLAN_AUDIENCE_MISMATCH", path, "page audience differs from the approved plan"))
            if meta.get("title") != item["title"]:
                problems.append(finding("WIKI_PAGE_PLAN_TITLE_MISMATCH", path, "page title differs from the approved plan"))
    problems.extend(check_contract_leak(root))
    problems.extend(check_opaque_identifiers(root))
    report = {
        "planned_pages": len(expected),
        "actual_pages": len(actual),
        "missing_pages": sorted(set(expected) - set(actual)),
        "unapproved_pages": sorted(set(actual) - set(expected)),
    }
    return report, problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check Wiki pages against the approved structure plan.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--config", default=None)
    parser.add_argument("--plan", default=".maglev/wiki/wiki-plan.yaml")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    config, findings = load_and_validate(root, args.config)
    plan, plan_findings = load_wiki_plan(root, args.plan)
    findings.extend(plan_findings)
    report = {"planned_pages": 0, "actual_pages": 0, "missing_pages": [], "unapproved_pages": []}
    if config is not None and plan is not None and not findings:
        findings.extend(validate_plan_approval(root, plan, config["source_policy"]))
    if config is not None and plan is not None and not findings:
        report, findings = build_report(root, config, plan)
    payload = {"ok": not any(item.get("severity") == "error" for item in findings), "report": report, "findings": findings}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
