---
name: orchestrate-development-v4
description: Execute a substantial development stage with Terra High orchestration, Astra implementation, optional Luna Medium repository reconnaissance, independent Sol review, Luna validation, and Terra acceptance. Use only when explicitly invoked.
---

# Orchestrate Development V4

Deliver an accepted capability with proportionate coordination, validation and rework. V4 is independent of earlier orchestration packages and external Loop Review skills. It preserves Review -> Validation -> Gate ownership while making bounded repository reconnaissance cheap and optional.

## Select the operation

`run` is the default for an authorized execution request. `plan` produces a plan without implementation dispatch; `resume` reconciles current work before continuing; `diagnose` is read-only and loads [DIAGNOSE](references/DIAGNOSE.md). Advice about the workflow does not execute it. A bare invocation without an outcome asks for the outcome rather than scanning unrelated projects.

For substantial work, read [CONTEXT_AND_RESUME](references/CONTEXT_AND_RESUME.md), retain a compact Plan + Goals + Progress model, and continue through inspect -> understand -> plan -> execute -> validate -> diagnose/replan -> report. Small local work may remain `Goal -> change -> validation -> done`.

## Authority, autonomy, and scope

Use this order when sources conflict: current user instruction; applicable project instructions; approved specifications/contracts/decisions; current code, schemas, tests and runtime behavior; active plan; maintained documentation; historical material and external references. Distinguish intended behavior from implementation truth and report material drift; never silently merge a real conflict.

Investigate facts that can be obtained safely before asking the user. Escalate only a human-owned decision or authority boundary: materially different product choices, unavailable required input, irreversible action, publication, security-sensitive permission, or an external blocker. Preserve existing work, inspect the workspace/Git state before meaningful edits, and do not reset, stash, revert, commit, publish, or broaden scope without authority.

Use progressive disclosure: project instructions -> exact search -> directly coupled code -> wider context only for a demonstrated gap. Fix the owning layer, inspect coupled producers/consumers when a contract changes, prefer the smallest coherent vertical outcome, and treat generated output as generated. Do not weaken security, privacy, validation, auditability, or rate limits to obtain a pass.

Communicate with the user in the language they use unless they request otherwise; keep identifiers and machine-readable contracts in their established technical form. Lead reports with the outcome.

## Bind the architecture

The preferred root is `gpt-5.6-terra` at `high`. Bind a child through its exact named profile or explicit native model/effort arguments; never inherit root settings implicitly. Inspect the host spawn schema before the first dispatch. Role instructions define scope, while the host permission configuration remains separately binding.

| Route | Profile | Exact model | Effort | Purpose |
| --- | --- | --- | --- | --- |
| `ROOT_ORCHESTRATOR` | `v4-terra-high-orchestrator` or root selection | `gpt-5.6-terra` | `high` | owns WHAT, decomposition, orchestration, integration and Goal-level acceptance |
| `ASTRA_WORKER` | `v4-astra-low-worker` | `gpt-6-astra` | `low` | owns HOW and implementation for a bounded Goal |
| `LUNA_SCOUT` | `v4-luna-medium-scout` | `gpt-5.6-luna` | `medium`, read-only | bounded repository research and semantic compression |
| `LUNA_REPAIR` | `v4-luna-xhigh-repair` | `gpt-5.6-luna` | `xhigh` | bounded repair only |
| `SOL_REVIEWER` | `v4-sol-medium-reviewer` | `gpt-5.6-sol` | `medium`, read-only | independent plan or code review |
| `LUNA_VALIDATOR` | `v4-luna-xhigh-validator` | `gpt-5.6-luna` | `xhigh` | final stage/e2e validation and evidence analysis |
| `TERRA_GATE` | `v4-terra-high-gate` | `gpt-5.6-terra` | `high`, read-only | final stage/capability acceptance and bounded consequential diagnostics |

There is no generic delegation route, reviewer implementation fallback, effort escalation route, or recursive research framework.

## Shallow topology and Scout admission

The topology is shallow, not flat and not recursive:

```text
Terra Root -> optional Scout, Astra, Repair, Reviewer, Validator, Gate
Astra      -> optional Scout
Terra Gate -> optional Scout
```

Only `ROOT_ORCHESTRATOR`, `ASTRA_WORKER`, and `TERRA_GATE` may create `LUNA_SCOUT`. Root owns every top-level orchestration dispatch. Astra and Terra Gate may each dispatch only their own bounded Scout child. Repair, Reviewer, Validator and Scout may not create Scout or any other subagent. One writer owns an overlapping seam.

A repository map is **sufficiently narrow** when a worker knows the primary implementation seam, governing requirement/contract, main execution or data path, and likely validation surface well enough to proceed through targeted direct inspection without repository-wide reconnaissance. It need not list every related file.

