#!/usr/bin/env python3
"""Read-only package diagnostics and explicit-scope evidence fingerprints (Python 3.11+)."""
import argparse
import hashlib
import json
from pathlib import Path
import tomllib


def inside(root, name):
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Expected a project-relative path: ' + name)
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Path escapes root: ' + name)
    return path


def fingerprint(root, paths):
    if not paths:
        raise ValueError('An explicit nonempty evidence scope is required')
    files = {}
    for name in sorted(set(paths)):
        path = inside(root, name)
        if path.is_dir():
            raise ValueError('List individual files, not directories: ' + name)
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    return {'schema_version': 1, 'project_root': str(root.resolve()), 'files': files}


def verify(root, snapshot):
    if snapshot.get('schema_version') != 1 or not isinstance(snapshot.get('files'), dict) or not snapshot['files']:
        raise ValueError('Unsupported or empty evidence snapshot')
    if snapshot.get('project_root') != str(root.resolve()):
        raise ValueError('Evidence belongs to another project root')
    current = fingerprint(root, list(snapshot['files']))
    changed = [p for p, digest in current['files'].items() if snapshot['files'][p] != digest]
    return {'status': 'STALE' if changed else 'MATCH', 'changed': changed,
            'scope': list(current['files']), 'semantic_validity': 'not-assessed'}


def diagnose(package, project):
    findings = []
    def add(code, path, summary):
        findings.append({'id': code, 'path': str(path), 'summary': summary})
    manifest = json.loads((package / 'install-manifest.json').read_text(encoding='utf-8'))
    for name in manifest['skill_files']:
        path = inside(package, name)
        if not path.is_file():
            add('package-file-missing', name, 'Restore this file from the matching package version')
    for asset in manifest['project_assets']:
        source = inside(package, asset['source'])
        target = inside(project, asset['destination'])
        if not source.is_file():
            continue
        try:
            expected = tomllib.loads(source.read_text(encoding='utf-8'))
            if not target.is_file():
                add('profile-missing', target, 'Required project profile is absent')
                continue
            actual = tomllib.loads(target.read_text(encoding='utf-8'))
            fields = ['name', 'model', 'model_reasoning_effort', 'developer_instructions',
                      'default_permissions', 'sandbox_mode', 'sandbox_workspace_write']
            different = [key for key in fields if actual.get(key) != expected.get(key)]
            if different:
                add('profile-drift', target, 'Different fields: ' + ', '.join(different))
        except (ValueError, OSError) as exc:
            add('profile-invalid', target, str(exc))
    installed = project / '.agents/skills' / manifest['skill_name']
    if not installed.is_dir():
        add('skill-not-installed', installed, 'No project-scoped installation at this location')
    else:
        for name in manifest['skill_files']:
            source, target = inside(package, name), inside(installed, name)
            if source.is_file() and (not target.is_file() or source.read_bytes() != target.read_bytes()):
                add('installed-file-drift', target, 'Installed file differs from the selected source package')
    return {'schema_version': 1, 'mutations': False, 'findings': findings,
            'comparison_source': str(package.resolve()), 'project_root': str(project.resolve()),
            'model_availability': 'not-assessed', 'upstream_version': 'not-checked',
            'semantic_validity': 'not-assessed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['diagnose', 'snapshot', 'verify'])
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--files', nargs='+')
    parser.add_argument('--snapshot', type=Path)
    args = parser.parse_args()
    try:
        if not args.project.is_dir():
            raise ValueError('Project directory does not exist')
        if args.mode == 'diagnose':
            result = diagnose(args.package.resolve(), args.project.resolve())
        elif args.mode == 'snapshot':
            result = fingerprint(args.project.resolve(), args.files)
        else:
            if args.snapshot is None:
                raise ValueError('--snapshot is required for verify')
            result = verify(args.project.resolve(), json.loads(args.snapshot.read_text(encoding='utf-8-sig')))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get('status') == 'STALE' else 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
