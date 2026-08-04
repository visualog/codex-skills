# Codex Skills

Versioned, portable custom skills for Codex.

## Included skills

| Skill | Purpose |
| --- | --- |
| `project-operating-system` | Safely initialize or align project operating rules, state, handoffs, and durable research. |
| `codex-deep-research` | Run evidence-led research with claim mapping, counterevidence, and traceable conclusions. |
| `reconstruct-reference-ui` | Rebuild web interfaces from visual references through measured browser comparison and iteration. |

## Install on another Mac

Clone this repository, then copy the skill directories into Codex's global skill directory:

```bash
git clone https://github.com/visualog/codex-skills.git
mkdir -p ~/.codex/skills
cp -R codex-skills/project-operating-system ~/.codex/skills/
cp -R codex-skills/codex-deep-research ~/.codex/skills/
cp -R codex-skills/reconstruct-reference-ui ~/.codex/skills/
```

Restart Codex if it does not recognize the new skills immediately. Invoke them in the desktop app with `@skill-name`; use `$skill-name` in the CLI or IDE.

## Repository policy

Keep only custom, shareable skills here. Do not commit built-in skills, plugin caches, third-party skills that can be reinstalled, credentials, personal paths, or project-specific research data.
