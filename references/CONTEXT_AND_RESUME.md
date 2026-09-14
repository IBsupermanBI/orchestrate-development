# Context ownership and resume

Read when preparing a substantial stage or resuming interrupted work. Use the project's existing locations; do not create a second specification system or modify AGENTS.md.

| Layer | Authority | Lifetime |
| --- | --- | --- |
| Project contracts | User decisions, governing project instructions and current specifications | Until explicitly superseded; implementation discrepancies require reconciliation |
| Stage plan | Root's outcome, dependencies, seams, acceptance and validation ownership | Current stage; revise when intent or dependencies change |
| Worker Goal | One outcome, writable seam and relevant contract pointers | One active Goal; replace on ownership/scope change |
| Evidence capsule | Observed result, input marker, commands, environment and artifacts | Only while relevant inputs and assumptions remain valid |

Load the selected target, directly coupled contracts and compact stage record. Give workers only relevant pointers and their Goal, never the root history. Preserve existing records; root owns stage decisions, workers own implementation evidence. A document's filename or age alone does not establish authority or staleness.

For a substantial stage persist a compact record in a project-approved local artifact directory (default `.scratch/orchestration/<stage-id>/`). Include outcome, contract pointers, acceptance, ownership, completed/pending Goals, unresolved decisions, evidence locations and the next action. Update at integration, handoff or material change, not after every tool call. This record is not a hook ledger and never gates ordinary work on mechanical status transitions.

## Evidence markers

Include a stable revision/diff marker in each capsule. HEAD alone is insufficient with uncommitted changes. When a reliable host marker is unavailable, use the bundled read-only helper to fingerprint explicitly selected source files, tests, configuration and governing contracts:

```sh
python <skill-base>/scripts/orchestration_doctor.py snapshot --project <project> --files src/example.py tests/test_example.py pyproject.toml
```

Root may save stdout as `inputs.json` in its stage artifact directory. The helper itself writes nothing. Capture around validation on stable inputs; if inputs change during execution, evidence is incomplete. Include relevant untracked files and expected absent paths. MATCH proves only selected bytes are unchanged; omitted dependencies, environment changes and semantic coverage still need assessment. Never claim a whole-tree guarantee from a partial snapshot.

## Resume

1. Read the latest user intent, project contracts and compact stage record. Inspect current repository changes without resetting, stashing or overwriting them.
2. Reconcile recorded worker ownership with live task state if available. An unavailable task is unknown, not finished; do not start another writer on its seam until ownership is resolved.
3. Verify relevant input markers (`verify --project <project> --snapshot <inputs.json>`), artifacts, validation results and environment assumptions. Changed inputs invalidate affected evidence; retain unaffected evidence only with a reason. Missing evidence is unknown, never PASS.
4. Record completed, remaining and invalidated work. Bind new workers only to pending outcomes. Reuse a process only under the existing same-seam/profile/owner rules.
5. Continue in the same turn when the next action is authorized. Ask only for consequential missing decisions. Do not restart completed work or rerun a broad suite solely because the conversation resumed.

If no record exists, reconstruct a compact one from current files, diffs and available evidence. Do not invent past acceptance or agent results.
