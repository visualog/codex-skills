# Operating rules

## Non-negotiable safeguards

- Inspect before applying. An AgentOS folder or zip is a source package, not evidence that a repository is configured.
- Preserve existing repository instructions. If `AGENTS.md` exists, generate an addendum and ask for a deliberate merge; do not replace or append it automatically.
- Require explicit user approval before package installation, project initialization, registry/MCP changes, deployment, payments, data migration, or secret/API-key work.
- Keep scope to one bounded task. Do not begin a queued task merely because the previous one completed.
- Do not expose or write secrets or personal data.

## Default Lite operating model

Use Lite unless the project is disposable (UltraLite) or requires formal policies/release/decision records (Enterprise).

Required Lite records:

| Purpose | File |
| --- | --- |
| Current work and next action | `docs/states/work-state.md` |
| Queued and completed tasks | `docs/states/task-board.md` |
| Scope, stack, and constraints | `docs/states/project-state.md` |
| Research evidence, when used | `docs/states/research-state.md` |
| User-flow verification, when used | `docs/states/qa-state.md` |
| Product intent and metrics | `docs/product/` |
| Continuation across sessions | `docs/handoffs/` |

## Routing and validation

Classify requests as General, Feature, Bugfix, Refactor, Release, UI, Iteration, Research, User Flow QA, or Growth Iteration. Read only the corresponding workflow, not the entire documentation tree.

Prefer small diffs and targeted checks. Keep new source files below roughly 250 lines when feasible; do not add a new responsibility to a file nearing 300 lines. Record changed files, verification, and remaining risk at task completion.

## Growth loop

Run it only for explicit project-improvement work or when investigation and user-flow verification are materially needed. Limit sources to 3–7, summaries to three lines per source, and new backlog candidates to 1–3. Verify only the changed user flow.

For a dedicated deep-research run, use [codex-deep-research.md](codex-deep-research.md) instead. Its source count is driven by claim coverage, not a fixed quota.
