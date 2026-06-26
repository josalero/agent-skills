# Documentation index

Number prefixes define the recommended reading order within each section.

```text
docs/
  README.md                 ← you are here
  01-getting-started.md
  02-install.md
  03-choosing-packs.md
  04-authoring-skills.md
  05-skillctl-reference.md
  06-contributing.md
  architecture/
    README.md
    01-brd.md
    02-high-level-architecture.md

registry/                     ← packs, collections, backlog (see registry/README.md)
  README.md
  packs/
  collections/
  skill-backlog.yaml
```

## Install skills (consumers)

Read in order:

| # | Doc | What you'll learn |
| --- | --- | --- |
| 1 | [Getting started](01-getting-started.md) | Concepts, first install, glossary |
| 2 | [Install guide](02-install.md) | Cursor, Codex, Copilot, teams, updates |
| 3 | [Choosing packs](03-choosing-packs.md) | Which pack matches your stack *(optional)* |

## Maintain this catalog (contributors)

Read in order:

| # | Doc | What you'll learn |
| --- | --- | --- |
| 4 | [Authoring skills](04-authoring-skills.md) | Create, edit, promote, activate skills |
| 5 | [CLI reference](05-skillctl-reference.md) | All `skillctl` and `make` commands |
| 6 | [Contributing](06-contributing.md) | PR workflow, CI, what to commit |

## Generated catalog reports

After `make build`, browse under `dist/catalog/`:

| Report | Path |
| --- | --- |
| All packs (with skill lists) | [dist/catalog/packs.md](../dist/catalog/packs.md) |
| Active skills | [dist/catalog/active-skills.md](../dist/catalog/active-skills.md) |
| Coverage by mode (planning / coding) | [dist/catalog/coverage-by-mode.md](../dist/catalog/coverage-by-mode.md) |
| Coverage by domain | [dist/catalog/coverage-by-domain.md](../dist/catalog/coverage-by-domain.md) |
| Machine-readable catalog | [dist/catalog/skills.json](../dist/catalog/skills.json) |

## Architecture (maintainers)

| Doc | Topic |
| --- | --- |
| [BRD](architecture/01-brd.md) | Goals, user stories, acceptance criteria |
| [High-level architecture](architecture/02-high-level-architecture.md) | System design (as-built) |

Index: **[architecture/README.md](architecture/README.md)**

## Quick links

```bash
make list-catalog                      # all skills + dist/catalog paths
./tools/skillctl list --packs          # pack IDs
./tools/skillctl list --skills         # skill IDs only
./scripts/install-from-clone.sh --help # install helper
make help                              # Makefile targets
```