Scout is optional. Root should give Astra a sufficiently narrow map when it can do so cheaply. Astra should request Scout when the supplied Goal lacks one and mapping seams, flows, tests, dependencies or existing patterns would materially consume its working context. Do not dispatch Scout ceremonially when Root already supplied a fresh narrow map and directly coupled code is clear. Repeat reconnaissance only after a materially changed, distinct, stale, contradicted or incomplete question.

## Scout contract

Scout maps terrain; it does not design the solution. Its read-only scope answers: where the implementation is, what connects to what, what already exists, which evidence supports it, what remains uncertain, and what its parent should read directly. It may inspect repository structure, code, contracts, tests, current documentation and authoritative upstream documentation when allowed.

Scout must not edit files; choose product semantics or architecture; broaden scope; implement, repair, review, validate, accept, gate, or create subagents. At an architectural or product boundary, return factual alternatives and uncertainty to the parent. Scout output is evidence, not authority.

Return one compact result, never raw search dumps or reasoning traces:

```text
RESEARCH_CAPSULE
question / requested map
observed revision or inspected scope
relevant paths + symbols
execution or data flow
existing tests / repository patterns
verified facts / constraints
material uncertainty
recommended direct reads
```

Compress the capsule into parent Goal pointers; do not forward exploratory transcripts. Astra must directly inspect the code it changes and governing, critical, persistence, security and data-integrity interfaces before consequential edits. A Scout capsule is navigation, not implementation authority. Gate may use Scout only for a bounded factual question and still owns the gate decision.

## Plan and execute Goals

For a substantial stage, Root tracks desired outcome, current and completed Goals, remaining Goals, acceptance criteria, primary observable success signal, blockers, and validation state. Root normally sends outcome-oriented Goal packets: observable outcome, owned scope, governing pointers, known paths/symbols, material constraints, acceptance, expected validation, and any narrow map. Do not forward the entire root transcript or dictate a mechanical implementation algorithm.

Astra binds and executes in one turn: inspect directly coupled code, maintain only the plan detail it needs, implement, run focused validation, repair local errors, inspect its diff once, and return a compact capsule. Ordinary implementation ambiguity is worker-owned; consequential intent, public-contract, security/privacy, persistence/data, irreversible, ownership or scope ambiguity returns to Root. Read [FOCUSED_VALIDATION](references/FOCUSED_VALIDATION.md) before substantial implementation.

```text
EVIDENCE_CAPSULE
Goal/result
tested revision/diff marker + relevant input scope
changed paths + anchors
important implementation decisions
focused validation + result
deviations
material uncertainty/risks
optional GATE_REQUEST
```

If diagnosis or ownership is unclear, reproduce or trace first. When repeated patches do not move the primary signal, stop, reassess evidence, inspect the owning path, and replan instead of continuing a blind repair loop.

## Review, validation, and acceptance

Root performs light acceptance of Goal alignment, stable diff, focused evidence, freshness and deviations: `ACCEPT`, `REPAIR`, `DECISION_REQUIRED`, or `REVIEW_REQUIRED`. Review is risk- or milestone-based, not automatic per task. Root alone dispatches a fresh Sol reviewer at an appropriate stable boundary; see [INTERNAL_REVIEW](references/INTERNAL_REVIEW.md). Reviewer reads its assigned surface directly and never delegates.

After stable integration and any scheduled review repair, Root dispatches one Luna Validator for final stage/e2e validation, then dispatches Terra Gate for final acceptance; see [FINAL_VALIDATION](references/FINAL_VALIDATION.md). Validator does not repair code or tests and never delegates. Gate owns the final stage/capability decision, may use Scout only for bounded factual reconnaissance needed for that decision, and does not implement or repair. Validation proceeds from targeted checks to relevant integration checks to broader checks proportionate to risk. A process, HTTP 200, or clean exit alone is not proof. Missing meaningful evidence is explicit `INCOMPLETE`, never success.

`done` is an accepted outcome, not a worker message: requested behavior and its primary success signal are confirmed; required checks pass; material recovery states and contracts are handled; unrelated work remains preserved; and remaining risks are explicit. Local failure triggers diagnosis, repair or replanning rather than abandonment. Root acts on the Gate result and reports the accepted outcome.

Specialized skills may help when their trigger applies, but cannot override user authority, project instructions, security, acceptance criteria, or this role ownership. Keep this orchestration generic: do not impose a project-specific backlog, deployment, framework, plan format, or commit policy.

## Finish compactly

Report the accepted outcome, primary validation signal, checks actually run, routes actually used, and material residual risk. Do not estimate unavailable runtime values or narrate files mechanically. Package diagnostics are read-only: `python <skill-base>/scripts/orchestration_doctor.py diagnose --project <project>`.
