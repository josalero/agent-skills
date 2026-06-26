# Authoring skills

Guide for **contributors** who add or edit skills in this repository.

Consumers who only install skills into their apps should read [Getting started](01-getting-started.md) instead.

## Repository zones

| Zone | Path | Purpose |
| --- | --- | --- |
| **Skills** | `skills/<skill-id>/` | Workflow, references, eval prompt |
| **Registry** | `registry/` | Packs, collections, backlog — see [registry/README.md](../registry/README.md) |
| **Output** | `dist/` | Generated vendor install files (never edit by hand) |

## Skill anatomy

Each skill is a folder under `skills/<skill-id>/`:

```text
skills/java-spring-boot-service/
  SKILL.md           # Agent workflow (frontmatter + body)
  skill.yaml         # Machine metadata
  references/        # Code samples, checklists, commands
  eval/
    prompt.md        # Realistic user prompt + expected behavior
  scripts/           # Optional helpers
  assets/            # Optional diagrams
```

| File | Purpose |
| --- | --- |
| `SKILL.md` | What the agent does. Keep concise. Frontmatter: `name`, `description`. |
| `skill.yaml` | Domain, kind, **modes**, status, packs, collections, targets. |
| `references/` | Detailed examples linked from `SKILL.md`. |
| `eval/prompt.md` | Quality check prompt for manual or future automated evals. |

Generated output lands in `dist/` for Cursor, Copilot, and Codex. **Do not edit `dist/` by hand.**

## Edit an existing skill

1. Change `skills/<skill-id>/SKILL.md` and/or `references/`.
2. Update `skill.yaml` only if metadata changed (summary, modes, packs, status).
3. Validate and rebuild:

```bash
make validate
./tools/skillctl validate java-spring-boot-service
make build
```

4. Commit **both** source and regenerated `dist/`.

## Add a new skill manually

### 1. Create the folder

Use lowercase letters, digits, and hyphens:

```bash
SKILL_ID=my-new-skill
mkdir -p skills/$SKILL_ID/references skills/$SKILL_ID/eval
cp templates/canonical-skill/SKILL.md skills/$SKILL_ID/SKILL.md
cp templates/canonical-skill/skill.yaml skills/$SKILL_ID/skill.yaml
```

### 2. Author `SKILL.md`

- Set frontmatter `name` to match the folder name.
- Write a strong `description`: **what** the skill does and **when** to use it.
- Body: workflow steps, checklist, output format.
- Link references:

```markdown
- Read `references/api-design.md` for controller and DTO patterns.
```

### 3. Fill in `skill.yaml`

Required fields:

- `id`, `display_name`, `domain`, `kind`, `modes`, `status`, `summary`
- `areas`, `tags`, `collections`, `packs`
- `targets` (`codex`, `cursor`, `copilot`)
- `owners`, `stability`

**modes** — when agents should use the skill:

| Mode | Use for |
| --- | --- |
| `planning` | Design, review, strategy, go/no-go |
| `coding` | Implement, refactor, write tests |
| Both | Workflows that plan then implement (migrations, hardening) |

Start new skills as `status: draft`. Set `active` when authored and reviewed.

### 4. Add eval prompt

Create `skills/$SKILL_ID/eval/prompt.md` with a realistic user request and expected agent behavior.

### 5. Register the skill

Add the skill ID to relevant files under `registry/`:

- `registry/collections/*.yaml`
- `registry/packs/*.yaml`

### 6. Validate, build, test

```bash
make check
```

## Propose a skill without implementing

Add a candidate to `registry/skill-backlog.yaml` with `status: proposed`, or regenerate from taxonomy:

```bash
make backlog-generate
make validate-backlog
./tools/skillctl backlog list
```

Proposed skills do not generate vendor output until promoted.

## Promote from backlog (draft scaffold)

```bash
./tools/skillctl backlog promote my-new-skill
# or promote a whole wave:
./tools/skillctl backlog promote --wave java-production-readiness
make backlog-promote-waves   # all waves
```

Promoted folders start with `status: draft`, `TODO` markers in `SKILL.md`, and a scaffold `eval/prompt.md`. Author content, then set `status: active` in `skill.yaml` and backlog.

## Scale the catalog (taxonomy + waves)

```bash
make backlog-generate      # merge registry/taxonomy.yaml → skill-backlog.yaml
make backlog-promote-waves # promote all waves to draft folders
make catalog-build         # dist/catalog/*.md reports
```

Catalog reports:

| Report | Path |
| --- | --- |
| Backlog | `dist/catalog/backlog.md` |
| Waves | `dist/catalog/waves.md` |
| Packs | `dist/catalog/packs.md` |
| Mode coverage | `dist/catalog/coverage-by-mode.md` |

## Skill structure rules (validation)

Validation fails if:

- Folder name ≠ `skill.yaml` id ≠ `SKILL.md` frontmatter `name`
- Required metadata missing (including `modes`)
- `references/*.md` not linked from `SKILL.md`
- Unknown pack or collection IDs in `registry/`
- No enabled target in `targets`
- Active skills contain `TODO` in `SKILL.md`

Run `./tools/skillctl validate --all` before opening a PR.

## See also

- [Contributing](06-contributing.md) — PR workflow and CI
- [CLI reference](05-skillctl-reference.md) — all commands
- [Registry README](../registry/README.md) — packs vs collections vs backlog
- [High-level architecture](architecture/02-high-level-architecture.md) — validation and build pipeline
