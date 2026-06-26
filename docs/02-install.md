# Install guide

Install generated skills from a local **agent-skills** clone into your project or user config.

> **Important:** Cursor and Codex do not pull skills from a GitHub URL at runtime. You copy local files from `dist/` (or use `skillctl` / the install script).

## Prerequisites

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills
```

Optional: `pip install -e .` to get `skillctl` on your PATH.

If `dist/` is missing (e.g. you are on a dev branch), run `make build` or pass `--build` to the install script.

## Where files go

| Agent | Installed paths in your project |
| --- | --- |
| **Cursor** | `.cursor/skills/<id>/` and `.cursor/rules/<id>.mdc` |
| **Codex** | `skills/<id>/` and optional `AGENTS.md` |
| **Copilot** | `.github/skills/<id>/` and `.github/instructions/<id>.instructions.md` |

The skill **bundle** (`SKILL.md` + `references/`) is the source of truth. Cursor rules and Copilot instruction files are thin routers that point to the bundle.

---

## Recommended: install script

```bash
# One pack → Cursor (most common)
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack

# All 55 active skills → Cursor
./scripts/install-from-clone.sh --dest /path/to/project

# All skills → Codex layout
./scripts/install-from-clone.sh --dest /path/to/project --target codex

# All skills → Copilot layout
./scripts/install-from-clone.sh --dest /path/to/project --target copilot

# Planning skills only (skips coding-only skills in the pack)
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack --modes planning

# Cursor user-wide (every project on this machine)
./scripts/install-from-clone.sh --user --pack architecture-review-pack

# Clone lives elsewhere
AGENT_SKILLS_ROOT=/path/to/agent-skills \
  ./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
```

If `dist/` is missing: add `--build`.

List packs: `./tools/skillctl list --packs`

---

## Cursor

### One pack

```bash
./tools/skillctl install --pack java-backend-pack --target cursor --dest /path/to/project
```

Or via Makefile (from repo root):

```bash
make install-pack PACK=java-backend-pack DEST=/path/to/project
```

### All skills

```bash
make install-all DEST=/path/to/project
# equivalent:
cp -R dist/cursor/.cursor /path/to/project/.cursor
```

### User-wide install

Installs to `~/.cursor/` so every Cursor workspace can use the skills:

```bash
./scripts/install-from-clone.sh --user --pack frontend-react-pack
```

Prefer **project `.cursor/`** when you want skills versioned with the codebase.

### Filter by mode

```bash
./tools/skillctl install \
  --pack java-backend-pack \
  --target cursor \
  --dest /path/to/project \
  --modes planning
```

See [dist/catalog/coverage-by-mode.md](../dist/catalog/coverage-by-mode.md) for which skills support each mode.

---

## Codex

```bash
./scripts/install-from-clone.sh --dest /path/to/project --target codex
```

Manual copy:

```bash
cp -R dist/codex/skills /path/to/project/skills
cp dist/codex/AGENTS.md /path/to/project/AGENTS.md
```

---

## Copilot

```bash
./scripts/install-from-clone.sh --dest /path/to/project --target copilot
```

Manual copy:

```bash
cp -R dist/copilot/.github /path/to/project/.github
```

---

## Teams

Install once, commit with the application repo:

```bash
cd /path/to/your-project
# after install...
git add .cursor/              # Cursor
# git add skills/ AGENTS.md   # Codex
# git add .github/            # Copilot
git commit -m "chore: add agent skills from agent-skills"
```

Teammates get skills on `git pull`. They do not need the agent-skills clone for day-to-day work.

---

## Pin catalog version (submodule)

```bash
cd /path/to/your-project
git submodule add git@github.com:josalero/agent-skills.git vendor/agent-skills
./vendor/agent-skills/scripts/install-from-clone.sh --dest . --pack java-backend-pack
git add .cursor/ vendor/agent-skills .gitmodules
git commit -m "chore: pin agent-skills submodule and install Java pack"
```

Update later:

```bash
git submodule update --remote vendor/agent-skills
./vendor/agent-skills/scripts/install-from-clone.sh --dest . --pack java-backend-pack
```

---

## Update installed skills

```bash
cd /path/to/agent-skills
git pull
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
```

Re-commit changes in the app repo if files under `.cursor/` (or `skills/`) changed.

---

## Install all packs via loop

Same result as installing everything; useful if you want `skillctl` logging per pack:

```bash
DEST=/path/to/project
for pack in $(./tools/skillctl list --packs); do
  ./tools/skillctl install --pack "$pack" --target cursor --dest "$DEST"
done
```

Skills in multiple packs are overwritten, not duplicated.

---

## Not supported yet

- Remote install URL (`skillctl install --repo https://...`)
- Live GitHub sync without copying files into the project

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `dist/ output not found` | Run `make build` in the clone or use `--build` on the install script |
| Unknown pack | `./tools/skillctl list --packs` |
| Skills not appearing in Cursor | Confirm `.cursor/skills/<id>/SKILL.md` exists; restart Cursor or reopen workspace |
| CI fails on dist | Commit regenerated `dist/` after skill changes |

---

## See also

- [Getting started](01-getting-started.md)
- [Choosing packs](03-choosing-packs.md)
- [CLI reference](05-skillctl-reference.md)
