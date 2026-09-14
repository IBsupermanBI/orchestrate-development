# Bind roles using available native tools

Read once before child dispatch, or when diagnosing profile/permission errors. Inspect the current tool schema; installed TOML files do not add parameters to a tool.

## Model and role selection

1. If the native spawn tool supports a named custom-agent selector and the selected profile is available, select the exact profile in SKILL.md.
2. Otherwise read `assets/project/.codex/agents/<profile>.toml`. Pass its `model` and `model_reasoning_effort` through the tool's supported model/effort arguments. Include the complete `developer_instructions` in the child task message, followed by the bounded Goal and evidence pointers. This is an explicit native binding and is a supported execution route; no profile installation or user confirmation is needed just because the selector is absent.
3. For `collaboration.spawn_agent`, use `model`, `reasoning_effort`, `fork_turns="none"`, `task_name` and `message`. Full-history forks cannot accept model/effort overrides. Supply the necessary context in the message instead. Do not pass invented `profile`, `agent_type`, `sandbox_mode` or permission arguments. Use another host's actual schema when names differ.

Keep requested settings separate from observed runtime metadata. Explicit arguments establish requested binding; do not claim the model/effort was independently verified unless runtime evidence exposes it. Missing observation alone does not invalidate a supported explicit dispatch. A rejected model or actual mismatch does invalidate that route.

Only when neither named selection nor explicit exact model/effort selection is available, identify the specific missing field or rejected route and stop dependent delegation. Continue independent authorized work if possible. Do not repeatedly retry the same unsupported call, create sidebar tasks or invent a general CLI-worker fallback. The Spark CLI route remains separately governed by its adapter. Root model mismatch cannot be repaired by pretending a child changed the invoking root. `terra-high-orchestrator` records the preferred root model and instructions, but custom-agent TOML is normally applied to spawned sessions; select Terra High in the main session when the host does not expose a root-profile selector. An already active Luna Max root is the supported compatibility route, not a binding failure.

## Permissions and isolation

Agent role profiles, CLI `--profile` configuration layers and permission profiles are different mechanisms. Changing `default_permissions` cannot add a native agent selector or select a model.

Preserve the active user's permissions, approval policy and Windows sandbox setup. Do not rewrite global/project configuration, switch to full access or change elevated/unelevated sandbox to solve a binding error. Current permission-profile configuration must not be combined with legacy `sandbox_mode` or `[sandbox_workspace_write]` in the same effective configuration. Packaged Terra/Sol defaults use `default_permissions = ":read-only"`; implementation and validation inherit host permissions.

Native children inherit the parent's live permission mode, which can override file defaults. When the spawn tool has no per-child permission control, Terra and Sol still have a strict no-write task contract; report isolation as inherited, not as an enforced read-only sandbox. Do not claim that task instructions enforce filesystem isolation. If the user/project requires enforced per-child isolation, use a host-supported restrictive mechanism or report that specific capability gap before dispatch; do not silently weaken that requirement.

For shell execution use only exposed parameters and the current approval policy. Under approval policy `never`, an unavailable operation is a concrete execution limitation, not a reason to request escalation. A sandbox/process denial does not prove model binding failed.

The Spark adapter deliberately uses `--ignore-user-config` and its own bounded `--sandbox`; preserve that separate contract. Do not copy its legacy flag into a launcher that loads managed permission-profile configuration. If a project/managed layer still conflicts, report the actual error and use the documented Luna fallback without rewriting that layer.

Official references (checked 2026-09-11): [configuration](https://learn.chatgpt.com/docs/config-file/config-reference), [subagent permission inheritance](https://learn.chatgpt.com/docs/agent-configuration/subagents). The live tool schema and enforced runtime permissions remain authoritative.
