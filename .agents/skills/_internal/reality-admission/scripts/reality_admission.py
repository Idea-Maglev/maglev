#!/usr/bin/env python3
"""CLI adapter for committed Reality projection admission."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = SKILL_ROOT / "core.py"
SPEC = importlib.util.spec_from_file_location("maglev_reality_admission_core", CORE_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Unable to load Reality Admission core: {CORE_PATH}")
CORE = importlib.util.module_from_spec(SPEC)
sys.modules.setdefault(SPEC.name, CORE)
SPEC.loader.exec_module(CORE)


def _write_json(path: str | None, value: dict) -> None:
    if not path:
        return
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _load_validation(path: str) -> object:
    if path == "-":
        data = json.loads(sys.stdin.read())
        return CORE.ValidationResult.from_mapping(data)
    return CORE.ValidationResult.from_path(path)


def _render(value: dict, as_json: bool) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) if as_json else str(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Describe, validate, and accept a committed Reality projection"
    )
    parser.add_argument("--reality-root", default="specs/10_reality")
    parser.add_argument(
        "--base-ref",
        required=True,
        help="Git commit/ref before the Reality projection",
    )
    parser.add_argument(
        "--candidate-ref",
        default="HEAD",
        help="Committed projection ref checked out in the current worktree",
    )
    parser.add_argument(
        "--intended-use",
        action="append",
        default=[],
        help="Validation use case; may be repeated",
    )
    parser.add_argument(
        "--validation-result",
        help="Projection-bound Validation Result path, or '-' for JSON stdin",
    )
    parser.add_argument("--plan-out")
    parser.add_argument("--receipt-out")
    parser.add_argument(
        "--accept",
        action="store_true",
        help="Emit an acceptance receipt after the dry-run gate passes",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    projection = CORE.RealityProjection.from_repository(
        args.reality_root,
        args.base_ref,
        args.candidate_ref,
        intended_use=args.intended_use,
    )
    if not args.validation_result:
        data = projection.to_mapping()
        print(_render(data, args.json))
        return 0

    validation = _load_validation(args.validation_result)
    admission = CORE.Admission(args.reality_root)
    plan = admission.dry_run(projection, validation)
    plan_data = plan.to_mapping()
    if not args.accept:
        _write_json(args.plan_out, plan_data)
        print(_render(plan_data, args.json))
        return 0 if plan.status == "ready" else 1

    receipt = admission.accept(plan)
    receipt_data = receipt.to_mapping()
    _write_json(args.plan_out, plan_data)
    _write_json(args.receipt_out, receipt_data)
    print(_render(receipt_data, args.json))
    return 0 if receipt.status in {"accepted", "no_change"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
