# Focused validation

Read before the first implementation dispatch; convey relevant expectations in the Goal. Workers use their profile and Goal rather than loading the root workflow.

## Use risk-weighted testing

Astra keeps a compact working plan at a detail level appropriate to the Goal, updates it when scope, dependencies, or approach materially change, and uses it through implementation and validation. Define a few outcome-level scenarios before implementation; reuse relevant existing tests. Two or three scenarios are a starting point for a bounded Goal, not a cap for a large stage. Do not write tests for every small function or mirror implementation details. Writing executable tests first is optional except where the risk makes it useful.

Tests protect meaningful behavior and material regression risk; they do not maximize counts, coverage artifacts, or state matrices. The default evidence set for ordinary behavior is the primary success case plus a meaningful blocked/invalid case and a material recovery/error case when those risks exist. Add another test only for a distinct material failure mode not already covered.

Implementation-first is normal for ordinary business logic, UI, integrations, internal refactoring, established repository patterns, and well-understood local behavior. Prefer test-first for reproducible regressions, security/permissions, concurrency/transactions, subtle state transitions, destructive/data-integrity behavior, or fragile public contracts. A deterministic regression test is normally sufficient for a bounded bug fix. Do not require ceremonial RED/GREEN/REFACTOR or broad suites after each edit.

The worker owns focused validation: the smallest relevant combination of targeted tests, typecheck, lint/static checks, or runtime checks. Run stage validation once after stable integration and any scheduled review repair. Reserve release validation for release/MVP boundaries and assign every expensive validation to one owner.
