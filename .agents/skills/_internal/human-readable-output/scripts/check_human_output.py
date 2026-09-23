#!/usr/bin/env python3
"""Deterministic integrity checks for human-readable output.

The checker deliberately does not judge prose quality, page shape, reader-goal
coverage, or semantic correctness. It validates only declared file relations and
safe, reproducible integrity facts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

FINDINGS_SCHEMA = "human-readable-findings/v1"
BUNDLE_SCHEMA = "human-review-bundle/v1"
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
MERMAID_OPEN_RE = re.compile(r"^\s*```mermaid\s*$")
FENCE_RE = re.compile(r"^\s*```\s*$")


def _finding(code: str, severity: str, path: str, message: str, rule: str, observed: Any = None, expected: Any = None) -> dict[str, Any]:
    return {
        "code": code,
        "severity": severity,
        "path": path,
        "rule": rule,
        "message": message,
        "observed": observed,
        "expected": expected,
    }


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _safe_relative(value: Any) -> bool:
    if not isinstance(value, str) or not value or value.startswith("/"):
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts and not re.match(r"^[A-Za-z]:", value)


def _resolve(root: Path, value: str) -> Path:
    return (root / value).resolve()


def _inside(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _link_findings(root: Path, path: Path, relative: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8")
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path = target.split("#", 1)[0]
        if not target_path:
            continue
        resolved = (path.parent / target_path).resolve()
        if not _inside(root, resolved) or not resolved.exists():
            findings.append(
                _finding(
                    "HR_BROKEN_LINK",
                    "error",
                    relative,
                    "Markdown 相对链接不存在或越出项目根目录。",
                    "relative_link_integrity",
                    observed=target,
                    expected="existing project-relative target",
                )
            )
    return findings


def _fence_findings(path: Path, relative: str) -> list[dict[str, Any]]:
    """Only detect an unclosed Mermaid fence; do not require Mermaid usage."""
    findings: list[dict[str, Any]] = []
    open_mermaid = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if MERMAID_OPEN_RE.match(line):
            open_mermaid = True
        elif open_mermaid and FENCE_RE.match(line):
            open_mermaid = False
    if open_mermaid:
        findings.append(
            _finding(
                "HR_MERMAID_FENCE_UNCLOSED",
                "error",
                relative,
                "Mermaid 图表代码块没有闭合。",
                "fence_integrity",
                observed="unclosed mermaid fence",
                expected="closed fenced block",
            )
        )
    return findings


def check_document(root: Path, file_path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    root = root.resolve()
    file_path = file_path.resolve()
    relative = file_path.relative_to(root).as_posix() if _inside(root, file_path) else file_path.as_posix()
    if not _inside(root, file_path):
        return [_finding("HR_PATH_OUTSIDE_ROOT", "error", relative, "文件必须位于项目根目录内。", "safe_path")]
    if file_path.suffix.lower() != ".md":
        findings.append(_finding("HR_HUMAN_FILE_NOT_MARKDOWN", "error", relative, "人类审阅入口必须是 Markdown 文件。", "human_review_format", expected=".md"))
        return findings
    try:
        file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [_finding("HR_HUMAN_FILE_UNREADABLE", "error", relative, "Markdown 文件无法按 UTF-8 读取。", "human_review_format", observed=str(error))]
    findings.extend(_link_findings(root, file_path, relative))
    findings.extend(_fence_findings(file_path, relative))
    return findings


def _load_document(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    return value


def check_review_bundle(root: Path, manifest_path: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    manifest_path = manifest_path.resolve()
    relative_manifest = manifest_path.relative_to(root).as_posix() if _inside(root, manifest_path) else manifest_path.as_posix()
    if not _inside(root, manifest_path):
        return [_finding("HR_PATH_OUTSIDE_ROOT", "error", relative_manifest, "审阅清单必须位于项目根目录内。", "safe_path")]
    try:
        manifest = _load_document(manifest_path)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        return [_finding("HR_MANIFEST_INVALID", "error", relative_manifest, "机器审阅清单无法解析。", "manifest_schema", observed=str(error))]
    findings: list[dict[str, Any]] = []
    if not isinstance(manifest, dict) or manifest.get("schema_version") != BUNDLE_SCHEMA:
        findings.append(_finding("HR_MANIFEST_INVALID", "error", relative_manifest, "审阅清单版本不受支持。", "manifest_schema", expected=BUNDLE_SCHEMA))
        return findings
    if manifest.get("audience") != "human-review":
        findings.append(_finding("HR_AUDIENCE_INVALID", "error", relative_manifest, "审阅清单必须声明 human-review。", "audience_declaration", observed=manifest.get("audience"), expected="human-review"))
    project_root = manifest.get("project_root", ".")
    if not _safe_relative(project_root):
        findings.append(_finding("HR_PROJECT_ROOT_INVALID", "error", relative_manifest, "项目根目录必须是安全的相对路径。", "safe_path", observed=project_root))
        project_root_path = root
    else:
        project_root_path = _resolve(root, project_root)
        if not _inside(root, project_root_path):
            findings.append(_finding("HR_PROJECT_ROOT_INVALID", "error", relative_manifest, "项目根目录不得越出检查根目录。", "safe_path"))
    human_view = manifest.get("human_view")
    if not _safe_relative(human_view):
        findings.append(_finding("HR_HUMAN_VIEW_INVALID", "error", relative_manifest, "人类映射必须是安全的相对路径。", "safe_path", observed=human_view))
    else:
        human_view_path = _resolve(root, human_view)
        if not _inside(root, human_view_path) or not human_view_path.exists():
            findings.append(_finding("HR_HUMAN_VIEW_MISSING", "error", human_view, "人类 Markdown 映射不存在。", "human_view_presence"))
        else:
            findings.extend(check_document(project_root_path, human_view_path))
    sources = manifest.get("machine_sources")
    if not isinstance(sources, list) or not sources:
        findings.append(_finding("HR_MACHINE_SOURCES_MISSING", "error", relative_manifest, "审阅清单必须声明至少一个机器来源。", "manifest_schema"))
        return findings
    for index, source in enumerate(sources):
        label = f"{relative_manifest}#machine_sources[{index}]"
        if not isinstance(source, dict):
            findings.append(_finding("HR_MACHINE_SOURCE_INVALID", "error", label, "机器来源必须是映射。", "manifest_schema"))
            continue
        path_value = source.get("path")
        if not _safe_relative(path_value):
            findings.append(_finding("HR_SOURCE_PATH_INVALID", "error", label, "机器来源必须是项目内相对路径。", "safe_path", observed=path_value))
            continue
        source_path = _resolve(project_root_path, path_value)
        if not _inside(project_root_path, source_path) or not source_path.exists():
            findings.append(_finding("HR_SOURCE_MISSING", "error", label, "机器来源不存在或越出项目根目录。", "source_presence", observed=path_value))
            continue
        expected_digest = source.get("digest")
        actual_digest = _digest(source_path)
        if expected_digest != actual_digest:
            findings.append(_finding("HR_SOURCE_DIGEST_MISMATCH", "error", label, "机器来源摘要与当前内容不一致。", "source_digest", observed=actual_digest, expected=expected_digest))
    return findings


def _payload(findings: list[dict[str, Any]]) -> dict[str, Any]:
    errors = [item for item in findings if item["severity"] == "error"]
    advisories = [item for item in findings if item["severity"] == "advisory"]
    status = "blocked" if errors else "advisory" if advisories else "pass"
    return {"schema_version": FINDINGS_SCHEMA, "status": status, "findings": findings}


def _markdown(payload: dict[str, Any]) -> str:
    lines = ["# 人类可读输出完整性检查", "", f"机械状态：{payload['status']}", "", "> 机械通过不等于语义通过，也不等于人类接受。", ""]
    if not payload["findings"]:
        lines.append("未发现确定性完整性问题。")
        return "\n".join(lines) + "\n"
    lines.extend(["## 检查发现", "", "| 级别 | 代码 | 文件 | 说明 |", "|---|---|---|---|"])
    for item in payload["findings"]:
        lines.append(f"| {item['severity']} | `{item['code']}` | `{item['path']}` | {item['message']} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check human-readable output integrity without judging document shape or semantics.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    document = subparsers.add_parser("check-document")
    document.add_argument("--root", type=Path, required=True)
    document.add_argument("paths", nargs="+", type=Path)
    document.add_argument("--format", choices=("json", "markdown"), default="json")
    bundle = subparsers.add_parser("check-review-bundle")
    bundle.add_argument("--root", type=Path, required=True)
    bundle.add_argument("manifest", type=Path)
    bundle.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "check-document":
        findings: list[dict[str, Any]] = []
        for path in args.paths:
            findings.extend(check_document(root, path if path.is_absolute() else root / path))
    else:
        findings = check_review_bundle(root, args.manifest if args.manifest.is_absolute() else root / args.manifest)
    payload = _payload(findings)
    output = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else _markdown(payload)
    print(output)
    return 1 if payload["status"] == "blocked" else 0


if __name__ == "__main__":
    sys.exit(main())
