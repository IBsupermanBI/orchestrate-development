#!/usr/bin/env python3
"""Opt-in real Codex CLI smoke scenarios. Never part of unittest discovery."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('installer', ROOT / 'install.py')
INSTALL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALL)

SCENARIOS = {
    'plan': ('plan: Plan adding a greeting(name) function to app.py. Explain the proposed behavior and validation. Do not implement.', False),
    'direct': ('run: In message.txt replace Helo with Hello. This is the entire task.', True),
    'diagnose': ('diagnose: Inspect this project installation and explain concrete findings. Do not repair it.', False),
}


def observed_changes(before, after):
    return sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))


def tree(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}


def run_process(command, prompt, stdout, stderr, timeout):
    options = {'start_new_session': True} if os.name != 'nt' else {}
    with subprocess.Popen(command, stdin=subprocess.PIPE, text=True, encoding='utf-8',
                          stdout=stdout, stderr=stderr, **options) as process:
        try:
            process.communicate(prompt, timeout=timeout)
            return 'OBSERVED' if process.returncode == 0 else 'EXECUTION_ERROR'
        except subprocess.TimeoutExpired:
            if os.name == 'nt':
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            else:
                os.killpg(process.pid, signal.SIGKILL)
            process.kill()
            process.communicate()
            return 'TIMEOUT'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', choices=SCENARIOS, required=True)
    parser.add_argument('--execute', action='store_true', help='Actually consume model usage')
    parser.add_argument('--timeout', type=int, default=600)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    if not args.execute:
        print(json.dumps({'status': 'NOT_RUN', 'scenario': args.scenario, 'prompt': SCENARIOS[args.scenario][0]}))
        return 0
    executable = shutil.which('codex')
    if not executable:
        parser.error('Codex CLI is unavailable')
    run = ROOT / '.scratch/behavior' / (args.scenario + '-' + str(time.time_ns()))
    project = run / 'project'
    INSTALL.install(ROOT, project, apply=True)
    (project / 'app.py').write_text('VERSION = 1\n', encoding='utf-8')
    (project / 'message.txt').write_text('Helo\n', encoding='utf-8')
    (project / 'AGENTS.md').write_text(
        'Work only in this disposable project. Do not install, publish, commit, or modify external files. '
        'Keep unrelated files unchanged.\nPython interpreter for this fixture: ' + sys.executable +
        '\nUse this interpreter for Python commands when python is absent from PATH.\n', encoding='utf-8')
    if args.scenario == 'diagnose':
        path = project / '.codex/agents/astra-low-worker.toml'
        path.write_text(path.read_text().replace('gpt-6-astra', 'unexpected-model'), encoding='utf-8')
    before = tree(project)
    command = [executable, 'exec', '--ephemeral', '--json', '--skip-git-repo-check',
               '--model', 'gpt-5.6-terra', '-c', 'model_reasoning_effort="high"',
               '-c', 'default_permissions="' + (':workspace' if SCENARIOS[args.scenario][1] else ':read-only') + '"',
               '--cd', str(project), '--output-last-message', str(run / 'final.txt'), '-']
    prompt = ('Use $orchestrate-development-v3 from .agents/skills/orchestrate-development-v3/SKILL.md.\n'
              + SCENARIOS[args.scenario][0])
    started = time.monotonic()
    status = 'UNMEASURED'
    with (run / 'trace.jsonl').open('w', encoding='utf-8') as stdout, (run / 'stderr.txt').open('w', encoding='utf-8') as stderr:
        try:
            status = run_process(command, prompt, stdout, stderr, args.timeout)
        except OSError as exc:
            stderr.write(str(exc))
            status = 'EXECUTION_ERROR'
    changed = observed_changes(before, tree(project))
    final = (run / 'final.txt').read_text(encoding='utf-8') if (run / 'final.txt').exists() else ''
    assertions = {'delivered_response': bool(final.strip()),
                  'scope_preserved': changed == (['message.txt'] if args.scenario == 'direct' else [])}
    if args.scenario == 'direct':
        assertions['requested_edit'] = (project / 'message.txt').read_text() == 'Hello\n'
    # These observable smoke properties are not a semantic grading of the plan/diagnosis or delegation.
    if status == 'OBSERVED' and not all(assertions.values()):
        status = 'ASSERTION_FAILED'
    report = {'scenario': args.scenario, 'status': status, 'assertions': assertions,
              'changed_files': changed, 'elapsed_seconds': time.monotonic() - started,
              'model': 'gpt-5.6-terra', 'effort': 'high',
              'skill_sha256': hashlib.sha256((ROOT / 'SKILL.md').read_bytes()).hexdigest(),
              'package_files': {p: digest for p, digest in before.items() if p.startswith(('.agents/', '.codex/'))},
              'semantic_review': 'REQUIRED', 'artifacts': str(run)}
    (run / 'result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if status == 'OBSERVED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
