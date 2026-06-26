# CLI reference

Commands for **skillctl** and the **Makefile** wrapper.

Install skillctl:

```bash
pip install -e .    # from repo root
# or run directly:
./tools/skillctl ...
export PYTHONPATH=tools
```

## skillctl

Global option:

```bash
./tools/skillctl --root /path/to/agent-skills <command>
```

Defaults to current directory.

### Validate

```bash
./tools/skillctl validate --all
./tools/skillctl validate <skill-id>
./tools/skillctl backlog validate
```

### Build

```bash
./tools/skillctl build --target all
./tools/skillctl build --target cursor
./tools/skillctl build --target copilot
./tools/skillctl build --target codex
```

Build runs validation first; fails if skills are invalid.

### List

```bash
./tools/skillctl list --skills
./tools/skillctl list --collections
./tools/skillctl list --packs
make list-catalog    # summaries + dist/catalog/ file paths
```

### Install

```bash
./tools/skillctl install \
  --pack java-backend-pack \
  --target cursor \
  --dest /path/to/project

# Options:
#   --target cursor|copilot|codex   (default: cursor)
#   --include-draft                 include draft skills
#   --modes planning coding         filter by modes (subset match)
```

Requires `dist/` to exist (run `make build` first).

Helper script (recommended for consumers):

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
./scripts/install-from-clone.sh --help
```

### Backlog

```bash
./tools/skillctl backlog list
./tools/skillctl backlog list --priority P1 --domain java
./tools/skillctl backlog validate
./tools/skillctl backlog generate \
  --from registry/taxonomy.yaml \
  --out registry/skill-backlog.yaml \
  --merge
./tools/skillctl backlog promote <skill-id>
./tools/skillctl backlog promote --wave <wave-id>
./tools/skillctl backlog promote --all-waves
```

### Catalog

```bash
./tools/skillctl catalog                    # print active skills (text)
./tools/skillctl catalog --format json
./tools/skillctl catalog build --include-backlog
```

### Doctor

```bash
./tools/skillctl doctor
```

Checks repo layout and Python version.

---

## Makefile

Run from repo root. See all targets:

```bash
make help
```

| Target | Description |
| --- | --- |
| `make install` | `pip install -e .` (install skillctl) |
| `make doctor` | Check repo layout |
| `make validate` | Validate skills, collections, packs |
| `make validate-backlog` | Validate backlog |
| `make build` | Validate + build all vendor output |
| `make build-cursor` | Build Cursor output only |
| `make build-copilot` | Build Copilot output only |
| `make build-codex` | Build Codex output only |
| `make test` | Run unit tests |
| `make list-skills` | Active skill IDs only |
| `make list-catalog` | All active skills with summaries + `dist/catalog/` paths |
| `make catalog` | Print active skill catalog to terminal |
| `make catalog-build` | Build `dist/catalog/` reports |
| `make backlog-generate` | Generate backlog from taxonomy |
| `make backlog-promote-waves` | Generate backlog + promote all waves |
| `make install-pack PACK=... DEST=...` | Install one pack (Cursor) |
| `make install-all DEST=...` | Install all skills (Cursor) |
| `make check` | Full CI check locally |
| `make clean-dist` | Remove generated `dist/` output |

### Examples

```bash
make check
make install-pack PACK=java-backend-pack DEST=/path/to/project
make install-all DEST=/path/to/project
make catalog-build
```

---

## Environment

| Variable | Purpose |
| --- | --- |
| `PYTHONPATH=tools` | Run skillctl without pip install |
| `AGENT_SKILLS_ROOT` | Override repo root for `install-from-clone.sh` |
| `PYTHON` | Python binary for Makefile (default `python3`) |

---

## See also

- [Install guide](02-install.md)
- [Authoring skills](04-authoring-skills.md)
- [Contributing](06-contributing.md)
