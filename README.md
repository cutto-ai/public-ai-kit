# Public AI Kit

Publicly reusable AI agents, skills, plugins, and capability packages maintained by Cutto.

## Install a Skill

List the available Skills:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@latest add \
  https://github.com/cutto-ai/public-ai-kit.git \
  --list
```

Install `max-ctr` globally for Codex:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@latest add \
  https://github.com/cutto-ai/public-ai-kit.git \
  --skill max-ctr \
  --agent codex \
  --global \
  --copy \
  --yes
```

## Available Skills

| Skill | Purpose |
| --- | --- |
| [`max-ctr`](skills/max-ctr/SKILL.md) | Design, adapt, validate, and deliver high-CTR video and social cover systems. |

## Contributing

Keep each Skill self-contained under `skills/<skill-name>/`. Run `python3 scripts/validate-skills.py` before opening a PR. See [AGENTS.md](AGENTS.md) for repository boundaries and contribution rules.

Maintainers: [`@cutto-ai/dev`](https://github.com/orgs/cutto-ai/teams/dev).

## License

[MIT](LICENSE)
