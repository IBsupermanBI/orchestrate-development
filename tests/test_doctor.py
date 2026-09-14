import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_install import INSTALL, ROOT

SPEC = importlib.util.spec_from_file_location('doctor', ROOT / 'scripts/orchestration_doctor.py')
DOCTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOCTOR)


class DoctorTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.scratch').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / '.scratch')
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name).resolve()

    def test_installed_roundtrip_readonly_and_profile_drift(self):
        INSTALL.install(ROOT, self.project, apply=True)
        before = {str(p): p.read_bytes() for p in self.project.rglob('*') if p.is_file()}
        self.assertEqual(DOCTOR.diagnose(ROOT, self.project)['findings'], [])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.project.rglob('*') if p.is_file()})
        profile = self.project / '.codex/agents/astra-low-worker.toml'
        profile.write_text(profile.read_text().replace('gpt-6-astra', 'other-model'))
        report = DOCTOR.diagnose(ROOT, self.project)
        self.assertIn('profile-drift', [f['id'] for f in report['findings']])
        profile.write_text('invalid = [')
        self.assertIn('profile-invalid', [f['id'] for f in DOCTOR.diagnose(ROOT, self.project)['findings']])

    def test_permission_drift_is_detected_without_repair(self):
        INSTALL.install(ROOT, self.project, apply=True)
        profile = self.project / '.codex/agents/terra-high-gate.toml'
        for replacement in ('default_permissions = ":workspace"', 'sandbox_mode = "read-only"'):
            original = (ROOT / 'assets/project/.codex/agents/terra-high-gate.toml').read_text()
            profile.write_text(original.replace('default_permissions = ":read-only"', replacement))
            before = profile.read_bytes()
            findings = DOCTOR.diagnose(ROOT, self.project)['findings']
            drift = [f for f in findings if f['id'] == 'profile-drift']
            self.assertEqual(len(drift), 1)
            self.assertIn('default_permissions', drift[0]['summary'])
            self.assertEqual(profile.read_bytes(), before)

    def test_missing_install_is_not_created(self):
        result = DOCTOR.diagnose(ROOT, self.project)
        self.assertIn('skill-not-installed', [f['id'] for f in result['findings']])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_dirty_deleted_and_new_inputs_invalidate_evidence(self):
        file = self.project / 'source.py'
        file.write_text('original')
        snapshot = DOCTOR.fingerprint(self.project, ['source.py', 'new.py'])
        self.assertEqual(DOCTOR.verify(self.project, snapshot)['status'], 'MATCH')
        file.write_text('dirty')
        self.assertEqual(DOCTOR.verify(self.project, snapshot)['changed'], ['source.py'])
        file.unlink()
        (self.project / 'new.py').write_text('added')
        self.assertEqual(set(DOCTOR.verify(self.project, snapshot)['changed']), {'source.py', 'new.py'})

    def test_foreign_empty_and_escaping_evidence_rejected(self):
        snapshot = DOCTOR.fingerprint(self.project, ['missing'])
        snapshot['project_root'] = str(self.project.parent)
        with self.assertRaises(ValueError):
            DOCTOR.verify(self.project, snapshot)
        for paths in ([], ['../outside'], [str(self.project / 'absolute')], ['.']):
            with self.assertRaises(ValueError):
                DOCTOR.fingerprint(self.project, paths)
        with self.assertRaises(ValueError):
            DOCTOR.verify(self.project, {'schema_version': 1, 'files': {}})

    def test_source_missing_reference_and_installed_drift(self):
        INSTALL.install(ROOT, self.project, apply=True)
        installed = self.project / '.agents/skills/orchestrate-development-v3'
        (installed / 'references/DIAGNOSE.md').unlink()
        self.assertIn('installed-file-drift', [f['id'] for f in DOCTOR.diagnose(ROOT, self.project)['findings']])
        self.assertIn('package-file-missing', [f['id'] for f in DOCTOR.diagnose(installed, self.project)['findings']])

    def test_cli_snapshot_verify_and_diagnose(self):
        INSTALL.install(ROOT, self.project, apply=True)
        command = [sys.executable, str(ROOT / 'scripts/orchestration_doctor.py')]
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        def run(*args):
            return subprocess.run(command + list(args), capture_output=True, text=True,
                                  encoding='utf-8', env=env, check=False)
        report = run('diagnose', '--project', str(self.project))
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertEqual(json.loads(report.stdout)['findings'], [])
        source = self.project / 'input.txt'
        source.write_text('first')
        snapshot = run('snapshot', '--project', str(self.project), '--files', 'input.txt')
        self.assertEqual(snapshot.returncode, 0, snapshot.stderr)
        saved = self.project / 'snapshot.json'
        saved.write_text(snapshot.stdout, encoding='utf-8')
        same = run('verify', '--project', str(self.project), '--snapshot', str(saved))
        self.assertEqual(same.returncode, 0, same.stderr)
        source.write_text('changed')
        stale = run('verify', '--project', str(self.project), '--snapshot', str(saved))
        self.assertEqual(stale.returncode, 1, stale.stderr)
        self.assertEqual(json.loads(stale.stdout)['status'], 'STALE')
