# Public AI Kit Repository Rules

## Scope

This repository owns publicly reusable AI agents, Skills, plugins, and capability packages. Assets must be useful outside Cutto and safe to publish.

Do not add:

- Cutto workspace rules, hooks, or `cutto-dev` configuration; those belong to `internal-workspace-settings`.
- Internal operations, credentials, private endpoints, or service-management tools; those belong to `internal-ai-toolkit`.
- Product runtime code or business data models.

## Skill contract

- Put the canonical package at `skills/<skill-name>/` and keep the folder name identical to the `name` in `SKILL.md`.
- Keep `SKILL.md` frontmatter limited to `name` and `description`.
- Keep scripts, references, assets, and `agents/openai.yaml` inside the Skill folder so installation is self-contained.
- Use relative links within a Skill. Never commit local absolute paths, secrets, private URLs, or user-specific data.
- Do not add auxiliary README, changelog, or installation files inside a Skill folder. Repository-level documentation belongs in the root README.
- Preserve executable permissions for runnable scripts and test them directly.

## Verification

Run:

```bash
python3 scripts/validate-skills.py
```

Also run syntax or behavior checks for every changed script. A PR must state what was validated and what was not covered.

## Git and review

- Branches with a Linear Issue use `<lowercase-issue-id>-<3-to-5-word-topic>`.
- Commit and PR titles use `<type>(<scope>): <summary>` and retain the Linear Issue ID in the PR title and body.
- Each PR changes one capability. Use the PR Quiz structure: TLDR, Explainer, key decisions and deviations, risks and verification, and Reviewer Quiz.
