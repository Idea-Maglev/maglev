#!/usr/bin/env python3
"""Wiki structure-plan, evidence, readability, and review primitives.

Agents infer the information architecture from project evidence. This module
validates and projects that decision; it never invents dimensions, aspects,
pages, prose, or semantic verdicts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml

PLAN_SCHEMA = "wiki-plan/v2"
SOURCE_UNIVERSE_SCHEMA = "wiki-source-universe/v1"
CHALLENGE_SCHEMA = "wiki-challenge/v1"
CHALLENGE_RECEIPT_SCHEMA = "wiki-challenge-receipt/v2"
DIVERGENCE_SCHEMA = "wiki-divergence/v2"
EVIDENCE_BUNDLE_SCHEMA = "wiki-evidence-bundle/v3"
REVIEW_LEDGER_SCHEMA = "wiki-review-ledger/v2"
SEMANTIC_REVIEW_SCHEMA = "wiki-semantic-review/v2"
CONSUMER_REVIEW_SCHEMA = "wiki-consumer-review/v3"
PLAN_APPROVAL_SCHEMA = "wiki-plan-approval/v1"
WIKI_STATE_DIR = Path(".maglev/wiki")
PLAN_PATH = (WIKI_STATE_DIR / "wiki-plan.yaml").as_posix()
SOURCE_UNIVERSE_PATH = (WIKI_STATE_DIR / "wiki-source-universe.yaml").as_posix()
CHALLENGE_RECEIPT_PATH = (WIKI_STATE_DIR / "wiki-challenge-receipt.yaml").as_posix()
CHALLENGE_PATH = (WIKI_STATE_DIR / "wiki-challenge.yaml").as_posix()
DIVERGENCE_PATH = (WIKI_STATE_DIR / "wiki-divergence.yaml").as_posix()
PLAN_APPROVAL_PATH = (WIKI_STATE_DIR / "wiki-plan-approval.yaml").as_posix()
HUMAN_PLAN_PATH = (WIKI_STATE_DIR / "wiki-plan.md").as_posix()
REVIEW_ROOT = (WIKI_STATE_DIR / "wiki-reviews").as_posix()
SOURCE_ROLES = {"fact", "material", "operation"}
DISPOSITIONS = {"reused", "review_required", "invalidated", "new"}
DIVERGENCE_DISPOSITIONS = {"covered", "merged", "deferred", "not_applicable", "blocked"}
VERDICTS = {"pass", "partial", "fail", "blocked", "not_applicable"}
CONFIDENCES = {"low", "medium", "high"}
ADEQUACY_STATUSES = {"validated", "provisional"}
SAFE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
LINE_LOCATOR_RE = re.compile(r"^(?:L|lines:)?(\d+)(?:-(?:L)?(\d+))?$")
OPAQUE_IDENTIFIER_PATTERNS = (
    re.compile(r"\b[A-Z]{1,4}\d+(?:-[A-Z0-9]+)*\b"),
    re.compile(r"\b[a-z][a-z0-9]{1,20}-\d+(?:-\d+)*\b"),
)
OPAQUE_IDENTIFIER_ALLOWLIST = {"UTF-8", "ISO-8601", "SHA-256", "SHA256"}
HUMAN_READABLE_CONTRACT_RELATIVE = Path(".agents/skills/_internal/human-readable-output/contract.md")
CHALLENGE_FORBIDDEN_INPUTS = (
    PLAN_PATH,
    HUMAN_PLAN_PATH,
    DIVERGENCE_PATH,
    PLAN_APPROVAL_PATH,
    ".maglev/temp",
    REVIEW_ROOT,
    "docs/wiki",
)


def validate_human_readable_contract(root: Path) -> list[dict[str, str]]:
    contract = root / HUMAN_READABLE_CONTRACT_RELATIVE
    if not contract.is_file():
        return [
            finding(
                "HUMAN_READABLE_CONTRACT_MISSING",
                HUMAN_READABLE_CONTRACT_RELATIVE.as_posix(),
                "Human-facing Wiki planning and writing require the shared readability contract.",
            )
        ]
    try:
        text = contract.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return [finding("HUMAN_READABLE_CONTRACT_UNREADABLE", HUMAN_READABLE_CONTRACT_RELATIVE.as_posix(), str(error))]
    return [] if text.strip() else [finding("HUMAN_READABLE_CONTRACT_EMPTY", HUMAN_READABLE_CONTRACT_RELATIVE.as_posix(), "Contract must not be empty.")]


def finding(code: str, path: str, message: str, severity: str = "error") -> dict[str, str]:
    return {"code": code, "severity": severity, "path": str(path), "message": message}


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _safe_relative_path(value: Any) -> str | None:
    if not isinstance(value, str) or not value or value.startswith("/"):
        return None
    if "\\" in value or "://" in value or any(part in {"", ".", ".."} for part in value.split("/")):
        return None
    normalized = PurePosixPath(value).as_posix()
    return normalized if normalized == value else None


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True
def _paths_overlap(first: Path, second: Path) -> bool:
    return _inside(first, second) or _inside(second, first)
def _first_symlink_component(root: Path, relative: str) -> Path | None:
    candidate = root
    for part in PurePosixPath(relative).parts:
        candidate = candidate / part
        if candidate.is_symlink():
            return candidate
    return None


def _has_actor_evidence(evidence_refs: Any, actor_id: Any) -> bool:
    if not isinstance(evidence_refs, list) or not _non_empty(actor_id):
        return False
    return any(ref in {f"history://{actor_id}", f"agent://{actor_id}"} for ref in evidence_refs)
def _forbidden_shape_fields(value: Any, prefix: str, ancestors: set[int] | None = None) -> list[str]:
    forbidden = {"dimensions", "pages", "plan_digest", "linked_page_ids", "linked_page_paths", "page_id", "page_ids", "page_path", "page_paths", "page_binding", "page_bindings"}
    if not isinstance(value, (Mapping, list)):
        return []
    ancestors = set() if ancestors is None else ancestors
    marker = id(value)
    if marker in ancestors:
        raise ValueError(f"recursive YAML alias at {prefix}")
    ancestors.add(marker)
    matches: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            location = f"{prefix}.{key}"
            if key in forbidden:
                matches.append(location)
            matches.extend(_forbidden_shape_fields(child, location, ancestors))
    else:
        for index, child in enumerate(value):
            matches.extend(_forbidden_shape_fields(child, f"{prefix}[{index}]", ancestors))
    ancestors.remove(marker)
    return matches








def check_opaque_identifiers(root: Path, wiki_root: str = "docs/wiki") -> list[dict[str, str]]:
    """Report identifiers that lack an adjacent human description."""
    findings: list[dict[str, str]] = []
    wiki_path = root / wiki_root
    if not wiki_path.is_dir():
        return findings
    navigation = {"WIKI.md", "INDEX.md", "README.md", "FRAMEWORK.md"}
    for path in sorted(wiki_path.rglob("*.md")):
        if path.name in navigation:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        in_frontmatter = bool(lines and lines[0].strip() == "---")
        in_fence = False
        for line_number, line in enumerate(lines, 1):
            if in_frontmatter:
                if line.strip() == "---" and line_number > 1:
                    in_frontmatter = False
                continue
            if re.match(r"^\s*(```|~~~)", line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            visible = re.sub(r"`[^`]*`", lambda match: " " * len(match.group(0)), line)
            for pattern in OPAQUE_IDENTIFIER_PATTERNS:
                for match in pattern.finditer(visible):
                    token = match.group(0)
                    if token in OPAQUE_IDENTIFIER_ALLOWLIST or re.fullmatch(r"[0-9A-Fa-f]{6}", token):
                        continue
                    before = visible[: match.start()].rstrip()
                    after = visible[match.end() :].lstrip()
                    if before.endswith(("(", "（")) and after.startswith((")", "）")):
                        continue
                    findings.append(
                        finding(
                            "WIKI_OPAQUE_IDENTIFIER",
                            f"{path.relative_to(root).as_posix()}:{line_number}",
                            f"identifier {token!r} needs a human description first",
                            severity="warning",
                        )
                    )
    return findings


def _normalize_ref(ref: Any, location: str) -> tuple[dict[str, str] | None, list[dict[str, str]]]:
    if not isinstance(ref, Mapping):
        return None, [finding("EVIDENCE_REF_INVALID", location, "source must be a mapping")]
    path = _safe_relative_path(ref.get("path"))
    if path is None:
        return None, [finding("EVIDENCE_REF_PATH_UNSAFE", location, "source path must be safe and relative")]
    role = ref.get("role", "fact")
    if role not in SOURCE_ROLES:
        return None, [finding("EVIDENCE_REF_ROLE_INVALID", location, f"unsupported role: {role!r}")]
    locator = ref.get("locator")
    if not _non_empty(locator):
        return None, [finding("EVIDENCE_LOCATOR_REQUIRED", location, "section or line locator is required")]
    return {"path": path, "role": str(role), "locator": str(locator)}, []

def _digest_without(document: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: value for key, value in document.items() if key != field})


def build_source_universe(root: Path, source_policy: Mapping[str, Any], provider_reports: list[str] | None = None) -> tuple[dict, list[dict[str, str]]]:
    problems: list[dict[str, str]] = []
    sources: list[dict[str, str]] = []
    for role in sorted(SOURCE_ROLES):
        for root_text in source_policy.get(f"{role}_roots", []) or []:
            safe_root = _safe_relative_path(root_text)
            if safe_root is None:
                problems.append(finding("SOURCE_UNIVERSE_ROOT_UNSAFE", str(root_text), "source root must be safe and relative"))
                continue
            configured_root = root / safe_root
            symlink = _first_symlink_component(root, safe_root)
            if symlink is not None:
                problems.append(finding("SOURCE_UNIVERSE_SYMLINK_FORBIDDEN", symlink.as_posix(), "configured source path cannot contain a symbolic link"))
                continue
            source_root = configured_root.resolve()
            if not source_root.is_dir() or not _inside(source_root, root):
                problems.append(finding("SOURCE_UNIVERSE_ROOT_MISSING", safe_root, "configured source root is unavailable"))
                continue
            for path in sorted(source_root.rglob("*")):
                if path.is_symlink():
                    problems.append(finding("SOURCE_UNIVERSE_SYMLINK_FORBIDDEN", path.as_posix(), "source roots cannot contain symbolic links"))
                    continue
                if not path.is_file():
                    continue
                if not _inside(path, source_root):
                    problems.append(finding("SOURCE_UNIVERSE_PATH_ESCAPE", path.as_posix(), "source file escapes its configured root"))
                    continue
                sources.append({"path": path.resolve().relative_to(root.resolve()).as_posix(), "digest": file_digest(path), "role": role})
    reports: list[dict[str, str]] = []
    for report_text in provider_reports or []:
        safe = _safe_relative_path(report_text)
        symlink = _first_symlink_component(root, safe) if safe is not None else None
        if safe is None or symlink is not None or not (root / safe).is_file() or not _inside(root / safe, root):
            problems.append(finding("SOURCE_UNIVERSE_PROVIDER_INVALID", str(report_text), "provider report must be a readable repository-relative file without symbolic links"))
            continue
        reports.append({"path": safe, "digest": file_digest(root / safe)})
    universe = {
        "schema_version": SOURCE_UNIVERSE_SCHEMA,
        "source_policy_digest": canonical_digest(dict(source_policy)),
        "sources": sources,
        "excluded": [],
        "provider_reports": reports,
        "change_refs": [],
    }
    universe["universe_digest"] = _digest_without(universe, "universe_digest")
    return ({}, problems) if problems else (universe, problems)
def validate_source_universe(
    universe: Any,
    path: str = "source_universe",
    root: Path | None = None,
    source_policy: Mapping[str, Any] | None = None,
) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    if not isinstance(universe, Mapping):
        return [finding("SOURCE_UNIVERSE_INVALID", path, "source universe must be a mapping")]
    if universe.get("schema_version") != SOURCE_UNIVERSE_SCHEMA:
        problems.append(finding("SOURCE_UNIVERSE_SCHEMA_INVALID", path, "unsupported schema_version"))
    if universe.get("universe_digest") != _digest_without(universe, "universe_digest"):
        problems.append(finding("SOURCE_UNIVERSE_DIGEST_MISMATCH", path, "universe digest does not match current inputs"))
    sources = universe.get("sources")
    if not isinstance(sources, list) or not sources:
        problems.append(finding("SOURCE_UNIVERSE_SOURCES_EMPTY", f"{path}.sources", "at least one available source is required"))
    else:
        seen: set[str] = set()
        for index, source in enumerate(sources):
            location = f"{path}.sources[{index}]"
            if not isinstance(source, Mapping):
                problems.append(finding("SOURCE_UNIVERSE_SOURCE_INVALID", location, "source must be a mapping"))
                continue
            source_path = _safe_relative_path(source.get("path"))
            if source_path is None or source_path in seen:
                problems.append(finding("SOURCE_UNIVERSE_SOURCE_PATH_INVALID", f"{location}.path", "source path must be unique and repository-relative"))
            else:
                seen.add(source_path)
            if source.get("role") not in SOURCE_ROLES:
                problems.append(finding("SOURCE_UNIVERSE_SOURCE_ROLE_INVALID", f"{location}.role", "unsupported source role"))
            if not DIGEST_RE.fullmatch(str(source.get("digest", ""))):
                problems.append(finding("SOURCE_UNIVERSE_SOURCE_DIGEST_INVALID", f"{location}.digest", "sha256 digest is required"))
            if root is not None and source_path is not None:
                current = root / source_path
                if not current.is_file() or not _inside(current, root):
                    problems.append(finding("SOURCE_UNIVERSE_SOURCE_MISSING", source_path, "inspected source no longer exists inside the repository"))
                elif source.get("digest") != file_digest(current):
                    problems.append(finding("SOURCE_UNIVERSE_SOURCE_STALE", source_path, "inspected source changed after universe creation"))
    reports = universe.get("provider_reports", [])
    report_paths: list[str] = []
    if not isinstance(reports, list):
        problems.append(finding("SOURCE_UNIVERSE_PROVIDERS_INVALID", f"{path}.provider_reports", "provider_reports must be a list"))
    else:
        for index, report in enumerate(reports):
            location = f"{path}.provider_reports[{index}]"
            if not isinstance(report, Mapping):
                problems.append(finding("SOURCE_UNIVERSE_PROVIDER_INVALID", location, "provider report must be a mapping"))
                continue
            report_path = _safe_relative_path(report.get("path"))
            if report_path is None or not DIGEST_RE.fullmatch(str(report.get("digest", ""))):
                problems.append(finding("SOURCE_UNIVERSE_PROVIDER_INVALID", location, "provider path and digest are required"))
            elif root is not None:
                report_paths.append(report_path)
                current = root / report_path
                if not current.is_file() or not _inside(current, root) or report.get("digest") != file_digest(current):
                    problems.append(finding("SOURCE_UNIVERSE_PROVIDER_STALE", report_path, "provider report is missing, outside the repository, or changed"))
    change_refs = universe.get("change_refs", [])
    if not isinstance(change_refs, list):
        problems.append(finding("SOURCE_UNIVERSE_CHANGE_REFS_INVALID", f"{path}.change_refs", "change_refs must be a list"))
    else:
        change_ids: set[str] = set()
        for index, change in enumerate(change_refs):
            location = f"{path}.change_refs[{index}]"
            change_id = change.get("id") if isinstance(change, Mapping) else None
            if not isinstance(change_id, str) or not SAFE_ID_RE.fullmatch(change_id) or change_id in change_ids:
                problems.append(finding("SOURCE_UNIVERSE_CHANGE_REF_INVALID", location, "change ref needs a unique kebab-case id"))
            else:
                change_ids.add(change_id)
            if not isinstance(change, Mapping) or not _non_empty(change.get("description")):
                problems.append(finding("SOURCE_UNIVERSE_CHANGE_REF_INVALID", location, "change ref description is required"))
    if root is not None and source_policy is not None and isinstance(sources, list) and isinstance(reports, list):
        expected, rebuild_problems = build_source_universe(root, source_policy, report_paths)
        problems.extend(rebuild_problems)
        if not rebuild_problems:
            actual_entries = {(str(item.get("path")), str(item.get("role")), str(item.get("digest"))) for item in sources if isinstance(item, Mapping)}
            expected_entries = {(str(item["path"]), str(item["role"]), str(item["digest"])) for item in expected["sources"]}
            if actual_entries != expected_entries:
                problems.append(finding("SOURCE_UNIVERSE_POLICY_COVERAGE_MISMATCH", f"{path}.sources", "source entries must exactly cover the current source policy roots"))
    return problems



def source_universe_digest(universe: Mapping[str, Any]) -> str:
    return str(universe.get("universe_digest", _digest_without(universe, "universe_digest")))


def validate_challenge_receipt(receipt: Any, path: str = "challenge_receipt", root: Path | None = None) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    if not isinstance(receipt, Mapping):
        return [finding("CHALLENGE_RECEIPT_INVALID", path, "challenge receipt must be a mapping")]
    if receipt.get("schema_version") != CHALLENGE_RECEIPT_SCHEMA:
        problems.append(finding("CHALLENGE_RECEIPT_SCHEMA_INVALID", path, "unsupported schema_version"))
    for key in ("source_universe_digest", "protocol_digest"):
        if not DIGEST_RE.fullmatch(str(receipt.get(key, ""))):
            problems.append(finding("CHALLENGE_RECEIPT_DIGEST_INVALID", f"{path}.{key}", "sha256 digest is required"))
    visible = receipt.get("visible_inputs")
    if not isinstance(visible, list) or not visible:
        problems.append(finding("CHALLENGE_RECEIPT_INPUTS_EMPTY", f"{path}.visible_inputs", "visible inputs are required"))
    else:
        forbidden_paths = [(root / item).resolve() for item in CHALLENGE_FORBIDDEN_INPUTS] if root is not None else []
        for index, value in enumerate(visible):
            location = f"{path}.visible_inputs[{index}]"
            safe = _safe_relative_path(value)
            if safe is None:
                problems.append(finding("CHALLENGE_RECEIPT_INPUT_UNSAFE", location, "visible input must be a safe repository-relative path"))
                continue
            lexical_forbidden = any(safe == blocked or safe.startswith(blocked + "/") or blocked.startswith(safe + "/") for blocked in CHALLENGE_FORBIDDEN_INPUTS)
            candidate = root / safe if root is not None else None
            resolved = candidate.resolve() if candidate is not None else None
            canonical_forbidden = bool(resolved is not None and any(_paths_overlap(resolved, blocked) for blocked in forbidden_paths))
            symlink = _first_symlink_component(root, safe) if root is not None else None
            if lexical_forbidden or canonical_forbidden or symlink is not None:
                problems.append(finding("CHALLENGE_RECEIPT_CONTAMINATED", location, f"forbidden or symbolic-link challenge input: {value!r}"))
            elif candidate is not None and (not candidate.exists() or not _inside(candidate, root)):
                problems.append(finding("CHALLENGE_RECEIPT_INPUT_MISSING", location, f"visible input is unavailable inside the repository: {value!r}"))
            elif candidate is not None and candidate.is_dir():
                for descendant in candidate.rglob("*"):
                    if descendant.is_symlink() or any(_paths_overlap(descendant.resolve(), blocked) for blocked in forbidden_paths):
                        problems.append(finding("CHALLENGE_RECEIPT_CONTAMINATED", location, f"visible directory contains a symbolic link or forbidden descendant: {descendant.relative_to(root)}"))
                        break
    forbidden = receipt.get("forbidden_inputs")
    normalized_forbidden = {_safe_relative_path(item) for item in forbidden} if isinstance(forbidden, list) else set()
    if not isinstance(forbidden, list) or None in normalized_forbidden or not set(CHALLENGE_FORBIDDEN_INPUTS).issubset(normalized_forbidden):
        problems.append(finding("CHALLENGE_RECEIPT_FORBIDDEN_INCOMPLETE", f"{path}.forbidden_inputs", "all canonical plan, approval, review and existing Wiki paths must be forbidden"))
    isolation = receipt.get("isolation_status")
    if isolation not in {"attested", "unproven"}:
        problems.append(finding("CHALLENGE_RECEIPT_ISOLATION_INVALID", f"{path}.isolation_status", "isolation_status must be attested or unproven"))
    execution = receipt.get("execution")
    if not isinstance(execution, Mapping):
        problems.append(finding("CHALLENGE_RECEIPT_EXECUTION_MISSING", f"{path}.execution", "execution handoff record is required"))
    else:
        producer = execution.get("producer_id")
        challenger = execution.get("challenger_id")
        if not _non_empty(producer) or not _non_empty(challenger) or producer == challenger:
            problems.append(finding("CHALLENGE_RECEIPT_ACTORS_INVALID", f"{path}.execution", "producer_id and challenger_id must be non-empty and distinct"))
        if not _non_empty(execution.get("mechanism")):
            problems.append(finding("CHALLENGE_RECEIPT_MECHANISM_MISSING", f"{path}.execution.mechanism", "isolation mechanism is required"))
        evidence = execution.get("evidence_refs")
        if isolation == "attested" and (not _has_actor_evidence(evidence, producer) or not _has_actor_evidence(evidence, challenger)):
            problems.append(finding("CHALLENGE_RECEIPT_EXECUTION_EVIDENCE_MISSING", f"{path}.execution.evidence_refs", "attested isolation requires canonical history or agent evidence for both actors"))
    return problems


def validate_wiki_challenge(challenge: Any, universe: Mapping[str, Any], path: str = "challenge") -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    if not isinstance(challenge, Mapping):
        return [finding("WIKI_CHALLENGE_INVALID", path, "challenge must be a mapping")]
    if challenge.get("schema_version") != CHALLENGE_SCHEMA:
        problems.append(finding("WIKI_CHALLENGE_SCHEMA_INVALID", path, "unsupported schema_version"))
    if challenge.get("source_universe_digest") != source_universe_digest(universe):
        problems.append(finding("WIKI_CHALLENGE_UNIVERSE_MISMATCH", f"{path}.source_universe_digest", "challenge does not bind the current source universe"))
    if not DIGEST_RE.fullmatch(str(challenge.get("protocol_digest", ""))):
        problems.append(finding("WIKI_CHALLENGE_PROTOCOL_INVALID", f"{path}.protocol_digest", "protocol digest is required"))
    if challenge.get("blind_to_plan") is not True:
        problems.append(finding("WIKI_CHALLENGE_NOT_BLIND", f"{path}.blind_to_plan", "blind_to_plan must be true"))
    try:
        forbidden_fields = _forbidden_shape_fields(challenge, path)
    except ValueError as error:
        problems.append(finding("WIKI_CHALLENGE_RECURSIVE_ALIAS", path, str(error)))
        forbidden_fields = []
    if forbidden_fields:
        problems.append(finding("WIKI_CHALLENGE_PAGE_SHAPE_LEAK", path, f"challenge cannot define page shape: {forbidden_fields}"))
    source_paths = {str(item.get("path")) for item in universe.get("sources", []) if isinstance(item, Mapping)}
    concerns = challenge.get("concerns")
    if not isinstance(concerns, list) or not concerns:
        problems.append(finding("WIKI_CHALLENGE_CONCERNS_EMPTY", f"{path}.concerns", "at least one independently derived concern is required"))
    else:
        seen: set[str] = set()
        for index, concern in enumerate(concerns):
            location = f"{path}.concerns[{index}]"
            if not isinstance(concern, Mapping):
                problems.append(finding("WIKI_CHALLENGE_CONCERN_INVALID", location, "concern must be a mapping"))
                continue
            concern_id = concern.get("id")
            if not isinstance(concern_id, str) or not SAFE_ID_RE.fullmatch(concern_id) or concern_id in seen:
                problems.append(finding("WIKI_CHALLENGE_CONCERN_ID_INVALID", f"{location}.id", "concern id must be unique kebab-case"))
            else:
                seen.add(concern_id)
            for key in ("audience", "reader_task", "why_it_matters"):
                if not _non_empty(concern.get(key)):
                    problems.append(finding("WIKI_CHALLENGE_FIELD_MISSING", f"{location}.{key}", "field is required"))
            if concern.get("risk_level") not in {"core", "normal"}:
                problems.append(finding("WIKI_CHALLENGE_RISK_INVALID", f"{location}.risk_level", "risk_level must be core or normal"))
            signals = concern.get("depth_signals")
            if not isinstance(signals, list):
                problems.append(finding("WIKI_CHALLENGE_DEPTH_INVALID", f"{location}.depth_signals", "depth_signals must be a list"))
            refs = concern.get("source_refs")
            if not isinstance(refs, list) or not refs:
                problems.append(finding("WIKI_CHALLENGE_SOURCES_EMPTY", f"{location}.source_refs", "source refs are required"))
            else:
                for source_ref in refs:
                    source_path = source_ref.get("path") if isinstance(source_ref, Mapping) else source_ref
                    if source_path not in source_paths:
                        problems.append(finding("WIKI_CHALLENGE_SOURCE_OUTSIDE_UNIVERSE", location, f"source not inspected: {source_path!r}"))
    return problems


def challenge_digest(challenge: Mapping[str, Any]) -> str:
    return canonical_digest(challenge)


def validate_wiki_divergence(
    divergence: Any,
    plan: Mapping[str, Any],
    challenge: Mapping[str, Any],
    receipt: Mapping[str, Any] | None = None,
    path: str = "divergence",
) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    if not isinstance(divergence, Mapping):
        return [finding("WIKI_DIVERGENCE_INVALID", path, "divergence must be a mapping")]
    if divergence.get("schema_version") != DIVERGENCE_SCHEMA:
        problems.append(finding("WIKI_DIVERGENCE_SCHEMA_INVALID", path, "unsupported schema_version"))
    if divergence.get("plan_digest") != plan_digest(plan):
        problems.append(finding("WIKI_DIVERGENCE_PLAN_MISMATCH", f"{path}.plan_digest", "divergence does not bind the current plan"))
    if divergence.get("challenge_digest") != challenge_digest(challenge):
        problems.append(finding("WIKI_DIVERGENCE_CHALLENGE_MISMATCH", f"{path}.challenge_digest", "divergence does not bind the current challenge"))
    concern_ids = {str(item.get("id")) for item in challenge.get("concerns", []) if isinstance(item, Mapping)}
    page_ids = {str(page.get("id")) for _, _, page in iter_plan_pages(plan)}
    seen: set[str] = set()
    unresolved: set[str] = set()
    items = divergence.get("items")
    if not isinstance(items, list):
        problems.append(finding("WIKI_DIVERGENCE_ITEMS_INVALID", f"{path}.items", "items must be a list"))
    else:
        for index, item in enumerate(items):
            location = f"{path}.items[{index}]"
            if not isinstance(item, Mapping):
                problems.append(finding("WIKI_DIVERGENCE_ITEM_INVALID", location, "item must be a mapping"))
                continue
            concern_id = item.get("concern_id")
            if concern_id not in concern_ids or concern_id in seen:
                problems.append(finding("WIKI_DIVERGENCE_CONCERN_INVALID", f"{location}.concern_id", "concern must exist and appear once"))
            else:
                seen.add(str(concern_id))
            disposition = item.get("disposition")
            if disposition not in DIVERGENCE_DISPOSITIONS:
                problems.append(finding("WIKI_DIVERGENCE_DISPOSITION_INVALID", f"{location}.disposition", "unsupported disposition"))
            elif disposition in {"deferred", "blocked"} and isinstance(concern_id, str):
                unresolved.add(concern_id)
            linked = item.get("linked_page_ids", [])
            if not isinstance(linked, list) or any(page_id not in page_ids for page_id in linked):
                problems.append(finding("WIKI_DIVERGENCE_PAGE_INVALID", f"{location}.linked_page_ids", "linked pages must exist in the plan"))
            if disposition in {"covered", "merged"} and not linked:
                problems.append(finding("WIKI_DIVERGENCE_COVERAGE_EMPTY", f"{location}.linked_page_ids", "covered or merged concerns need a planned page"))
            if not _non_empty(item.get("rationale")):
                problems.append(finding("WIKI_DIVERGENCE_RATIONALE_MISSING", f"{location}.rationale", "rationale is required"))
    for missing in sorted(concern_ids - seen):
        problems.append(finding("WIKI_DIVERGENCE_CONCERN_MISSING", f"{path}.items", f"missing:{missing}"))
    alternatives = divergence.get("alternatives", [])
    if not isinstance(alternatives, list):
        problems.append(finding("WIKI_DIVERGENCE_ALTERNATIVES_INVALID", f"{path}.alternatives", "alternatives must be a list"))
    integration = divergence.get("integration")
    if not isinstance(integration, Mapping):
        problems.append(finding("WIKI_DIVERGENCE_INTEGRATION_MISSING", f"{path}.integration", "independent integration handoff is required"))
    else:
        integrator = integration.get("integrator_id")
        if not _non_empty(integrator):
            problems.append(finding("WIKI_DIVERGENCE_INTEGRATOR_MISSING", f"{path}.integration.integrator_id", "integrator_id is required"))
        evidence = integration.get("evidence_refs")
        if not _has_actor_evidence(evidence, integrator):
            problems.append(finding("WIKI_DIVERGENCE_INTEGRATION_EVIDENCE_MISSING", f"{path}.integration.evidence_refs", "integration handoff requires canonical history or agent evidence for the integrator"))
        execution = receipt.get("execution") if isinstance(receipt, Mapping) else None
        if isinstance(execution, Mapping) and integrator in {execution.get("producer_id"), execution.get("challenger_id")}:
            problems.append(finding("WIKI_DIVERGENCE_INTEGRATOR_NOT_INDEPENDENT", f"{path}.integration.integrator_id", "integrator must differ from producer and challenger"))
    residual_risks = divergence.get("residual_risks")
    residual_concerns: set[str] = set()
    if not isinstance(residual_risks, list):
        problems.append(finding("WIKI_DIVERGENCE_RESIDUAL_RISKS_INVALID", f"{path}.residual_risks", "residual_risks must be a list"))
    else:
        risk_ids: set[str] = set()
        for index, risk in enumerate(residual_risks):
            location = f"{path}.residual_risks[{index}]"
            risk_id = risk.get("id") if isinstance(risk, Mapping) else None
            if not isinstance(risk_id, str) or not SAFE_ID_RE.fullmatch(risk_id) or risk_id in risk_ids:
                problems.append(finding("WIKI_DIVERGENCE_RESIDUAL_RISK_INVALID", location, "residual risk needs a unique kebab-case id"))
            else:
                risk_ids.add(risk_id)
            linked_concerns = risk.get("linked_concern_ids") if isinstance(risk, Mapping) else None
            if not isinstance(linked_concerns, list) or not linked_concerns or any(item not in concern_ids for item in linked_concerns):
                problems.append(finding("WIKI_DIVERGENCE_RESIDUAL_RISK_CONCERNS_INVALID", f"{location}.linked_concern_ids", "residual risk must link existing concerns"))
            else:
                residual_concerns.update(str(item) for item in linked_concerns)
            if not isinstance(risk, Mapping) or risk.get("status") not in {"open", "accepted", "blocked"}:
                problems.append(finding("WIKI_DIVERGENCE_RESIDUAL_RISK_STATUS_INVALID", f"{location}.status", "status must be open, accepted or blocked"))
            if not isinstance(risk, Mapping) or not _non_empty(risk.get("description")) or not _non_empty(risk.get("next_evidence")):
                problems.append(finding("WIKI_DIVERGENCE_RESIDUAL_RISK_DETAIL_MISSING", location, "description and next_evidence are required"))
    for concern_id in sorted(unresolved - residual_concerns):
        problems.append(finding("WIKI_DIVERGENCE_UNRESOLVED_RISK_MISSING", f"{path}.residual_risks", f"missing:{concern_id}"))
    return problems


def divergence_digest(divergence: Mapping[str, Any]) -> str:
    return canonical_digest(divergence)


def _load_mapping(root: Path, relative: str, code: str) -> tuple[dict | None, list[dict[str, str]]]:
    path = root / relative
    if not path.is_file():
        return None, [finding(f"{code}_MISSING", relative, "required Wiki review artifact is missing")]
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        return None, [finding(f"{code}_READ_FAILED", relative, str(error))]
    if not isinstance(value, Mapping):
        return None, [finding(f"{code}_INVALID", relative, "artifact must be a mapping")]
    return dict(value), []


def load_open_world_artifacts(root: Path) -> tuple[dict | None, dict | None, dict | None, dict | None, list[dict[str, str]]]:
    universe, problems = _load_mapping(root, SOURCE_UNIVERSE_PATH, "SOURCE_UNIVERSE")
    receipt, receipt_problems = _load_mapping(root, CHALLENGE_RECEIPT_PATH, "CHALLENGE_RECEIPT")
    challenge, challenge_problems = _load_mapping(root, CHALLENGE_PATH, "WIKI_CHALLENGE")
    divergence, divergence_problems = _load_mapping(root, DIVERGENCE_PATH, "WIKI_DIVERGENCE")
    return universe, receipt, challenge, divergence, problems + receipt_problems + challenge_problems + divergence_problems


def validate_open_world_bundle(
    root: Path,
    plan: Mapping[str, Any],
    source_policy: Mapping[str, Any] | None = None,
) -> tuple[dict | None, dict | None, dict | None, dict | None, list[dict[str, str]]]:
    universe, receipt, challenge, divergence, problems = load_open_world_artifacts(root)
    if source_policy is None:
        config, config_problems = _load_config(root)
        problems.extend(config_problems)
        source_policy = config.get("source_policy") if isinstance(config, Mapping) else None
    if universe is not None:
        problems.extend(validate_source_universe(universe, root=root, source_policy=source_policy))
    if receipt is not None:
        problems.extend(validate_challenge_receipt(receipt, root=root))
    if universe is not None and receipt is not None and receipt.get("source_universe_digest") != source_universe_digest(universe):
        problems.append(finding("CHALLENGE_RECEIPT_UNIVERSE_MISMATCH", "challenge_receipt.source_universe_digest", "receipt does not bind the current source universe"))
    challenge_valid = False
    if universe is not None and challenge is not None:
        challenge_problems = validate_wiki_challenge(challenge, universe)
        problems.extend(challenge_problems)
        challenge_valid = not challenge_problems
    if receipt is not None and challenge is not None and receipt.get("protocol_digest") != challenge.get("protocol_digest"):
        problems.append(finding("WIKI_CHALLENGE_PROTOCOL_MISMATCH", "challenge.protocol_digest", "challenge and input receipt use different protocols"))
        challenge_valid = False
    if challenge_valid and challenge is not None and divergence is not None:
        problems.extend(validate_wiki_divergence(divergence, plan, challenge, receipt))
    return universe, receipt, challenge, divergence, problems

def iter_plan_pages(plan: Mapping[str, Any]):
    for dimension in plan.get("dimensions", []):
        if not isinstance(dimension, Mapping):
            continue
        for aspect in dimension.get("aspects", []):
            if not isinstance(aspect, Mapping):
                continue
            for page in aspect.get("pages", []):
                if isinstance(page, Mapping):
                    yield dimension, aspect, page


def plan_structure(plan: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": plan.get("schema_version"),
        "project": plan.get("project"),
        "source_policy_digest": plan.get("source_policy_digest"),
        "dimensions": plan.get("dimensions"),
    }


def plan_digest(plan: Mapping[str, Any]) -> str:
    return canonical_digest(plan_structure(plan))


def validate_wiki_plan(plan: Any, path: str = "plan") -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    if not isinstance(plan, Mapping):
        return [finding("WIKI_PLAN_INVALID", path, "plan must be a mapping")]
    if plan.get("schema_version") != PLAN_SCHEMA:
        problems.append(finding("WIKI_PLAN_SCHEMA_INVALID", path, "unsupported schema_version"))
    if not _non_empty(plan.get("project")):
        problems.append(finding("WIKI_PLAN_PROJECT_MISSING", f"{path}.project", "project is required"))
    if not DIGEST_RE.fullmatch(str(plan.get("source_policy_digest", ""))):
        problems.append(finding("WIKI_PLAN_SOURCE_POLICY_DIGEST_INVALID", f"{path}.source_policy_digest", "sha256 digest is required"))

    human_plan = plan.get("human_plan")
    if not isinstance(human_plan, Mapping) or human_plan.get("path") != HUMAN_PLAN_PATH:
        problems.append(finding("WIKI_PLAN_HUMAN_PATH_INVALID", f"{path}.human_plan", f"human review path must be {HUMAN_PLAN_PATH}"))
    elif human_plan.get("digest") is not None:
        problems.append(finding("WIKI_PLAN_HUMAN_DIGEST_EMBEDDED", f"{path}.human_plan.digest", "human review digest belongs in the independent approval receipt"))

    approval = plan.get("approval")
    if not isinstance(approval, Mapping) or approval.get("status") != "pending":
        problems.append(finding("WIKI_PLAN_APPROVAL_INVALID", f"{path}.approval", "producer plan status must remain pending; human approval is a separate receipt"))

    dimensions = plan.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        return problems + [finding("WIKI_PLAN_DIMENSIONS_EMPTY", f"{path}.dimensions", "Agent-inferred dimensions are required")]

    dimension_ids: set[str] = set()
    aspect_ids: set[str] = set()
    page_ids: set[str] = set()
    page_paths: set[str] = set()
    for d_index, dimension in enumerate(dimensions):
        d_path = f"{path}.dimensions[{d_index}]"
        if not isinstance(dimension, Mapping):
            problems.append(finding("WIKI_PLAN_DIMENSION_INVALID", d_path, "dimension must be a mapping"))
            continue
        dimension_id = dimension.get("id")
        if not isinstance(dimension_id, str) or not SAFE_ID_RE.fullmatch(dimension_id):
            problems.append(finding("WIKI_PLAN_DIMENSION_ID_INVALID", f"{d_path}.id", "id must be kebab-case"))
        elif dimension_id in dimension_ids:
            problems.append(finding("WIKI_PLAN_DIMENSION_DUPLICATED", f"{d_path}.id", f"duplicate:{dimension_id}"))
        else:
            dimension_ids.add(dimension_id)
        for key in ("title", "audience", "purpose", "rationale"):
            if not _non_empty(dimension.get(key)):
                problems.append(finding("WIKI_PLAN_DIMENSION_FIELD_MISSING", f"{d_path}.{key}", "field is required"))
        aspects = dimension.get("aspects")
        if not isinstance(aspects, list) or not aspects:
            problems.append(finding("WIKI_PLAN_ASPECTS_EMPTY", f"{d_path}.aspects", "at least one inferred aspect is required"))
            continue
        for a_index, aspect in enumerate(aspects):
            a_path = f"{d_path}.aspects[{a_index}]"
            if not isinstance(aspect, Mapping):
                problems.append(finding("WIKI_PLAN_ASPECT_INVALID", a_path, "aspect must be a mapping"))
                continue
            aspect_id = aspect.get("id")
            if not isinstance(aspect_id, str) or not SAFE_ID_RE.fullmatch(aspect_id):
                problems.append(finding("WIKI_PLAN_ASPECT_ID_INVALID", f"{a_path}.id", "id must be kebab-case"))
            elif aspect_id in aspect_ids:
                problems.append(finding("WIKI_PLAN_ASPECT_DUPLICATED", f"{a_path}.id", f"duplicate:{aspect_id}"))
            else:
                aspect_ids.add(aspect_id)
            for key in ("title", "reader_need", "rationale"):
                if not _non_empty(aspect.get(key)):
                    problems.append(finding("WIKI_PLAN_ASPECT_FIELD_MISSING", f"{a_path}.{key}", "field is required"))
            pages = aspect.get("pages")
            if not isinstance(pages, list):
                problems.append(finding("WIKI_PLAN_PAGES_INVALID", f"{a_path}.pages", "pages must be a list; zero pages is allowed"))
                continue
            for p_index, page in enumerate(pages):
                p_path = f"{a_path}.pages[{p_index}]"
                if not isinstance(page, Mapping):
                    problems.append(finding("WIKI_PLAN_PAGE_INVALID", p_path, "page must be a mapping"))
                    continue
                page_id = page.get("id")
                if not isinstance(page_id, str) or not SAFE_ID_RE.fullmatch(page_id):
                    problems.append(finding("WIKI_PLAN_PAGE_ID_INVALID", f"{p_path}.id", "id must be kebab-case"))
                elif page_id in page_ids:
                    problems.append(finding("WIKI_PLAN_PAGE_ID_DUPLICATED", f"{p_path}.id", f"duplicate:{page_id}"))
                else:
                    page_ids.add(page_id)
                relative = _safe_relative_path(page.get("path"))
                if relative is None or not relative.startswith("docs/wiki/") or not relative.endswith(".md"):
                    problems.append(finding("WIKI_PLAN_PAGE_PATH_INVALID", f"{p_path}.path", "page path must be a safe docs/wiki/*.md path"))
                elif relative in {"docs/wiki/WIKI.md", "docs/wiki/INDEX.md", "docs/wiki/FRAMEWORK.md", f"docs/wiki/{dimension_id}/README.md"}:
                    problems.append(finding("WIKI_PLAN_PAGE_PATH_RESERVED", f"{p_path}.path", "generated navigation paths cannot be planned as content pages"))
                elif relative in page_paths:
                    problems.append(finding("WIKI_PLAN_PAGE_PATH_DUPLICATED", f"{p_path}.path", f"duplicate:{relative}"))
                else:
                    page_paths.add(relative)
                for key in ("title", "reader_task", "purpose"):
                    if not _non_empty(page.get(key)):
                        problems.append(finding("WIKI_PLAN_PAGE_FIELD_MISSING", f"{p_path}.{key}", "field is required"))
                guidance = page.get("guidance")
                if guidance is not None and (not isinstance(guidance, str) or not SAFE_ID_RE.fullmatch(guidance)):
                    problems.append(finding("WIKI_PLAN_GUIDANCE_INVALID", f"{p_path}.guidance", "guidance must be a safe optional label"))
                sources = page.get("sources")
                if not isinstance(sources, list) or not sources:
                    problems.append(finding("WIKI_PLAN_PAGE_SOURCES_EMPTY", f"{p_path}.sources", "planned content needs at least one source"))
                else:
                    for s_index, source in enumerate(sources):
                        _, source_problems = _normalize_ref(source, f"{p_path}.sources[{s_index}]")
                        problems.extend(source_problems)
    return problems


def load_wiki_plan(root: Path, relative: str = PLAN_PATH) -> tuple[dict | None, list[dict[str, str]]]:
    path = root / relative
    if not path.is_file():
        return None, [finding("WIKI_PLAN_MISSING", relative, "Agent must infer and write a structure plan before generation")]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        return None, [finding("WIKI_PLAN_READ_FAILED", relative, str(error))]
    problems = validate_wiki_plan(data, relative)
    return (dict(data) if isinstance(data, Mapping) else None), problems


def validate_plan_approval(root: Path, plan: Mapping[str, Any], source_policy: Mapping[str, Any]) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = validate_human_readable_contract(root)
    universe, receipt, challenge, divergence, bundle_problems = validate_open_world_bundle(root, plan, source_policy)
    problems.extend(bundle_problems)
    approval, approval_problems = _load_mapping(root, PLAN_APPROVAL_PATH, "WIKI_PLAN_APPROVAL_RECEIPT")
    problems.extend(approval_problems)
    if approval is None:
        problems.append(finding("WIKI_PLAN_NOT_APPROVED", PLAN_APPROVAL_PATH, "an independent human approval receipt is required before Wiki generation"))
        return problems
    if approval.get("schema_version") != PLAN_APPROVAL_SCHEMA:
        problems.append(finding("WIKI_PLAN_APPROVAL_SCHEMA_INVALID", PLAN_APPROVAL_PATH, "unsupported approval receipt schema_version"))
    if approval.get("status") != "approved":
        problems.append(finding("WIKI_PLAN_NOT_APPROVED", f"{PLAN_APPROVAL_PATH}.status", "human approval is required before Wiki generation"))
    if approval.get("plan_digest") != plan_digest(plan):
        problems.append(finding("WIKI_PLAN_APPROVAL_STALE", f"{PLAN_APPROVAL_PATH}.plan_digest", "approval receipt does not bind the current plan"))
    expected_policy = canonical_digest(dict(source_policy))
    if plan.get("source_policy_digest") != expected_policy:
        problems.append(finding("WIKI_PLAN_SOURCE_POLICY_CHANGED", "source_policy_digest", "source policy changed after the plan was prepared"))
    if universe is not None and universe.get("source_policy_digest") != expected_policy:
        problems.append(finding("SOURCE_UNIVERSE_POLICY_CHANGED", "source_universe.source_policy_digest", "source universe does not match the current source policy"))
    if universe is not None and approval.get("source_universe_digest") != source_universe_digest(universe):
        problems.append(finding("WIKI_PLAN_UNIVERSE_APPROVAL_STALE", f"{PLAN_APPROVAL_PATH}.source_universe_digest", "approval receipt does not bind the current source universe"))
    if challenge is not None and approval.get("challenge_digest") != challenge_digest(challenge):
        problems.append(finding("WIKI_PLAN_CHALLENGE_APPROVAL_STALE", f"{PLAN_APPROVAL_PATH}.challenge_digest", "approval receipt does not bind the current challenge"))
    if divergence is not None and approval.get("divergence_digest") != divergence_digest(divergence):
        problems.append(finding("WIKI_PLAN_DIVERGENCE_APPROVAL_STALE", f"{PLAN_APPROVAL_PATH}.divergence_digest", "approval receipt does not bind the current divergence ledger"))
    adequacy_status = approval.get("adequacy_status")
    if adequacy_status not in ADEQUACY_STATUSES:
        problems.append(finding("WIKI_PLAN_ADEQUACY_STATUS_INVALID", f"{PLAN_APPROVAL_PATH}.adequacy_status", "adequacy_status must be validated or provisional"))
    elif adequacy_status != "provisional":
        problems.append(finding("WIKI_PLAN_ADEQUACY_OVERSTATED", f"{PLAN_APPROVAL_PATH}.adequacy_status", "repository receipts are attestations, not independently verified execution; adequacy remains provisional"))
    human = plan.get("human_plan", {})
    human_path = human.get("path")
    human_file = root / HUMAN_PLAN_PATH
    if human_path != HUMAN_PLAN_PATH or not human_file.is_file():
        problems.append(finding("WIKI_PLAN_HUMAN_VIEW_MISSING", str(human_path or ""), f"human-readable review must exist at {HUMAN_PLAN_PATH}"))
    elif universe is not None and challenge is not None and divergence is not None:
        rendered = render_plan_markdown(plan, source_policy, universe, challenge, divergence, receipt)
        if human_file.read_text(encoding="utf-8") != rendered:
            problems.append(finding("WIKI_PLAN_HUMAN_VIEW_STALE", HUMAN_PLAN_PATH, "human-readable review was not rendered from the current open-world artifacts"))
        human_digest = file_digest(human_file)
        if approval.get("human_plan_digest") != human_digest:
            problems.append(finding("WIKI_PLAN_HUMAN_VIEW_APPROVAL_STALE", f"{PLAN_APPROVAL_PATH}.human_plan_digest", "approval receipt does not bind the reviewed Markdown"))
    for key in ("approved_by", "approved_at", "decision_ref"):
        if not _non_empty(approval.get(key)):
            problems.append(finding("WIKI_PLAN_APPROVAL_EVIDENCE_MISSING", f"{PLAN_APPROVAL_PATH}.{key}", "independent human approval evidence is required"))
    return problems


def render_plan_markdown(
    plan: Mapping[str, Any],
    source_policy: Mapping[str, Any],
    universe: Mapping[str, Any] | None = None,
    challenge: Mapping[str, Any] | None = None,
    divergence: Mapping[str, Any] | None = None,
    receipt: Mapping[str, Any] | None = None,
) -> str:
    lines = [
        f"# {plan.get('project', '项目')} 结构与充分性审阅",
        "",
        "> 请同时审核结构提案、独立遗漏挑战、差异处置和剩余风险。批准前不会生成正文。",
        "",
        "## 输入边界",
        "",
    ]
    for role in ("fact_roots", "material_roots", "operation_roots"):
        values = source_policy.get(role, []) if isinstance(source_policy, Mapping) else []
        lines.append(f"- {role}: {', '.join(f'`{value}`' for value in values) or '未配置'}")
    if universe is not None:
        lines.extend([
            f"- 可访问来源：{len(universe.get('sources', []))} 个",
            f"- Evidence Provider：{len(universe.get('provider_reports', []))} 个",
            f"- 排除项：{len(universe.get('excluded', []))} 个",
        ])
    if receipt is not None:
        execution = receipt.get("execution", {})
        lines.extend([
            f"- 挑战隔离：{receipt.get('isolation_status', 'unproven')}",
            f"- Producer：{execution.get('producer_id', '未登记')}",
            f"- Challenger：{execution.get('challenger_id', '未登记')}",
            f"- 隔离依据：{', '.join(execution.get('evidence_refs', [])) or '未登记'}",
        ])
    if divergence is not None:
        integration = divergence.get("integration", {})
        lines.extend([
            f"- Integrator：{integration.get('integrator_id', '未登记')}",
            f"- 裁决依据：{', '.join(integration.get('evidence_refs', [])) or '未登记'}",
        ])
    lines.extend(["", "## 结构提案"])
    for dimension in plan.get("dimensions", []):
        lines.extend([
            "",
            f"### {dimension['title']}",
            "",
            f"- **目标读者**：{dimension['audience']}",
            f"- **目的**：{dimension['purpose']}",
            f"- **形成理由**：{dimension['rationale']}",
        ])
        for aspect in dimension.get("aspects", []):
            lines.extend([
                "",
                f"#### {aspect['title']}",
                "",
                f"- **读者需要**：{aspect['reader_need']}",
                f"- **划分理由**：{aspect['rationale']}",
            ])
            pages = aspect.get("pages", [])
            if not pages:
                lines.append("- **页面安排**：不生成页面；理由见上。")
                continue
            lines.extend(["", "| 页面 | 读者任务 | 用途 | 写作方向 | 来源 |", "|---|---|---|---|---|"])
            for page in pages:
                sources = "、".join(f"`{item['path']}` {item['locator']}" for item in page.get("sources", []))
                lines.append(f"| `{page['path']}`<br>{page['title']} | {page['reader_task']} | {page['purpose']} | {page.get('guidance', '按项目决定')} | {sources} |")
    if challenge is not None:
        lines.extend(["", "## 独立挑战", "", "| 问题 | 读者 | 风险 | 深度信号 | 为什么重要 | 来源依据 |", "|---|---|---|---|---|---|"])
        for concern in challenge.get("concerns", []):
            source_refs = "、".join(f"`{item.get('path') if isinstance(item, Mapping) else item}`" for item in concern.get("source_refs", []))
            lines.append(f"| `{concern['id']}`：{concern['reader_task']} | {concern['audience']} | {concern['risk_level']} | {', '.join(concern.get('depth_signals', [])) or '—'} | {concern['why_it_matters']} | {source_refs or '—'} |")
    if divergence is not None:
        lines.extend(["", "## 差异处置", "", "| 挑战项 | 处置 | 关联页面 | 依据 |", "|---|---|---|---|"])
        for item in divergence.get("items", []):
            lines.append(f"| `{item['concern_id']}` | {item['disposition']} | {', '.join(item.get('linked_page_ids', [])) or '—'} | {item['rationale']} |")
        alternatives = divergence.get("alternatives", [])
        lines.extend(["", "### 被考虑的替代方案", ""])
        lines.extend(f"- {value}" for value in alternatives) if alternatives else lines.append("（无登记的替代方案。）")
        residual_risks = divergence.get("residual_risks", [])
        lines.extend(["", "### 剩余风险", ""])
        if residual_risks:
            lines.extend(["| 风险 | 状态 | 关联挑战 | 下一证据 |", "|---|---|---|---|"])
            for risk in residual_risks:
                lines.append(f"| `{risk['id']}`：{risk['description']} | {risk['status']} | {', '.join(risk.get('linked_concern_ids', []))} | {risk['next_evidence']} |")
        else:
            lines.append("（无登记的剩余风险。）")
    lines.extend([
        "",
        "## 审核结论",
        "",
        "请确认结构是否覆盖独立挑战中的真实问题，差异处置是否合理，以及剩余风险是否可以接受。",
        "",
    ])
    return "\n".join(lines)


def _role_roots(source_policy: Mapping[str, Any]) -> dict[str, list[str]]:
    return {role: list(source_policy.get(f"{role}_roots", []) or []) for role in SOURCE_ROLES}


def _extract_excerpt(text: str, locator: str) -> str | None:
    lines = text.splitlines()
    match = LINE_LOCATOR_RE.fullmatch(locator)
    if match:
        start = int(match.group(1))
        end = int(match.group(2) or start)
        if start < 1 or end < start or start > len(lines):
            return None
        return "\n".join(lines[start - 1 : min(end, len(lines))])
    if locator.startswith("#"):
        heading = locator[1:].strip()
        for index, line in enumerate(lines):
            if re.match(r"^#{1,6}\s+" + re.escape(heading) + r"\s*#*$", line):
                level = len(line) - len(line.lstrip("#"))
                end = index + 1
                while end < len(lines):
                    next_match = re.match(r"^(#+)\s+", lines[end])
                    if next_match and len(next_match.group(1)) <= level:
                        break
                    end += 1
                return "\n".join(lines[index:end]).strip()
    return None


def build_evidence_bundle(root: Path, plan: Mapping[str, Any], source_policy: Mapping[str, Any]) -> tuple[dict, list[dict[str, str]]]:
    problems = validate_wiki_plan(plan)
    universe, receipt, challenge, divergence, bundle_problems = validate_open_world_bundle(root, plan, source_policy)
    problems.extend(bundle_problems)
    if problems or universe is None or challenge is None or divergence is None:
        return {}, problems
    roots = _role_roots(source_policy)
    source_entries: dict[tuple[str, str], dict[str, Any]] = {}
    page_refs: dict[str, list[dict[str, str]]] = {}
    for _, _, page in iter_plan_pages(plan):
        page_id = str(page["id"])
        page_refs[page_id] = []
        for index, raw_ref in enumerate(page.get("sources", [])):
            ref, ref_problems = _normalize_ref(raw_ref, f"pages[{page_id}].sources[{index}]")
            problems.extend(ref_problems)
            if ref is None:
                continue
            path_text, role, locator = ref["path"], ref["role"], ref["locator"]
            source = (root / path_text).resolve()
            allowed = any(_inside(source, root / prefix) for prefix in roots.get(role, []))
            if not allowed:
                problems.append(finding("EVIDENCE_SOURCE_NOT_ALLOWED", path_text, f"path is outside {role}_roots"))
                continue
            if not source.is_file():
                problems.append(finding("EVIDENCE_SOURCE_MISSING", path_text, "source file does not exist"))
                continue
            try:
                text = source.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as error:
                problems.append(finding("EVIDENCE_SOURCE_READ_FAILED", path_text, str(error)))
                continue
            excerpt = _extract_excerpt(text, locator)
            if excerpt is None:
                problems.append(finding("EVIDENCE_LOCATOR_NOT_FOUND", path_text, f"locator not found: {locator}"))
                continue
            key = (path_text, role)
            entry = source_entries.setdefault(key, {"path": path_text, "digest": file_digest(source), "role": role, "excerpts": []})
            excerpt_digest = canonical_digest({"path": path_text, "locator": locator, "text": excerpt})
            if not any(item["locator"] == locator for item in entry["excerpts"]):
                entry["excerpts"].append({"locator": locator, "text": excerpt, "digest": excerpt_digest})
            page_refs[page_id].append({"path": path_text, "role": role, "locator": locator, "digest": excerpt_digest})
    bundle = {
        "schema_version": EVIDENCE_BUNDLE_SCHEMA,
        "plan_digest": plan_digest(plan),
        "source_universe_digest": source_universe_digest(universe),
        "challenge_digest": challenge_digest(challenge),
        "divergence_digest": divergence_digest(divergence),
        "sources": sorted(source_entries.values(), key=lambda item: (item["path"], item["role"])),
        "page_refs": page_refs,
    }
    bundle["evidence_digest"] = canonical_digest(bundle)
    return ({}, problems) if problems else (bundle, problems)


def _source_digest_map(snapshot: Mapping[str, Any]) -> dict[str, str]:
    value = snapshot.get("source_digests", {})
    return {str(path): str(digest) for path, digest in value.items()} if isinstance(value, Mapping) else {}


def validate_review_ledger(ledger: Any, path: str = "ledger") -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    if not isinstance(ledger, Mapping):
        return [finding("REVIEW_LEDGER_INVALID", path, "ledger must be a mapping")]
    if ledger.get("schema_version") != REVIEW_LEDGER_SCHEMA:
        problems.append(finding("REVIEW_LEDGER_SCHEMA_INVALID", path, "unsupported schema_version"))
    for key in ("review_id", "plan_digest", "protocol_digest", "source_universe_digest", "challenge_digest", "divergence_digest"):
        if not _non_empty(ledger.get(key)):
            problems.append(finding("REVIEW_LEDGER_FIELD_MISSING", f"{path}.{key}", "field is required"))
    pages = ledger.get("pages")
    if not isinstance(pages, list):
        problems.append(finding("REVIEW_LEDGER_PAGES_INVALID", f"{path}.pages", "must be a list"))
    else:
        seen: set[str] = set()
        for index, page in enumerate(pages):
            location = f"{path}.pages[{index}]"
            page_id = page.get("page_id") if isinstance(page, Mapping) else None
            if not isinstance(page_id, str) or not SAFE_ID_RE.fullmatch(page_id):
                problems.append(finding("REVIEW_LEDGER_PAGE_ID_INVALID", f"{location}.page_id", "invalid page_id"))
            elif page_id in seen:
                problems.append(finding("REVIEW_LEDGER_PAGE_DUPLICATED", f"{location}.page_id", f"duplicate:{page_id}"))
            else:
                seen.add(page_id)
            if not isinstance(page, Mapping) or page.get("disposition") not in DISPOSITIONS:
                problems.append(finding("REVIEW_LEDGER_DISPOSITION_INVALID", f"{location}.disposition", "unsupported disposition"))
    return problems


def _validate_review(review: Any, expected: Mapping[str, Any] | None, consumer: bool, path: str) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    schema = CONSUMER_REVIEW_SCHEMA if consumer else SEMANTIC_REVIEW_SCHEMA
    prefix = "CONSUMER_REVIEW" if consumer else "SEMANTIC_REVIEW"
    if not isinstance(review, Mapping):
        return [finding(f"{prefix}_INVALID", path, "review must be a mapping")]
    if review.get("schema_version") != schema:
        problems.append(finding(f"{prefix}_SCHEMA_INVALID", path, "unsupported schema_version"))
    digest_keys = ["plan_digest", "draft_digest", "evidence_digest"]
    if consumer:
        digest_keys.extend(["source_universe_digest", "challenge_digest", "divergence_digest"])
    for key in digest_keys:
        value = review.get(key)
        if not isinstance(value, str) or not DIGEST_RE.fullmatch(value):
            problems.append(finding(f"{prefix}_FIELD_INVALID", f"{path}.{key}", "missing or invalid digest"))
    if expected:
        for key in digest_keys:
            if key in expected and review.get(key) != expected[key]:
                problems.append(finding(f"{prefix}_DIGEST_MISMATCH", f"{path}.{key}", "digest does not match current inputs"))
    provider = review.get("provider")
    if not isinstance(provider, Mapping) or not all(_non_empty(provider.get(key)) for key in ("name", "model", "prompt_version")):
        problems.append(finding(f"{prefix}_PROVIDER_INVALID", f"{path}.provider", "provider name, model and prompt_version are required"))
    records = review.get("cases" if consumer else "findings")
    seen: set[str] = set()
    origins: set[str] = set()
    page_ids = {str(value) for value in (expected or {}).get("page_ids", [])}
    if not isinstance(records, list) or not records:
        problems.append(finding(f"{prefix}_RECORDS_EMPTY", path, "review records are required"))
    else:
        for index, record in enumerate(records):
            location = f"{path}.{index}"
            if not isinstance(record, Mapping):
                problems.append(finding(f"{prefix}_RECORD_INVALID", location, "record must be a mapping"))
                continue
            if consumer:
                record_id = record.get("task_id")
                origin = record.get("origin")
                if not isinstance(record_id, str) or not SAFE_ID_RE.fullmatch(record_id) or record_id in seen:
                    problems.append(finding(f"{prefix}_TASK_ID_INVALID", f"{location}.task_id", "task id must be unique kebab-case"))
                else:
                    seen.add(record_id)
                if origin not in {"plan", "challenge", "external", "risk", "change"}:
                    problems.append(finding(f"{prefix}_ORIGIN_INVALID", f"{location}.origin", "unsupported task origin"))
                else:
                    origins.add(str(origin))
                expected_origin = (expected or {}).get("task_origins", {}).get(str(record_id))
                if expected_origin is not None and origin != expected_origin:
                    problems.append(finding(f"{prefix}_ORIGIN_MISMATCH", f"{location}.origin", f"task {record_id} must use origin {expected_origin}"))
                linked = record.get("linked_page_ids")
                if not isinstance(linked, list) or not linked or (page_ids and any(str(value) not in page_ids for value in linked)):
                    problems.append(finding(f"{prefix}_LINKED_PAGES_INVALID", f"{location}.linked_page_ids", "linked pages must exist in the plan"))
            else:
                record_id = record.get("page_id")
                if not isinstance(record_id, str) or not SAFE_ID_RE.fullmatch(record_id) or record_id in seen:
                    problems.append(finding(f"{prefix}_PAGE_ID_INVALID", f"{location}.page_id", "page id must be unique kebab-case"))
                else:
                    seen.add(record_id)
            verdict_key = "verdict" if consumer else "proposed_verdict"
            if record.get(verdict_key) not in VERDICTS:
                problems.append(finding(f"{prefix}_VERDICT_INVALID", f"{location}.{verdict_key}", "unsupported verdict"))
            if record.get("confidence") not in CONFIDENCES:
                problems.append(finding(f"{prefix}_CONFIDENCE_INVALID", f"{location}.confidence", "unsupported confidence"))
            if consumer:
                for key in ("audience", "reader_task", "reader_answer", "repair_hint"):
                    if not _non_empty(record.get(key)):
                        problems.append(finding(f"{prefix}_FIELD_MISSING", f"{location}.{key}", "field must be non-empty"))
                findings_value = record.get("findings")
                if not isinstance(findings_value, list) or not findings_value or any(not _non_empty(item) for item in findings_value):
                    problems.append(finding(f"{prefix}_FINDINGS_INVALID", f"{location}.findings", "must be a non-empty list"))
                evidence_keys = ("page_evidence", "source_evidence")
            else:
                for key in ("finding", "revision_hint"):
                    if not _non_empty(record.get(key)):
                        problems.append(finding(f"{prefix}_EXPLANATION_MISSING", f"{location}.{key}", "must be non-empty"))
                evidence_keys = ("draft_evidence", "source_evidence")
            for key in evidence_keys:
                evidence = record.get(key)
                if not isinstance(evidence, list) or not evidence:
                    problems.append(finding(f"{prefix}_EVIDENCE_INVALID", f"{location}.{key}", "must be a non-empty list"))
    expected_ids = (expected or {}).get("task_ids" if consumer else "page_ids")
    if expected_ids is not None:
        expected_set = {str(value) for value in expected_ids}
        for value in sorted(expected_set - seen):
            problems.append(finding(f"{prefix}_{'TASK' if consumer else 'PAGE'}_MISSING", path, f"missing:{value}"))
        if not consumer:
            for value in sorted(seen - expected_set):
                problems.append(finding(f"{prefix}_PAGE_UNEXPECTED", path, f"unexpected:{value}"))
    if consumer:
        falsifications = review.get("attempted_falsifications")
        if not isinstance(falsifications, list) or not falsifications:
            problems.append(finding("CONSUMER_REVIEW_FALSIFICATION_EMPTY", f"{path}.attempted_falsifications", "at least one attempted falsification is required"))
        else:
            for index, attempt in enumerate(falsifications):
                if not isinstance(attempt, Mapping) or not all(_non_empty(attempt.get(key)) for key in ("claim", "counterevidence", "outcome")):
                    problems.append(finding("CONSUMER_REVIEW_FALSIFICATION_INVALID", f"{path}.attempted_falsifications[{index}]", "claim, counterevidence and outcome are required"))
        most_likely = review.get("most_likely_wrong_page")
        if not isinstance(most_likely, str) or (page_ids and most_likely not in page_ids):
            problems.append(finding("CONSUMER_REVIEW_SUSPECT_PAGE_INVALID", f"{path}.most_likely_wrong_page", "a planned page id is required"))
        adequacy = review.get("adequacy_status")
        if adequacy not in ADEQUACY_STATUSES:
            problems.append(finding("CONSUMER_REVIEW_ADEQUACY_INVALID", f"{path}.adequacy_status", "adequacy_status must be validated or provisional"))
        elif adequacy != "provisional":
            problems.append(finding("CONSUMER_REVIEW_ADEQUACY_OVERSTATED", f"{path}.adequacy_status", "repository execution receipts are attestations; adequacy remains provisional without an external verifier"))
        if adequacy == "validated" and "external" not in origins:
            problems.append(finding("CONSUMER_REVIEW_EXTERNAL_TASK_MISSING", f"{path}.cases", "validated adequacy requires an external task"))
    return problems


def validate_semantic_review(review: Any, expected: Mapping[str, Any] | None = None, path: str = "review") -> list[dict[str, str]]:
    return _validate_review(review, expected, False, path)


def validate_consumer_review(review: Any, expected: Mapping[str, Any] | None = None, path: str = "consumer_review") -> list[dict[str, str]]:
    return _validate_review(review, expected, True, path)


def build_review_ledger(current: Mapping[str, Any], previous: Mapping[str, Any] | None = None) -> dict:
    current_pages = {str(item["page_id"]): item for item in current.get("pages", [])}
    previous_pages = {str(item["page_id"]): item for item in (previous or {}).get("pages", [])}
    global_changed = bool(previous) and any(
        current.get(key) != previous.get(key)
        for key in ("plan_digest", "protocol_digest", "source_universe_digest", "challenge_digest", "divergence_digest")
    )
    previous_sources = _source_digest_map(previous or {})
    current_sources = _source_digest_map(current)
    changed_sources = {path for path in set(previous_sources) | set(current_sources) if previous_sources.get(path) != current_sources.get(path)}
    entries: list[dict[str, Any]] = []
    for page_id, item in current_pages.items():
        prior = previous_pages.get(page_id)
        if prior is None:
            disposition, reason = "new", "page_not_in_previous_review"
        elif global_changed:
            disposition, reason = "review_required", "global_review_inputs_changed"
        elif prior.get("draft_digest") != item.get("draft_digest"):
            disposition, reason = "review_required", "page_draft_changed"
        elif set(_source_digest_map(prior)) & changed_sources:
            disposition, reason = "review_required", "page_source_changed"
        elif prior.get("source_digests", {}) != item.get("source_digests", {}):
            disposition, reason = "review_required", "page_sources_changed"
        elif prior.get("acceptance_status") != "accepted":
            disposition, reason = "review_required", "previous_page_not_accepted"
        else:
            disposition, reason = "reused", "page_and_sources_unchanged"
        entry = dict(item)
        entry.update({"page_id": page_id, "disposition": disposition, "reason": reason})
        entries.append(entry)
    ledger = {
        "schema_version": REVIEW_LEDGER_SCHEMA,
        "review_id": str(current.get("review_id", "current-review")),
        "parent_review_id": (previous or {}).get("review_id"),
        "plan_digest": current.get("plan_digest"),
        "protocol_digest": current.get("protocol_digest"),
        "source_universe_digest": current.get("source_universe_digest"),
        "challenge_digest": current.get("challenge_digest"),
        "divergence_digest": current.get("divergence_digest"),
        "source_digests": current_sources,
        "pages": entries,
        "invalidated": [
            {"page_id": page_id, "reason": "page_removed"}
            for page_id in sorted(set(previous_pages) - set(current_pages))
        ],
    }
    return ledger


def write_review_artifact(root: Path, review_id: str, filename: str, payload: Mapping[str, Any]) -> Path:
    if not SAFE_ID_RE.fullmatch(review_id):
        raise ValueError("invalid review_id")
    if filename not in {"evidence.yaml", "semantic_review.yaml", "consumer_review.yaml", "ledger.yaml", "human-review.md"}:
        raise ValueError("unsupported review artifact")
    target = root / REVIEW_ROOT / review_id / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    if filename.endswith(".yaml"):
        target.write_text(yaml.safe_dump(dict(payload), allow_unicode=True, sort_keys=False), encoding="utf-8")
    else:
        target.write_text(str(payload.get("content", "")), encoding="utf-8")
    return target


def digest_paths(root: Path, relative_paths: list[str]) -> str:
    entries = []
    for relative in sorted(relative_paths):
        safe = _safe_relative_path(relative)
        if safe is None:
            raise ValueError(f"unsafe path: {relative}")
        path = root / safe
        if not path.is_file():
            raise FileNotFoundError(safe)
        entries.append({"path": safe, "digest": file_digest(path)})
    return canonical_digest(entries)


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_config(root: Path):
    from wiki_config import load_and_validate

    return load_and_validate(root)


def _page_ids(plan: Mapping[str, Any]) -> list[str]:
    return [str(page["id"]) for _, _, page in iter_plan_pages(plan)]

def _review_task_contract(
    plan: Mapping[str, Any],
    challenge: Mapping[str, Any],
    universe: Mapping[str, Any] | None = None,
    divergence: Mapping[str, Any] | None = None,
) -> dict[str, str]:
    tasks = {f"plan-{page_id}": "plan" for page_id in _page_ids(plan)}
    tasks.update({f"challenge-{item['id']}": "challenge" for item in challenge.get("concerns", []) if isinstance(item, Mapping) and item.get("id")})
    if isinstance(divergence, Mapping):
        tasks.update({f"risk-{item['id']}": "risk" for item in divergence.get("residual_risks", []) if isinstance(item, Mapping) and item.get("id")})
    if isinstance(universe, Mapping):
        tasks.update({f"change-{item['id']}": "change" for item in universe.get("change_refs", []) if isinstance(item, Mapping) and item.get("id")})
    return tasks


def _task_ids(
    plan: Mapping[str, Any],
    challenge: Mapping[str, Any],
    universe: Mapping[str, Any] | None = None,
    divergence: Mapping[str, Any] | None = None,
) -> list[str]:
    return list(_review_task_contract(plan, challenge, universe, divergence))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wiki structure plan and review utilities.")
    sub = parser.add_subparsers(dest="command", required=True)

    universe_parser = sub.add_parser("build-universe")
    universe_parser.add_argument("--root", default=".")
    universe_parser.add_argument("--output", default=SOURCE_UNIVERSE_PATH)
    universe_parser.add_argument("--provider-report", action="append", default=[])

    open_world_parser = sub.add_parser("validate-open-world")
    open_world_parser.add_argument("--root", default=".")
    open_world_parser.add_argument("--plan", default=PLAN_PATH)

    validate = sub.add_parser("validate-plan")
    validate.add_argument("--root", default=".")
    validate.add_argument("--plan", default=PLAN_PATH)
    validate.add_argument("--require-approved", action="store_true")

    render = sub.add_parser("render-plan")
    render.add_argument("--root", default=".")
    render.add_argument("--plan", default=PLAN_PATH)
    render.add_argument("--output", default=HUMAN_PLAN_PATH)

    evidence = sub.add_parser("build-evidence")
    evidence.add_argument("--root", default=".")
    evidence.add_argument("--plan", default=PLAN_PATH)
    evidence.add_argument("--output", default=None)

    ledger = sub.add_parser("ledger")
    ledger.add_argument("--current", required=True)
    ledger.add_argument("--previous", default=None)
    ledger.add_argument("--output", default=None)

    for name in ("validate-review", "validate-consumer-review"):
        review = sub.add_parser(name)
        review.add_argument("--review", required=True)
        review.add_argument("--root", default=".")
        review.add_argument("--plan", default=None)
        review.add_argument("--plan-digest", default=None)
        review.add_argument("--draft-digest", default=None)
        review.add_argument("--evidence-digest", default=None)
        review.add_argument("--source-universe-digest", default=None)
        review.add_argument("--challenge-digest", default=None)
        review.add_argument("--divergence-digest", default=None)

    digest = sub.add_parser("digest")
    digest.add_argument("--root", default=".")
    digest.add_argument("paths", nargs="+")
    readable = sub.add_parser("check-readable")
    readable.add_argument("--root", default=".")
    readable.add_argument("--wiki-root", default="docs/wiki")

    args = parser.parse_args(argv)
    root = Path(getattr(args, "root", ".")).resolve()
    if args.command == "build-universe":
        config, problems = _load_config(root)
        universe = {}
        if config is not None and not problems:
            universe, problems = build_source_universe(root, config["source_policy"], args.provider_report)
        if not problems:
            output = root / args.output
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(yaml.safe_dump(universe, allow_unicode=True, sort_keys=False), encoding="utf-8")
        payload = {"ok": not problems, "output": args.output if not problems else None, "summary": {"source_count": len(universe.get("sources", [])), "provider_count": len(universe.get("provider_reports", [])), "excluded_count": len(universe.get("excluded", [])), "universe_digest": universe.get("universe_digest")}, "findings": problems}
    elif args.command == "validate-open-world":
        plan, problems = load_wiki_plan(root, args.plan)
        artifacts = {}
        if plan is not None and not problems:
            universe, receipt, challenge, divergence, bundle_problems = validate_open_world_bundle(root, plan)
            problems.extend(bundle_problems)
            artifacts = {"source_universe": universe, "challenge_receipt": receipt, "challenge": challenge, "divergence": divergence}
        payload = {"ok": not problems, "artifacts": artifacts, "findings": problems}
    elif args.command in {"validate-plan", "render-plan", "build-evidence"}:
        plan, problems = load_wiki_plan(root, args.plan)
        config, config_findings = _load_config(root)
        problems += config_findings
        problems += validate_human_readable_contract(root)
        if args.command == "validate-plan":
            if plan is not None and config is not None and args.require_approved and not problems:
                problems += validate_plan_approval(root, plan, config["source_policy"])
            payload = {"ok": not problems, "plan": plan, "findings": problems}
        elif args.command == "render-plan":
            output = root / args.output
            universe = receipt = challenge = divergence = None
            if plan is not None and config is not None and not problems:
                universe, receipt, challenge, divergence, bundle_problems = validate_open_world_bundle(root, plan, config["source_policy"])
                problems.extend(bundle_problems)
            if plan is not None and config is not None and universe is not None and challenge is not None and divergence is not None and not problems:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(render_plan_markdown(plan, config["source_policy"], universe, challenge, divergence, receipt), encoding="utf-8")
            payload = {"ok": not problems, "output": args.output if not problems else None, "findings": problems}
        else:
            bundle = {}
            if plan is not None and config is not None and not problems:
                problems += validate_plan_approval(root, plan, config["source_policy"])
            if plan is not None and config is not None and not problems:
                bundle, problems = build_evidence_bundle(root, plan, config["source_policy"])
            if args.output and not problems:
                output = root / args.output
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(yaml.safe_dump(bundle, allow_unicode=True, sort_keys=False), encoding="utf-8")
            payload = {"ok": not problems, "bundle": bundle, "findings": problems}
    elif args.command == "ledger":
        current = _load_yaml(Path(args.current))
        previous = _load_yaml(Path(args.previous)) if args.previous else None
        result = build_review_ledger(current, previous)
        problems = validate_review_ledger(result)
        if args.output and not problems:
            Path(args.output).write_text(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), encoding="utf-8")
        payload = {"ok": not problems, "ledger": result, "findings": problems}
    elif args.command in {"validate-review", "validate-consumer-review"}:
        review_data = _load_yaml(Path(args.review))
        expected = {key: value for key, value in {"plan_digest": args.plan_digest, "draft_digest": args.draft_digest, "evidence_digest": args.evidence_digest, "source_universe_digest": args.source_universe_digest, "challenge_digest": args.challenge_digest, "divergence_digest": args.divergence_digest}.items() if value}
        plan_findings: list[dict[str, str]] = []
        if args.plan:
            plan, plan_findings = load_wiki_plan(root, args.plan)
            if plan is not None and not plan_findings:
                expected["page_ids"] = _page_ids(plan)
                universe, receipt, challenge, divergence, bundle_problems = validate_open_world_bundle(root, plan)
                plan_findings.extend(bundle_problems)
                if universe is not None and receipt is not None and challenge is not None and divergence is not None and not bundle_problems:
                    expected["task_origins"] = _review_task_contract(plan, challenge, universe, divergence)
                    expected["task_ids"] = list(expected["task_origins"])
                    expected["source_universe_digest"] = source_universe_digest(universe)
                    expected["challenge_digest"] = challenge_digest(challenge)
                    expected["max_adequacy"] = "provisional"
        validator = validate_consumer_review if args.command == "validate-consumer-review" else validate_semantic_review
        problems = plan_findings + validator(review_data, expected)
        payload = {"ok": not problems, "review": review_data, "findings": problems}
    elif args.command == "check-readable":
        problems = check_opaque_identifiers(root, args.wiki_root)
        payload = {"ok": not problems, "findings": problems}
    else:
        try:
            digest_value = digest_paths(root, args.paths)
            payload = {"ok": True, "digest": digest_value, "findings": []}
        except (OSError, ValueError) as error:
            payload = {"ok": False, "digest": None, "findings": [{"code": "DIGEST_FAILED", "message": str(error)}]}
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    return 0 if not payload["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
