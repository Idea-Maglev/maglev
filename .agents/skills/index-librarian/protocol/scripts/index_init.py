#!/usr/bin/env python3
"""
index_init.py — Index protocol initialization.

5-step flow:
  1. Environment check (Python, pyyaml, registry)
  2. Log directory creation + .gitignore update
  3. Registry health check (calls scan logic)
  4. Baseline verify (calls verify logic for managed modules)
  5. Output initialization summary

Exit codes:
  0 — initialization complete, all ready
  1 — some modules incomplete
  2 — environment error
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common.logger import IndexLogger

try:
    import yaml
    PYYAML_VERSION = yaml.__version__
except ImportError:
    PYYAML_VERSION = None

SCRIPT_DIR = Path(__file__).parent
PROTOCOL_DIR = SCRIPT_DIR.parent
REGISTRY_PATH = PROTOCOL_DIR / "registry.yaml"
LOG_DIRS = ["verify", "update", "scan", "init"]


def find_repo_root() -> Path:
    current = PROTOCOL_DIR
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def check_environment(repo_root: Path) -> list[dict]:
    """Step 1: Environment checks."""
    results = []

    # Python version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 8):
        results.append({"check": "Python version", "status": "pass", "detail": py_ver})
    else:
        results.append({"check": "Python version", "status": "fail", "detail": f"{py_ver} (need >= 3.8)"})

    # pyyaml
    if PYYAML_VERSION:
        results.append({"check": "pyyaml", "status": "pass", "detail": PYYAML_VERSION})
    else:
        results.append({"check": "pyyaml", "status": "fail", "detail": "not installed (pip install pyyaml)"})

    # registry.yaml
    if REGISTRY_PATH.exists():
        reg = yaml.safe_load(REGISTRY_PATH.read_text()) or {}
        mod_count = len(reg.get("modules", []))
        results.append({"check": "registry.yaml", "status": "pass", "detail": f"{mod_count} modules"})
    else:
        results.append({"check": "registry.yaml", "status": "fail", "detail": "not found"})

    return results


def setup_log_dirs(repo_root: Path) -> list[dict]:
    """Step 2: Create log directories and update .gitignore."""
    results = []
    log_root = repo_root / ".index-logs"

    for subdir in LOG_DIRS:
        dir_path = log_root / subdir
        dir_path.mkdir(parents=True, exist_ok=True)

    results.append({"check": "Log directories", "status": "pass", "detail": f"created {len(LOG_DIRS)} dirs"})

    # Check .gitignore
    gitignore = repo_root / ".gitignore"
    gitignore_entry = ".index-logs/"

    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")
        if gitignore_entry not in content:
            with open(gitignore, "a", encoding="utf-8") as f:
                f.write(f"\n# Index protocol local logs (debug only, never commit)\n{gitignore_entry}\n")
            results.append({"check": ".gitignore", "status": "pass", "detail": "appended .index-logs/"})
        else:
            results.append({"check": ".gitignore", "status": "pass", "detail": "already includes .index-logs/"})
    else:
        gitignore.write_text(
            f"# Index protocol local logs (debug only, never commit)\n{gitignore_entry}\n",
            encoding="utf-8",
        )
        results.append({"check": ".gitignore", "status": "pass", "detail": "created with .index-logs/"})

    return results


def run_scan(repo_root: Path) -> dict:
    """Step 3: Run scan and return results."""
    scan_script = SCRIPT_DIR / "index_scan.py"
    try:
        result = subprocess.run(
            [sys.executable, str(scan_script), "--format", "json"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=30,
        )
        if result.stdout.strip():
            return json.loads(result.stdout)
        return {"error": result.stderr.strip() or "no output"}
    except Exception as e:
        return {"error": str(e)}


def run_verify(repo_root: Path, modules: list[str]) -> dict:
    """Step 4: Run verify on managed modules."""
    verify_script = SCRIPT_DIR / "index_verify.py"
    for module_name in modules:
        try:
            result = subprocess.run(
                [sys.executable, str(verify_script), "--module", module_name, "--level", "local", "--format", "json"],
                capture_output=True,
                text=True,
                cwd=str(repo_root),
                timeout=60,
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
        except Exception:
            pass
    return {"nodes_checked": 0, "results": {"health_pct": 0}}


def main():
    parser = argparse.ArgumentParser(description="Index Protocol — Initializer")
    parser.add_argument("--module", type=str, help="Init specific module only")
    parser.add_argument("--force", action="store_true", help="Rebuild log dirs")
    parser.add_argument("--status", action="store_true", help="Check status only, no action")
    parser.add_argument("--migrate", action="store_true", help="Run README→INDEX migration")
    parser.add_argument("--registry", type=str, default=None)
    args = parser.parse_args()

    logger = IndexLogger("init", args=sys.argv[1:])
    repo_root = find_repo_root()

    # Step 1: Environment check
    env_results = check_environment(repo_root)
    env_ok = all(r["status"] == "pass" for r in env_results)

    if not env_ok and not args.status:
        print("\n═══════════════════════════════════════")
        print("  Index Protocol — 环境检查失败")
        print("═══════════════════════════════════════\n")
        for r in env_results:
            icon = "✅" if r["status"] == "pass" else "❌"
            print(f"  {icon} {r['check']}: {r['detail']}")
        logger.finalize(exit_code=2, summary={"error": "environment_check_failed"})
        sys.exit(2)

    # Step 2: Log directory setup
    if not args.status:
        log_results = setup_log_dirs(repo_root)
    else:
        log_results = [{"check": "Log directories", "status": "skip", "detail": "status-only mode"}]

    # Step 3: Registry health check (scan)
    scan_results = run_scan(repo_root)
    modules_info = scan_results.get("modules", [])

    # Step 4: Baseline verify (only for ready modules)
    ready_modules = [m["name"] for m in modules_info if m.get("status") == "ready"]
    verify_results = {}
    if ready_modules and not args.status:
        verify_results = run_verify(repo_root, ready_modules)

    # Step 5: Output summary
    print("\n═══════════════════════════════════════════════════")
    print("  Index Protocol — 初始化" + (" (status-only)" if args.status else " 完成"))
    print("═══════════════════════════════════════════════════\n")

    print("  环境:")
    for r in env_results:
        icon = "✅" if r["status"] == "pass" else "❌"
        print(f"    {icon} {r['check']}: {r['detail']}")
    for r in log_results:
        icon = "✅" if r["status"] == "pass" else "⏭️"
        print(f"    {icon} {r['check']}: {r['detail']}")

    print("\n  模块状态:")
    status_icons = {"ready": "🟢", "incomplete": "🔴", "missing": "⚫", "bootstrap": "🟡"}
    for m in modules_info:
        icon = status_icons.get(m["status"], "❓")
        issues_str = " — " + "; ".join(m.get("issues", [])) if m.get("issues") else ""
        print(f"    {m['name']}/    {icon} {m['status']}{issues_str}")

    if ready_modules and verify_results:
        health = verify_results.get("results", {}).get("health_pct", 0)
        nodes = verify_results.get("nodes_checked", 0)
        print(f"\n  基线巡检:")
        print(f"    → 模块: {', '.join(ready_modules)}")
        print(f"    → 健康度: {health}% ({nodes} 节点已检查)")
    elif not ready_modules:
        print(f"\n  基线巡检:")
        print(f"    → 无模块处于 ready 状态，跳过巡检")

    print(f"\n  下一步:")
    incomplete = [m["name"] for m in modules_info if m.get("status") == "incomplete"]
    if incomplete:
        print(f"    1. 为 {incomplete[0]}/ 补充 index_protocol_version + stats_schema")
        print(f"    2. 重新执行: python3 {SCRIPT_DIR / 'index_init.py'} --module {incomplete[0]}")
    elif ready_modules:
        print(f"    1. 执行全量验证: python3 {SCRIPT_DIR / 'index_verify.py'} --level global")
    else:
        print(f"    1. 为第一个模块创建 INDEX.md 并声明协议")

    summary = {
        "env_ok": env_ok,
        "modules_total": len(modules_info),
        "modules_ready": len(ready_modules),
        "modules_incomplete": len(incomplete),
    }

    exit_code = 0 if not incomplete else 1
    log_path = logger.finalize(exit_code=exit_code, summary=summary)
    print(f"\n  日志: {log_path}\n")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
