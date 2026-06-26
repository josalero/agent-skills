# agent-skills

Engineering skills for AI coding agents — **Cursor**, **Codex**, and **GitHub Copilot**.

Each skill is a focused workflow (Spring Boot services, React performance, security review, migrations, and more) with references and checklists. Install them as files into your project; agents read them locally.

| | |
| --- | --- |
| **65** active skills | Java, .NET, PHP, React, Angular, architecture, AI engineering |
| **11** install packs | Stack bundles + quality gates — see [Choosing packs](docs/03-choosing-packs.md) |
| **3** agent targets | Cursor, Codex, Copilot (generated under `dist/`) |

---

## Use skills in your project

**You need:** Git and a clone of this repo (Python not required if `dist/` is present).

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills

# One pack (e.g. Java backend)
./scripts/install-from-clone.sh --dest /path/to/your-project --pack java-backend-pack

# All skills
./scripts/install-from-clone.sh --dest /path/to/your-project

# Codex or Copilot instead of Cursor
./scripts/install-from-clone.sh --dest /path/to/your-project --pack java-backend-pack --target codex
```

**Next steps**

| Step | Doc |
| --- | --- |
| Concepts and glossary | [Getting started](docs/01-getting-started.md) |
| Cursor, Codex, Copilot, teams | [Install guide](docs/02-install.md) |
| Which pack fits your stack | [Choosing packs](docs/03-choosing-packs.md) |
| Browse every skill | [dist/catalog/active-skills.md](dist/catalog/active-skills.md) or `make list-catalog` |

List pack IDs: `./tools/skillctl list --packs`

---

## Contribute to this catalog

**You need:** Python 3.11+, `make`, Git.

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills
pip install -e .    # optional — or use ./tools/skillctl directly
make check          # validate, test, build, verify dist/ is committed
```

| Task | Where to start |
| --- | --- |
| Add or edit a skill | [Authoring skills](docs/04-authoring-skills.md) |
| CLI and Makefile commands | [CLI reference](docs/05-skillctl-reference.md) |
| PR workflow and CI | [Contributing](docs/06-contributing.md) · [CONTRIBUTING.md](CONTRIBUTING.md) |
| Rules for AI agents | [AGENTS.md](AGENTS.md) |
| Design and architecture | [BRD](docs/architecture/01-brd.md) · [HLA](docs/architecture/02-high-level-architecture.md) |

**Three zones** — edit the right folder:

| Zone | Path | You change… |
| --- | --- | --- |
| Skills | `skills/<skill-id>/` | Workflows, references, `eval/prompt.md` |
| Registry | `registry/` | Packs, collections, backlog — [registry/README.md](registry/README.md) |
| Output | `dist/` | Never by hand — run `make build` |

---

## Repository layout

```text
skills/           Canonical skill source (author here)
registry/         Packs, collections, backlog YAML
dist/             Generated Cursor / Copilot / Codex output (committed)
tools/skillforge/ skillctl CLI
scripts/          install-from-clone.sh, git hooks
docs/             Numbered guides (01–06) + architecture/
```

Full doc index: **[docs/README.md](docs/README.md)**
