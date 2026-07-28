---
name: project-operating-system
description: Bootstrap a new software project or safely align an existing repository with lightweight operating rules, state tracking, task routing, approval gates, growth loops, and evidence-backed deep research. Use when asked to set up project foundations, AGENTS.md, project operating rules, handoff/state documents, research vaults, source provenance, or Codex-native deep research without overwriting an active project.
---

# Project Operating System

Create a small, inspectable operating layer. Preserve application code and existing project instructions; never treat an archived AgentOS package in a repository as an active installation.

## 1. Inspect and choose a mode

1. Locate the repository root and read any root `AGENTS.md`, `README*`, package manifest, and existing `docs/` state files.
2. Run `scripts/project_os.py <repo> --mode auto` to report the safe action without modifying files.
3. Choose the smallest edition that fits:
   - `ultralite`: one-person, short-lived or prototype work.
   - `lite`: default for active product/app work; task board, work/project/QA/research state, product brief, workflows, and handoffs.
   - `enterprise`: only when the repository genuinely needs policy, release, decision, and compliance records.
4. For a new repository, use `--mode new`. For a repository with meaningful code or docs, use `--mode existing`.

Read [references/operating-rules.md](references/operating-rules.md) before choosing an edition or resolving conflicts with existing project rules.

## 2. Apply safely

Run an explicit preview first, then apply it only after reporting the proposed files and receiving approval:

```bash
python3 scripts/project_os.py /absolute/path/to/repo --mode existing --edition lite
python3 scripts/project_os.py /absolute/path/to/repo --mode existing --edition lite --apply
```

- The script creates only missing files. It does not overwrite existing files.
- If root `AGENTS.md` exists, it creates `AGENTS_AGENTOS_ADDENDUM.md`; review it and merge deliberately. Do not append rules automatically.
- If root `AGENTS.md` is absent, it creates one with the operating router.
- Use `--force` only for an intentionally replaceable, generated skeleton after confirming the exact target with the user.

## 3. Enable Codex Deep Research

Use this mode only for research that needs durable, evidence-backed conclusions: market/competitor studies, technical choices, policy analysis, literature review, or a decision that will be revisited. It is not a substitute for a simple web lookup.

```bash
python3 scripts/project_os.py /absolute/path/to/repo --mode existing --edition lite --research
python3 scripts/project_os.py /absolute/path/to/repo --mode existing --edition lite --research --apply
```

The mode adds only missing `docs/research/` templates and, for an existing `AGENTS.md`, a reviewable research addendum. Read [references/codex-deep-research.md](references/codex-deep-research.md) before conducting a run.

## 4. Operate the project

After installation, route each request through root `AGENTS.md`; load only the state files and one workflow relevant to the task. On a change task, update `work-state.md` and `task-board.md`; update QA or research state only when that work occurred. Stop after the agreed single task rather than silently beginning the next one.

For a growth request, use the conditional loop: Research → Document → Plan → Implement → Test → User Flow QA → Report → Improve Backlog → Stop. Do not use the loop for ordinary implementation or small fixes.

For deep research, preserve the canonical question; define claims and coverage before searching; seek primary sources and counter-evidence; deduplicate syndicated sources; map each material claim to evidence; then save a concise report and handoff. Do not claim factual certainty merely because the evidence passes structural checks.
