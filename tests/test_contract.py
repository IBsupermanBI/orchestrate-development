import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_package_validator_passes(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_package.py")], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])

    def test_scout_permissions_and_leaf_invariant_are_explicit(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Only `ROOT_ORCHESTRATOR`, `ASTRA_WORKER`, and `TERRA_GATE` may create `LUNA_SCOUT`", skill)
        scout = (ROOT / "assets/project/.codex/agents/v4-luna-medium-scout.toml").read_text(encoding="utf-8")
        self.assertIn('default_permissions = ":read-only"', scout)
        self.assertIn("Do not edit files", scout)
        for name in ("v4-luna-xhigh-repair.toml", "v4-sol-medium-reviewer.toml", "v4-luna-xhigh-validator.toml"):
            self.assertIn("Do not create Scout", (ROOT / "assets/project/.codex/agents" / name).read_text(encoding="utf-8"))

    def test_final_gate_ownership_is_distinct_from_goal_acceptance(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Goal-level acceptance", skill)
        self.assertIn("Gate owns the final stage/capability decision", skill)
        self.assertIn("Root owns every top-level orchestration dispatch", skill)
        self.assertNotIn("Root owns the final" + " gate", skill)
        self.assertNotIn("never accepts" + " for Root", skill)
        gate = (ROOT / "assets/project/.codex/agents/v4-terra-high-gate.toml").read_text(encoding="utf-8")
        self.assertIn('default_permissions = ":read-only"', gate)
        self.assertIn("Own the final stage/capability acceptance decision", gate)
        self.assertIn("Do not implement or repair", gate)


if __name__ == "__main__":
    unittest.main()
