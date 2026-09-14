# Diagnose the selected installation

Read for `diagnose` or a concrete installation/context failure. Run:

```sh
python <skill-base>/scripts/orchestration_doctor.py diagnose --project <project>
```

Python 3.11+ is required for this optional helper. If unavailable, inspect the manifest and relevant TOML profiles directly and disclose that automated diagnostics did not run. This alone does not block planning or implementation when exact role binding is otherwise possible.

The selected package is the comparison authority. To compare a project install against a development checkout, pass `--package <checkout>`. Running inside the installed copy cannot discover upstream updates or prove that copy matches the dev checkout.

Report findings with the affected path and smallest corrective action. A missing project installation is expected in a source-only checkout; it is not evidence that source development is broken. File drift is mechanical; whether changed instructions are intentional requires inspection. Model account availability and document truth are not checked. For launcher/runtime issues use the existing `check_orchestration_runtime.py`; its receipt does not prove exact native model binding.

This mode is read-only. It does not reinstall, update other projects, rewrite profiles or touch hooks. An explicitly requested repair is a separate scoped action. An empty report means only the checked files/profiles match, not that the workflow is behaviorally correct.

For a dispatch/profile error, read [RUNTIME_BINDING.md](RUNTIME_BINDING.md). Compare the live spawn schema before declaring binding unavailable. The doctor compares permission fields as well as model/role fields; it does not inspect global configuration or prove effective child isolation. Report inherited permissions separately from role no-write instructions.
