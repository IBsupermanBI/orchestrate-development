import importlib.util
from pathlib import Path
import tempfile
import unittest

from test_install import INSTALL, ROOT

spec = importlib.util.spec_from_file_location("doctor", ROOT / "scripts" / "orchestration_doctor.py")
DOCTOR = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(DOCTOR)


class DoctorTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".scratch").mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / ".scratch")
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)

    def test_diagnose_is_readonly_and_detects_profile_drift(self):
        INSTALL.install(ROOT, self.project, apply=True)
        before = {str(path): path.read_bytes() for path in self.project.rglob("*") if path.is_file()}
        self.assertEqual(DOCTOR.diagnose(ROOT, self.project)["findings"], [])
        self.assertEqual(before, {str(path): path.read_bytes() for path in self.project.rglob("*") if path.is_file()})
        profile = self.project / ".codex/agents/v4-luna-medium-scout.toml"
        profile.write_text(profile.read_text().replace('model_reasoning_effort = "medium"', 'model_reasoning_effort = "high"'))
        self.assertIn("profile-drift", [item["id"] for item in DOCTOR.diagnose(ROOT, self.project)["findings"]])

    def test_snapshot_detects_changed_and_missing_inputs(self):
        file = self.project / "source.py"
        file.write_text("first")
        snapshot = DOCTOR.fingerprint(self.project, ["source.py", "new.py"])
        self.assertEqual(DOCTOR.verify(self.project, snapshot)["status"], "MATCH")
        file.write_text("changed")
        (self.project / "new.py").write_text("created")
        self.assertEqual(set(DOCTOR.verify(self.project, snapshot)["changed"]), {"source.py", "new.py"})


if __name__ == "__main__":
    unittest.main()
