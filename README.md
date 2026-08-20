# Public AI Kit

Publicly reusable AI agents, skills, plugins, and capability packages maintained by Cutto.

## Install a Skill

List the available Skills:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@latest add \
  https://github.com/cutto-ai/public-ai-kit.git \
  --list
```

Install `cutto-ai-verify` globally for Codex:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@latest add \
  https://github.com/cutto-ai/public-ai-kit.git \
  --skill cutto-ai-verify \
  --agent codex \
  --global \
  --copy \
  --yes
```

## Available Skills

| Skill | Purpose |
| --- | --- |
| [`cutto-ai-verify`](skills/cutto-ai-verify/SKILL.md) | Run evidence-backed, spec-driven acceptance verification and regression. |

## License

[MIT](LICENSE)
