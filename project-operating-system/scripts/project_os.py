#!/usr/bin/env python3
"""Preview or create a minimal AgentOS-style operating layer without overwrites."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT_AGENTS = """# AGENTS.md — Project Operating System

## Operating rules

- Classify each request before working. Read only the relevant workflow, never scan all `docs/`.
- For a change, read `docs/states/work-state.md`, `docs/states/task-board.md`, and `docs/states/project-state.md`.
- Do one bounded task, validate it proportionately, update state, and stop for approval.
- Ask before package installs, init/registry/MCP changes, deployment, payments, migrations, or secret/API-key work.
- Never expose secrets or personal data.

## Routing

| Type | Workflow |
| --- | --- |
| Feature | `docs/workflows/feature.md` |
| Bugfix | `docs/workflows/bugfix.md` |
| Refactor | `docs/workflows/refactor.md` |
| Release | `docs/workflows/release.md` |
| UI | `docs/workflows/ui.md` |
| Research | `docs/workflows/research.md` |
| User Flow QA | `docs/workflows/user-flow-qa.md` |
| Growth Iteration | `docs/workflows/growth.md` |
| Deep Research | `docs/workflows/deep-research.md` |

Run Growth only for explicit improvement work: Research → Document → Plan → Implement → Test → User Flow QA → Report → Improve Backlog → Stop.
"""

ADDENDUM = """# AgentOS operating-rule addendum (review before merging)

Preserve this repository's existing instructions. Add only compatible rules:

- Route work to one relevant workflow; do not scan all documentation.
- On change tasks, keep current work, task board, and project state concise.
- Complete one bounded task, run proportionate validation, report evidence, then wait for approval.
- Request approval before installs, deployment, migrations, secret/API-key work, or external configuration changes.
- Run the growth loop only for explicit project-improvement work.
"""

RESEARCH_ADDENDUM = """# Deep-research addendum (review before merging)

