#!/usr/bin/env python3
"""Safely install V4 and archive known V3 assets after an explicit opt-in."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil

PACKAGE = Path(__file__).resolve().parents[1]
V3_PROFILES = (
    "terra-high-orchestrator.toml", "astra-low-worker.toml", "luna-xhigh-worker.toml",
    "terra-high-gate.toml", "v3-sol-medium-reviewer.toml", "v3-luna-xhigh-validator.toml",
)


def load_installer():
    spec = importlib.util.spec_from_file_location("v4_installer", PACKAGE / "install.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def legacy_paths(target: Path, user: bool) -> list[Path]:
    skill_root = target / ("skills" if user else ".agents/skills")
    paths = [skill_root / "orchestrate-development-v3"]
    agent_root = target / ("agents" if user else ".codex/agents")
    paths.extend(agent_root / name for name in V3_PROFILES)
    return [path for path in paths if path.exists()]


def legacy_backup_dirs(target: Path, user: bool) -> list[Path]:
    agent_root = target / ("agents" if user else ".codex/agents")
    backup_root = agent_root / ".backups"
    if not backup_root.is_dir():
        return []
    candidates = []
    for directory in backup_root.iterdir():
        if not directory.is_dir():
            continue
        files = [path for path in directory.rglob("*") if path.is_file()]
        if files and all(path.name in V3_PROFILES for path in files):
            candidates.append(directory)
    return candidates


def upgrade(target: Path, *, user: bool = False, apply: bool = False, force: bool = False) -> dict:
    target = target.resolve()
    installer = load_installer()
    result = installer.install(PACKAGE, target, user=user, apply=apply, force=force)
    legacy = legacy_paths(target, user)
    backup_dirs = legacy_backup_dirs(target, user)
    base = target / ("skills" if user else ".agents/skills")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    archive = base / "archive-orchestrate-development-v3-pending-removal" / stamp
    planned = [{"source": str(path), "destination": str(archive / path.name), "action": "archive"} for path in legacy]
    planned.extend({"source": str(path), "destination": str(archive / "legacy-agent-backups" / path.name), "action": "archive"} for path in backup_dirs)
    if apply:
        for path in legacy:
            destination = archive / path.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(destination))
        for path in backup_dirs:
            destination = archive / "legacy-agent-backups" / path.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(destination))
    result["retired_v3"] = planned
    result["archive_root"] = str(archive) if legacy or backup_dirs else None
    result["migration"] = "applied" if apply else "dry-run"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path)
    scope.add_argument("--user", action="store_true")
    parser.add_argument("--home", type=Path, help="Codex home override; only with --user")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.home and not args.user:
        parser.error("--home requires --user")
    target = args.project if not args.user else args.home or Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    try:
        print(json.dumps(upgrade(target, user=args.user, apply=args.apply, force=args.force), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
