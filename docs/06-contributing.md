# Contributing

How to change this catalog and get PRs merged.

## Before you start

- **Consumers** (install only): [Getting started](01-getting-started.md) — no need to run full CI locally.
- **Contributors** (edit skills or tooling): Python 3.11+, `make`, Git.

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills
pip install -e .
make check
```

## What to change where

| Change | Edit | Regenerate |
| --- | --- | --- |
| Skill workflow | `skills/<id>/SKILL.md`, `references/`, `eval/prompt.md` | `make build` |
| Skill metadata | `skills/<id>/skill.yaml` | `make build` |
| Pack membership | `registry/packs/*.yaml` | `make build` |
| Collection membership | `registry/collections/*.yaml` | `make build` |
| Proposed future skills | `registry/skill-backlog.yaml` or taxonomy | `make backlog-generate` |
| Tooling | `tools/skillforge/` | `make test` |

## PR workflow

1. Create a branch from `main` / `master`.
2. Make changes under `skills/`, `registry/packs/`, `registry/collections/`, or `tools/`.
3. Run the full check locally:

```bash
make check
```

This runs: validate → backlog validate → tests → build → **`git diff --exit-code dist/`**.

4. Commit **source and `dist/` together** when skills changed.
5. Open a PR. CI runs the same checks on Ubuntu, macOS, and Windows (Python 3.11 and 3.12).

Optional — catch issues before commit:

```bash
./scripts/install-git-hooks.sh   # runs validate + backlog validate on git commit
```

## What is enforced automatically

| Rule | How | Blocks merge? |
| --- | --- | --- |
| Valid skill structure (`SKILL.md`, `skill.yaml`, refs, packs) | `skillctl validate --all` | Yes — CI |
| Backlog consistency | `skillctl backlog validate` | Yes — CI |
| Unit tests pass | `make test` | Yes — CI |
| `dist/` matches `make build` | `git diff --exit-code dist/` | Yes — CI |
| Active skills have no `TODO` in `SKILL.md` | `skillctl validate --all` | Yes — CI |
| Eval prompt exists | `skillctl validate --all` | Warn only |
| Unreferenced `references/*.md` | `skillctl validate --all` | Warn only |
| Active skill missing references | `skillctl validate --all` | Warn only |
| Conventional commit messages | — | No — review habit |
| Doc updates when behavior changes | — | No — review checklist |
| No AI attribution in commits/PRs | — | No — review |

GitHub PR template: [.github/pull_request_template.md](../.github/pull_request_template.md)

**Branch protection (repo settings):** require CI checks to pass before merge. That is the main gate for everything marked “Yes — CI” above.

## Commit rules

- **Always commit `dist/`** when skill content or metadata changes — CI verifies it matches `make build`.
- **Never edit `dist/` by hand** — it is overwritten on build.
- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
- Do not add AI tool attribution to commits or PR descriptions.

## Skill quality bar

Before setting `status: active`:

- [ ] `SKILL.md` has no `TODO` markers
- [ ] Frontmatter `description` says what + when
- [ ] At least one `references/*.md` when samples are needed
- [ ] `skill.yaml` has correct `modes`, `packs`, `targets`
- [ ] Eval prompt in `skills/<id>/eval/prompt.md` (recommended)
- [ ] `make check` passes

See [Authoring skills](04-authoring-skills.md) for details.

## Adding tests

Add tests under `tests/` for tooling changes:

```bash
make test
python3 -m unittest discover -s tests -v
```

New skill content does not require unit tests, but eval prompts help manual quality checks.

## Documentation

Update user docs when behavior changes:

| Change | Update |
| --- | --- |
| Install flow | [docs/02-install.md](02-install.md) |
| New pack | [docs/03-choosing-packs.md](03-choosing-packs.md), `registry/packs/*.yaml`, rebuild catalog |
| New planning-only skill | `tools/skillforge/modes.py`, `tests/test_modes.py`, `skill.yaml` modes |
| New CLI flag or command | [docs/05-skillctl-reference.md](05-skillctl-reference.md) |
| High-level overview | [README.md](../README.md) |

## CI

Workflow: `.github/workflows/ci.yml`

Steps per matrix job:

1. `pip install -e .`
2. `python -m unittest discover -s tests`
3. `skillctl validate --all`
4. `skillctl backlog validate`
5. `skillctl build --target all`
6. `git diff --exit-code dist`

If step 6 fails, run `make build` locally and commit `dist/`.

## Getting help

- Doc index: [docs/README.md](README.md)
- Architecture deep dives: [architecture/README.md](architecture/README.md)
