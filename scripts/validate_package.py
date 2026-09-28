#!/usr/bin/env python3
"""Validate V5 package structure, routes, topology and retired route absence."""
from __future__ import annotations

import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "v5-sol-medium-orchestrator": ("gpt-6-sol", "medium", False),
    "v5-sol-medium-worker": ("gpt-6-sol", "medium", False),
    "v5-astra-low-worker": ("gpt-6-astra", "low", False),
    "v5-luna-medium-scout": ("gpt-6-luna", "medium", True),
    "v5-luna-xhigh-repair": ("gpt-6-luna", "xhigh", False),
    "v5-sol-medium-reviewer": ("gpt-6-sol", "medium", True),
    "v5-luna-xhigh-validator": ("gpt-6-luna", "xhigh", False),
    "v5-sol-high-gate": ("gpt-6-sol", "high", True),
}


def source_files() -> list[Path]:
    ignored = {".git", ".scratch", "__pycache__", ".backups"}
    return [path for path in ROOT.rglob("*") if path.is_file() and not ignored.intersection(path.relative_to(ROOT).parts)]


def main() -> int:
    failures: list[str] = []
    manifest = json.loads((ROOT / "install-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("skill_name") != "orchestrate-development-v5":
        failures.append("wrong skill name")
    for name in manifest.get("skill_files", []):
        if not (ROOT / name).is_file():
            failures.append("manifest missing file: " + name)
    profiles = {}
    for asset in manifest.get("project_assets", []):
        path = ROOT / asset["source"]
        if not path.is_file():
            failures.append("missing profile: " + asset["source"])
            continue
        value = tomllib.loads(path.read_text(encoding="utf-8"))
        if value.get("name") in profiles:
            failures.append("duplicate profile: " + str(value.get("name")))
        if path.stem != value.get("name") or asset["destination"] != ".codex/agents/" + path.name:
            failures.append("profile identity/path mismatch: " + asset["source"])
        profiles[value.get("name")] = (value.get("model"), value.get("model_reasoning_effort"), value.get("default_permissions") == ":read-only")
    if profiles != EXPECTED:
        failures.append("profile routes do not match the V5 contract")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    table_routes = {}
    for line in skill.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5:
            continue
        profile = cells[1].split("`")[1]
        table_routes[profile] = (cells[2].strip("`"), cells[3].split("`")[1], "read-only" in cells[3])
    if table_routes != EXPECTED:
        failures.append("SKILL route table differs from executable profiles")
    packaged_profiles = {name for name in manifest.get("skill_files", []) if name.endswith(".toml")}
    asset_profiles = {asset["source"] for asset in manifest.get("project_assets", [])}
    if packaged_profiles != asset_profiles:
        failures.append("skill payload and project profile assets differ")
    content = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in source_files())
    if ("sp" + "ark") in content.lower():
        failures.append("retired route reference found")
    required = ("LUNA_SCOUT", "RESEARCH_CAPSULE", "sufficiently narrow", "Only `ROOT_ORCHESTRATOR`, `SOL_WORKER`, `ASTRA_WORKER`, and `SOL_GATE`", "shallow, not flat", "Goal-level acceptance", "final stage/capability acceptance", "Root owns every top-level orchestration dispatch")
    for token in required:
        if token not in content:
            failures.append("missing contract token: " + token)
    for stale in ("Root owns the final" + " gate", "never accepts" + " for Root"):
        if stale in content:
            failures.append("stale final-acceptance ownership: " + stale)
    scout = (ROOT / "assets/project/.codex/agents/v5-luna-medium-scout.toml").read_text(encoding="utf-8")
    for token in ("Do not edit files", "create subagents", "RESEARCH_CAPSULE"):
        if token not in scout:
            failures.append("Scout restriction missing: " + token)
    gate = (ROOT / "assets/project/.codex/agents/v5-sol-high-gate.toml").read_text(encoding="utf-8")
    for token in ("final stage/capability acceptance", "Do not implement or repair", "read-only V5 Luna Medium Scout"):
        if token not in gate:
            failures.append("Gate ownership restriction missing: " + token)
    print(json.dumps({"valid": not failures, "failures": failures, "profiles": sorted(profiles)}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
