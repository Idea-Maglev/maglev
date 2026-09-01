"""Candidate-external immutable Result artifact support shared by adapters."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


class ResultArtifactError(ValueError):
    """Raised when a Result cannot be persisted as an external immutable artifact."""


def canonical_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def result_digest(result: Mapping[str, Any]) -> str:
    payload = copy.deepcopy(dict(result))
    artifact = payload.get("artifact")
    if isinstance(artifact, Mapping):
        artifact = dict(artifact)
        artifact.pop("store_ref", None)
        artifact.pop("result_digest", None)
        payload["artifact"] = artifact
    return canonical_digest(payload)


def write_external_result(
    result: Mapping[str, Any],
    *,
    kind: str,
    artifact_store_root: Path | str,
    candidate_root: Path | str,
) -> Mapping[str, Any]:
    """Write a Result once outside candidate Reality and return its bound mapping."""

    store = Path(artifact_store_root).resolve()
    candidate = Path(candidate_root).resolve()
    if not kind or "/" in kind or "\\" in kind:
        raise ResultArtifactError("artifact kind must be a path segment")
    if _inside(store, candidate) or _inside(candidate, store):
        raise ResultArtifactError("artifact store must be outside the candidate Reality tree")
    stored = copy.deepcopy(dict(result))
    artifact = stored.get("artifact")
    if not isinstance(artifact, Mapping):
        raise ResultArtifactError("result artifact mapping is required")
    digest = result_digest(stored)
    stored["artifact"] = dict(artifact)
    stored["artifact"]["result_digest"] = digest
    stored["artifact"]["store_ref"] = f"{kind}/{digest}.json"
    destination = (store / stored["artifact"]["store_ref"]).resolve()
    if not _inside(destination, store):
        raise ResultArtifactError("artifact path escapes the external store")
    payload = json.dumps(stored, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    if destination.exists():
        if destination.read_text(encoding="utf-8") != payload:
            raise ResultArtifactError("immutable artifact conflict")
        return stored
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(payload, encoding="utf-8")
    return stored


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True
