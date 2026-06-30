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
  07-introducing-agent-skills.md   ← repo overview & contribution story (article)
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
| 1 | [Getting started](01-getting-started.md) | Concepts, first install, browse skills & packs |
| 2 | [Install guide](02-install.md) | Cursor, Codex, Copilot, Claude Code, teams, updates |
| 3 | [Choosing packs](03-choosing-packs.md) | Which pack matches your stack *(optional)* |
| — | [CLI reference — Recommend](05-skillctl-reference.md#recommend) | Auto-suggest packs from your repo |
| — | [CLI reference — Discover](05-skillctl-reference.md#discover-skills-and-packs) | `skillctl list`, `skillctl catalog`, `make list-catalog` |

## Maintain this catalog (contributors)

Read in order:

| # | Doc | What you'll learn |
| --- | --- | --- |
| 4 | [Authoring skills](04-authoring-skills.md) | Create, edit, promote, activate skills |
| 5 | [CLI reference](05-skillctl-reference.md) | All `skillctl` and `make` commands |
| 6 | [Contributing](06-contributing.md) | PR workflow, CI, what to commit |
| — | [Introducing agent-skills](07-introducing-agent-skills.md) | Overview article: what it is, how to use & contribute |

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
./tools/skillctl recommend --dest /path/to/project   # suggest packs from repo signals
./tools/skillctl list --packs          # pack IDs
./tools/skillctl list --skills         # skill IDs only
./tools/skillctl catalog               # id + summary (terminal)
./tools/skillctl catalog --format json # machine-readable catalog
./scripts/install-from-clone.sh --help # install helper
make help                              # Makefile targets
```

**AI architect / LLM planning skills** (planning mode): `llm-application-architecture`, `ai-evaluation-architecture`, `agent-orchestration-design` — in `architecture-review-pack`. See [Choosing packs](03-choosing-packs.md).

**UX/UI skills:** `ux-design-review`, `ui-design-system-review`, `frontend-ui-engineering` — planning review skills in `architecture-review-pack`; implementation in each frontend technology pack.
