#!/usr/bin/env python3
"""Validation for the project inputs available to Wiki structure inference."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

DEFAULT_CONFIG_RELATIVE_PATH = Path(".maglev/wiki.yaml")
SAFE_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CONFIG_TEMPLATE = """\
# Project inputs for Wiki structure inference.
wiki:
  title: "{project_title}"
  description: >-
    {one_line_description}
  language: zh
source_policy:
  fact_roots:
    - specs/10_reality
  material_roots: []
  operation_roots: []
audience_hints: []
"""


def finding(code, path, message, severity="error"):
    return {"code": code, "severity": severity, "path": str(path), "message": message}


def _is_safe_relative_path(value):
    return (
        isinstance(value, str)
        and bool(value)
        and not value.startswith("/")
        and "://" not in value
        and "\\" not in value
        and ".." not in Path(value).parts
    )


def validate_config(config, path="config"):
    errors = []
    if not isinstance(config, dict):
        return [finding("CONFIG_NOT_MAPPING", path, "Wiki config root must be a mapping.")]
    if "dimensions" in config:
        errors.append(
            finding(
                "CONFIG_STRUCTURE_NOT_ALLOWED",
                f"{path}#dimensions",
                "Project configuration cannot predefine Wiki dimensions; the Agent must infer them from project inputs.",
            )
        )

    wiki = config.get("wiki")
    if not isinstance(wiki, dict):
        errors.append(finding("WIKI_SECTION_MISSING", path, "Top-level 'wiki' mapping is required."))
    else:
        for field in ("title", "description"):
            value = wiki.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(finding("WIKI_FIELD_EMPTY", f"{path}#wiki.{field}", f"Field 'wiki.{field}' must be non-empty."))
        language = wiki.get("language", "zh")
        if not isinstance(language, str) or not language.strip():
            errors.append(finding("WIKI_LANGUAGE_INVALID", f"{path}#wiki.language", "Field 'wiki.language' must be non-empty."))

    policy = config.get("source_policy")
    if not isinstance(policy, dict):
        errors.append(finding("SOURCE_POLICY_MISSING", path, "Top-level 'source_policy' mapping is required."))
        return errors
    roles = {}
    for field in ("fact_roots", "material_roots", "operation_roots"):
        roots = policy.get(field, [])
        if field == "fact_roots" and (not isinstance(roots, list) or not roots):
            errors.append(finding("FACT_ROOTS_EMPTY", f"{path}#source_policy.fact_roots", "At least one fact root is required."))
            roots = []
        elif not isinstance(roots, list):
            errors.append(finding("SOURCE_ROOTS_INVALID", f"{path}#source_policy.{field}", f"'{field}' must be a list."))
            roots = []
        for index, root in enumerate(roots):
            if not _is_safe_relative_path(root):
                errors.append(finding("SOURCE_ROOT_UNSAFE", f"{path}#source_policy.{field}[{index}]", f"Unsafe source root: {root!r}."))
        roles[field] = roots
    overlaps = (set(roles["fact_roots"]) & set(roles["material_roots"])) | (set(roles["fact_roots"]) & set(roles["operation_roots"])) | (set(roles["material_roots"]) & set(roles["operation_roots"]))
    if overlaps:
        errors.append(finding("SOURCE_ROOT_OVERLAP", f"{path}#source_policy", f"A root can have only one source role: {sorted(overlaps)}."))

    hints = config.get("audience_hints", [])
    if not isinstance(hints, list):
        errors.append(finding("AUDIENCE_HINTS_INVALID", f"{path}#audience_hints", "audience_hints must be a list."))
    else:
        seen = set()
        for index, hint in enumerate(hints):
            location = f"{path}#audience_hints[{index}]"
            if not isinstance(hint, dict):
                errors.append(finding("AUDIENCE_HINT_INVALID", location, "Audience hint must be a mapping."))
                continue
            identifier = hint.get("id")
            if not isinstance(identifier, str) or not SAFE_ID_PATTERN.fullmatch(identifier):
                errors.append(finding("AUDIENCE_HINT_ID_INVALID", f"{location}.id", "Audience id must be kebab-case."))
            elif identifier in seen:
                errors.append(finding("AUDIENCE_HINT_DUPLICATED", f"{location}.id", f"Duplicate audience id: {identifier}."))
            else:
                seen.add(identifier)
            if not isinstance(hint.get("description"), str) or not hint["description"].strip():
                errors.append(finding("AUDIENCE_HINT_DESCRIPTION_MISSING", f"{location}.description", "Audience concern is required."))
    return errors


def load_and_validate(root, config_path=None):
    relative = config_path or DEFAULT_CONFIG_RELATIVE_PATH
    path = root / relative
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [finding("CONFIG_MISSING", relative, "Wiki input configuration is missing; create it before structure inference.")]
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        return None, [finding("CONFIG_INVALID_YAML", relative, str(error))]
    return config, validate_config(config, str(relative))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate Wiki project inputs.")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--root", default=".")
    validate.add_argument("--config", default=None)
    sub.add_parser("template")
    args = parser.parse_args(argv)
    if args.command == "template":
        sys.stdout.write(CONFIG_TEMPLATE)
        return 0
    config, findings = load_and_validate(Path(args.root), args.config)
    payload = {"config_path": str(args.config or DEFAULT_CONFIG_RELATIVE_PATH), "ok": not findings, "findings": findings}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if config is not None and not findings else 1


if __name__ == "__main__":
    sys.exit(main())
