#!/usr/bin/env python3
"""Validate Wiki page metadata against project inputs and the approved plan."""

from __future__ import annotations

import argparse
import json
import re
import hashlib
import sys
from pathlib import Path

from wiki_config import load_and_validate
from wiki_content import load_wiki_plan, validate_plan_approval

PAGE_TYPE_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_ROLES = {"fact", "material", "operation"}


def finding(code, path, message, severity="error"):
    return {"code": code, "severity": severity, "path": str(path), "message": message}


def _is_below(child, roots):
    child = str(child).rstrip("/")
    return any(child == str(root).rstrip("/") or child.startswith(str(root).rstrip("/") + "/") for root in roots)


def validate_frontmatter(meta, config, plan, path="page", root=None):
    errors = []
    if not isinstance(meta, dict):
        return [finding("FRONTMATTER_NOT_MAPPING", path, "Page frontmatter must be a mapping.")]
    allowed_fields = {"title", "dimension", "audience", "page_type", "source_bindings", "last_updated", "generator"}
    for unsupported in sorted(set(meta) - allowed_fields):
        errors.append(finding("PAGE_FIELD_UNSUPPORTED", path, f"Unsupported frontmatter field: {unsupported}."))
    if not isinstance(meta.get("title"), str) or not meta["title"].strip():
        errors.append(finding("PAGE_TITLE_EMPTY", path, "Field 'title' must be non-empty."))

    dimensions = {item.get("id"): item for item in plan.get("dimensions", []) if isinstance(item, dict)}
    dimension = dimensions.get(meta.get("dimension"))
    if dimension is None:
        errors.append(finding("PAGE_DIMENSION_UNKNOWN", path, f"Field 'dimension' must be one of {sorted(dimensions)}."))
    elif meta.get("audience") != dimension.get("audience"):
        errors.append(finding("PAGE_AUDIENCE_INVALID", path, "Field 'audience' must match the approved dimension audience."))

    page_type = meta.get("page_type")
    if page_type is not None and (not isinstance(page_type, str) or not PAGE_TYPE_PATTERN.fullmatch(page_type)):
        errors.append(finding("PAGE_TYPE_INVALID", path, "Optional page_type must be a safe kebab-case guidance label."))
    if not isinstance(meta.get("last_updated"), str) or not DATE_PATTERN.fullmatch(str(meta.get("last_updated", ""))):
        errors.append(finding("PAGE_LAST_UPDATED_INVALID", path, "Field 'last_updated' must use YYYY-MM-DD."))

    bindings = meta.get("source_bindings")
    if not isinstance(bindings, list) or not bindings:
        errors.append(finding("PAGE_BINDINGS_REQUIRED", path, "Field 'source_bindings' must contain at least one approved source."))
        bindings = []
    policy = config.get("source_policy", {})
    roots_by_role = {
        "fact": policy.get("fact_roots", []),
        "material": policy.get("material_roots", []),
        "operation": policy.get("operation_roots", []),
    }
    for index, binding in enumerate(bindings):
        label = f"{path}#source_bindings[{index}]"
        if not isinstance(binding, dict):
            errors.append(finding("BINDING_NOT_MAPPING", label, "Source binding must be a mapping."))
            continue
        binding_path = binding.get("path")
        path_valid = isinstance(binding_path, str) and bool(binding_path) and not binding_path.startswith("/") and ".." not in Path(binding_path).parts
        if not path_valid:
            errors.append(finding("BINDING_PATH_INVALID", label, "Binding path must be repository-relative."))
        role = binding.get("role")
        if role not in VALID_ROLES:
            errors.append(finding("BINDING_ROLE_INVALID", label, f"Binding role must be one of {sorted(VALID_ROLES)}."))
            continue
        digest = binding.get("digest")
        digest_valid = isinstance(digest, str) and bool(DIGEST_PATTERN.fullmatch(digest))
        if not digest_valid:
            errors.append(finding("BINDING_DIGEST_INVALID", label, "Binding digest must match sha256:<64 hex chars>."))
        if path_valid and roots_by_role[role] and not _is_below(binding_path, roots_by_role[role]):
            errors.append(finding("BINDING_PATH_OUTSIDE_SOURCE_ROOTS", label, f"{role} binding is outside configured roots."))
        if root is not None and path_valid and digest_valid:
            source = (Path(root) / binding_path).resolve()
            try:
                source.relative_to(Path(root).resolve())
            except ValueError:
                errors.append(finding("BINDING_PATH_INVALID", label, "Binding path escapes the repository."))
            else:
                if not source.is_file():
                    errors.append(finding("BINDING_SOURCE_MISSING", label, "Bound source file does not exist."))
                else:
                    actual_digest = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
                    if digest != actual_digest:
                        errors.append(finding("BINDING_SOURCE_STALE", label, "Binding digest does not match the current source file."))
    planned_pages = {
        str(page.get("path")): page
        for dimension_item in plan.get("dimensions", [])
        if isinstance(dimension_item, dict)
        for aspect in dimension_item.get("aspects", [])
        if isinstance(aspect, dict)
        for page in aspect.get("pages", [])
        if isinstance(page, dict)
    }
    approved_page = planned_pages.get(path)
    if approved_page is not None:
        expected_bindings = {(str(item.get("path")), str(item.get("role", "fact"))) for item in approved_page.get("sources", []) if isinstance(item, dict)}
        actual_bindings = {(str(item.get("path")), str(item.get("role"))) for item in bindings if isinstance(item, dict)}
        if actual_bindings != expected_bindings:
            errors.append(finding("PAGE_BINDINGS_PLAN_MISMATCH", path, "source_bindings must exactly match the approved page sources"))
    return errors


def parse_frontmatter(text, path="page"):
    import yaml

    if not text.startswith("---"):
        return None, text, [finding("FRONTMATTER_MISSING", path, "Page must start with frontmatter.")]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text, [finding("FRONTMATTER_UNTERMINATED", path, "Frontmatter block is not terminated.")]
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as error:
        return None, parts[2], [finding("FRONTMATTER_INVALID_YAML", path, str(error))]
    if not isinstance(meta, dict):
        return None, parts[2], [finding("FRONTMATTER_NOT_MAPPING", path, "Frontmatter must be a mapping.")]
    return meta, parts[2], []


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate Wiki page frontmatter.")
    parser.add_argument("pages", nargs="+")
    parser.add_argument("--root", default=".")
    parser.add_argument("--config", default=None)
    parser.add_argument("--plan", default=".maglev/wiki/wiki-plan.yaml")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    config, findings = load_and_validate(root, args.config)
    plan, plan_findings = load_wiki_plan(root, args.plan)
    findings.extend(plan_findings)
    if config is not None and plan is not None and not findings:
        findings.extend(validate_plan_approval(root, plan, config["source_policy"]))
    if config is not None and plan is not None and not findings:
        for raw in args.pages:
            page = Path(raw)
            if not page.is_absolute():
                page = root / page
            try:
                text = page.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as error:
                findings.append(finding("PAGE_READ_FAILED", str(page), str(error)))
                continue
            label = page.relative_to(root).as_posix() if page.is_relative_to(root) else str(page)
            meta, _, parse_findings = parse_frontmatter(text, label)
            findings.extend(parse_findings)
            if meta is not None:
                findings.extend(validate_frontmatter(meta, config, plan, label, root))
    payload = {"ok": not findings, "findings": findings}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
