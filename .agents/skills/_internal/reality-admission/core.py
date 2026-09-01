"""Executable Reality Contract and projection admission primitives.

Semantic validation targets a committed repository projection: the complete
Reality tree after existing and proposed facts have been combined.  Git is the
cross-worktree transport and immutability boundary; Admission never depends on
an ignored candidate directory or writes a second copy of Reality.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml


CONTRACT_VERSION = "reality-contract-v2"
PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"
BLOCKED = "BLOCKED"
_SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def _contract_path() -> Path:
    return Path(__file__).with_name("protocol") / "reality_contract.yaml"


def load_contract() -> dict[str, Any]:
    return yaml.safe_load(_contract_path().read_text(encoding="utf-8")) or {}


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        _jsonable(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _load_yaml_or_json(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _content_without_fences(body: str) -> str:
    lines = body.splitlines()
    inside = False
    kept = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            inside = not inside
            continue
        if not inside:
            kept.append(line)
    return "\n".join(kept)


def _profile_version(profile: Mapping[str, Any]) -> Any:
    return profile.get("version", profile.get("layout_version"))


def _profile_id(profile: Mapping[str, Any]) -> Any:
    return profile.get("profile_id", profile.get("id"))


def _domain_contract_errors(profile: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if "capability_domains" in profile:
        errors.append("legacy_domain_field:capability_domains")

    policy = profile.get("domain_policy")
    if policy is not None and policy != "business_evidence":
        errors.append("domain_policy")

    source_units = profile.get("source_units")
    source_unit_ids: set[str] = set()
    if source_units is not None:
        if not isinstance(source_units, list):
            errors.append("source_units")
        else:
            for index, source_unit in enumerate(source_units):
                if not isinstance(source_unit, Mapping):
                    errors.append(f"source_units[{index}]")
                    continue
                source_unit_id = str(source_unit.get("id", ""))
                if not source_unit_id or source_unit_id in source_unit_ids:
                    errors.append(f"source_units.id:{source_unit_id or index}")
                source_unit_ids.add(source_unit_id)
                if not isinstance(source_unit.get("kind"), str) or not source_unit.get("kind"):
                    errors.append(f"source_units.kind:{source_unit_id or index}")
                source_path = source_unit.get("path")
                if not isinstance(source_path, str) or not _safe_relative(source_path):
                    errors.append(f"source_units.path:{source_unit_id or index}")

    registry = profile.get("domain_registry")
    if registry is not None and not isinstance(registry, Mapping):
        errors.append("domain_registry")
        return errors
    if policy == "business_evidence" and not isinstance(registry, Mapping):
        errors.append("domain_registry_required")
        return errors
    if not isinstance(registry, Mapping):
        return errors

    domains = profile.get("domains")
    if not isinstance(domains, list) or any(not isinstance(item, str) for item in domains):
        errors.append("domains_required_for_domain_registry")
        return errors
    domain_ids = set(domains)
    registry_ids = {str(key) for key in registry}
    for missing in sorted(domain_ids - registry_ids):
        errors.append(f"domain_registry.missing:{missing}")
    for extra in sorted(registry_ids - domain_ids):
        errors.append(f"domain_registry.extra:{extra}")

    contract = load_contract().get("domain_boundary_contract", {})
    if not isinstance(contract, Mapping):
        contract = {}
    required_fields = set(
        contract.get(
            "required_fields",
            ["boundary_reason", "boundary_basis", "evidence_refs"],
        )
    )
    allowed_basis = set(
        contract.get(
            "allowed_basis",
            [
                "business_object",
                "user_task",
                "workflow",
                "data_ownership",
                "permission_boundary",
                "product_outcome",
                "api_contract",
                "event_contract",
                "operational_responsibility",
            ],
        )
    )
    forbidden_fields = set(contract.get("forbidden_fields", []))
    for domain_id in sorted(domain_ids & registry_ids):
        entry = registry[domain_id]
        if not isinstance(entry, Mapping):
            errors.append(f"domain_registry.entry:{domain_id}")
            continue
        missing_fields = required_fields - set(entry)
        if missing_fields:
            errors.append(
                f"domain_registry.required:{domain_id}:{','.join(sorted(missing_fields))}"
            )
        basis = entry.get("boundary_basis")
        if not isinstance(basis, list) or not basis:
            errors.append(f"domain_registry.boundary_basis:{domain_id}")
        else:
            invalid_basis = sorted(
                str(item) for item in basis if not isinstance(item, str) or item not in allowed_basis
            )
            if invalid_basis:
                errors.append(
                    f"domain_registry.boundary_basis_values:{domain_id}:{','.join(invalid_basis)}"
                )
        evidence_refs = entry.get("evidence_refs")
        if not isinstance(evidence_refs, list) or not evidence_refs:
            errors.append(f"domain_registry.evidence_refs:{domain_id}")
        for forbidden in sorted(forbidden_fields):
            if forbidden in entry:
                errors.append(f"domain_registry.forbidden:{domain_id}:{forbidden}")
        entry_source_units = entry.get(contract.get("source_units_field", "source_units"), [])
        if not isinstance(entry_source_units, list) or any(
            not isinstance(item, str) for item in entry_source_units
        ):
            errors.append(f"domain_registry.source_units:{domain_id}")
        elif source_unit_ids and any(item not in source_unit_ids for item in entry_source_units):
            errors.append(f"domain_registry.unknown_source_unit:{domain_id}")
    return errors


def _layout_contract_errors(profile: Mapping[str, Any]) -> list[str]:
    if profile.get("domain_policy") != "business_evidence":
        return []

    layout = load_contract().get("layout_contract", {})
    if not isinstance(layout, Mapping):
        return ["layout_contract"]

    errors: list[str] = []
    expected_domain_entries = tuple(
        str(item) for item in layout.get("domain_entry_files", []) if isinstance(item, str)
    )
    expected_crosscutting_entries = tuple(
        str(item)
        for item in layout.get("crosscutting_entry_files", [])
        if isinstance(item, str)
    )
    expected_slots = {
        str(item) for item in layout.get("domain_slots", []) if isinstance(item, str)
    }

    domain_entries = profile.get("domain_entry_files")
    if not isinstance(domain_entries, list):
        errors.append("domain_entry_files_required")
    else:
        actual_entries = tuple(str(item) for item in domain_entries)
        if len(actual_entries) != len(set(actual_entries)):
            errors.append("domain_entry_files_duplicate")
        missing = sorted(set(expected_domain_entries) - set(actual_entries))
        unexpected = sorted(set(actual_entries) - set(expected_domain_entries))
        if missing:
            errors.append("domain_entry_files_missing:" + ",".join(missing))
        if unexpected:
            errors.append("domain_entry_files_unexpected:" + ",".join(unexpected))

    crosscutting_entries = profile.get("crosscutting_entry_files")
    if not isinstance(crosscutting_entries, list):
        errors.append("crosscutting_entry_files_required")
    else:
        actual_entries = tuple(str(item) for item in crosscutting_entries)
        if len(actual_entries) != len(set(actual_entries)):
            errors.append("crosscutting_entry_files_duplicate")
        missing = sorted(set(expected_crosscutting_entries) - set(actual_entries))
        unexpected = sorted(set(actual_entries) - set(expected_crosscutting_entries))
        if missing:
            errors.append("crosscutting_entry_files_missing:" + ",".join(missing))
        if unexpected:
            errors.append("crosscutting_entry_files_unexpected:" + ",".join(unexpected))

    registry = profile.get("document_registry")
    if not isinstance(registry, Mapping):
        errors.append("document_registry_required")
    else:
        owner_slots = registry.get("owner_slots")
        if not isinstance(owner_slots, list):
            errors.append("document_registry.owner_slots_required")
        else:
            missing_slots = sorted(expected_slots - {str(item) for item in owner_slots})
            if missing_slots:
                errors.append(
                    "document_registry.owner_slots_missing:" + ",".join(missing_slots)
                )
    return errors


def load_profile(profile_path: Path | str) -> dict[str, Any]:
    path = Path(profile_path)
    if not path.is_file():
        raise FileNotFoundError(f"Reality Profile not found: {path}")
    profile = _load_yaml_or_json(path)
    if not isinstance(profile, dict):
        raise ValueError("Reality Profile must be a mapping")
    if not profile.get("profile_id"):
        raise ValueError("Reality Profile requires profile_id")
    if _profile_version(profile) is None:
        raise ValueError("Reality Profile requires version or layout_version")
    errors = _profile_contract_errors(profile)
    if errors:
        raise ValueError("Reality Profile contract invalid: " + "; ".join(errors))
    return profile


def _profile_contract_errors(profile: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    errors.extend(_domain_contract_errors(profile))
    errors.extend(_layout_contract_errors(profile))
    for key in ("root_entries", "domain_entry_files", "crosscutting_entry_files"):
        value = profile.get(key)
        if value is not None and (
            not isinstance(value, list)
            or any(not isinstance(item, str) or not _safe_relative(item) for item in value)
        ):
            errors.append(key)
    domains = profile.get("domains")
    if domains is not None and (
        not isinstance(domains, list) or any(not isinstance(item, str) for item in domains)
    ):
        errors.append("domains")
    profile_statuses = profile.get("knowledge_statuses")
    if profile_statuses is not None and (
        not isinstance(profile_statuses, list)
        or any(not isinstance(item, str) for item in profile_statuses)
    ):
        errors.append("knowledge_statuses")
    registry = profile.get("document_registry")
    if registry is not None and not isinstance(registry, Mapping):
        errors.append("document_registry")
    if isinstance(registry, Mapping):
        for key in ("required_fields", "owner_slots", "crosscutting_slots"):
            value = registry.get(key, [])
            if not isinstance(value, list):
                errors.append(f"document_registry.{key}")
    state_registry = profile.get("state_file_registry")
    if state_registry is not None and not isinstance(state_registry, Mapping):
        errors.append("state_file_registry")
    if isinstance(state_registry, Mapping):
        for key in ("required_fields", "owner_slots"):
            value = state_registry.get(key, [])
            if not isinstance(value, list):
                errors.append(f"state_file_registry.{key}")
    slot_contract = profile.get("slot_entry_contract")
    if slot_contract is not None and not isinstance(slot_contract, Mapping):
        errors.append("slot_entry_contract")
    if isinstance(slot_contract, Mapping):
        required_slot_fields = slot_contract.get("required_fields", [])
        if not isinstance(required_slot_fields, list):
            errors.append("slot_entry_contract.required_fields")
        if "not_applicable_requires_evidence" in slot_contract and not isinstance(
            slot_contract["not_applicable_requires_evidence"], bool
        ):
            errors.append("slot_entry_contract.not_applicable_requires_evidence")
    statuses = set(load_contract().get("knowledge_statuses", []))
    registered = profile.get("documents", [])
    if registered is not None and not isinstance(registered, list):
        errors.append("documents")
        registered = []
    owner_slots = set(registry.get("owner_slots", [])) if isinstance(registry, Mapping) else set()
    crosscutting_slots = (
        set(registry.get("crosscutting_slots", []))
        if isinstance(registry, Mapping)
        else set()
    )
    domain_set = set(domains or []) if isinstance(domains, list) else set()
    seen_document_paths: set[str] = set()
    for item in registered:
        if not isinstance(item, Mapping):
            errors.append("document_entry")
            continue
        path = str(item.get("path", ""))
        if path in seen_document_paths:
            errors.append(f"duplicate_document_path:{path}")
        seen_document_paths.add(path)
        if not path or not _safe_relative(path):
            errors.append(f"document_path:{path}")
            continue
        owner_domain = str(item.get("owner_domain", ""))
        owner_slot = str(item.get("owner_slot", ""))
        if item.get("knowledge_status") not in statuses:
            errors.append(f"document_status:{path}")
        if owner_domain == "crosscutting":
            valid = owner_slot in crosscutting_slots and path.startswith(
                "crosscutting/" + owner_slot + "/"
            )
        else:
            valid = (
                owner_domain in domain_set
                and owner_slot in owner_slots
                and path.startswith(f"{owner_domain}/{owner_slot}/")
            )
        if not valid:
            errors.append(f"document_owner:{path}")
        if not isinstance(item.get("evidence_refs"), list):
            errors.append(f"document_evidence_refs:{path}")
    state_files = profile.get("state_files", [])
    if state_files is None:
        state_files = []
    elif not isinstance(state_files, list):
        errors.append("state_files")
        state_files = []
    for item in state_files:
        if not isinstance(item, Mapping):
            errors.append("state_file_entry")
            continue
        path = str(item.get("path", ""))
        if not path or not _safe_relative(path):
            errors.append(f"state_file_path:{path}")
    return errors


def _required_profile_paths(profile: Mapping[str, Any]) -> set[str]:
    paths = set(profile.get("root_entries", []))
    for domain in profile.get("domains", []):
        for entry in profile.get("domain_entry_files", []):
            paths.add(f"{domain}/{entry}")
    for entry in profile.get("crosscutting_entry_files", []):
        paths.add(f"crosscutting/{entry}")
    return paths


def _slot_entry_metadata(path: Path) -> dict[str, Any]:
    metadata, _ = parse_frontmatter(path)
    if metadata is not None:
        return metadata
    text = path.read_text(encoding="utf-8")
    fallback: dict[str, Any] = {}
    for field in ("knowledge_status", "evidence_refs"):
        match = re.search(
            rf"^{re.escape(field)}:\s*(.+?)\s*$",
            text,
            re.MULTILINE,
        )
        if match:
            fallback[field] = yaml.safe_load(match.group(1))
    return fallback


def _profile_registry_checks(root: Path, profile: Mapping[str, Any]) -> list["CheckResult"]:
    """Validate Profile-owned paths and registrations in the shared admission gate."""

    registry_keys = {
        "root_entries",
        "domains",
        "domain_policy",
        "domain_registry",
        "source_units",
        "domain_entry_files",
        "crosscutting_entry_files",
        "document_registry",
        "state_file_registry",
    }
    if not registry_keys.intersection(profile):
        return []

    results: list[CheckResult] = []
    if profile.get("domain_policy") == "business_evidence":
        results.append(
            CheckResult(
                PASS,
                "domain_boundary_contract",
                f"{len(profile.get('domains', []))} business domains",
            )
        )
        layout = load_contract().get("layout_contract", {})
        domain_entries = layout.get("domain_entry_files", []) if isinstance(layout, Mapping) else []
        results.append(
            CheckResult(
                PASS,
                "reality_layout_contract",
                f"{len(domain_entries)} domain entry files",
            )
        )
    required_paths = _required_profile_paths(profile)
    missing = sorted(path for path in required_paths if not (root / path).is_file())
    if missing:
        results.extend(CheckResult(FAIL, "profile_required_paths", path) for path in missing)
    else:
        results.append(
            CheckResult(PASS, "profile_required_paths", f"{len(required_paths)} paths")
        )

    slot_contract = profile.get("slot_entry_contract", {})
    if not isinstance(slot_contract, Mapping):
        slot_contract = {}
    slot_required_fields = set(
        slot_contract.get("required_fields", ["knowledge_status", "evidence_refs"])
    )
    slot_requires_evidence = slot_contract.get("not_applicable_requires_evidence", True)
    slot_paths = {
        f"{domain}/{entry}"
        for domain in profile.get("domains", [])
        for entry in profile.get("domain_entry_files", [])
        if str(entry).endswith("/INDEX.md")
    }
    slot_paths.update(
        f"crosscutting/{entry}"
        for entry in profile.get("crosscutting_entry_files", [])
        if str(entry).endswith("/INDEX.md")
    )
    allowed_statuses = set(
        profile.get("knowledge_statuses") or load_contract().get("knowledge_statuses", [])
    )
    for path in sorted(slot_paths):
        slot_path = root / path
        if not slot_path.is_file():
            continue
        try:
            metadata = _slot_entry_metadata(slot_path)
        except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError) as error:
            results.append(CheckResult(FAIL, "knowledge_status_valid", f"{path}: {error}"))
            continue
        if slot_required_fields - set(metadata):
            results.append(CheckResult(FAIL, "knowledge_status_valid", path))
            continue
        status = metadata.get("knowledge_status")
        if status not in allowed_statuses:
            results.append(CheckResult(FAIL, "knowledge_status_valid", path))
        elif status == "not_applicable" and slot_requires_evidence and not metadata.get(
            "evidence_refs"
        ):
            results.append(CheckResult(FAIL, "not_applicable_evidenced", path))

    registry = profile.get("document_registry", {})
    if not isinstance(registry, Mapping):
        registry = {}
    required_fields = set(
        registry.get(
            "required_fields",
            ["path", "owner_domain", "owner_slot", "purpose", "knowledge_status", "evidence_refs"],
        )
    )
    domains = set(profile.get("domains", []))
    domain_slots = set(registry.get("owner_slots", []))
    crosscutting_slots = set(registry.get("crosscutting_slots", []))
    allowed_statuses = set(
        profile.get("knowledge_statuses") or load_contract().get("knowledge_statuses", [])
    )
    registered_paths: set[str] = set()
    registered_owners: dict[str, tuple[str, str]] = {}

    for document in profile.get("documents", []) or []:
        if not isinstance(document, Mapping):
            results.append(CheckResult(FAIL, "profile_document_registry", "invalid document entry"))
            continue
        path = str(document.get("path", ""))
        registered_paths.add(path)
        missing_fields = required_fields - set(document)
        owner_domain = str(document.get("owner_domain", ""))
        owner_slot = str(document.get("owner_slot", ""))
        if owner_domain == "crosscutting":
            valid_owner = owner_slot in crosscutting_slots
        else:
            valid_owner = (not domains or owner_domain in domains) and owner_slot in domain_slots
        expected_prefix = f"{owner_domain}/{owner_slot}/"
        valid_path = bool(path) and path.startswith(
            "crosscutting/" + owner_slot + "/"
            if owner_domain == "crosscutting"
            else expected_prefix
        )
        if (
            missing_fields
            or not valid_owner
            or not valid_path
            or not (root / path).is_file()
        ):
            results.append(
                CheckResult(FAIL, "profile_document_registry", path or "invalid document entry")
            )
            continue
        registered_owners[path] = (owner_domain, owner_slot)
        status = document.get("knowledge_status")
        if status not in allowed_statuses:
            results.append(CheckResult(FAIL, "knowledge_status_valid", path))
        elif status == "not_applicable" and not document.get("evidence_refs"):
            results.append(CheckResult(FAIL, "not_applicable_evidenced", path))

    state_registry = profile.get("state_file_registry", {})
    if not isinstance(state_registry, Mapping):
        state_registry = {}
    state_required_fields = set(
        state_registry.get("required_fields", ["path", "owner_domain", "owner_slot", "purpose"])
    )
    state_slots = set(
        state_registry.get("owner_slots", [])
        or registry.get("owner_slots", [])
    )
    for state_file in profile.get("state_files", []) or []:
        if not isinstance(state_file, Mapping):
            results.append(CheckResult(FAIL, "profile_state_file_registry", "invalid state file entry"))
            continue
        path = str(state_file.get("path", ""))
        owner_domain = str(state_file.get("owner_domain", ""))
        owner_slot = str(state_file.get("owner_slot", ""))
        expected_prefix = f"{owner_domain}/{owner_slot}/"
        if (
            state_required_fields - set(state_file)
            or (domains and owner_domain not in domains)
            or owner_slot not in state_slots
            or not path.startswith(expected_prefix)
            or not (root / path).is_file()
        ):
            results.append(
                CheckResult(FAIL, "profile_state_file_registry", path or "invalid state file entry")
            )

    migration = profile.get("migration", {})
    if not isinstance(migration, Mapping):
        migration = {}
    legacy_paths = set(migration.get("legacy_paths", []))
    for markdown in root.rglob("*.md"):
        rel_path = markdown.relative_to(root).as_posix()
        if rel_path in required_paths or rel_path in registered_paths:
            continue
        if any(
            rel_path == legacy.rstrip("/")
            or rel_path.startswith(legacy.rstrip("/") + "/")
            for legacy in legacy_paths
        ):
            continue
        results.append(CheckResult(FAIL, "profile_document_registry", rel_path))

    layout = load_contract().get("layout_contract", {})
    forbidden_shapes = layout.get("forbidden_legacy_shapes", []) if isinstance(layout, Mapping) else []
    for pattern in forbidden_shapes:
        if not isinstance(pattern, str):
            continue
        path_pattern = Path(pattern)
        if len(path_pattern.parts) != 2 or path_pattern.parts[1] != "*.md":
            continue
        legacy_root = root / path_pattern.parts[0]
        for markdown in sorted(legacy_root.glob("*.md")):
            results.append(
                CheckResult(
                    FAIL,
                    "reality_layout_legacy_shape",
                    markdown.relative_to(root).as_posix(),
                )
            )
    for domain in profile.get("domains", []) or []:
        domain_root = root / str(domain)
        for markdown in sorted(domain_root.glob("*.md")):
            if markdown.name == "README.md":
                continue
            results.append(
                CheckResult(
                    FAIL,
                    "reality_layout_domain_root_file",
                    markdown.relative_to(root).as_posix(),
                )
            )

    for path, expected_owner in registered_owners.items():
        try:
            metadata, _ = parse_frontmatter(root / path)
        except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError) as error:
            results.append(CheckResult(FAIL, "profile_document_owner", f"{path}: {error}"))
            continue
        if metadata is None:
            continue
        actual_owner = (
            metadata.get("owner_domain"),
            metadata.get("owner_slot"),
        )
        if actual_owner != expected_owner and any(value is not None for value in actual_owner):
            results.append(CheckResult(FAIL, "profile_document_owner", path))

    return results


def _repo_root(path: Path) -> Path:
    current = path.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return path.resolve()


def _run_git(
    repo_root: Path,
    *args: str,
    text: bool = True,
) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=text,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() if text else result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"git {' '.join(args)} failed: {stderr}")
    return result.stdout.strip() if text else result.stdout


def _resolve_commit(repo_root: Path, ref: str) -> str:
    return str(_run_git(repo_root, "rev-parse", "--verify", f"{ref}^{{commit}}"))


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"path outside repository: {path}") from error


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str]:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"frontmatter must be a mapping: {path}")
    return metadata, text[match.end():]


def _content_purity_warnings(body: str) -> list[str]:
    """Return leftover placeholder markers as advisory hints.

    The admission script never judges how a page is structured or written;
    page shape is owned by the selected Reality template pack.  Placeholder
    leftovers are only surfaced as non-blocking hints so authors can go back
    to the template and reflect on what the page still owes the reader.
    """

    markers = load_contract().get(
        "content_purity_forbidden_markers",
        ("TODO", "TBD", "FIXME", "待补充", "<待补>", "<占位符>", "placeholder"),
    )
    pattern = re.compile(
        "|".join(
            (
                rf"\b{re.escape(marker)}\b"
                if re.match(r"^[A-Za-z0-9_]+$", str(marker))
                else re.escape(str(marker))
            )
            for marker in markers
        ),
        re.IGNORECASE,
    )
    matches = []
    for match in pattern.finditer(_content_without_fences(body)):
        marker = match.group(0)
        if marker not in matches:
            matches.append(marker)
    return matches


def _safe_relative(path_value: str) -> bool:
    path = Path(path_value)
    return not path.is_absolute() and ".." not in path.parts


def _evidence_path_candidates(ref_path: str, root: Path) -> Iterable[Path]:
    if Path(ref_path).is_absolute():
        yield Path(ref_path)
        return
    yield root / ref_path
    repo = _repo_root(root)
    if repo != root:
        yield repo / ref_path


def _evidence_refs(metadata: Mapping[str, Any]) -> list[Any]:
    refs = metadata.get("evidence_refs", [])
    return refs if isinstance(refs, list) else []


@dataclass(frozen=True)
class CheckResult:
    level: str
    check: str
    detail: str


def check_reality_root(
    root: Path | str,
    *,
    strict_frontmatter: bool = False,
    strict_paths: set[str] | None = None,
) -> list[CheckResult]:
    """Run deterministic checks over the complete projected Reality root.

    Role boundary: this script is an auxiliary verifier, never a structural
    authority.  It only enforces objectively checkable traceability facts
    (frontmatter identity, evidence existence/digest, profile declarations)
    and surfaces leftover placeholder markers as non-blocking hints.  It must
    not prescribe page sections, headings, wording patterns or length; page
    shape is owned by the Reality template pack selected for the run, and any
    structure or content concern must be resolved by going back to that
    template, not by reshaping content to satisfy this script.

    Legacy pages remain readable.  Newly added or modified Markdown paths can
    be supplied through ``strict_paths`` so a changed legacy page cannot evade
    the current Artifact Contract.
    """

    root = Path(root)
    strict_paths = strict_paths or set()
    results: list[CheckResult] = []
    profile_path = root / "00_profile.yaml"
    if not profile_path.is_file():
        return [CheckResult(BLOCKED, "profile_required", "00_profile.yaml missing")]
    try:
        profile = load_profile(profile_path)
    except (OSError, ValueError, yaml.YAMLError) as error:
        return [CheckResult(FAIL, "profile_valid", str(error))]
    results.append(CheckResult(PASS, "profile_valid", str(profile.get("profile_id"))))
    results.extend(_profile_registry_checks(root, profile))

    for entry in profile.get("documents", []) or []:
        if not isinstance(entry, Mapping):
            continue
        path = str(entry.get("path", ""))
        if path and not (root / path).is_file():
            results.append(CheckResult(FAIL, "profile_document_exists", path))

    contract = load_contract()
    allowed_fact_types = set((contract.get("canonical_fact_types") or {}).keys())
    extensions = profile.get("fact_type_extensions", profile.get("fact_types", {}))
    if isinstance(extensions, Mapping):
        allowed_fact_types.update(str(key) for key in extensions)
    elif isinstance(extensions, list):
        allowed_fact_types.update(str(item) for item in extensions)
    statuses = set(contract.get("knowledge_statuses", []))
    required_fields = set(contract.get("required_frontmatter", []))
    root_exceptions = {"README.md", "INDEX.md", "glossary.md", "positioning.md"}
    reality_ids: dict[str, str] = {}

    for page in sorted(root.rglob("*.md")):
        rel = page.relative_to(root).as_posix()
        strict_page = strict_frontmatter or rel in strict_paths
        try:
            metadata, body = parse_frontmatter(page)
        except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError) as error:
            results.append(CheckResult(FAIL, "frontmatter_parseable", f"{rel}: {error}"))
            continue
        if metadata is None:
            if strict_page and page.name not in root_exceptions:
                results.append(CheckResult(FAIL, "frontmatter_required", rel))
            continue
        reality_id = metadata.get("reality_id")
        if "reality_id" not in metadata:
            if strict_page and page.name not in root_exceptions:
                results.append(CheckResult(FAIL, "reality_id", rel))
            continue
        if not isinstance(reality_id, str) or not reality_id.strip():
            results.append(CheckResult(FAIL, "reality_id", rel))
        elif reality_id in reality_ids:
            results.append(
                CheckResult(
                    FAIL,
                    "reality_id_unique",
                    f"{rel}: duplicates {reality_ids[reality_id]}",
                )
            )
        else:
            reality_ids[reality_id] = rel
        missing = sorted(required_fields - set(metadata))
        if missing:
            results.append(CheckResult(FAIL, "frontmatter_required", f"{rel}: {','.join(missing)}"))
        fact_type = metadata.get("fact_type")
        if fact_type not in allowed_fact_types:
            results.append(CheckResult(FAIL, "canonical_fact_type", f"{rel}: {fact_type!r}"))
        status = metadata.get("knowledge_status")
        if status not in statuses:
            results.append(CheckResult(FAIL, "knowledge_status", f"{rel}: {status!r}"))
        if not isinstance(metadata.get("claim_refs"), list) or not metadata.get("claim_refs"):
            results.append(CheckResult(FAIL, "claim_refs", rel))
        refs = _evidence_refs(metadata)
        if not refs:
            results.append(CheckResult(FAIL, "evidence_refs", rel))
        for ref in refs:
            if isinstance(ref, str):
                ref_path, declared_digest = ref, None
            elif isinstance(ref, Mapping):
                ref_path, declared_digest = str(ref.get("path", "")), ref.get("digest")
            else:
                results.append(CheckResult(FAIL, "evidence_reference", f"{rel}: malformed"))
                continue
            if not ref_path or not _safe_relative(ref_path):
                results.append(CheckResult(FAIL, "evidence_reference", f"{rel}: {ref_path!r}"))
                continue
            evidence_path = next(
                (
                    candidate
                    for candidate in _evidence_path_candidates(ref_path, root)
                    if candidate.is_file()
                ),
                None,
            )
            if evidence_path is None:
                results.append(CheckResult(FAIL, "evidence_exists", f"{rel}: {ref_path}"))
            elif declared_digest and declared_digest != file_digest(evidence_path):
                results.append(CheckResult(FAIL, "evidence_digest", f"{rel}: {ref_path}"))
        # Advisory only: placeholder hints never block admission and never
        # prescribe page structure.  Page shape is owned by the template pack;
        # a hint tells the author to go back to the template and reflect.
        for marker in _content_purity_warnings(body):
            results.append(
                CheckResult(
                    WARN,
                    "content_purity_hint",
                    f"{rel}: leftover marker {marker}; go back to the selected "
                    "template pack and reflect on what this page still owes the reader",
                )
            )
    return results


def _result_dict(result: CheckResult) -> dict[str, str]:
    return {"level": result.level, "check": result.check, "detail": result.detail}


def _reality_tree_entries(
    repo_root: Path,
    reality_path: str,
    commit: str,
) -> list[dict[str, str]]:
    output = str(
        _run_git(repo_root, "ls-tree", "-r", "--name-only", commit, "--", reality_path)
    )
    entries: list[dict[str, str]] = []
    for path in output.splitlines():
        if not path:
            continue
        content = bytes(_run_git(repo_root, "show", f"{commit}:{path}", text=False))
        entries.append(
            {
                "path": path,
                "digest": "sha256:" + hashlib.sha256(content).hexdigest(),
            }
        )
    return entries


@dataclass(frozen=True)
class RealityProjection:
    repo_root: Path
    reality_root: Path
    base_commit: str
    candidate_commit: str
    reality_digest: str
    change_digest: str
    changed_paths: tuple[str, ...]
    profile_id: Any
    profile_version: Any
    intended_use: tuple[str, ...] = ()
    contract_version: str = CONTRACT_VERSION
    file_count: int = 0

    @classmethod
    def from_repository(
        cls,
        reality_root: Path | str,
        base_ref: str,
        candidate_ref: str = "HEAD",
        *,
        intended_use: Sequence[str] = (),
    ) -> "RealityProjection":
        reality_root = Path(reality_root).resolve()
        repo_root = _repo_root(reality_root)
        if not (repo_root / ".git").exists():
            raise ValueError(f"repository_required:{repo_root}")
        base_commit = _resolve_commit(repo_root, base_ref)
        candidate_commit = _resolve_commit(repo_root, candidate_ref)
        head_commit = _resolve_commit(repo_root, "HEAD")
        ancestry = subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "merge-base",
                "--is-ancestor",
                base_commit,
                candidate_commit,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if ancestry.returncode != 0:
            raise ValueError(
                f"base_commit_not_ancestor:{base_commit}:{candidate_commit}"
            )
        if candidate_commit != head_commit:
            raise ValueError(
                f"candidate_commit_not_checked_out:{candidate_commit}:{head_commit}"
            )
        status = str(
            _run_git(repo_root, "status", "--porcelain=v1", "--untracked-files=all")
        )
        if status:
            first = status.splitlines()[0]
            raise ValueError(f"repository_worktree_dirty:{first}")

        reality_path = _repo_relative(reality_root, repo_root)
        entries = _reality_tree_entries(repo_root, reality_path, candidate_commit)
        reality_digest = canonical_digest({"root": reality_path, "files": entries})
        patch = bytes(
            _run_git(
                repo_root,
                "diff",
                "--binary",
                "--no-ext-diff",
                base_commit,
                candidate_commit,
                "--",
                reality_path,
                text=False,
            )
        )
        change_digest = "sha256:" + hashlib.sha256(patch).hexdigest()
        changed_output = str(
            _run_git(
                repo_root,
                "diff",
                "--name-only",
                "--diff-filter=ACDMRTUXB",
                base_commit,
                candidate_commit,
                "--",
                reality_path,
            )
        )
        changed_paths = tuple(path for path in changed_output.splitlines() if path)
        try:
            profile = load_profile(reality_root / "00_profile.yaml")
        except (FileNotFoundError, OSError, ValueError, yaml.YAMLError):
            profile = {}
        return cls(
            repo_root=repo_root,
            reality_root=reality_root,
            base_commit=base_commit,
            candidate_commit=candidate_commit,
            reality_digest=reality_digest,
            change_digest=change_digest,
            changed_paths=changed_paths,
            profile_id=_profile_id(profile),
            profile_version=_profile_version(profile),
            intended_use=tuple(str(item) for item in intended_use),
            file_count=len(entries),
        )

    @property
    def projection_digest(self) -> str:
        return canonical_digest(self.to_mapping(include_digest=False))

    @property
    def reality_path(self) -> str:
        return _repo_relative(self.reality_root, self.repo_root)

    def to_mapping(self, *, include_digest: bool = True) -> dict[str, Any]:
        data = {
            "schema_version": 1,
            "contract_version": self.contract_version,
            "repository": {
                "base_commit": self.base_commit,
                "candidate_commit": self.candidate_commit,
            },
            "reality": {
                "root": self.reality_path,
                "profile_id": self.profile_id,
                "profile_version": self.profile_version,
                "digest": self.reality_digest,
                "file_count": self.file_count,
            },
            "change": {
                "digest": self.change_digest,
                "paths": list(self.changed_paths),
            },
            "intended_use": list(self.intended_use),
        }
        if include_digest:
            data["projection_digest"] = self.projection_digest
        return data


def _validation_result_schema_errors(data: Mapping[str, Any]) -> list[str]:
    required = (
        "schema_version",
        "validator_context_ref",
        "projection_digest",
        "base_commit",
        "candidate_commit",
        "reality_digest",
        "change_digest",
        "contract_version",
        "profile_id",
        "profile_version",
        "review_binding",
        "isolation_attestation",
        "status",
        "claim_findings",
        "conflicts",
        "unsupported_assertions",
        "scenario_results",
        "blocking_gaps",
        "evidence_refs",
    )
    errors = [f"missing:{key}" for key in required if key not in data]
    if data.get("schema_version") != 2:
        errors.append("schema_version")
    if not isinstance(data.get("validator_context_ref"), str) or not data.get(
        "validator_context_ref"
    ):
        errors.append("validator_context_ref")
    for key in ("projection_digest", "reality_digest", "change_digest"):
        if not isinstance(data.get(key), str) or not _SHA256_RE.fullmatch(data[key]):
            errors.append(key)
    for key in ("base_commit", "candidate_commit", "contract_version"):
        if not isinstance(data.get(key), str) or len(data[key]) < 7:
            errors.append(key)
    if data.get("contract_version") != CONTRACT_VERSION:
        errors.append("contract_version")
    if data.get("profile_id") is not None and not isinstance(data.get("profile_id"), str):
        errors.append("profile_id")
    if data.get("profile_version") is not None and (
        isinstance(data.get("profile_version"), bool)
        or not isinstance(data.get("profile_version"), (int, str))
    ):
        errors.append("profile_version")
    review_binding = data.get("review_binding")
    if not isinstance(review_binding, Mapping):
        errors.append("review_binding")
    else:
        review_required = (
            "reverse_review_result_digest",
            "work_contract_digest",
            "module_map_digest",
            "gate_a_digest",
            "gate_b_digest",
            "pack_id",
            "manifest_digest",
            "pack_digest",
            "consumer_contract_version",
            "review_layers",
            "projection_digest",
            "candidate_commit",
            "reality_digest",
            "change_digest",
        )
        errors.extend(
            f"review_binding.{key}"
            for key in review_required
            if key not in review_binding
        )
        for key in (
            "reverse_review_result_digest",
            "work_contract_digest",
            "module_map_digest",
            "gate_a_digest",
            "gate_b_digest",
            "manifest_digest",
            "pack_digest",
            "projection_digest",
            "reality_digest",
            "change_digest",
        ):
            if key in review_binding and (
                not isinstance(review_binding[key], str)
                or not _SHA256_RE.fullmatch(review_binding[key])
            ):
                errors.append(f"review_binding.{key}")
        if (
            not isinstance(review_binding.get("pack_id"), str)
            or not review_binding.get("pack_id")
        ):
            errors.append("review_binding.pack_id")
        if review_binding.get("consumer_contract_version") != (
            "reality-template-effect-pack-consumer/v1"
        ):
            errors.append("review_binding.consumer_contract_version")
        if not isinstance(review_binding.get("candidate_commit"), str) or len(
            review_binding.get("candidate_commit", "")
        ) < 7:
            errors.append("review_binding.candidate_commit")
        review_layers = review_binding.get("review_layers")
        if not isinstance(review_layers, Mapping):
            errors.append("review_binding.review_layers")
        else:
            for layer in ("structure", "content", "confidence"):
                if review_layers.get(layer) not in (
                    "pass",
                    "fail",
                    "blocked",
                    "not_proven",
                ):
                    errors.append(f"review_binding.review_layers.{layer}")
    isolation = data.get("isolation_attestation")
    if not isinstance(isolation, Mapping):
        errors.append("isolation_attestation")
    else:
        if isolation.get("mode") != "separate_worktree":
            errors.append("isolation_attestation.mode")
        if isolation.get("producer_is_validator") is not False:
            errors.append("isolation_attestation.producer_is_validator")
    if data.get("status") not in ("pass", "fail", "blocked"):
        errors.append("status")
    for key in (
        "claim_findings",
        "conflicts",
        "unsupported_assertions",
        "blocking_gaps",
        "evidence_refs",
    ):
        if not isinstance(data.get(key), list):
            errors.append(key)
    scenarios = data.get("scenario_results")
    if not isinstance(scenarios, Mapping):
        errors.append("scenario_results")
    else:
        for scenario in ("explain", "locate", "verify"):
            if scenario not in scenarios:
                errors.append(f"scenario_results.{scenario}")
            elif scenarios[scenario] not in ("pass", "fail", "blocked", "not_applicable"):
                errors.append(f"scenario_results.{scenario}")
    return list(dict.fromkeys(errors))


@dataclass
class ValidationResult:
    data: dict[str, Any]

    @classmethod
    def from_path(cls, path: Path | str) -> "ValidationResult":
        path = Path(path)
        if str(path) == "-":
            raise ValueError("stdin must be handled by the CLI adapter")
        data = _load_yaml_or_json(path)
        if not isinstance(data, dict):
            raise ValueError("Validation Result must be a mapping")
        return cls.from_mapping(data)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ValidationResult":
        if not isinstance(data, Mapping):
            raise ValueError("Validation Result must be a mapping")
        copied = copy.deepcopy(dict(data))
        errors = _validation_result_schema_errors(copied)
        if errors:
            raise ValueError("Validation Result schema invalid: " + "; ".join(errors))
        return cls(copied)

    def validate_for(self, projection: RealityProjection) -> list[str]:
        errors = _validation_result_schema_errors(self.data)
        if errors:
            return ["validation_schema:" + error for error in errors]
        if self.data.get("schema_version") != 2:
            errors.append("validation_schema_version")
        if self.data.get("status") != "pass":
            errors.append(f"validation_status:{self.data.get('status')}")
        bindings = {
            "projection_digest": projection.projection_digest,
            "base_commit": projection.base_commit,
            "candidate_commit": projection.candidate_commit,
            "reality_digest": projection.reality_digest,
            "change_digest": projection.change_digest,
            "contract_version": projection.contract_version,
            "profile_id": projection.profile_id,
            "profile_version": projection.profile_version,
        }
        for key, expected in bindings.items():
            actual = self.data.get(key)
            if str(actual) != str(expected):
                errors.append(f"validation_{key}_mismatch")
        review_binding = self.data.get("review_binding", {})
        if not isinstance(review_binding, Mapping):
            errors.append("review_binding")
            review_binding = {}
        review_projection_bindings = {
            "projection_digest": projection.projection_digest,
            "candidate_commit": projection.candidate_commit,
            "reality_digest": projection.reality_digest,
            "change_digest": projection.change_digest,
        }
        for key, expected in review_projection_bindings.items():
            if str(review_binding.get(key)) != str(expected):
                errors.append(f"review_binding_{key}_mismatch")
        review_layers = review_binding.get("review_layers", {})
        if not isinstance(review_layers, Mapping):
            errors.append("review_binding_review_layers")
        else:
            for layer in ("structure", "content", "confidence"):
                if review_layers.get(layer) != "pass":
                    errors.append(
                        f"review_binding_{layer}:{review_layers.get(layer)}"
                    )
        isolation = self.data.get("isolation_attestation", {})
        if (
            not isinstance(isolation, Mapping)
            or isolation.get("mode") != "separate_worktree"
        ):
            errors.append("isolation_mode")
        if not isinstance(isolation, Mapping) or isolation.get("producer_is_validator") is not False:
            errors.append("producer_is_validator")
        if self.data.get("blocking_gaps"):
            errors.append("blocking_gaps")
        if self.data.get("conflicts"):
            errors.append("validation_conflicts")
        if self.data.get("unsupported_assertions"):
            errors.append("unsupported_assertions")
        scenarios = self.data.get("scenario_results", {})
        if not isinstance(scenarios, Mapping):
            errors.append("scenario_results")
            scenarios = {}
        for scenario in ("explain", "locate", "verify"):
            if scenarios.get(scenario) not in ("pass", "not_applicable"):
                errors.append(f"scenario_{scenario}:{scenarios.get(scenario)}")
        return errors


@dataclass
class AdmissionPlan:
    projection_digest: str
    base_commit: str
    candidate_commit: str
    reality_digest: str
    change_digest: str
    contract_version: str
    profile_version: Any
    intended_use: list[str]
    validation_result_digest: str
    changed_paths: list[str] = field(default_factory=list)
    validation: dict[str, Any] = field(default_factory=dict)
    status: str = "ready"
    plan_digest: str = ""

    def __post_init__(self) -> None:
        if not self.plan_digest:
            self.plan_digest = canonical_digest(self.to_mapping(include_digest=False))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AdmissionPlan":
        plan = cls(
            projection_digest=str(data.get("projection_digest", "")),
            base_commit=str(data.get("base_commit", "")),
            candidate_commit=str(data.get("candidate_commit", "")),
            reality_digest=str(data.get("reality_digest", "")),
            change_digest=str(data.get("change_digest", "")),
            contract_version=str(data.get("contract_version", "")),
            profile_version=data.get("profile_version"),
            intended_use=list(data.get("intended_use", [])),
            validation_result_digest=str(data.get("validation_result_digest", "")),
            changed_paths=list(data.get("changed_paths", [])),
            validation=dict(data.get("validation", {})),
            status=str(data.get("status", "blocked")),
            plan_digest=str(data.get("plan_digest", "")),
        )
        expected = canonical_digest(plan.to_mapping(include_digest=False))
        if plan.plan_digest != expected:
            raise ValueError("plan_digest mismatch")
        return plan

    def to_mapping(self, *, include_digest: bool = True) -> dict[str, Any]:
        data = {
            "contract_version": self.contract_version,
            "projection_digest": self.projection_digest,
            "base_commit": self.base_commit,
            "candidate_commit": self.candidate_commit,
            "reality_digest": self.reality_digest,
            "change_digest": self.change_digest,
            "profile_version": self.profile_version,
            "intended_use": self.intended_use,
            "validation_result_digest": self.validation_result_digest,
            "changed_paths": self.changed_paths,
            "validation": self.validation,
            "status": self.status,
        }
        if include_digest:
            data["plan_digest"] = self.plan_digest
        return data


@dataclass
class AdmissionReceipt:
    status: str
    plan_digest: str
    projection_digest: str
    validation_result_digest: str
    contract_version: str
    base_commit: str
    candidate_commit: str
    reality_digest: str
    change_digest: str
    profile_version: Any
    changed_paths: list[str] = field(default_factory=list)
    validation_summary: dict[str, int] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": self.contract_version,
            "plan_digest": self.plan_digest,
            "projection_digest": self.projection_digest,
            "validation_result_digest": self.validation_result_digest,
            "base_commit": self.base_commit,
            "candidate_commit": self.candidate_commit,
            "reality_digest": self.reality_digest,
            "change_digest": self.change_digest,
            "profile_version": self.profile_version,
            "status": self.status,
            "changed_paths": self.changed_paths,
            "validation_summary": self.validation_summary,
        }


class Admission:
    """Validate and accept a committed Reality projection without rewriting it."""

    def __init__(
        self,
        reality_root: Path | str,
        *,
        contract_version: str = CONTRACT_VERSION,
    ) -> None:
        self.reality_root = Path(reality_root).resolve()
        self.contract_version = contract_version

    def _validation_digest(self, validation: ValidationResult) -> str:
        return canonical_digest(validation.data)

    def _recompute(self, projection: RealityProjection) -> RealityProjection:
        return RealityProjection.from_repository(
            self.reality_root,
            projection.base_commit,
            projection.candidate_commit,
            intended_use=projection.intended_use,
        )

    def _committed_evidence_checks(
        self,
        projection: RealityProjection,
    ) -> list[CheckResult]:
        results: list[CheckResult] = []
        evidence_entries: list[tuple[str, Any]] = []
        for page in sorted(self.reality_root.rglob("*.md")):
            try:
                metadata, _ = parse_frontmatter(page)
            except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError):
                continue
            if not metadata or "reality_id" not in metadata:
                continue
            rel_page = page.relative_to(self.reality_root).as_posix()
            for ref in _evidence_refs(metadata):
                evidence_entries.append((rel_page, ref))

        profile_path = self.reality_root / "00_profile.yaml"
        if profile_path.is_file():
            try:
                profile = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
            except (OSError, UnicodeDecodeError, yaml.YAMLError):
                profile = {}
            if not isinstance(profile, Mapping):
                profile = {}
            documents = profile.get("documents", [])
            if isinstance(documents, list):
                for document in documents:
                    if not isinstance(document, Mapping):
                        continue
                    source = f"00_profile.yaml:{document.get('path', '<unknown>')}"
                    for ref in _evidence_refs(document):
                        evidence_entries.append((source, ref))

        for source, ref in evidence_entries:
            if isinstance(ref, str):
                ref_path = ref
            elif isinstance(ref, Mapping):
                ref_path = str(ref.get("path", ""))
            else:
                continue
            evidence_path = next(
                (
                    candidate
                    for candidate in _evidence_path_candidates(
                        ref_path,
                        self.reality_root,
                    )
                    if candidate.is_file()
                ),
                None,
            )
            if evidence_path is None:
                continue
            try:
                repo_path = _repo_relative(evidence_path, projection.repo_root)
                _run_git(
                    projection.repo_root,
                    "cat-file",
                    "-e",
                    f"{projection.candidate_commit}:{repo_path}",
                )
            except ValueError:
                results.append(
                    CheckResult(
                        FAIL,
                        "evidence_committed",
                        f"{source}: {ref_path}",
                    )
                )
        return results

    def dry_run(
        self,
        projection: RealityProjection,
        validation: ValidationResult,
    ) -> AdmissionPlan:
        projection_errors: list[str] = []
        try:
            current = self._recompute(projection)
        except ValueError as error:
            current = projection
            projection_errors.append(str(error))
        if current.projection_digest != projection.projection_digest:
            projection_errors.append("projection_digest_changed")
        if projection.contract_version != self.contract_version:
            projection_errors.append("unsupported_contract_version")

        reality_prefix = projection.reality_path.rstrip("/") + "/"
        strict_paths = {
            path[len(reality_prefix):]
            for path in projection.changed_paths
            if path.startswith(reality_prefix) and path.endswith(".md")
        }
        checks = check_reality_root(
            self.reality_root,
            strict_paths=strict_paths,
        )
        checks.extend(self._committed_evidence_checks(projection))
        validation_errors = validation.validate_for(projection)
        validation_map: dict[str, Any] = {
            "projection": "pass" if not projection_errors else "fail",
            "worktree_visibility": "pass" if not projection_errors else "fail",
            "full_reality": (
                "pass"
                if not any(item.level in (FAIL, BLOCKED) for item in checks)
                else "fail"
            ),
            "validation_result": "pass" if not validation_errors else "fail",
            "checks": [_result_dict(item) for item in checks],
        }
        if projection_errors:
            validation_map["projection_errors"] = projection_errors
        if validation_errors:
            validation_map["validation_errors"] = validation_errors

        status = "ready"
        if projection_errors or validation_errors or any(item.level == BLOCKED for item in checks):
            status = "blocked"
        elif any(item.level == FAIL for item in checks):
            status = "failed"
        return AdmissionPlan(
            projection_digest=projection.projection_digest,
            base_commit=projection.base_commit,
            candidate_commit=projection.candidate_commit,
            reality_digest=projection.reality_digest,
            change_digest=projection.change_digest,
            contract_version=projection.contract_version,
            profile_version=projection.profile_version,
            intended_use=list(projection.intended_use),
            validation_result_digest=self._validation_digest(validation),
            changed_paths=list(projection.changed_paths),
            validation=validation_map,
            status=status,
        )

    def accept(self, plan: AdmissionPlan) -> AdmissionReceipt:
        expected_plan_digest = canonical_digest(plan.to_mapping(include_digest=False))
        common = {
            "plan_digest": plan.plan_digest,
            "projection_digest": plan.projection_digest,
            "validation_result_digest": plan.validation_result_digest,
            "contract_version": plan.contract_version,
            "base_commit": plan.base_commit,
            "candidate_commit": plan.candidate_commit,
            "reality_digest": plan.reality_digest,
            "change_digest": plan.change_digest,
            "profile_version": plan.profile_version,
            "changed_paths": plan.changed_paths,
        }
        if plan.plan_digest != expected_plan_digest:
            return AdmissionReceipt(
                status="failed",
                validation_summary={"fail": 1},
                **common,
            )
        if plan.status != "ready":
            return AdmissionReceipt(
                status="blocked" if plan.status == "blocked" else "failed",
                validation_summary={"fail": 1},
                **common,
            )
        try:
            current = RealityProjection.from_repository(
                self.reality_root,
                plan.base_commit,
                plan.candidate_commit,
                intended_use=plan.intended_use,
            )
        except ValueError:
            return AdmissionReceipt(
                status="failed",
                validation_summary={"fail": 1},
                **common,
            )
        if (
            current.projection_digest != plan.projection_digest
            or current.reality_digest != plan.reality_digest
            or current.change_digest != plan.change_digest
        ):
            return AdmissionReceipt(
                status="failed",
                validation_summary={"fail": 1},
                **common,
            )
        return AdmissionReceipt(
            status="accepted" if plan.changed_paths else "no_change",
            validation_summary={"pass": 1},
            **common,
        )

    def admit(
        self,
        projection: RealityProjection,
        validation: ValidationResult,
    ) -> AdmissionReceipt:
        return self.accept(self.dry_run(projection, validation))
