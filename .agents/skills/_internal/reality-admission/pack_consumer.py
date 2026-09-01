"""Deterministic consumer for registry-registered Reality Template Packs.

This module resolves Pack contracts and validates target bindings. It never
generates page content, chooses modules, or performs Reality writes.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import yaml


REGISTRY_SCHEMA_VERSION = "reality-template-pack-registry/v1"
MANIFEST_SCHEMA_VERSION = "reality-template-effect-pack/v2"
CONSUMER_CONTRACT_VERSION = "reality-template-effect-pack-consumer/v1"
_SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_DRIVE_PATH_RE = re.compile(r"^[A-Za-z]:")
_FORBIDDEN_OPERATIONS = frozenset({"admit", "compose_page", "discover_modules", "infer_dependencies"})
_ALLOWED_APPLICABILITY = frozenset({"required", "conditional", "optional", "not_applicable"})
_ALLOWED_KNOWLEDGE_STATUS = frozenset(
    {"established", "unknown", "not_established", "not_applicable"}
)
_ALLOWED_REVIEW_STATUS = frozenset({"pass", "fail", "blocked", "not_proven"})
_ALLOWED_SOURCE_ROLES = frozenset({"intent", "design_protocol", "implementation", "verification"})
_ALLOWED_EVIDENCE_STATES = frozenset(
    {"established", "unknown", "not_established", "not_applicable"}
)
_ALLOWED_LOCATOR_QUALITY = frozenset(
    {"exact_symbol", "exact_anchor", "exact_test", "exact_line", "file", "section", "unresolved"}
)
_ALLOWED_EVIDENCE_SUFFICIENCY = frozenset({"supported", "partial", "missing", "blocked"})
_ALLOWED_CONFLICT_DECISIONS = frozenset({"replace", "merge", "block"})


class PackContractError(ValueError):
    """A deterministic Pack contract failure with a stable error code."""

    def __init__(self, code: str, location: str, detail: str) -> None:
        self.code = code
        self.location = location
        self.detail = detail
        super().__init__(f"{code}:{location}:{detail}")


def _mapping(value: Any, code: str, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PackContractError(code, location, "expected_mapping")
    return value


def _list(value: Any, code: str, location: str) -> list[Any]:
    if not isinstance(value, list):
        raise PackContractError(code, location, "expected_list")
    return value


def _text(value: Any, code: str, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise PackContractError(code, location, "expected_non_empty_string")
    return value


def _sha256(value: Any, code: str, location: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise PackContractError(code, location, "expected_sha256")
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


def profile_digest(profile: Mapping[str, Any]) -> str:
    """Return the stable digest for a profile's semantic content."""
    content = dict(profile)
    content.pop("_source_path", None)
    content.pop("profile_digest", None)
    content.pop("digest", None)
    return canonical_digest(content)


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    return value


def _safe_relative_path(value: Any, code: str, location: str) -> str:
    path = _text(value, code, location)
    if (
        "\x00" in path
        or "\\" in path
        or path.startswith("/")
        or _DRIVE_PATH_RE.match(path)
        or "://" in path
    ):
        raise PackContractError(code, location, "unsafe_path")
    parts = path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise PackContractError(code, location, "non_canonical_path")
    normalized = PurePosixPath(path).as_posix()
    if normalized != path:
        raise PackContractError(code, location, "non_canonical_path")
    return path


def _safe_path_or_finding(value: Any, location: str) -> tuple[str | None, dict[str, str] | None]:
    try:
        return _safe_relative_path(value, "unsafe_path", location), None
    except PackContractError as error:
        return None, _finding(error.code, error.location, error.detail)


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _repository_root(path: Path) -> Path:
    current = path.resolve()
    for candidate in (current, *current.parents):
        git_marker = candidate / ".git"
        if git_marker.is_dir() or git_marker.is_file():
            return candidate
    return Path.cwd().resolve()


def _posix_path_is_within(parent: str, child: str) -> bool:
    try:
        PurePosixPath(child).relative_to(PurePosixPath(parent))
    except ValueError:
        return False
    return True


