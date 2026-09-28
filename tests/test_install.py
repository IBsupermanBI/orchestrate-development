import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


INSTALL = load("v5_install", ROOT / "install.py")
UPGRADE = load("v5_upgrade", ROOT / "scripts" / "upgrade_from_v3.py")


class InstallTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".scratch").mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / ".scratch")
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name) / "project"

    def test_dry_run_roundtrip_and_idempotence(self):
        INSTALL.install(ROOT, self.target)
        self.assertFalse(self.target.exists())
        INSTALL.install(ROOT, self.target, apply=True)
        manifest = json.loads((ROOT / "install-manifest.json").read_text())
        for asset in manifest["project_assets"]:
            installed = self.target / asset["destination"]
            self.assertEqual((ROOT / asset["source"]).read_bytes(), installed.read_bytes())
            tomllib.loads(installed.read_text())
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertTrue(all(item["action"] == "unchanged" for item in INSTALL.install(ROOT, self.target, apply=True)["operations"]))

    def test_conflict_is_backed_up_only_when_forced(self):
        INSTALL.install(ROOT, self.target, apply=True)
        destination = self.target / ".agents/skills/orchestrate-development-v5/SKILL.md"
        destination.write_text("local edit")
        with self.assertRaises(ValueError):
            INSTALL.install(ROOT, self.target, apply=True)
        INSTALL.install(ROOT, self.target, apply=True, force=True)
        self.assertEqual(destination.read_bytes(), (ROOT / "SKILL.md").read_bytes())
        self.assertEqual(next(destination.parent.glob(".backups/*/SKILL.md")).read_text(), "local edit")

    def test_upgrade_archives_only_known_v3_assets(self):
        legacy_skill = self.target / ".agents/skills/orchestrate-development-v3"
        legacy_skill.mkdir(parents=True)
        (legacy_skill / "SKILL.md").write_text("legacy local edit")
        old_profile = self.target / ".codex/agents/astra-low-worker.toml"
        old_profile.parent.mkdir(parents=True)
        old_profile.write_text("legacy profile")
        v3_backup = self.target / ".codex/agents/.backups/20260101T000000000000Z"
        v3_backup.mkdir(parents=True)
        (v3_backup / "astra-low-worker.toml").write_text("old backup")
        unrelated = self.target / ".codex/agents/unrelated.toml"
        unrelated.write_text("keep")
        dry = UPGRADE.upgrade(self.target, apply=False)
        self.assertEqual(dry["migration"], "dry-run")
        self.assertTrue(legacy_skill.exists())
        applied = UPGRADE.upgrade(self.target, apply=True)
        self.assertEqual(applied["migration"], "applied")
        self.assertTrue((self.target / ".agents/skills/orchestrate-development-v5/SKILL.md").exists())
        self.assertFalse(legacy_skill.exists())
        self.assertFalse(old_profile.exists())
        archive = Path(applied["archive_root"])
        self.assertEqual((archive / "orchestrate-development-v3/SKILL.md").read_text(), "legacy local edit")
        self.assertEqual((archive / "astra-low-worker.toml").read_text(), "legacy profile")
        self.assertEqual((archive / "legacy-agent-backups/20260101T000000000000Z/astra-low-worker.toml").read_text(), "old backup")
        self.assertEqual(unrelated.read_text(), "keep")

    def test_user_scope_upgrade_uses_user_paths(self):
        legacy = self.target / "skills/orchestrate-development-v3"
        legacy.mkdir(parents=True)
        (legacy / "SKILL.md").write_text("legacy")
        result = UPGRADE.upgrade(self.target, user=True, apply=True)
        self.assertTrue((self.target / "skills/orchestrate-development-v5/SKILL.md").is_file())
        self.assertTrue((self.target / "agents/v5-luna-medium-scout.toml").is_file())
        self.assertFalse(legacy.exists())
        self.assertTrue((Path(result["archive_root"]) / "orchestrate-development-v3/SKILL.md").is_file())

    def test_backup_only_migration_reports_archive(self):
        backup = self.target / ".codex/agents/.backups/20260101T000000000000Z"
        backup.mkdir(parents=True)
        (backup / "terra-high-gate.toml").write_text("legacy backup")
        result = UPGRADE.upgrade(self.target, apply=True)
        self.assertIsNotNone(result["archive_root"])
        self.assertTrue((Path(result["archive_root"]) / "legacy-agent-backups/20260101T000000000000Z/terra-high-gate.toml").is_file())

    def test_required_profiles_match_contract(self):
        expected = {
            "v5-sol-medium-orchestrator": ("gpt-6-sol", "medium", False),
            "v5-sol-medium-worker": ("gpt-6-sol", "medium", False),
            "v5-astra-low-worker": ("gpt-6-astra", "low", False),
            "v5-luna-medium-scout": ("gpt-6-luna", "medium", True),
            "v5-luna-xhigh-repair": ("gpt-6-luna", "xhigh", False),
            "v5-sol-medium-reviewer": ("gpt-6-sol", "medium", True),
            "v5-luna-xhigh-validator": ("gpt-6-luna", "xhigh", False),
            "v5-sol-high-gate": ("gpt-6-sol", "high", True),
        }
        actual = {}
        manifest = json.loads((ROOT / "install-manifest.json").read_text())
        for asset in manifest["project_assets"]:
            profile = tomllib.loads((ROOT / asset["source"]).read_text())
            actual[profile["name"]] = (profile["model"], profile["model_reasoning_effort"], profile.get("default_permissions") == ":read-only")
        self.assertEqual(actual, expected)

    def test_v5_preserves_existing_versions_in_both_scopes(self):
        for user in (False, True):
            target = self.target / str(user)
            skills = target / ("skills" if user else ".agents/skills")
            agents = target / ("agents" if user else ".codex/agents")
            preserved = []
            for version in (2, 4):
                path = skills / f"orchestrate-development-v{version}/SKILL.md"
                path.parent.mkdir(parents=True)
                path.write_text(f"local v{version}")
                preserved.append(path)
            agents.mkdir(parents=True)
            profile = agents / "v4-terra-high-orchestrator.toml"
            profile.write_text("local profile")
            preserved.append(profile)
            before = {path: path.read_bytes() for path in preserved}
            INSTALL.install(ROOT, target, user=user, apply=True)
            self.assertEqual(before, {path: path.read_bytes() for path in preserved})
            self.assertTrue((skills / "orchestrate-development-v5/SKILL.md").is_file())

    def test_manifest_escape_rejected_before_any_write(self):
        package = Path(self.tmp.name) / "unsafe-package"
        package.mkdir()
        manifest = json.loads((ROOT / "install-manifest.json").read_text())
        manifest["skill_files"] = ["../outside.md"]
        (package / "install-manifest.json").write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            INSTALL.install(package, self.target, apply=True)
        self.assertFalse(self.target.exists())
        with self.assertRaises(ValueError):
            INSTALL.inside(self.target, str(Path(self.tmp.name).resolve() / "outside.md"))

    def test_public_package_runs_without_sibling_dependencies(self):
        package = Path(self.tmp.name) / "standalone"
        manifest = json.loads((ROOT / "install-manifest.json").read_text())
        for name in set(manifest["skill_files"] + ["install.py"]):
            destination = package / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)
        for arguments in (
            ["scripts/validate_package.py"],
            ["install.py", "--project", str(self.target)],
            ["install.py", "--project", str(self.target), "--apply"],
            ["scripts/orchestration_doctor.py", "diagnose", "--project", str(self.target)],
        ):
            result = subprocess.run([sys.executable, *arguments], cwd=package, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["findings"], [])


if __name__ == "__main__":
    unittest.main()
