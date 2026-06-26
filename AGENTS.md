# Agent instructions — agent-skills repository

Rules for AI agents editing this catalog.

## Layout

```text
skills/<skill-id>/     Canonical skill source (edit here)
  SKILL.md
  skill.yaml
  references/
  eval/prompt.md
registry/              Packs, collections, backlog (register skills here)
dist/                  Generated output — do not edit by hand
tools/skillforge/      skillctl implementation
```

## When editing skills

1. Change `skills/<skill-id>/` only for skill content
2. Update `registry/packs/` and `registry/collections/` when registering membership
3. Run `make validate` or `make check` before finishing
4. Run `make build` and include `dist/` changes when skill source changed
5. Never set `status: active` while `SKILL.md` contains `TODO`

## When adding a skill

Copy `templates/canonical-skill/`, fill in `skills/<id>/`, register in `registry/`, add `eval/prompt.md`.

## Commands

```bash
make check
./tools/skillctl validate --all
./tools/skillctl validate <skill-id>
make build
```

Human docs: [docs/README.md](docs/README.md)
