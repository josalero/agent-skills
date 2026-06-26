# Contributing

Quick start for contributors. Full guide: [docs/06-contributing.md](docs/06-contributing.md).

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills
pip install -e .
make check
```

## Three zones

| Zone | Path | You change… |
| --- | --- | --- |
| **Skills** | `skills/<skill-id>/` | Workflows, references, eval prompts |
| **Registry** | `registry/` | Packs, collections, backlog |
| **Output** | `dist/` | Never by hand — run `make build` |

## Before opening a PR

1. `make check` passes
2. Skill changes include regenerated `dist/` in the same PR
3. Active skills have no `TODO` in `SKILL.md`

Optional local hook: `./scripts/install-git-hooks.sh`

## Docs

- [04 Authoring skills](docs/04-authoring-skills.md)
- [05 CLI reference](docs/05-skillctl-reference.md)
- [Registry README](registry/README.md)
