#!/usr/bin/env python3
"""Deterministic consumer for registry-registered Wiki Template Packs.

Consumes the registered Wiki writing guide with canonical digest validation and
the production-status gate. Template packs provide guidance only: they do not
declare project pages or generate Wiki content.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml

REGISTRY_SCHEMA_VERSION = "wiki-template-pack-registry/v1"
MANIFEST_SCHEMA_VERSION = "wiki-template-effect-pack/v1"
CONSUMER_CONTRACT_VERSION = "wiki-template-effect-pack-consumer/v1"
_SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_DRIVE_PATH_RE = re.compile(r"^[A-Za-z]:")


class WikiPackError(ValueError):
    """A deterministic wiki pack contract failure with a stable error code."""

    def __init__(self, code: str, location: str, detail: str) -> None:
        self.code = code
        self.location = location
        self.detail = detail
        super().__init__(f"{code}:{location}:{detail}")


def _mapping(value: Any, code: str, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise WikiPackError(code, location, "expected_mapping")
    return value


def _list(value: Any, code: str, location: str) -> list[Any]:
    if not isinstance(value, list):
        raise WikiPackError(code, location, "expected_list")
    return value


def _text(value: Any, code: str, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise WikiPackError(code, location, "expected_non_empty_string")
    return value


def _sha256(value: Any, code: str, location: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise WikiPackError(code, location, "expected_sha256")
    return value


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


def _safe_relative_path(value: Any, code: str, location: str) -> str:
    path = _text(value, code, location)
    if "\x00" in path or "\\" in path or path.startswith("/") or _DRIVE_PATH_RE.match(path) or "://" in path:
        raise WikiPackError(code, location, "unsafe_path")
    parts = path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise WikiPackError(code, location, "non_canonical_path")
    normalized = PurePosixPath(path).as_posix()
    if normalized != path:
        raise WikiPackError(code, location, "non_canonical_path")
    return path


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _load_yaml(path: Path, code: str) -> Mapping[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise WikiPackError(code, path.as_posix(), f"read_failed:{error}") from error
    return _mapping(value, code, path.as_posix())


def _finding(code: str, location: str, detail: str) -> dict[str, str]:
    return {"code": code, "location": location, "detail": detail}


@dataclass(frozen=True)
class WikiRegistryEntry:
    registry_path: Path
    pack_id: str
    manifest_path: Path
    manifest_relative_path: str
    status: str
    source_of_truth: bool
    raw: Mapping[str, Any]


@dataclass(frozen=True)
class WikiAssetResolution:
    asset_id: str
    asset_type: str
    public_path: str
    path: Path
    digest: str


@dataclass(frozen=True)
class WikiPackManifest:
    root: Path
    registry_path: Path
    manifest_path: Path
    pack_id: str
    version: str
    consumer_contract_version: str
    declared_operations: tuple[str, ...]
    manifest_digest: str
    pack_digest: str
    assets: Mapping[str, WikiAssetResolution]
    raw: Mapping[str, Any]


def resolve_registry(registry_path: Path | str, pack_id: str | None = None) -> WikiRegistryEntry:
    registry_path = Path(registry_path).resolve()
    data = _load_yaml(registry_path, "registry_invalid")
    if data.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        raise WikiPackError("registry_invalid", "schema_version", "unsupported_schema")
    registry_root = registry_path.parent
    raw_path_base = data.get("path_base", ".")
    path_base = "." if raw_path_base == "." else _safe_relative_path(raw_path_base, "registry_invalid", "path_base")
    packs = _mapping(data.get("packs"), "registry_invalid", "packs")
    selected_id = pack_id or data.get("default_pack_id")
    selected_id = _text(selected_id, "registry_invalid", "default_pack_id")
    raw_entry = _mapping(packs.get(selected_id), "registry_invalid", f"packs.{selected_id}")
    manifest_relative_path = _safe_relative_path(
        raw_entry.get("manifest_path"), "registry_invalid", f"packs.{selected_id}.manifest_path"
    )
    manifest_path = (registry_root / path_base / manifest_relative_path).resolve()
    if not _inside(manifest_path, registry_root) or not manifest_path.is_file():
        raise WikiPackError(
            "registry_invalid", f"packs.{selected_id}.manifest_path", "manifest_unavailable"
        )
    status = _text(raw_entry.get("status"), "registry_invalid", f"packs.{selected_id}.status")
    source_of_truth = raw_entry.get("source_of_truth")
    if not isinstance(source_of_truth, bool):
        raise WikiPackError("registry_invalid", f"packs.{selected_id}.source_of_truth", "expected_boolean")
    if status != "production":
        raise WikiPackError("registry_invalid", f"packs.{selected_id}.status", "pack_not_production")
    if source_of_truth is not True:
        raise WikiPackError("registry_invalid", f"packs.{selected_id}.source_of_truth", "pack_not_source_of_truth")
    return WikiRegistryEntry(
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
    supplied_manifest = _sha256(integrity.get("manifest_digest"), "manifest_invalid", "integrity.manifest_digest")
    supplied_pack = _sha256(integrity.get("pack_digest"), "manifest_invalid", "integrity.pack_digest")
    canonical = copy.deepcopy(dict(data))
    canonical_integrity = dict(_mapping(canonical.get("integrity"), "manifest_invalid", "integrity"))
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
        raise WikiPackError("manifest_digest_mismatch", "integrity.manifest_digest", "digest_mismatch")
    if supplied_pack != calculated_pack:
        raise WikiPackError("manifest_digest_mismatch", "integrity.pack_digest", "digest_mismatch")
    return supplied_manifest, supplied_pack


def _validate_asset_type(asset: WikiAssetResolution) -> None:
    if asset.asset_type not in {"methodology", "pack_readme"}:
        raise WikiPackError("asset_invalid", f"assets.{asset.asset_id}", "unsupported_asset_type")


def load_manifest(entry: WikiRegistryEntry) -> WikiPackManifest:
    data = _load_yaml(entry.manifest_path, "manifest_invalid")
    if data.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise WikiPackError("manifest_invalid", "schema_version", "unsupported_schema")
    pack = _mapping(data.get("pack"), "manifest_invalid", "pack")
    manifest_pack_id = _text(pack.get("pack_id"), "manifest_invalid", "pack.pack_id")
    if manifest_pack_id != entry.pack_id:
        raise WikiPackError("manifest_invalid", "pack.pack_id", "registry_manifest_pack_mismatch")
    version = _text(pack.get("version"), "manifest_invalid", "pack.version")
    if pack.get("source_of_truth") is not True:
        raise WikiPackError("manifest_invalid", "pack.source_of_truth", "must_be_true")

    consumer_interface = _mapping(data.get("consumer_interface"), "manifest_invalid", "consumer_interface")
    consumer_version = _text(consumer_interface.get("version"), "manifest_invalid", "consumer_interface.version")
    if consumer_version != CONSUMER_CONTRACT_VERSION:
        raise WikiPackError("manifest_invalid", "consumer_interface.version", "unsupported_consumer_contract")
    operations = _list(consumer_interface.get("operations"), "manifest_invalid", "consumer_interface.operations")
    declared_operations = tuple(_text(op, "manifest_invalid", "consumer_interface.operations") for op in operations)
    if len(set(declared_operations)) != len(declared_operations):
        raise WikiPackError("manifest_invalid", "consumer_interface.operations", "duplicate_operation")
    required_operations = {"resolve_pack", "resolve_asset"}
    if not required_operations.issubset(declared_operations):
        raise WikiPackError("manifest_invalid", "consumer_interface.operations", "required_operation_missing")

    assets_raw = _mapping(data.get("assets"), "manifest_invalid", "assets")
    assets: dict[str, WikiAssetResolution] = {}
    public_paths: set[str] = set()
    pack_root = entry.manifest_path.parent.resolve()
    for raw_asset_id, raw_asset in assets_raw.items():
        asset_id = _text(raw_asset_id, "manifest_invalid", "assets.asset_id")
        asset = _mapping(raw_asset, "manifest_invalid", f"assets.{asset_id}")
        asset_type = _text(asset.get("type"), "manifest_invalid", f"assets.{asset_id}.type")
        public_path = _safe_relative_path(asset.get("public_path"), "manifest_invalid", f"assets.{asset_id}.public_path")
        digest = _sha256(asset.get("digest"), "manifest_invalid", f"assets.{asset_id}.digest")
        if public_path in public_paths:
            raise WikiPackError("manifest_invalid", f"assets.{asset_id}.public_path", "duplicate_public_path")
        asset_path = (pack_root / public_path).resolve()
        if not _inside(asset_path, pack_root) or not asset_path.is_file():
            raise WikiPackError("asset_unavailable", f"assets.{asset_id}", "asset_missing_or_outside_pack")
        if file_digest(asset_path) != digest:
            raise WikiPackError("asset_unavailable", f"assets.{asset_id}.digest", "asset_digest_mismatch")
        resolution = WikiAssetResolution(
            asset_id=asset_id, asset_type=asset_type, public_path=public_path, path=asset_path, digest=digest
        )
        _validate_asset_type(resolution)
        assets[asset_id] = resolution
        public_paths.add(public_path)

    manifest_digest, pack_digest = _manifest_integrity(data)

    return WikiPackManifest(
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
        raw=copy.deepcopy(dict(data)),
    )


def resolve_pack(registry_path: Path | str, pack_id: str | None = None) -> WikiPackManifest:
    return load_manifest(resolve_registry(registry_path, pack_id))


def resolve_asset(pack: WikiPackManifest, asset_id: str) -> WikiAssetResolution:
    asset_id = _text(asset_id, "asset_invalid", "asset_id")
    try:
        return pack.assets[asset_id]
    except KeyError as error:
        raise WikiPackError("asset_invalid", f"assets.{asset_id}", "asset_missing") from error


def resolve_methodology(pack: WikiPackManifest) -> WikiAssetResolution:
    """Return the methodology catalog asset (the FRAMEWORK.md render source)."""
    for asset in pack.assets.values():
        if asset.asset_type == "methodology":
            return asset
    raise WikiPackError("asset_invalid", "assets", "methodology_asset_missing")
