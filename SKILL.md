---
name: orchestrate-development-v3
description: Execute a substantial development stage with a Terra High root by default, temporary Luna Max root compatibility, exact Astra Low autonomous implementation workers, bounded Luna XHigh repair workers, optional Terra High read-only gates, internal Sol Medium review and Luna XHigh final validation. Experimental v3; use only when explicitly invoked and never replace v2 implicitly.
---

# Orchestrate Development V3

Deliver a correct, maintainable, accepted capability with proportionate model cost, elapsed time, coordination, testing, review, and rework. This is an experimental workflow independent of `orchestrate-development` v2 and the external loop-review skills.

## Select the operation

These are arguments to this skill, not separately installed slash commands. Explicit intent wins; `run` is the default for an authorized execution request.

| Mode | Action | Load when needed |
| --- | --- | --- |
| `plan` | Produce the stage plan; do not implement or dispatch implementation workers | Context below; internal review only at a warranted boundary |
| `run` | Execute the requested outcome; keep small work direct | Context for substantial stages; focused validation before implementation dispatch |
| `resume` | Reconcile current state and continue pending work | [CONTEXT_AND_RESUME](references/CONTEXT_AND_RESUME.md) |
| `diagnose` | Inspect package/profile drift without repairs | [DIAGNOSE](references/DIAGNOSE.md) |

Advice about this workflow does not execute it. A bare invocation with no outcome asks for the intended task; do not scan unrelated projects or automatically start a stage. Before planning a substantial stage read [references/CONTEXT_AND_RESUME.md](references/CONTEXT_AND_RESUME.md). Load review, final-validation and Spark references only at their existing dispatch boundaries. Planning and diagnosis do not load implementation-only mechanics. Exact root/child model contracts below apply to plan/run/resume execution; standalone read-only diagnostics do not require spawning or rebinding a model.

## Bind the architecture

The preferred invoking root is `gpt-5.6-terra` at `high`. `gpt-5.6-luna` at `max` remains a supported compatibility root during migration; use the root that actually invoked the skill and report which route ran. Do not spawn a replacement root or claim that a profile changed an already active main session. The bundled `terra-high-orchestrator` profile is an exact configuration layer for hosts that expose custom-agent startup and a reference for manual model/effort selection.

Bind each child to the exact model, effort and role instructions below, using either a supported named agent profile or explicit native spawn arguments. A missing profile selector is not a missing model-binding capability. Before the first child dispatch read [references/RUNTIME_BINDING.md](references/RUNTIME_BINDING.md) and inspect the actual tool schema. Never inherit root model settings implicitly or substitute another model. Scoring reviewers start without parent history (`fork_turns="none"` where supported). Permission profiles govern tool access separately from model/role binding; preserve the user's current permission configuration.

| Route | Profile | Exact model | Effort | Purpose |
| --- | --- | --- | --- | --- |
| `ROOT_ORCHESTRATOR` | `terra-high-orchestrator` or root selection | `gpt-5.6-terra` | `high` | preferred semantic context, stage decomposition, ownership, integration, light acceptance |
| `LUNA_ROOT_COMPAT` | root selection | `gpt-5.6-luna` | `max` | temporarily supported root with the same ownership contract |
| `ASTRA_WORKER` | `astra-low-worker` | `gpt-6-astra` | `low` | default substantial autonomous implementation |
| `LUNA_WORKER` | `luna-xhigh-worker` | `gpt-5.6-luna` | `xhigh` | bounded repair, continuation, or economical background work |
| `TERRA_GATE` | `terra-high-gate` | `gpt-5.6-terra` | `high`, read-only | one evidence or diagnostic gate requested by root |
| `SOL_REVIEWER` | `v3-sol-medium-reviewer` | `gpt-5.6-sol` | `medium`, read-only | independent plan or code review at a selected stage/risk boundary |
| `LUNA_VALIDATOR` | `v3-luna-xhigh-validator` | `gpt-5.6-luna` | `xhigh` | final stage/e2e execution and evidence analysis |
| `SPARK_TOOL` | adapter, not a native agent | `gpt-5.3-codex-spark` | adapter-owned | qualifying deterministic operation |

