# Diagnose the selected installation

Run `python <skill-base>/scripts/orchestration_doctor.py diagnose --project <project>`. It compares a selected package to the project installation and reports file/profile drift without writes. Passing diagnosis proves only the compared files match; it does not prove live model availability or behavioral correctness.

Use `snapshot` and `verify` for an explicit set of relevant files when evidence freshness matters. The helper never repairs an install. For a V3-to-V4 transition, use the separate opt-in `upgrade_from_v3.py` after reviewing its dry-run plan.
