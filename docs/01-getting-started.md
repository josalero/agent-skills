# Getting started

This guide is for developers who want to **use** skills in their own projects. You do not need to understand the full catalog tooling to get value from this repo.

## What is this repo?

**agent-skills** is a library of engineering skills — structured instructions that AI coding agents (Cursor, Codex, Copilot, Claude Code, OpenCode) follow when you work on specific tasks.

Each skill includes:

- A **workflow** (what steps the agent should take)
- **References** (code samples, checklists, commands)
- **Metadata** (domain, planning vs coding mode, which agents support it)

Skills are **installed as files** into your project. Agents read those files locally; they do not fetch skills from GitHub at runtime.

## Key concepts

| Term | Meaning |
| --- | --- |
| **Skill** | One focused capability, e.g. `java-spring-boot-service` |
| **Pack** | A bundle of related skills you install together, e.g. `java-backend-pack` |
| **Collection** | A technology or cross-stack browse label in the catalog (`java`, `react`, `architecture`) — not an install unit |
| **dist/** | Generated, agent-ready output. **Install from here**, not from `skills/` directly |
| **modes** | When to use a skill: `planning` (design/review) or `coding` (implement/test), or both |

## What you need

| Task | Requirements |
| --- | --- |
| Install skills into a project | Git + this repo cloned (or submodule) |
| Rebuild after editing skills | Python 3.11+, `make` |

If you cloned a release that includes `dist/`, you can install immediately without running `make build`.

## Your first install (Cursor + Java)

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills

./scripts/install-from-clone.sh \
  --dest /path/to/your-java-project \
  --pack java-backend-pack
```

This copies into your project:

```text
your-java-project/
  .cursor/
    skills/          # full skill bundles
    rules/           # thin routers that point agents to each skill
```

Open the project in Cursor. When your task matches a skill description (Spring Boot API, tests, migration, etc.), Cursor can apply that skill's workflow.

## Browse skills and packs

You do not need to read every skill file to pick a pack. Use the CLI or generated catalog:

```bash
./tools/skillctl list --packs         # install bundle IDs
./tools/skillctl list --skills        # all active skill IDs
./tools/skillctl catalog              # id + one-line summary
./tools/skillctl catalog --format json   # machine-readable (scripts, IDE)
make list-catalog                     # summaries + paths to dist/catalog/
```

After `make build`, the full catalog lives in **`dist/catalog/`**:

| File | Best for |
| --- | --- |
| [active-skills.md](../dist/catalog/active-skills.md) | Reading in GitHub or an editor |
| [skills.json](../dist/catalog/skills.json) | Scripts and tooling |
| [packs.md](../dist/catalog/packs.md) | Skills grouped by install pack |
| [coverage-by-mode.md](../dist/catalog/coverage-by-mode.md) | Planning vs coding skills |

Regenerate catalog reports only (no full vendor build):

```bash
make catalog-build
```

**Suggest packs for your app repo:**

```bash
./tools/skillctl recommend --dest /path/to/your-project
make recommend DEST=/path/to/your-project
```

**AI / architecture planning example:** install `architecture-review-pack` with `--modes planning` for skills such as `llm-application-architecture`, `ai-evaluation-architecture`, and `agent-orchestration-design`. See [Choosing packs](03-choosing-packs.md).

## Pick a different stack?

See [Choosing packs](03-choosing-packs.md) for pack IDs and skill lists.

## Other agents

| Agent | Install doc section |
| --- | --- |
| Codex | [Install guide — Codex](02-install.md#codex) |
| GitHub Copilot | [Install guide — Copilot](02-install.md#copilot) |
| Claude Code | [Install guide — Claude Code](02-install.md#claude-code) |
| OpenCode | [Install guide — OpenCode](02-install.md#opencode) |

## Team workflow

1. One person installs skills into the app repo.
2. Commit `.cursor/` (or `skills/` for Codex, `.claude/` for Claude Code, `.opencode/` for OpenCode) with the application code.
3. Teammates get skills when they `git pull` — no separate clone required for daily work.

Details: [Install guide — Teams](02-install.md#teams).

## Updating skills later

```bash
cd /path/to/agent-skills
git pull
./scripts/install-from-clone.sh --dest /path/to/your-project --pack java-backend-pack
```

Re-commit changed files in the app repo if needed.

## Next steps

- [Install guide](02-install.md) — all targets, all packs, user-wide Cursor install
- [Choosing packs](03-choosing-packs.md) — which pack for your stack
- [Authoring skills](04-authoring-skills.md) — only if you contribute to this catalog