There is no Astra Medium route, effort escalation route, Sol implementation fallback, or Astra reviewer route; Sol supplies review evidence, while root owns acceptance. When Astra Low does not succeed, reassess the Goal, requirements, decomposition, or ownership before routing a bounded repair.

## Plan only a substantial stage

For a substantial stage, root records the outcome, dependencies, coherent implementation streams, governing contracts and invariants, owned seams, acceptance, focused validation, stage validation, review boundary, and integration/release gate. Keep small work direct.

Root alone may dispatch `SOL_REVIEWER` for a plan review before implementation, when the stage plan is materially cross-cutting, ambiguous, architecture-heavy, dependency-heavy, risky, or expensive to correct. Worker micro-plans never receive plan review. Read [references/INTERNAL_REVIEW.md](references/INTERNAL_REVIEW.md) before dispatching internal review. Keep standalone Loop Review packages and profiles independent.

## Dispatch outcome-oriented Goals

Send Astra the observable outcome, owned writable seam, governing specification pointers, architecture/contracts/invariants, acceptance criteria, focused validation expectations, and consequential stop conditions. Do not send this skill, the root transcript, old worker history, a mandatory implementation algorithm, mandatory TDD choreography, an internal review loop, or a request to create subagents.

Root specifies **what** and the hard boundaries; Astra owns **how**. The worker inspects directly coupled code, forms and maintains a compact working plan, identifies outcome-level validation scenarios, implements and refactors, chooses focused tests, repairs local errors, inspects its diff once, and returns one compact `EVIDENCE_CAPSULE`.

Ordinary implementation ambiguity is worker-owned. Return to root only when uncertainty can materially change product intent, architecture, a public contract, security/privacy, persistence/data semantics, irreversible behavior, or ownership/scope.

## Bind and execute in one turn

Every delegated Goal uses `BIND_AND_EXECUTE`: create or bind the Goal, form a compact micro-plan, and execute in the same turn. Never spend a separate model round acknowledging `GOAL_BOUND`, waiting for `EXECUTE`, or normalizing lifecycle status. Do not poll on a timer.

Use `LEAF` for one bounded outcome. Use `PROCESS` for sequential Goals only while seam, model/profile, owner, and useful code/domain context remain the same; exactly one Goal may be active. Retire the process when the seam or owner changes, the next Goal is not ready, independence is needed, or retained context becomes noisy. Do not impose a numeric Goal quota.

Native topology is flat: root may create Astra, Luna, and Terra leaves/processes, plus root-dispatched Sol review and Luna validation leaves. Workers create no native subagents, gates, plan reviews, or code reviews. A worker that needs separate evidence returns a compact `GATE_REQUEST`; root decides whether to dispatch Terra.

`MAX_ACTIVE_CHILD_TASKS` is a ceiling, never a target. Parallelize only independent seams or read-only work on stable inputs. Keep one writer per overlapping boundary.

## Preserve workflow ownership

Root and every child must not load or invoke external review/orchestration workflows, including Loop Code Review and Loop Plan Review under any version or alias. Do not import their scoring loops, model routing, or acceptance rules. A separately requested standalone Loop Review is outside this workflow, never an internal delegation route. Project architecture, contracts, mandatory validation and publication permissions remain binding. Project-required review milestones use internal Sol review; project Loop Review invocation/cadence is replaced only by an explicit project/user exception. See the optional [project integration fragment](docs/AGENTS.integration.md). Task-relevant specialist skills remain available when they do not replace this workflow; governing higher-priority instructions still apply.

## Focus validation on risk

Before implementation dispatch, read [references/FOCUSED_VALIDATION.md](references/FOCUSED_VALIDATION.md). Workers own focused validation; root assigns expensive stage validation once after stable integration and scheduled repair. Preserve project-required checks.

## Normalize one worker return

Before returning, the worker performs one self-check: Goal alignment, unrelated-change check, acceptance coverage, focused validation, deviations, and material uncertainty. This is not an independent code review and has no score or repeated review rounds.

