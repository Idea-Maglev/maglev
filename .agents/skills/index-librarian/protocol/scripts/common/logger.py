"""
JSON logging framework for index protocol scripts.

Design authority: spec 04 §7
Execution authority: THIS FILE.

Logs are stored in .index-logs/{command}/ as JSON files.
Each execution produces one log file. Auto-cleanup keeps max 50 files per directory.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

DEFAULT_LOG_ROOT = ".index-logs"
MAX_FILES_PER_DIR = 50


def _find_repo_root() -> Path:
    """Walk up from cwd to find .git directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def _get_log_dir(command: str, log_root: Optional[str] = None) -> Path:
    """Get or create the log directory for a command."""
    if log_root:
        root = Path(log_root)
    else:
        root = _find_repo_root() / DEFAULT_LOG_ROOT

    log_dir = root / command
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def _cleanup_old_logs(log_dir: Path) -> None:
    """Keep only the most recent MAX_FILES_PER_DIR log files."""
    files = sorted(log_dir.glob("*.json"), key=lambda f: f.stat().st_mtime)
    excess = len(files) - MAX_FILES_PER_DIR
    if excess > 0:
        for f in files[:excess]:
            f.unlink()


class IndexLogger:
    """Structured logger for index protocol commands.

    Usage:
        logger = IndexLogger("verify", args=["--module", "meetings"])
        logger.add_execution("meetings/INDEX.md", {"L01": "pass", "L02": "fail"})
        logger.finalize(exit_code=1, summary={"passed": 10, "failed": 2})
    """

    def __init__(
        self,
        command: str,
        args: list[str] | None = None,
        protocol_version: str = "1.0",
        script_version: str = "0.1.0",
        log_root: Optional[str] = None,
    ):
        self.command = command
        self.start_time = time.time()
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.log_dir = _get_log_dir(command, log_root)

        self.data: dict[str, Any] = {
            "meta": {
                "command": command,
                "args": args or [],
                "timestamp": self.timestamp,
                "duration_ms": 0,
                "exit_code": 0,
                "protocol_version": protocol_version,
                "script_version": script_version,
            },
            "input": {},
            "execution": [],
            "summary": {},
        }

    def set_input(self, **kwargs) -> None:
        """Set input metadata."""
        self.data["input"].update(kwargs)

    def add_execution(self, node: str, checks: dict) -> None:
        """Add execution details for a single node."""
        self.data["execution"].append({"node": node, "checks": checks})

    def add_entry(self, key: str, value: Any) -> None:
        """Add arbitrary data to the log."""
        self.data[key] = value

    def finalize(self, exit_code: int, summary: Optional[dict] = None) -> str:
        """Finalize and write the log file.

        Args:
            exit_code: Script exit code.
            summary: Summary statistics dict.

        Returns:
            Path to the written log file.
        """
        duration_ms = int((time.time() - self.start_time) * 1000)
        self.data["meta"]["duration_ms"] = duration_ms
        self.data["meta"]["exit_code"] = exit_code

        if summary:
            self.data["summary"] = summary

        # Clean old logs
        _cleanup_old_logs(self.log_dir)

        # Write log file
        filename = self.timestamp.replace(":", "") + ".json"
        log_path = self.log_dir / filename
        log_path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return str(log_path)
