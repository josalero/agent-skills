# Registry

Everything that **lists, groups, or plans** skills lives here. Skill workflows themselves live under `skills/<skill-id>/`.

| Path | Purpose | Edit when… |
| --- | --- | --- |
| [packs/](packs/) | Install bundles (`java-backend-pack`, …) | Registering which skills ship together |
| [collections/](collections/) | Browse/group labels (`java`, `backend`, …) | Adding a skill to a catalog view |
| [skill-backlog.yaml](skill-backlog.yaml) | Planned and promoted skills with status | Proposing or tracking skill lifecycle |
| [taxonomy.yaml](taxonomy.yaml) | Source definitions for backlog generation | Adding new skill types at scale (maintainers) |
| [waves.yaml](waves.yaml) | Promotion waves for draft scaffolding | Batch-promoting groups of skills |

## Contributor checklist (new skill)

1. Create `skills/<skill-id>/` with `SKILL.md`, `skill.yaml`, `references/`, and `eval/prompt.md`
2. Add the skill ID to relevant files under `registry/packs/` and `registry/collections/`
3. Set `status: active` in `skill.yaml` and sync `registry/skill-backlog.yaml` if listed there
4. Run `make check` and commit `skills/`, `registry/`, and regenerated `dist/`

## Commands

```bash
./tools/skillctl list --packs
./tools/skillctl list --collections
./tools/skillctl backlog list
make backlog-generate    # merge taxonomy → skill-backlog.yaml
```

See [docs/04-authoring-skills.md](../docs/04-authoring-skills.md) for the full authoring guide.