For explicit evidence-backed research, preserve the verbatim user question; define claims before searching; use primary sources and counter-evidence; cluster syndicated sources; map each material claim to direct evidence and caveats; then save the report and handoff under `docs/research/`. Structural checks do not guarantee factual certainty.
"""

WORKFLOWS = {
    "feature.md": "Define the smallest useful slice, inspect local patterns, implement a small diff, run targeted checks, then update state.\n",
    "bugfix.md": "Reproduce or inspect evidence first, isolate the cause, make the smallest fix, verify the affected path, then update state.\n",
    "refactor.md": "State the preserved behavior, limit the structural change, run focused regression checks, then update state.\n",
    "release.md": "Confirm scope, versioning, checks, rollback implications, and explicit deployment approval before release actions.\n",
    "ui.md": "Use the existing design system first; verify the changed user path and accessibility implications.\n",
    "research.md": "Use authoritative sources when facts may change; record only decisions, sources, and implications.\n",
    "user-flow-qa.md": "Verify one changed end-to-end flow; record steps, result, environment, and any remaining issue.\n",
    "growth.md": "Use only for explicit improvement: Research → Document → Plan → Implement → Test → User Flow QA → Report → Improve Backlog → Stop. Keep 1–3 backlog candidates and wait for approval.\n",
    "deep-research.md": "Use only for an evidence-backed decision. Preserve the canonical question, define a claim matrix, search primary and counter-evidence, cluster syndication, map material claims to evidence, run a citation/date/numeric gate, then save the report under docs/research.\n",
}

FILES = {
    "docs/states/work-state.md": "# Work state\n\n- Current task: Not set\n- Status: Ready\n- Next action: Define one bounded task\n- Last verification: Not run\n",
    "docs/states/task-board.md": "# Task board\n\n## Now\n\n- [ ] Define the first bounded task\n\n## Next\n\n- [ ] None\n\n## Done\n\n- [ ] None\n",
    "docs/states/project-state.md": "# Project state\n\n- Purpose: Not set\n- Users: Not set\n- Stack: Inspect repository\n- Constraints: Preserve existing repository rules\n",
    "docs/states/research-state.md": "# Research state\n\nRecord only research that informed a decision.\n",
    "docs/states/qa-state.md": "# QA state\n\nRecord affected user flow, environment, result, and remaining issue.\n",
    "docs/product/product-brief.md": "# Product brief\n\n- Problem: Not set\n- Target user: Not set\n- Value: Not set\n",
    "docs/product/success-metrics.md": "# Success metrics\n\n- Primary metric: Not set\n- Guardrail: Not set\n",
    "docs/product/user-flows.md": "# User flows\n\n- Primary flow: Not set\n",
    "docs/handoffs/README.md": "# Handoffs\n\nCreate a dated handoff for unfinished work: goal, current state, changed files, verification, risks, and next approved action.\n",
}

RESEARCH_FILES = {
    "docs/research/README.md": "# Deep research runs\n\nCreate a dated topic folder. Preserve the canonical question, sources, counter-evidence, claim map, report, and handoff.\n",
    "docs/research/_template/research-brief.md": "# Research brief\n\n## Canonical question\n\n## Decision and audience\n\n## Time boundary and exclusions\n\n## Coverage matrix\n\n| Claim or question | Needed evidence | Status |\n| --- | --- | --- |\n",
    "docs/research/_template/source-register.md": "# Source register\n\n| ID | URL | Publisher | Date | Type | Independence cluster | Supports / challenges | Status |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n",
    "docs/research/_template/evidence-digest.md": "# Evidence digest\n\n## Source notes\n\nRecord concise evidence with the relevant passage, section, table, or page.\n",
    "docs/research/_template/contradictions.md": "# Contradictions and counter-evidence\n\n| Claim | Counter-evidence | Resolution or open question |\n| --- | --- | --- |\n",
    "docs/research/_template/claim-map.md": "# Claim map\n\n| Material claim | Evidence IDs | Counter-evidence IDs | Confidence | Caveat |\n| --- | --- | --- | --- | --- |\n",
    "docs/research/_template/final-report.md": "# Final report\n\n## Executive conclusion\n\n## Findings\n\n## Caveats and unresolved questions\n\n## Sources\n",
}


def mode_for(root: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    indicators = [root / "AGENTS.md", root / "package.json", root / ".git", root / "src", root / "README.md"]
    return "existing" if any(item.exists() for item in indicators) else "new"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path)
    parser.add_argument("--mode", choices=("auto", "new", "existing"), default="auto")
    parser.add_argument("--edition", choices=("ultralite", "lite", "enterprise"), default="lite")
    parser.add_argument("--research", action="store_true", help="add Codex deep-research templates without overwriting files")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force", action="store_true", help="replace generated files; use only after explicit confirmation")
    args = parser.parse_args()
    root = args.repo.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository directory does not exist: {root}")
    selected_mode = mode_for(root, args.mode)
    files = dict(FILES)
    files.update({f"docs/workflows/{name}": content for name, content in WORKFLOWS.items()})
    if args.edition == "ultralite":
        keep = {"docs/states/work-state.md", "docs/states/task-board.md", "docs/workflows/feature.md", "docs/workflows/bugfix.md", "docs/workflows/growth.md"}
        files = {key: value for key, value in files.items() if key in keep}
    if args.edition == "enterprise":
        files.update({
            "docs/states/decision-log.md": "# Decision log\n\n| Date | Decision | Rationale | Owner |\n| --- | --- | --- | --- |\n",
            "docs/policies/README.md": "# Policies\n\nAdd only policies required by this project.\n",
        })
    planned = []
    agents = root / "AGENTS.md"
    if agents.exists():
        planned.append((root / "AGENTS_AGENTOS_ADDENDUM.md", ADDENDUM))
    else:
        planned.append((agents, ROOT_AGENTS))
    planned.extend((root / rel, content) for rel, content in files.items())
    if args.research:
        if agents.exists():
            planned.append((root / "AGENTS_DEEP_RESEARCH_ADDENDUM.md", RESEARCH_ADDENDUM))
        planned.extend((root / rel, content) for rel, content in RESEARCH_FILES.items())
    print(f"Mode: {selected_mode}; edition: {args.edition}; research: {args.research}; root: {root}")
    for path, _ in planned:
        action = "create" if not path.exists() else ("replace" if args.force else "skip")
        print(f"{action:7} {path.relative_to(root)}")
    if not args.apply:
        print("Preview only. Re-run with --apply after approval.")
        return
    for path, content in planned:
        if path.exists() and not args.force:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print("Applied. Review any AGENTS addendum before merging it into an existing AGENTS.md.")


if __name__ == "__main__":
    main()