def _load_yaml(path: Path, code: str) -> Mapping[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise PackContractError(code, path.as_posix(), f"read_failed:{error}") from error
    return _mapping(value, code, path.as_posix())


def _finding(code: str, location: str, detail: str) -> dict[str, str]:
    return {"code": code, "location": location, "detail": detail}


def _read_frontmatter(path: Path) -> Mapping[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise PackContractError("page_reference_invalid", path.as_posix(), f"read_failed:{error}") from error
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        raise PackContractError("page_reference_invalid", path.as_posix(), "frontmatter_unclosed")
    try:
        value = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as error:
        raise PackContractError("page_reference_invalid", path.as_posix(), f"frontmatter_invalid:{error}") from error
    return _mapping(value, "page_reference_invalid", path.as_posix())


@dataclass(frozen=True)
class RegistryEntry:
    registry_path: Path
    pack_id: str
    manifest_path: Path
    manifest_relative_path: str
    status: str
    source_of_truth: bool
    raw: Mapping[str, Any]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "registry_path": self.registry_path.as_posix(),
            "pack_id": self.pack_id,
            "manifest_path": self.manifest_relative_path,
            "status": self.status,
            "source_of_truth": self.source_of_truth,
        }


@dataclass(frozen=True)
class AssetResolution:
    asset_id: str
    asset_type: str
    public_path: str
    path: Path
    digest: str

    @property
    def legacy_non_executable(self) -> bool:
        return False


@dataclass(frozen=True)
class PageResolution:
    page_id: str
    asset_id: str
    capability: str
    asset: AssetResolution
    target_scope: str
    target_path: str
    required: bool
    applicability: str
    raw: Mapping[str, Any]

    @property
    def legacy_non_executable(self) -> bool:
        return self.capability == "composer_eligible"

    def to_mapping(self) -> dict[str, Any]:
        return {
            "page_id": self.page_id,
            "asset_id": self.asset_id,
            "capability": self.capability,
            "legacy_non_executable": self.legacy_non_executable,
            "public_path": self.asset.public_path,
            "target_scope": self.target_scope,
            "target_path": self.target_path,
            "required": self.required,
            "applicability": self.applicability,
        }


@dataclass(frozen=True)
class PackManifest:
    root: Path
    registry_path: Path
    manifest_path: Path
    pack_id: str
    version: str
    consumer_contract_version: str
    declared_operations: tuple[str, ...]
    manifest_digest: str
    pack_digest: str
    assets: Mapping[str, AssetResolution]
    pages: Mapping[str, Mapping[str, Any]]
    materialization: Mapping[str, Any]
    raw: Mapping[str, Any]

    def to_mapping(self) -> dict[str, Any]:
        return copy.deepcopy(dict(self.raw))


@dataclass(frozen=True)
class BoundTarget:
    page_id: str
    module_id: str | None
    target_scope: str
    target_path: str
    output_path: str
    conflict_decision: str | None
    legacy_non_executable: bool

    def to_mapping(self) -> dict[str, Any]:
        return {
            "page_id": self.page_id,
            "module_id": self.module_id,
            "target_scope": self.target_scope,
            "target_path": self.target_path,
            "output_path": self.output_path,
            "conflict_decision": self.conflict_decision,
            "legacy_non_executable": self.legacy_non_executable,
        }


@dataclass(frozen=True)
class PackageValidation:
    status: str
    findings: tuple[dict[str, str], ...]
    bound_targets: tuple[BoundTarget, ...] = ()

    def to_mapping(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "findings": [dict(item) for item in self.findings],
            "bound_targets": [item.to_mapping() for item in self.bound_targets],
        }


def resolve_registry(registry_path: Path | str, pack_id: str | None = None) -> RegistryEntry:
    registry_path = Path(registry_path).resolve()
    data = _load_yaml(registry_path, "registry_invalid")
    if data.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        raise PackContractError("registry_invalid", "schema_version", "unsupported_schema")
    registry_root = registry_path.parent
    raw_path_base = data.get("path_base", ".")
    path_base = (
        "."
        if raw_path_base == "."
        else _safe_relative_path(raw_path_base, "registry_invalid", "path_base")
    )
    packs = _mapping(data.get("packs"), "registry_invalid", "packs")
    selected_id = pack_id or data.get("default_pack_id")
    selected_id = _text(selected_id, "registry_invalid", "default_pack_id")
    raw_entry = _mapping(packs.get(selected_id), "registry_invalid", f"packs.{selected_id}")
    manifest_relative_path = _safe_relative_path(
        raw_entry.get("manifest_path"),
        "registry_invalid",
        f"packs.{selected_id}.manifest_path",
    )
    manifest_path = (registry_root / path_base / manifest_relative_path).resolve()
    if not _inside(manifest_path, registry_root) or not manifest_path.is_file():
        raise PackContractError(
            "registry_invalid",
            f"packs.{selected_id}.manifest_path",
            "manifest_unavailable",
        )
    status = _text(raw_entry.get("status"), "registry_invalid", f"packs.{selected_id}.status")
    source_of_truth = raw_entry.get("source_of_truth")
    if not isinstance(source_of_truth, bool):
        raise PackContractError(
            "registry_invalid",
            f"packs.{selected_id}.source_of_truth",
            "expected_boolean",
        )
    if status != "production":
        raise PackContractError(
            "registry_invalid",
            f"packs.{selected_id}.status",
            "pack_not_production",
        )
    if source_of_truth is not True:
        raise PackContractError(
            "registry_invalid",
            f"packs.{selected_id}.source_of_truth",
            "pack_not_source_of_truth",
        )
    return RegistryEntry(
        registry_path=registry_path,
        pack_id=selected_id,
        manifest_path=manifest_path,
        manifest_relative_path=manifest_relative_path,
        status=status,
        source_of_truth=source_of_truth,
        raw=copy.deepcopy(dict(raw_entry)),
    )


def _manifest_integrity(data: Mapping[str, Any]) -> tuple[str, str]:
    integrity = _mapping(data.get("integrity"), "manifest_invalid", "integrity")
    supplied_manifest = _sha256(
        integrity.get("manifest_digest"),
        "manifest_invalid",
        "integrity.manifest_digest",
    )
    supplied_pack = _sha256(
        integrity.get("pack_digest"),
        "manifest_invalid",
        "integrity.pack_digest",
    )
    canonical = copy.deepcopy(dict(data))
    canonical_integrity = _mapping(canonical.get("integrity"), "manifest_invalid", "integrity")
    canonical_integrity = dict(canonical_integrity)
    canonical_integrity.pop("manifest_digest", None)
    canonical_integrity.pop("pack_digest", None)
    canonical["integrity"] = canonical_integrity
    calculated_manifest = canonical_digest(canonical)
    calculated_pack = canonical_digest(
        {
            "manifest_digest": calculated_manifest,
            "assets": [
                {"asset_id": asset_id, "digest": data["assets"][asset_id]["digest"]}
                for asset_id in sorted(data["assets"])
            ],
        }
    )
    if supplied_manifest != calculated_manifest:
        raise PackContractError("manifest_digest_mismatch", "integrity.manifest_digest", "digest_mismatch")
    if supplied_pack != calculated_pack:
        raise PackContractError("manifest_digest_mismatch", "integrity.pack_digest", "digest_mismatch")
    return supplied_manifest, supplied_pack


def _validate_page_discoverability(
    page: Mapping[str, Any],
    page_id: str,
    assets: Mapping[str, AssetResolution],
) -> None:
    for key in ("methodology_asset_id", "positive_example_anchor", "review_anchor"):
        if key not in page:
            continue
        _text(page.get(key), "page_reference_invalid", f"pages.{page_id}.{key}")
    methodology_id = page.get("methodology_asset_id")
    if methodology_id is not None:
        methodology_asset = assets.get(str(methodology_id))
        if methodology_asset is None or methodology_asset.asset_type != "methodology":
            raise PackContractError(
                "page_reference_invalid",
                f"pages.{page_id}.methodology_asset_id",
                "methodology_asset_missing",
            )
    page_asset = assets[page["asset_id"]]
    frontmatter = _read_frontmatter(page_asset.path)
    declared_page_id = frontmatter.get("page_id")
    if declared_page_id is not None and declared_page_id != page_id:
        raise PackContractError(
            "page_reference_invalid",
            f"pages.{page_id}.asset_id",
            "page_frontmatter_id_mismatch",
        )
    text = page_asset.path.read_text(encoding="utf-8")
    for key in ("positive_example_anchor", "review_anchor"):
        anchor = page.get(key)
        if not anchor:
            continue
        heading = str(anchor).lstrip("#").strip()
        if heading and f"## {heading}" not in text:
            raise PackContractError(
                "page_reference_invalid",
                f"pages.{page_id}.{key}",
                "anchor_missing",
            )


def load_manifest(entry: RegistryEntry) -> PackManifest:
    data = _load_yaml(entry.manifest_path, "manifest_invalid")
    if data.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise PackContractError("manifest_invalid", "schema_version", "unsupported_schema")
    pack = _mapping(data.get("pack"), "manifest_invalid", "pack")
    manifest_pack_id = _text(pack.get("pack_id"), "manifest_invalid", "pack.pack_id")
    if manifest_pack_id != entry.pack_id:
        raise PackContractError("manifest_invalid", "pack.pack_id", "registry_manifest_pack_mismatch")
    version = _text(pack.get("version"), "manifest_invalid", "pack.version")
    if pack.get("source_of_truth") is not True:
        raise PackContractError("manifest_invalid", "pack.source_of_truth", "must_be_true")

    consumer_interface = _mapping(
        data.get("consumer_interface"),
        "manifest_invalid",
        "consumer_interface",
    )
    consumer_version = _text(
        consumer_interface.get("version"),
        "manifest_invalid",
        "consumer_interface.version",
    )
    if consumer_version != CONSUMER_CONTRACT_VERSION:
        raise PackContractError(
            "manifest_invalid",
            "consumer_interface.version",
            "unsupported_consumer_contract",
        )
    operations = _list(
        consumer_interface.get("operations"),
        "manifest_invalid",
        "consumer_interface.operations",
    )
    declared_operations = tuple(
        _text(operation, "manifest_invalid", "consumer_interface.operations")
        for operation in operations
    )
    if len(set(declared_operations)) != len(declared_operations):
        raise PackContractError(
            "manifest_invalid",
            "consumer_interface.operations",
            "duplicate_operation",
        )
    required_operations = {"resolve_pack", "resolve_asset", "resolve_page_contract"}
    if not required_operations.issubset(declared_operations):
        raise PackContractError(
            "manifest_invalid",
            "consumer_interface.operations",
            "required_operation_missing",
        )
    forbidden = sorted(set(declared_operations) & _FORBIDDEN_OPERATIONS)
    if forbidden:
        raise PackContractError(
            "manifest_invalid",
            "consumer_interface.operations",
            "forbidden_operation:" + ",".join(forbidden),
        )

    assets_raw = _mapping(data.get("assets"), "manifest_invalid", "assets")
    assets: dict[str, AssetResolution] = {}
    public_paths: set[str] = set()
    pack_root = entry.manifest_path.parent.resolve()
    for raw_asset_id, raw_asset in assets_raw.items():
        asset_id = _text(raw_asset_id, "manifest_invalid", "assets.asset_id")
        asset = _mapping(raw_asset, "manifest_invalid", f"assets.{asset_id}")
        asset_type = _text(asset.get("type"), "manifest_invalid", f"assets.{asset_id}.type")
        public_path = _safe_relative_path(
            asset.get("public_path"),
            "manifest_invalid",
            f"assets.{asset_id}.public_path",
        )
        digest = _sha256(asset.get("digest"), "manifest_invalid", f"assets.{asset_id}.digest")
        if public_path in public_paths:
            raise PackContractError(
                "manifest_invalid",
                f"assets.{asset_id}.public_path",
                "duplicate_public_path",
            )
        asset_path = (pack_root / public_path).resolve()
        if not _inside(asset_path, pack_root) or not asset_path.is_file():
            raise PackContractError(
                "asset_unavailable",
                f"assets.{asset_id}",
                "asset_missing_or_outside_pack",
            )
        if file_digest(asset_path) != digest:
            raise PackContractError(
                "asset_unavailable",
                f"assets.{asset_id}.digest",
                "asset_digest_mismatch",
            )
        assets[asset_id] = AssetResolution(
            asset_id=asset_id,
            asset_type=asset_type,
            public_path=public_path,
            path=asset_path,
            digest=digest,
        )
        public_paths.add(public_path)

    manifest_digest, pack_digest = _manifest_integrity(data)

    pages_raw = _list(data.get("pages"), "manifest_invalid", "pages")
    pages: dict[str, Mapping[str, Any]] = {}
    for index, raw_page in enumerate(pages_raw):
        page = _mapping(raw_page, "manifest_invalid", f"pages[{index}]")
        page_id = _text(page.get("id"), "manifest_invalid", f"pages[{index}].id")
        asset_id = _text(page.get("asset_id"), "manifest_invalid", f"pages[{index}].asset_id")
        capability = _text(page.get("capability"), "manifest_invalid", f"pages[{index}].capability")
        if page_id in pages:
            raise PackContractError("page_reference_invalid", f"pages[{index}].id", "duplicate_page_id")
        if asset_id not in assets:
            raise PackContractError(
                "page_reference_invalid",
                f"pages.{page_id}.asset_id",
                "asset_missing",
            )
        _validate_page_discoverability(page, page_id, assets)
        pages[page_id] = copy.deepcopy(dict(page))

    materialization = _mapping(data.get("materialization"), "manifest_invalid", "materialization")
    scopes = _mapping(materialization.get("scopes"), "manifest_invalid", "materialization.scopes")
    for scope_name in scopes:
        _safe_relative_path(scope_name, "manifest_invalid", "materialization.scopes")
    materialization_pages = _mapping(
        materialization.get("pages"),
        "manifest_invalid",
        "materialization.pages",
    )
    if set(materialization_pages) != set(pages):
        raise PackContractError(
            "page_reference_invalid",
            "materialization.pages",
            "page_materialization_set_mismatch",
        )
    bound_targets: set[tuple[str, str]] = set()
    for page_id, raw_materialization in materialization_pages.items():
        item = _mapping(
            raw_materialization,
            "manifest_invalid",
            f"materialization.pages.{page_id}",
        )
        target_scope = _text(
            item.get("target_scope"),
            "manifest_invalid",
            f"materialization.pages.{page_id}.target_scope",
        )
        if target_scope not in scopes:
            raise PackContractError(
                "page_reference_invalid",
                f"materialization.pages.{page_id}.target_scope",
                "scope_missing",
            )
        target_path = _safe_relative_path(
            item.get("target_path"),
            "unsafe_path",
            f"materialization.pages.{page_id}.target_path",
        )
        required = item.get("required")
        if not isinstance(required, bool):
            raise PackContractError(
                "manifest_invalid",
                f"materialization.pages.{page_id}.required",
                "expected_boolean",
            )
        applicability = _text(
            item.get("applicability"),
            "manifest_invalid",
            f"materialization.pages.{page_id}.applicability",
        )
        if applicability not in _ALLOWED_APPLICABILITY:
            raise PackContractError(
                "manifest_invalid",
                f"materialization.pages.{page_id}.applicability",
                "unsupported_applicability",
            )
        collision_key = (target_scope, target_path.casefold())
        if collision_key in bound_targets:
            raise PackContractError(
                "page_reference_invalid",
                f"materialization.pages.{page_id}.target_path",
                "duplicate_target_path",
            )
        bound_targets.add(collision_key)

    return PackManifest(
        root=pack_root,
        registry_path=entry.registry_path.resolve(),
        manifest_path=entry.manifest_path.resolve(),
        pack_id=manifest_pack_id,
        version=version,
        consumer_contract_version=consumer_version,
        declared_operations=declared_operations,
        manifest_digest=manifest_digest,
        pack_digest=pack_digest,
        assets=assets,
        pages=pages,
        materialization=copy.deepcopy(dict(materialization)),
        raw=copy.deepcopy(dict(data)),
    )


def resolve_pack(registry_path: Path | str, pack_id: str | None = None) -> PackManifest:
    return load_manifest(resolve_registry(registry_path, pack_id))


def resolve_asset(pack: PackManifest, asset_id: str) -> AssetResolution:
    asset_id = _text(asset_id, "page_reference_invalid", "asset_id")
    try:
        return pack.assets[asset_id]
    except KeyError as error:
        raise PackContractError("page_reference_invalid", f"assets.{asset_id}", "asset_missing") from error


def resolve_page_contract(pack: PackManifest, page_id: str) -> PageResolution:
    page_id = _text(page_id, "page_reference_invalid", "page_id")
    try:
        page = pack.pages[page_id]
    except KeyError as error:
        raise PackContractError("page_reference_invalid", f"pages.{page_id}", "page_missing") from error
    materialization_pages = _mapping(
        pack.materialization["pages"],
        "manifest_invalid",
        "materialization.pages",
    )
    materialization = _mapping(
        materialization_pages[page_id],
        "manifest_invalid",
        f"materialization.pages.{page_id}",
    )
    return PageResolution(
        page_id=page_id,
        asset_id=str(page["asset_id"]),
        capability=str(page["capability"]),
        asset=resolve_asset(pack, str(page["asset_id"])),
        target_scope=str(materialization["target_scope"]),
        target_path=str(materialization["target_path"]),
        required=bool(materialization["required"]),
        applicability=str(materialization["applicability"]),
        raw=copy.deepcopy(dict(page)),
    )


def _validate_work_contract(
    work_contract: Mapping[str, Any],
    pack: PackManifest,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    required = (
        "schema_version",
        "work_contract_id",
        "project_id",
        "repository",
        "base_commit",
        "registry_path",
        "pack_id",
        "manifest_path",
        "manifest_digest",
        "pack_digest",
        "consumer_contract_version",
        "source_units",
        "target_profile_ref",
        "project_root",
        "module_root",
        "scope_bindings",
        "module_bindings",
        "module_map_digest",
        "permission_boundary",
        "batch",
        "prohibited",
        "evidence_refs",
        "confidence",
        "target_conflicts",
    )
    for key in required:
        if key not in work_contract:
            findings.append(_finding("work_contract_invalid", key, "missing"))
    if work_contract.get("schema_version") != 1:
        findings.append(_finding("work_contract_invalid", "schema_version", "unsupported_schema"))
    if work_contract.get("pack_id") != pack.pack_id:
        findings.append(_finding("review_binding_mismatch", "pack_id", "pack_id_mismatch"))
    if work_contract.get("manifest_digest") != pack.manifest_digest:
        findings.append(_finding("review_binding_mismatch", "manifest_digest", "manifest_digest_mismatch"))
    if work_contract.get("pack_digest") != pack.pack_digest:
        findings.append(_finding("review_binding_mismatch", "pack_digest", "pack_digest_mismatch"))
    if work_contract.get("consumer_contract_version") != pack.consumer_contract_version:
        findings.append(
            _finding(
                "review_binding_mismatch",
                "consumer_contract_version",
                "consumer_contract_version_mismatch",
            )
        )
    for key in ("work_contract_id", "project_id", "repository", "base_commit", "module_map_digest"):
        if key in work_contract and (
            not isinstance(work_contract[key], str)
            or not work_contract[key]
            or (key == "module_map_digest" and not _SHA256_RE.fullmatch(work_contract[key]))
        ):
            findings.append(_finding("work_contract_invalid", key, "invalid_value"))
    if "candidate_commit" in work_contract and (
        not isinstance(work_contract["candidate_commit"], str)
        or len(work_contract["candidate_commit"]) < 7
    ):
        findings.append(_finding("work_contract_invalid", "candidate_commit", "invalid_value"))
    for key in ("registry_path", "manifest_path", "project_root", "module_root"):
        try:
            _safe_relative_path(work_contract.get(key), "unsafe_path", key)
        except PackContractError as error:
            findings.append(_finding(error.code, error.location, error.detail))
    for key, expected_path in (
        ("registry_path", pack.registry_path),
        ("manifest_path", pack.manifest_path),
    ):
        declared_path = work_contract.get(key)
        if isinstance(declared_path, str):
            declared_absolute_path = (_repository_root(pack.registry_path) / declared_path).resolve()
            if declared_absolute_path != expected_path.resolve():
                findings.append(
                    _finding(
                        "review_binding_mismatch",
                        key,
                        "path_mismatch",
                    )
                )

    target_profile_ref = work_contract.get("target_profile_ref")
    if not isinstance(target_profile_ref, Mapping):
        findings.append(_finding("work_contract_invalid", "target_profile_ref", "expected_mapping"))
    else:
        for key in ("path", "profile_id", "profile_version", "profile_digest"):
            if key not in target_profile_ref:
                findings.append(_finding("work_contract_invalid", f"target_profile_ref.{key}", "missing"))
        if "profile_id" in target_profile_ref and (
            not isinstance(target_profile_ref["profile_id"], str)
            or not target_profile_ref["profile_id"]
        ):
            findings.append(
                _finding(
                    "work_contract_invalid",
                    "target_profile_ref.profile_id",
                    "expected_non_empty_string",
                )
            )
        if "profile_version" in target_profile_ref and (
            isinstance(target_profile_ref["profile_version"], bool)
            or not isinstance(target_profile_ref["profile_version"], (int, str))
            or (isinstance(target_profile_ref["profile_version"], str) and not target_profile_ref["profile_version"])
        ):
            findings.append(
                _finding(
                    "work_contract_invalid",
                    "target_profile_ref.profile_version",
                    "invalid_value",
                )
            )
        if "profile_digest" in target_profile_ref and (
            not isinstance(target_profile_ref["profile_digest"], str)
            or not _SHA256_RE.fullmatch(target_profile_ref["profile_digest"])
        ):
            findings.append(
                _finding(
                    "work_contract_invalid",
                    "target_profile_ref.profile_digest",
                    "expected_sha256",
                )
            )
        if "path" in target_profile_ref:
            try:
                _safe_relative_path(
                    target_profile_ref["path"],
                    "unsafe_path",
                    "target_profile_ref.path",
                )
            except PackContractError as error:
                findings.append(_finding(error.code, error.location, error.detail))

    source_units = work_contract.get("source_units")
    if not isinstance(source_units, list) or not source_units:
        findings.append(_finding("work_contract_invalid", "source_units", "expected_non_empty_list"))
    else:
        source_unit_ids: set[str] = set()
        for index, source_unit in enumerate(source_units):
            location = f"source_units[{index}]"
            if not isinstance(source_unit, Mapping):
                findings.append(_finding("work_contract_invalid", location, "expected_mapping"))
                continue
            unit_id = source_unit.get("unit_id")
            if not isinstance(unit_id, str) or not unit_id:
                findings.append(_finding("work_contract_invalid", f"{location}.unit_id", "expected_non_empty_string"))
            elif unit_id in source_unit_ids:
                findings.append(_finding("work_contract_invalid", f"{location}.unit_id", "duplicate"))
            source_unit_ids.add(str(unit_id))
            try:
                _safe_relative_path(
                    source_unit.get("relative_path"),
                    "unsafe_path",
                    f"{location}.relative_path",
                )
            except PackContractError as error:
                findings.append(_finding(error.code, error.location, error.detail))
            exclusions = source_unit.get("exclusions", [])
            if not isinstance(exclusions, list):
                findings.append(
                    _finding(
                        "work_contract_invalid",
                        f"{location}.exclusions",
                        "expected_list",
                    )
                )
            else:
                for exclusion_index, exclusion in enumerate(exclusions):
                    try:
                        _safe_relative_path(
                            exclusion,
                            "unsafe_path",
                            f"{location}.exclusions[{exclusion_index}]",
                        )
                    except PackContractError as error:
                        findings.append(_finding(error.code, error.location, error.detail))
            for key in ("repository_id", "baseline"):
                if key in source_unit and (
                    not isinstance(source_unit[key], str) or not source_unit[key]
                ):
                    findings.append(
                        _finding(
                            "work_contract_invalid",
                            f"{location}.{key}",
                            "expected_non_empty_string",
                        )
                    )
            roles = source_unit.get("roles")
            if not isinstance(roles, list) or not roles:
                findings.append(_finding("work_contract_invalid", f"{location}.roles", "expected_non_empty_list"))
            elif any(
                not isinstance(role, str) or role not in _ALLOWED_SOURCE_ROLES
                for role in roles
            ):
                findings.append(_finding("work_contract_invalid", f"{location}.roles", "unsupported_role"))
    scope_bindings = work_contract.get("scope_bindings")
    if not isinstance(scope_bindings, Mapping):
        findings.append(_finding("work_contract_invalid", "scope_bindings", "expected_mapping"))
    else:
        for scope_name in pack.materialization.get("scopes", {}):
            if scope_name not in scope_bindings:
                findings.append(
                    _finding(
                        "work_contract_invalid",
                        f"scope_bindings.{scope_name}",
                        "missing",
                    )
                )
            else:
                try:
                    _safe_relative_path(
                        scope_bindings[scope_name],
                        "unsafe_path",
                        f"scope_bindings.{scope_name}",
                    )
                except PackContractError as error:
                    findings.append(_finding(error.code, error.location, error.detail))
        bound_scope_paths = {
            value for value in scope_bindings.values() if isinstance(value, str)
        }
        for key in ("project_root", "module_root"):
            if work_contract.get(key) not in bound_scope_paths:
                findings.append(
                    _finding(
                        "work_contract_invalid",
                        key,
                        "scope_binding_missing",
                    )
                )
    module_bindings = work_contract.get("module_bindings")
    if not isinstance(module_bindings, list) or not module_bindings:
        findings.append(_finding("work_contract_invalid", "module_bindings", "expected_non_empty_list"))
    else:
        for index, module_binding in enumerate(module_bindings):
            location = f"module_bindings[{index}]"
            if not isinstance(module_binding, Mapping):
                findings.append(_finding("work_contract_invalid", location, "expected_mapping"))
                continue
            for key in ("module_id", "domain", "owner_slot", "module_root", "slot_index_path"):
                if not isinstance(module_binding.get(key), str) or not module_binding.get(key):
                    findings.append(
                        _finding(
                            "work_contract_invalid",
                            f"{location}.{key}",
                            "expected_non_empty_string",
                        )
                    )
            for key in ("module_root", "slot_index_path"):
                if key in module_binding:
                    try:
                        _safe_relative_path(
                            module_binding[key],
                            "unsafe_path",
                            f"{location}.{key}",
                        )
                    except PackContractError as error:
                        findings.append(_finding(error.code, error.location, error.detail))
            if module_binding.get("module_root") != work_contract.get("module_root"):
                findings.append(
                    _finding(
                        "work_contract_invalid",
                        f"{location}.module_root",
                        "module_root_mismatch",
                    )
                )
    batch = work_contract.get("batch")
    if not isinstance(batch, Mapping):
        findings.append(_finding("work_contract_invalid", "batch", "expected_mapping"))
    else:
        if not isinstance(batch.get("batch_id"), str) or not batch.get("batch_id"):
            findings.append(_finding("work_contract_invalid", "batch.batch_id", "expected_non_empty_string"))
        module_ids = batch.get("module_ids")
        if not isinstance(module_ids, list) or not module_ids:
            findings.append(_finding("work_contract_invalid", "batch.module_ids", "expected_non_empty_list"))
        elif any(not isinstance(module_id, str) or not module_id for module_id in module_ids):
            findings.append(_finding("work_contract_invalid", "batch.module_ids", "invalid_value"))
    if not isinstance(work_contract.get("prohibited"), list):
        findings.append(_finding("work_contract_invalid", "prohibited", "expected_list"))
    if not isinstance(work_contract.get("evidence_refs"), list):
        findings.append(_finding("work_contract_invalid", "evidence_refs", "expected_list"))
    if not isinstance(work_contract.get("confidence"), str) or not work_contract.get("confidence"):
        findings.append(_finding("work_contract_invalid", "confidence", "expected_non_empty_string"))
    target_conflicts = work_contract.get("target_conflicts")
    if not isinstance(target_conflicts, Mapping):
        findings.append(_finding("work_contract_invalid", "target_conflicts", "expected_mapping"))
    permission_boundary = work_contract.get("permission_boundary")
    if not isinstance(permission_boundary, Mapping):
        findings.append(_finding("work_contract_invalid", "permission_boundary", "expected_mapping"))
    else:
        for key in ("runtime_read", "business_write", "reality_write", "project_execution"):
            if permission_boundary.get(key) is not False:
                findings.append(
                    _finding(
                        "permission_boundary_invalid",
                        f"permission_boundary.{key}",
                        "must_be_false",
                    )
                )
        if permission_boundary.get("static_read") is not True:
            findings.append(
                _finding("permission_boundary_invalid", "permission_boundary.static_read", "must_be_true")
            )
    return findings


def validate_work_contract(
    work_contract: Mapping[str, Any],
    pack: PackManifest,
) -> PackageValidation:
    if not isinstance(work_contract, Mapping):
        return PackageValidation(
            status="blocked",
            findings=(_finding("work_contract_invalid", "$", "expected_mapping"),),
        )
    findings = _validate_work_contract(work_contract, pack)
    return PackageValidation(
        status="pass" if not findings else "blocked",
        findings=tuple(findings),
    )


def _profile_findings(
    profile: Mapping[str, Any] | None,
    page: PageResolution,
    module_instance: Mapping[str, Any] | None,
    scope_kind: str,
    work_contract: Mapping[str, Any],
    profile_path: Path | str | None,
) -> list[dict[str, str]]:
    if profile is None:
        return [
            _finding(
                "profile_reconciliation_required",
                "target_profile_ref",
                "profile_snapshot_required",
            )
        ]
    findings: list[dict[str, str]] = []
    if "artifact_type" in work_contract or "artifact_selector" in work_contract or "profile_version" in work_contract:
        profile_binding = validate_review_profile_binding(
            profile,
            artifact_type=work_contract.get("artifact_type"),
            selector=work_contract.get("artifact_selector"),
            expected_version=work_contract.get("profile_version"),
            expected_digest=work_contract.get("profile_digest"),
        )
        findings.extend(profile_binding["findings"])
    target_profile_ref = work_contract.get("target_profile_ref")
    if not isinstance(target_profile_ref, Mapping):
        return [
            _finding(
                "work_contract_invalid",
                "target_profile_ref",
                "expected_mapping",
            )
        ]
    expected_profile_id = target_profile_ref.get("profile_id")
    if profile.get("profile_id") != expected_profile_id:
        findings.append(
            _finding(
                "profile_reconciliation_required",
                "target_profile_ref.profile_id",
                "profile_id_mismatch",
            )
        )
    expected_profile_version = target_profile_ref.get("profile_version")
    actual_profile_version = profile.get("profile_version", profile.get("layout_version"))
    if actual_profile_version != expected_profile_version:
        findings.append(
            _finding(
                "profile_reconciliation_required",
                "target_profile_ref.profile_version",
                "profile_version_mismatch",
            )
        )
    expected_profile_digest = target_profile_ref.get("profile_digest")
    actual_profile_digest = profile.get("profile_digest", profile.get("digest"))
    if not isinstance(actual_profile_digest, str) or not _SHA256_RE.fullmatch(actual_profile_digest):
        findings.append(
            _finding(
                "profile_reconciliation_required",
                "target_profile_ref.profile_digest",
                "profile_digest_required",
            )
        )
    elif actual_profile_digest != profile_digest(profile):
        findings.append(
            _finding(
                "profile_reconciliation_required",
                "profile.profile_digest",
                "profile_digest_mismatch",
            )
        )
    if expected_profile_digest != actual_profile_digest:
        findings.append(
            _finding(
                "profile_reconciliation_required",
                "target_profile_ref.profile_digest",
                "profile_digest_mismatch",
            )
        )
    declared_profile_path = profile_path
    if declared_profile_path is None:
        candidate_profile_path = profile.get("_source_path")
        if isinstance(candidate_profile_path, (str, Path)):
            declared_profile_path = candidate_profile_path
    if declared_profile_path is None:
        findings.append(
            _finding(
                "profile_reconciliation_required",
                "target_profile_ref.path",
                "profile_source_path_required",
            )
        )
    else:
        try:
            profile_path_value = (
                declared_profile_path.as_posix()
                if isinstance(declared_profile_path, Path)
                else declared_profile_path
            )
            if isinstance(profile_path_value, str) and Path(profile_path_value).is_absolute():
                absolute_profile_path = Path(profile_path_value).resolve()
                profile_path_value = absolute_profile_path.relative_to(
                    _repository_root(absolute_profile_path)
                ).as_posix()
            actual_profile_path = _safe_relative_path(
                profile_path_value,
                "unsafe_path",
                "profile_path",
            )
        except PackContractError as error:
            findings.append(_finding(error.code, error.location, error.detail))
        else:
            if actual_profile_path != target_profile_ref.get("path"):
                findings.append(
                    _finding(
                        "profile_reconciliation_required",
                        "target_profile_ref.path",
                        "profile_path_mismatch",
                    )
                )
    if scope_kind == "project":
        root_entries = profile.get("root_entries", [])
        project_entry_contract = profile.get("project_entry_contract", {})
        required_files = (
            project_entry_contract.get("required_files", [])
            if isinstance(project_entry_contract, Mapping)
            else []
        )
        if page.target_path not in root_entries and page.target_path not in required_files:
            findings.append(
                _finding(
                    "profile_reconciliation_required",
                    page.page_id,
                    f"root_entry_missing:{page.target_path}",
                )
            )
    elif scope_kind == "module":
        if not isinstance(module_instance, Mapping):
            return [
                _finding(
                    "profile_reconciliation_required",
                    page.page_id,
                    "module_instance_required",
                )
            ]
        domain = module_instance.get("domain")
        owner_slot = module_instance.get("owner_slot")
        domains = profile.get("domains", [])
        if domain not in domains:
            findings.append(
                _finding("profile_reconciliation_required", page.page_id, f"domain_missing:{domain}")
            )
        registry = profile.get("document_registry", {})
        owner_slots = registry.get("owner_slots", []) if isinstance(registry, Mapping) else []
        if owner_slot not in owner_slots:
            findings.append(
                _finding("profile_reconciliation_required", page.page_id, f"owner_slot_missing:{owner_slot}")
            )
        slot_index_path = module_instance.get("slot_index_path")
        if slot_index_path is None:
            findings.append(
                _finding("profile_reconciliation_required", page.page_id, "slot_index_path_missing")
            )
        else:
            try:
                _safe_relative_path(slot_index_path, "unsafe_path", "module.slot_index_path")
            except PackContractError as error:
                findings.append(_finding(error.code, error.location, error.detail))
            domain_entry_files = profile.get("domain_entry_files", [])
            if isinstance(domain_entry_files, list):
                expected_suffix = f"{owner_slot}/INDEX.md"
                if expected_suffix not in domain_entry_files:
                    findings.append(
                        _finding(
                            "profile_reconciliation_required",
                            page.page_id,
                            f"slot_entry_contract_missing:{expected_suffix}",
                        )
                    )
    else:
        findings.append(
            _finding(
                "manifest_invalid",
                f"materialization.pages.{page.page_id}.target_scope",
                "unsupported_binding_scope",
            )
        )
    return findings


def resolve_review_profile(
    profile: Mapping[str, Any] | None = None,
    *,
    profile_path: Path | str | None = None,
) -> dict[str, Any]:
    """Resolve an explicitly declared profile; never infer one from directories."""
    if profile is None and profile_path is not None:
        try:
            profile = _load_yaml(Path(profile_path), "profile_invalid")
        except PackContractError as error:
            return {"status": "blocked", "findings": [_finding(error.code, error.location, error.detail)]}
    if not isinstance(profile, Mapping):
        return {"status": "blocked", "findings": [_finding("profile_missing", "profile", "explicit_profile_required")]}
    return {"status": "verified", "findings": [], "profile": copy.deepcopy(dict(profile))}


def validate_review_profile_binding(
    profile: Mapping[str, Any] | None,
    *,
    artifact_type: str | None,
    selector: str | None = None,
    expected_version: str | None = None,
    expected_digest: str | None = None,
) -> dict[str, Any]:
    """Validate artifact/profile identity with explicit blocked findings."""
    resolved = resolve_review_profile(profile)
    findings = list(resolved["findings"])
    if findings:
        return {"status": "blocked", "findings": findings}
    value = resolved["profile"]
    profile_id = value.get("profile_id", value.get("id"))
    if not isinstance(profile_id, str) or not profile_id:
        findings.append(_finding("profile_schema_invalid", "profile_id", "profile_id_required"))
    profile_type = value.get("artifact_type", value.get("artifact_types"))
    types = profile_type if isinstance(profile_type, list) else [profile_type]
    if not isinstance(artifact_type, str) or not artifact_type:
        findings.append(_finding("profile_binding_missing", "artifact_type", "explicit_artifact_type_required"))
    elif artifact_type not in types:
        findings.append(_finding("profile_selector_mismatch", "artifact_type", "artifact_type_not_bound"))
    profile_selector = value.get("selector", value.get("artifact_selector"))
    if selector is not None and selector != profile_selector and selector not in (profile_selector if isinstance(profile_selector, list) else []):
        findings.append(_finding("profile_selector_mismatch", "selector", "selector_not_bound"))
    actual_version = value.get("version", value.get("profile_version"))
    if expected_version is not None and actual_version != expected_version:
        findings.append(_finding("profile_version_conflict", "version", "version_mismatch"))
    actual_digest = value.get("profile_digest", value.get("digest"))
    if not isinstance(actual_digest, str) or not _SHA256_RE.fullmatch(actual_digest):
        findings.append(_finding("profile_digest_missing", "profile_digest", "expected_sha256"))
    elif actual_digest != profile_digest(value):
        findings.append(_finding("profile_digest_mismatch", "profile_digest", "digest_mismatch"))
    if expected_digest is not None and actual_digest != expected_digest:
        findings.append(_finding("profile_digest_mismatch", "profile_digest", "expected_digest_mismatch"))
    return {"status": "blocked" if findings else "verified", "findings": findings, "profile": value}


def _scope_kind(
    work_contract: Mapping[str, Any],
    target_scope: str,
) -> str | None:
    scope_bindings = work_contract.get("scope_bindings")
    if not isinstance(scope_bindings, Mapping):
        return None
    bound_path = scope_bindings.get(target_scope)
    if bound_path == work_contract.get("project_root"):
        return "project"
    if bound_path == work_contract.get("module_root"):
        return "module"
    return None


def _module_binding_authorized(
    work_contract: Mapping[str, Any],
    module_instance: Mapping[str, Any],
) -> bool:
    bindings = work_contract.get("module_bindings")
    if not isinstance(bindings, list):
        return False
    keys = ("module_id", "domain", "owner_slot", "module_root", "slot_index_path")
    return any(
        isinstance(binding, Mapping)
        and all(module_instance.get(key) == binding.get(key) for key in keys)
        for binding in bindings
    )


def _target_conflict(
    work_contract: Mapping[str, Any],
    output_path: str,
) -> tuple[str | None, dict[str, str] | None]:
    if "target_conflicts" not in work_contract:
        return None, _finding(
            "target_conflict_requires_decision",
            "target_conflicts",
            "target_conflict_snapshot_required",
        )
    conflicts = work_contract.get("target_conflicts")
    if not isinstance(conflicts, Mapping):
        return None, _finding("work_contract_invalid", "target_conflicts", "expected_mapping")
    if output_path not in conflicts:
        return None, _finding(
            "target_conflict_requires_decision",
            output_path,
            "missing_conflict_snapshot",
        )
    raw_decision = conflicts[output_path]
    if isinstance(raw_decision, Mapping):
        exists = raw_decision.get("exists")
        if not isinstance(exists, bool):
            return None, _finding(
                "target_conflict_requires_decision",
                output_path,
                "missing_existence_state",
            )
        if not exists:
            return None, None
        decision = raw_decision.get("decision")
    else:
        decision = raw_decision
    if decision not in _ALLOWED_CONFLICT_DECISIONS:
        return None, _finding(
            "target_conflict_requires_decision",
            output_path,
            "missing_or_invalid_decision",
        )
    if decision == "block":
        return None, _finding("target_conflict_requires_decision", output_path, "blocked_by_decision")
    return str(decision), None


def bind_target(
    pack: PackManifest,
    page_id: str,
    work_contract: Mapping[str, Any],
    module_instance: Mapping[str, Any] | None = None,
    *,
    profile: Mapping[str, Any] | None = None,
    profile_path: Path | str | None = None,
) -> BoundTarget:
    contract_findings = _validate_work_contract(work_contract, pack)
    if contract_findings:
        first = contract_findings[0]
        raise PackContractError(first["code"], first["location"], first["detail"])
    page = resolve_page_contract(pack, page_id)
    scope_kind = _scope_kind(work_contract, page.target_scope)
    if scope_kind is None:
        raise PackContractError(
            "manifest_invalid",
            f"materialization.pages.{page.page_id}.target_scope",
            "unsupported_binding_scope",
        )
    if scope_kind == "module" and (
        not isinstance(module_instance, Mapping)
        or not _module_binding_authorized(work_contract, module_instance)
    ):
        raise PackContractError(
            "work_contract_invalid",
            "module_bindings",
            "module_instance_not_authorized",
        )
    profile_findings = _profile_findings(
        profile,
        page,
        module_instance,
        scope_kind,
        work_contract,
        profile_path,
    )
    if profile_findings:
        first = profile_findings[0]
        raise PackContractError(first["code"], first["location"], first["detail"])
    scope_bindings = _mapping(work_contract["scope_bindings"], "work_contract_invalid", "scope_bindings")
    scope_root = _safe_relative_path(
        scope_bindings[page.target_scope],
        "unsafe_path",
        f"scope_bindings.{page.target_scope}",
    )
    output_path = (PurePosixPath(scope_root) / page.target_path).as_posix()
    conflict_decision, conflict_finding = _target_conflict(work_contract, output_path)
    if conflict_finding:
        raise PackContractError(
            conflict_finding["code"],
            conflict_finding["location"],
            conflict_finding["detail"],
        )
    module_id = None
    if isinstance(module_instance, Mapping):
        module_id_value = module_instance.get("module_id")
        if module_id_value is not None:
            module_id = _text(module_id_value, "work_contract_invalid", "module.module_id")
    return BoundTarget(
        page_id=page.page_id,
        module_id=module_id,
        target_scope=page.target_scope,
        target_path=page.target_path,
        output_path=output_path,
        conflict_decision=conflict_decision,
        legacy_non_executable=page.legacy_non_executable,
    )


def _source_ref_findings(
    source_ref: Any,
    location: str,
    work_contract: Mapping[str, Any] | None,
) -> list[dict[str, str]]:
    if not isinstance(source_ref, Mapping):
        return [_finding("source_ref_invalid", location, "expected_mapping")]
    findings: list[dict[str, str]] = []
    required = (
        "repository_id",
        "source_unit",
        "role",
        "baseline",
        "relative_path",
        "anchor",
        "evidence_state",
        "locator_quality",
        "evidence_sufficiency",
    )
    for key in required:
        if key not in source_ref:
            findings.append(_finding("source_ref_invalid", f"{location}.{key}", "missing"))
    for key in ("repository_id", "source_unit", "baseline", "anchor"):
        if key in source_ref and (not isinstance(source_ref[key], str) or not source_ref[key]):
            findings.append(_finding("source_ref_invalid", f"{location}.{key}", "expected_non_empty_string"))
    if "relative_path" in source_ref:
        path, finding = _safe_path_or_finding(source_ref["relative_path"], f"{location}.relative_path")
        if finding:
            findings.append(_finding("source_ref_invalid", finding["location"], finding["detail"]))
        elif path is None:
            findings.append(_finding("source_ref_invalid", f"{location}.relative_path", "invalid"))
    if source_ref.get("role") not in _ALLOWED_SOURCE_ROLES:
        findings.append(_finding("source_ref_invalid", f"{location}.role", "unsupported_role"))
    if source_ref.get("evidence_state") not in _ALLOWED_EVIDENCE_STATES:
        findings.append(_finding("source_ref_invalid", f"{location}.evidence_state", "unsupported_state"))
    if source_ref.get("locator_quality") not in _ALLOWED_LOCATOR_QUALITY:
        findings.append(
            _finding("source_ref_invalid", f"{location}.locator_quality", "unsupported_locator_quality")
        )
    if source_ref.get("evidence_sufficiency") not in _ALLOWED_EVIDENCE_SUFFICIENCY:
        findings.append(
            _finding(
                "source_ref_invalid",
                f"{location}.evidence_sufficiency",
                "unsupported_evidence_sufficiency",
            )
        )
    if isinstance(work_contract, Mapping):
        source_units = work_contract.get("source_units", [])
        matches = []
        source_unit_match = False
        source_path = source_ref.get("relative_path")
        if isinstance(source_units, list):
            for source_unit in source_units:
                if not isinstance(source_unit, Mapping):
                    continue
                if source_unit.get("unit_id") == source_ref.get("source_unit"):
                    source_unit_match = True
                    roles = source_unit.get("roles", [])
                    matches.append(source_ref.get("role") in roles)
                    expected_repository = source_unit.get(
                        "repository_id",
                        work_contract.get("repository"),
                    )
                    if source_ref.get("repository_id") != expected_repository:
                        findings.append(
                            _finding(
                                "source_ref_invalid",
                                f"{location}.repository_id",
                                "repository_mismatch",
                            )
                        )
                    expected_baseline = source_unit.get(
                        "baseline",
                        work_contract.get("base_commit"),
                    )
                    if source_ref.get("baseline") != expected_baseline:
                        findings.append(
                            _finding(
                                "source_ref_invalid",
                                f"{location}.baseline",
                                "baseline_mismatch",
                            )
                        )
                    unit_path = source_unit.get("relative_path")
                    if (
                        isinstance(unit_path, str)
                        and isinstance(source_path, str)
                        and not _posix_path_is_within(unit_path, source_path)
                    ):
                        findings.append(
                            _finding(
                                "source_ref_invalid",
                                f"{location}.relative_path",
                                "outside_source_unit",
                            )
                        )
                    exclusions = source_unit.get("exclusions", [])
                    if (
                        isinstance(source_path, str)
                        and isinstance(exclusions, list)
                        and any(
                            isinstance(exclusion, str)
                            and _posix_path_is_within(exclusion, source_path)
                            for exclusion in exclusions
                        )
                    ):
                        findings.append(
                            _finding(
                                "source_ref_invalid",
                                f"{location}.relative_path",
                                "excluded_source_path",
                            )
                        )
        if not source_unit_match:
            findings.append(
                _finding(
                    "source_ref_invalid",
                    f"{location}.source_unit",
                    "source_unit_not_authorized",
                )
            )
        if not any(matches):
            findings.append(
                _finding(
                    "source_ref_invalid",
                    f"{location}.source_unit",
                    "source_unit_role_not_authorized",
                )
            )
    return findings


def _review_layer_findings(review_layers: Any) -> list[dict[str, str]]:
    if not isinstance(review_layers, Mapping):
        return [_finding("review_binding_mismatch", "review_layers", "expected_mapping")]
    findings: list[dict[str, str]] = []
    for layer in ("structure", "content", "confidence"):
        item = review_layers.get(layer)
        if not isinstance(item, Mapping):
            findings.append(_finding("review_binding_mismatch", f"review_layers.{layer}", "missing"))
            continue
        status = item.get("status")
        if status not in _ALLOWED_REVIEW_STATUS:
            findings.append(
                _finding("review_binding_mismatch", f"review_layers.{layer}.status", "unsupported_status")
            )
        elif status != "pass":
            findings.append(
                _finding("review_binding_mismatch", f"review_layers.{layer}.status", "layer_not_pass")
            )
        if not isinstance(item.get("findings"), list):
            findings.append(
                _finding("review_binding_mismatch", f"review_layers.{layer}.findings", "expected_list")
            )
    return findings


def validate_package(
    package: Mapping[str, Any],
    pack: PackManifest,
    work_contract: Mapping[str, Any] | None = None,
    *,
    profile: Mapping[str, Any] | None = None,
    profile_path: Path | str | None = None,
) -> PackageValidation:
    if not isinstance(package, Mapping):
        return PackageValidation(
            status="blocked",
            findings=(_finding("package_invalid", "$", "expected_mapping"),),
        )
    findings: list[dict[str, str]] = []
    if work_contract is None:
        findings.append(
            _finding(
                "work_contract_invalid",
                "work_contract",
                "required_for_package_validation",
            )
        )
    required = (
        "schema_version",
        "package_id",
        "work_contract_digest",
        "pack_binding",
        "module_map_digest",
        "gate_a",
        "gate_b",
        "module",
        "reviewed_paths",
        "pages",
        "review_layers",
        "findings",
        "unknowns",
        "evidence_refs",
    )
    for key in required:
        if key not in package:
            findings.append(_finding("package_invalid", key, "missing"))
    if package.get("schema_version") != 1:
        findings.append(_finding("package_invalid", "schema_version", "unsupported_schema"))
    for key in ("work_contract_digest", "module_map_digest"):
        if key in package and (
            not isinstance(package[key], str) or not _SHA256_RE.fullmatch(package[key])
        ):
            findings.append(_finding("package_invalid", key, "expected_sha256"))

    pack_binding = package.get("pack_binding")
    if not isinstance(pack_binding, Mapping):
        findings.append(_finding("review_binding_mismatch", "pack_binding", "expected_mapping"))
    else:
        expected_bindings = {
            "pack_id": pack.pack_id,
            "manifest_digest": pack.manifest_digest,
            "pack_digest": pack.pack_digest,
            "consumer_contract_version": pack.consumer_contract_version,
        }
        for key, expected in expected_bindings.items():
            if pack_binding.get(key) != expected:
                findings.append(
                    _finding("review_binding_mismatch", f"pack_binding.{key}", "value_mismatch")
                )

    gate_digests: dict[str, str] = {}
    for gate_name in ("gate_a", "gate_b"):
        gate = package.get(gate_name)
        if not isinstance(gate, Mapping):
            findings.append(_finding("package_invalid", gate_name, "expected_mapping"))
            continue
        if gate.get("status") != "accepted":
            findings.append(_finding("review_binding_mismatch", f"{gate_name}.status", "gate_not_accepted"))
        digest = gate.get("digest")
        if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
            findings.append(_finding("package_invalid", f"{gate_name}.digest", "expected_sha256"))
        else:
            gate_digests[gate_name] = digest

    module = package.get("module")
    if not isinstance(module, Mapping):
        findings.append(_finding("package_invalid", "module", "expected_mapping"))
    else:
        for key in ("module_id", "domain", "owner_slot", "module_root"):
            if not isinstance(module.get(key), str) or not module.get(key):
                findings.append(_finding("package_invalid", f"module.{key}", "expected_non_empty_string"))
        try:
            _safe_relative_path(module.get("module_root"), "unsafe_path", "module.module_root")
        except PackContractError as error:
            findings.append(_finding(error.code, error.location, error.detail))
        if (
            "slot_index_path" not in module
            or not isinstance(module.get("slot_index_path"), str)
            or not module.get("slot_index_path")
        ):
            findings.append(_finding("package_invalid", "module.slot_index_path", "missing"))
        else:
            try:
                _safe_relative_path(
                    module["slot_index_path"],
                    "unsafe_path",
                    "module.slot_index_path",
                )
            except PackContractError as error:
                findings.append(_finding(error.code, error.location, error.detail))

    reviewed_paths = package.get("reviewed_paths")
    if not isinstance(reviewed_paths, list):
        findings.append(_finding("package_invalid", "reviewed_paths", "expected_list"))
    else:
        if not reviewed_paths:
            findings.append(
                _finding(
                    "package_invalid",
                    "reviewed_paths",
                    "expected_non_empty_list",
                )
            )
        for index, path in enumerate(reviewed_paths):
            try:
                _safe_relative_path(path, "unsafe_path", f"reviewed_paths[{index}]")
            except PackContractError as error:
                findings.append(_finding(error.code, error.location, error.detail))

    package_pages = package.get("pages")
    bound_targets: list[BoundTarget] = []
    target_keys: set[str] = set()
    if not isinstance(package_pages, list):
        findings.append(_finding("package_invalid", "pages", "expected_list"))
    else:
        if not package_pages:
            findings.append(
                _finding(
                    "package_invalid",
                    "pages",
                    "expected_non_empty_list",
                )
            )
        for index, raw_page in enumerate(package_pages):
            location = f"pages[{index}]"
            if not isinstance(raw_page, Mapping):
                findings.append(_finding("package_invalid", location, "expected_mapping"))
                continue
            page_id = raw_page.get("page_id")
            if not isinstance(page_id, str) or not page_id:
                findings.append(_finding("package_invalid", f"{location}.page_id", "expected_non_empty_string"))
                continue
            try:
                page = resolve_page_contract(pack, page_id)
            except PackContractError as error:
                findings.append(_finding(error.code, error.location, error.detail))
                continue
            if raw_page.get("target_scope") != page.target_scope:
                findings.append(_finding("review_binding_mismatch", f"{location}.target_scope", "value_mismatch"))
            if raw_page.get("target_path") != page.target_path:
                findings.append(_finding("review_binding_mismatch", f"{location}.target_path", "value_mismatch"))
            applicability = raw_page.get("applicability")
            if applicability not in _ALLOWED_APPLICABILITY:
                findings.append(_finding("package_invalid", f"{location}.applicability", "unsupported_applicability"))
            elif applicability != page.applicability:
                findings.append(
                    _finding(
                        "review_binding_mismatch",
                        f"{location}.applicability",
                        "value_mismatch",
                    )
                )
            knowledge_status = raw_page.get("knowledge_status")
            if knowledge_status not in _ALLOWED_KNOWLEDGE_STATUS:
                findings.append(
                    _finding("package_invalid", f"{location}.knowledge_status", "unsupported_knowledge_status")
                )
            fact_summary = raw_page.get("fact_summary")
            if applicability != "not_applicable" and (
                not isinstance(fact_summary, str) or not fact_summary.strip()
            ):
                findings.append(_finding("content_not_proven", f"{location}.fact_summary", "missing"))
            source_refs = raw_page.get("source_refs")
            if not isinstance(source_refs, list):
                findings.append(_finding("source_ref_invalid", f"{location}.source_refs", "expected_list"))
            else:
                if applicability != "not_applicable" and not source_refs:
                    findings.append(
                        _finding(
                            "source_ref_invalid",
                            f"{location}.source_refs",
                            "expected_non_empty_list",
                        )
                    )
                for source_index, source_ref in enumerate(source_refs):
                    findings.extend(
                        _source_ref_findings(
                            source_ref,
                            f"{location}.source_refs[{source_index}]",
                            work_contract,
                        )
                    )
            list_values: dict[str, list[Any]] = {}
            for list_key in ("claim_refs", "unknowns", "deep_dive_refs"):
                if not isinstance(raw_page.get(list_key), list):
                    findings.append(_finding("package_invalid", f"{location}.{list_key}", "expected_list"))
                else:
                    list_values[list_key] = raw_page[list_key]
            if (
                applicability == "not_applicable"
                and knowledge_status != "not_applicable"
            ) or (
                applicability != "not_applicable"
                and knowledge_status == "not_applicable"
            ):
                findings.append(
                    _finding(
                        "review_binding_mismatch",
                        f"{location}.knowledge_status",
                        "applicability_mismatch",
                    )
                )
            if applicability != "not_applicable":
                if knowledge_status == "established":
                    for list_key in ("claim_refs", "deep_dive_refs"):
                        if not list_values.get(list_key):
                            findings.append(
                                _finding(
                                    "content_not_proven",
                                    f"{location}.{list_key}",
                                    "expected_non_empty_list",
                                )
                            )
                elif knowledge_status in {"unknown", "not_established"} and not list_values.get("unknowns"):
                    findings.append(
                        _finding(
                            "content_not_proven",
                            f"{location}.unknowns",
                            "expected_non_empty_list",
                        )
                    )
            if work_contract is not None and isinstance(module, Mapping):
                try:
                    bound = bind_target(
                        pack,
                        page_id,
                        work_contract,
                        module,
                        profile=profile,
                        profile_path=profile_path,
                    )
                except PackContractError as error:
                    findings.append(_finding(error.code, error.location, error.detail))
                else:
                    key = bound.output_path.casefold()
                    if key in target_keys:
                        findings.append(
                            _finding("duplicate_target_path", location, bound.output_path)
                        )
                    else:
                        target_keys.add(key)
                        bound_targets.append(bound)

    for key in ("findings", "unknowns", "evidence_refs"):
        if not isinstance(package.get(key), list):
            findings.append(_finding("package_invalid", key, "expected_list"))
    findings.extend(_review_layer_findings(package.get("review_layers")))
    if work_contract is not None:
        expected_work_digest = canonical_digest(work_contract)
        if package.get("work_contract_digest") != expected_work_digest:
            findings.append(
                _finding("review_binding_mismatch", "work_contract_digest", "value_mismatch")
            )
        if package.get("module_map_digest") != work_contract.get("module_map_digest"):
            findings.append(
                _finding(
                    "review_binding_mismatch",
                    "module_map_digest",
                    "value_mismatch",
                )
            )
        findings.extend(_validate_work_contract(work_contract, pack))

    return PackageValidation(
        status="pass" if not findings else "blocked",
        findings=tuple(findings),
        bound_targets=tuple(bound_targets),
    )


__all__ = [
    "AssetResolution",
    "BoundTarget",
    "CONSUMER_CONTRACT_VERSION",
    "MANIFEST_SCHEMA_VERSION",
    "PackContractError",
    "PackManifest",
    "PackageValidation",
    "PageResolution",
    "RegistryEntry",
    "canonical_digest",
    "profile_digest",
    "file_digest",
    "bind_target",
    "load_manifest",
    "resolve_asset",
    "resolve_page_contract",
    "resolve_pack",
    "resolve_registry",
    "validate_package",
    "validate_work_contract",
    "resolve_review_profile",
    "validate_review_profile_binding",
]
