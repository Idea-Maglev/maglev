#!/usr/bin/env python3
"""Observe Wiki navigation, metadata, and bound-source drift."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from wiki_config import load_and_validate
from wiki_content import load_wiki_plan, validate_plan_approval
from wiki_frontmatter import parse_frontmatter, validate_frontmatter

WIKI_ROOT_RELATIVE = Path("docs/wiki")


def finding(code, path, message, severity="error"):
    return {"code": code, "severity": severity, "path": str(path), "message": message}


def sha256_of(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:{}".format(digest.hexdigest())


def check_wiki(root, config_path=None, plan_path=".maglev/wiki/wiki-plan.yaml"):
    config, findings = load_and_validate(root, config_path)
    plan, plan_findings = load_wiki_plan(root, plan_path)
    findings.extend(plan_findings)
    if config is None or plan is None or findings:
        return findings
    findings.extend(validate_plan_approval(root, plan, config["source_policy"]))
    if findings:
        return findings
    wiki_root = root / WIKI_ROOT_RELATIVE
    if not wiki_root.is_dir():
        return [finding("WIKI_NOT_GENERATED", WIKI_ROOT_RELATIVE, "docs/wiki does not exist.")]
    if not (wiki_root / "WIKI.md").is_file():
        findings.append(finding("WIKI_ENTRY_MISSING", wiki_root / "WIKI.md", "Wiki entry is missing."))

    dimension_ids = {item["id"] for item in plan["dimensions"]}
    navigation_paths = {"docs/wiki/WIKI.md", "docs/wiki/INDEX.md"}
    navigation_paths.update(f"docs/wiki/{dimension_id}/README.md" for dimension_id in dimension_ids)
    planned_content_dirs = {
        str(page["path"]).split("/")[2]
        for dimension in plan["dimensions"]
        for aspect in dimension.get("aspects", [])
        for page in aspect.get("pages", [])
        if isinstance(page, dict) and len(str(page.get("path", "")).split("/")) > 3
    }
    existing_dirs = {path.name for path in wiki_root.iterdir() if path.is_dir()}
    for dimension_id in sorted(dimension_ids):
        if not (wiki_root / dimension_id / "README.md").is_file():
            findings.append(finding("WIKI_DIMENSION_INCOMPLETE", wiki_root / dimension_id / "README.md", "Approved dimension navigation is missing."))
    for directory in sorted(existing_dirs - dimension_ids - planned_content_dirs):
        findings.append(finding("WIKI_DIMENSION_NOT_APPROVED", wiki_root / directory, "Directory is absent from the approved structure plan."))

    for page in sorted(wiki_root.rglob("*.md")):
        relative = page.relative_to(root)
        if page.name == "INDEX.md" or relative.as_posix() in navigation_paths:
            continue
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(finding("WIKI_PAGE_UNREADABLE", relative, "Page is not valid UTF-8 text."))
            continue
        meta, _, page_findings = parse_frontmatter(text, str(relative))
        findings.extend(page_findings)
        if meta is None:
            continue
        if relative.as_posix() != "docs/wiki/FRAMEWORK.md":
            findings.extend(validate_frontmatter(meta, config, plan, str(relative), root))
        for index, binding in enumerate(meta.get("source_bindings", []) or []):
            if not isinstance(binding, dict):
                continue
            bound_path = binding.get("path")
            recorded_digest = binding.get("digest")
            if not isinstance(bound_path, str) or not bound_path:
                continue
            source = root / bound_path
            if not source.is_file():
                findings.append(finding("WIKI_SOURCE_MISSING", relative, f"Source {bound_path} does not exist (binding #{index})."))
                continue
            current_digest = sha256_of(source)
            if recorded_digest and recorded_digest != current_digest:
                findings.append(finding("WIKI_SOURCE_DRIFT", relative, f"Source {bound_path} changed; review this page."))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check Wiki navigation and source drift.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--config", default=None)
    parser.add_argument("--plan", default=".maglev/wiki/wiki-plan.yaml")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    findings = check_wiki(Path(args.root).resolve(), args.config, args.plan)
    payload = {"ok": not findings, "wiki_root": str(WIKI_ROOT_RELATIVE), "findings": findings, "note": "Observation only; remediation belongs to the authoring workflow."}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else ("Wiki drift check passed." if not findings else json.dumps(payload, ensure_ascii=False, indent=2)))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
