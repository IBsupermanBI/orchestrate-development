import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('behavior_runner', ROOT / 'tests/behavior/run.py')
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class HarnessTests(unittest.TestCase):
    def test_observer_detects_write_delete_and_create(self):
        (ROOT / '.scratch').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch') as temp:
            root = Path(temp)
            (root / 'edit').write_text('before')
            (root / 'delete').write_text('before')
            before = RUNNER.tree(root)
            (root / 'edit').write_text('after')
            (root / 'delete').unlink()
            (root / 'create').write_text('after')
            self.assertEqual(RUNNER.observed_changes(before, RUNNER.tree(root)), ['create', 'delete', 'edit'])

    def test_execution_failure_is_not_behavior_failure(self):
        (ROOT / '.scratch').mkdir(exist_ok=True)
        with tempfile.TemporaryFile(mode='w+', dir=ROOT / '.scratch') as output:
            self.assertEqual(RUNNER.run_process([sys.executable, '-c', 'raise SystemExit(7)'], '', output, output, 10), 'EXECUTION_ERROR')
            self.assertEqual(RUNNER.run_process([sys.executable, '-c', 'print("observed")'], '', output, output, 10), 'OBSERVED')

    def test_timeout_is_not_an_assertion_failure(self):
        (ROOT / '.scratch').mkdir(exist_ok=True)
        with tempfile.TemporaryFile(mode='w+', dir=ROOT / '.scratch') as output:
            self.assertEqual(RUNNER.run_process([sys.executable, '-c', 'import time; time.sleep(20)'], '', output, output, 0.2), 'TIMEOUT')