```text
EVIDENCE_CAPSULE
Goal/result
tested revision/diff marker + relevant input scope
changed paths + anchors
important implementation decisions
focused validation + result
deviations
material uncertainty/risks
runtime metrics when exposed
optional GATE_REQUEST
```

Normalize the return once. Durable root context is specification, stage plan, invariants, owner decisions, repository state, stable diffs, tests, a compact ledger, and evidence capsules—not raw logs, transcripts, old statuses, receipts, or closed findings.

## Perform light acceptance

Root checks the Goal contract, stable diff/evidence, capsule, focused validation, evidence freshness and scope deviations, then chooses exactly one result:

- `ACCEPT` — the Goal is fit for integration.
- `REPAIR` — return a bounded repair Goal to Astra or Luna according to the work.
- `DECISION_REQUIRED` — a consequential owner/root decision is missing.
- `REVIEW_REQUIRED` — independent review is warranted by the stage risk.

Completion does not create a reviewer automatically. Independent review is stage-, risk-, or milestone-based. Root may dispatch `SOL_REVIEWER` for code review against a stable integrated diff for auth/security/privacy/payments, migrations or destructive data, concurrency/distributed state, material public contracts, risky multi-writer integration, material uncertainty, unexpected scope, repeated validation failure, or when root cannot confidently accept. Treat review as the default before an important release/MVP milestone unless the user chooses another assurance level.

For a reviewed stage use: implementation → focused validation → stable integration → independent review → bounded repair → affected focused retest → heavy stage validation → acceptance. Repeat independent review only when repair materially changes the reviewed behavior, contract, architecture, or risk boundary. Without review, use implementation → focused validation → integration → stage validation → acceptance.

## Final stage and end-to-end validation

After stable integration and scheduled review repairs, root dispatches one `LUNA_VALIDATOR` leaf as the owner of final stage validation. Read [references/FINAL_VALIDATION.md](references/FINAL_VALIDATION.md) before dispatch. Supply the stable revision/diff marker, acceptance criteria, required scenarios, commands, environment and integration assumptions, and artifact locations. Run existing deterministic suites through scripts; the validator checks actual execution, skips, environment fidelity, results, and relevant logs/traces/screenshots rather than merely reporting exit codes. Root owns acceptance.

The validator does not repair product code or weaken tests. Failures return evidence and a bounded diagnosis to root; root dispatches repair to Luna or Astra, then reruns affected validation. Repeat the full suite only when changes invalidate broad evidence. Never rerun until green without explaining the failure. Terra remains optional for one concrete unresolved question, never a mandatory second overview.

## Detect stagnation by evidence

Long reasoning is not itself failure. Require a new useful signal: implementation artifact, meaningful diagnostic evidence, exact blocker/root-cause anchor, or validation result. After two meaningful checkpoints without new evidence, request one compact status/stop capsule and then reroute or reframe; do not create repeated STOP/status loops.

## Use optional runtime assets

Read [references/SPARK_ADAPTER.md](references/SPARK_ADAPTER.md) before the first `SPARK_TOOL` use. The adapter remains a tool under root/worker supervision, never a planner, reviewer, process, or acceptance authority.

Project profiles are shipped under `assets/project/.codex/agents/`. Install them with the bundled `install.py`. Global telemetry, if present, observes exposed host events without requiring agent messages, ledger writes, or orchestration hooks. It is not a package dependency. The project orchestration guard is disabled. Root maintains its compact working record itself; do not call the old hook ledger or require hook acceptance/archival transitions. Profiles and workflow decisions belong to this skill, not telemetry.

Tag persisted runtime telemetry, when the host exposes it, with `workflow=orchestrate-development-v3`, `orchestration_version=3`, route, `stage_id`, `goal_id`, lifetime, and `interaction_class`. Do not dump telemetry to the user.

## Finish compactly

Report the accepted capability, focused/stage validation, models and routes actually used, and remaining material risk. Runtime values are reported only when exposed; never estimate them. Success is the accepted result at assurance proportionate to actual risk—not agent count, test count, coverage, review rounds, or occupied concurrency.
