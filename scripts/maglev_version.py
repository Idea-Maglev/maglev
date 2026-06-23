#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maglev Version Manager

统一管理 Maglev 的开发态与发行态版本事实，提供：
- show: 展示当前各版本源状态
- check: 校验各版本源是否一致
- set: 将所有受管版本文件同步到目标版本
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional


VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass
class ManagedJsonFile:
    path: str
    field: str = "version"
    required: bool = True


@dataclass
class ManagedTextFile:
    path: str
    pattern: str
    required: bool = False


CANONICAL_SOURCES: List[ManagedJsonFile] = [
    ManagedJsonFile("release.version.json", required=True),
    ManagedJsonFile("packages/maglev-cli/package.json", required=True),
]

DERIVED_JSON_TARGETS: List[ManagedJsonFile] = [
    ManagedJsonFile("packages/maglev-cli/dist/manifest.json", required=False),
    ManagedJsonFile(".maglev_build/manifest.json", required=False),
]

DERIVED_TEXT_TARGETS: List[ManagedTextFile] = [
    ManagedTextFile("packages/maglev-cli/dist/CHANGELOG.md", r"^# Maglev .+$"),
    ManagedTextFile("packages/maglev-cli/dist/CHANGELOG_DRAFT.md", r"^# Maglev .+ 变更草案 \(DRAFT\)$"),
    ManagedTextFile(".maglev_build/CHANGELOG.md", r"^# Maglev .+$"),
    ManagedTextFile(".maglev_build/CHANGELOG_DRAFT.md", r"^# Maglev .+ 变更草案 \(DRAFT\)$"),
]


def print_error(message: str) -> None:
    print(f"❌ {message}")


def print_success(message: str) -> None:
    print(f"✅ {message}")


def print_info(message: str) -> None:
    print(message)


def validate_version(version: str) -> None:
    if not VERSION_PATTERN.match(version):
        raise ValueError(f"非法版本号: {version}。当前仅支持 x.y.z 形式。")


def read_json_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json_file(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def read_version_from_json(spec: ManagedJsonFile) -> Optional[str]:
    if not os.path.exists(spec.path):
        if spec.required:
            raise FileNotFoundError(spec.path)
        return None

    data = read_json_file(spec.path)
    value = data.get(spec.field)
    if value is None:
        raise KeyError(f"{spec.path} 缺少字段 {spec.field}")
    return str(value)


def update_json_version(spec: ManagedJsonFile, version: str) -> bool:
    if not os.path.exists(spec.path):
        if spec.required:
            raise FileNotFoundError(spec.path)
        return False

    data = read_json_file(spec.path)
    data[spec.field] = version
    write_json_file(spec.path, data)
    return True


def update_text_title(spec: ManagedTextFile, version: str) -> bool:
    if not os.path.exists(spec.path):
        if spec.required:
            raise FileNotFoundError(spec.path)
        return False

    with open(spec.path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines:
        raise ValueError(f"{spec.path} 是空文件，无法更新版本标题。")

    first_line = lines[0].rstrip("\n")
    if not re.match(spec.pattern, first_line):
        raise ValueError(f"{spec.path} 的首行不符合预期格式: {first_line}")

    if "CHANGELOG_DRAFT" in spec.path:
        lines[0] = f"# Maglev {version} 变更草案 (DRAFT)\n"
    else:
        lines[0] = f"# Maglev {version}\n"

    with open(spec.path, "w", encoding="utf-8") as file:
        file.writelines(lines)
    return True


def read_version_from_text(spec: ManagedTextFile) -> Optional[str]:
    if not os.path.exists(spec.path):
        if spec.required:
            raise FileNotFoundError(spec.path)
        return None

    with open(spec.path, "r", encoding="utf-8") as file:
        first_line = file.readline().rstrip("\n")

    if not first_line:
        raise ValueError(f"{spec.path} 是空文件，无法读取版本标题。")

    if not re.match(spec.pattern, first_line):
        raise ValueError(f"{spec.path} 的首行不符合预期格式: {first_line}")

    match = re.search(r"(\d+\.\d+\.\d+)", first_line)
    if not match:
        raise ValueError(f"{spec.path} 未能解析出版本号: {first_line}")
    return match.group(1)


def collect_versions() -> List[tuple]:
    rows = []
    for spec in CANONICAL_SOURCES + DERIVED_JSON_TARGETS:
        try:
            version = read_version_from_json(spec)
        except Exception as error:
            version = f"<error: {error}>"
        rows.append((spec.path, version))
    for spec in DERIVED_TEXT_TARGETS:
        try:
            version = read_version_from_text(spec)
        except Exception as error:
            version = f"<error: {error}>"
        rows.append((spec.path, version))
    return rows


def cmd_show(_: argparse.Namespace) -> int:
    rows = collect_versions()
    for path, version in rows:
        print_info(f"{path}: {version}")
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    rows = collect_versions()
    versions = [version for _, version in rows if version and not str(version).startswith("<error:")]
    unique_versions = sorted(set(versions))

    for path, version in rows:
        print_info(f"{path}: {version}")

    if not unique_versions:
        print_error("未能读取任何版本源。")
        return 1

    if len(unique_versions) > 1:
        print_error(f"版本不一致: {', '.join(unique_versions)}")
        return 1

    print_success(f"版本一致: {unique_versions[0]}")
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    version = args.version
    validate_version(version)

    updated_paths = []
    for spec in CANONICAL_SOURCES + DERIVED_JSON_TARGETS:
        changed = update_json_version(spec, version)
        if changed:
            updated_paths.append(spec.path)

    for spec in DERIVED_TEXT_TARGETS:
        changed = update_text_title(spec, version)
        if changed:
            updated_paths.append(spec.path)

    print_success(f"已同步版本到 {version}")
    for path in updated_paths:
        print_info(f"- {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maglev 统一版本管理工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show_parser = subparsers.add_parser("show", help="展示当前版本状态")
    show_parser.set_defaults(func=cmd_show)

    check_parser = subparsers.add_parser("check", help="校验版本是否一致")
    check_parser.set_defaults(func=cmd_check)

    set_parser = subparsers.add_parser("set", help="同步所有受管版本文件到目标版本")
    set_parser.add_argument("version", help="目标版本号，例如 0.1.4")
    set_parser.set_defaults(func=cmd_set)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as error:
        print_error(str(error))
        return 1


if __name__ == "__main__":
    sys.exit(main())
