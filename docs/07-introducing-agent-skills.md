# Introducing agent-skills: a shared library for AI coding agents

**Audience:** Developers evaluating the repo, teams adopting Cursor/Codex/Copilot, and future contributors.

---

If you use Cursor, Codex, GitHub Copilot, or Claude Code, you have probably felt the same friction: every project reinvents how the agent should behave. One repo has a long `AGENTS.md` that nobody maintains. Another copies Spring Boot tips from a chat thread. A third disables rules because they conflict. The agent is capable — but the **instructions** are inconsistent, unreviewed, and trapped in individual codebases.

**agent-skills** is an open catalog that fixes that at the source. It is a version-controlled library of engineering **skills** — structured workflows with references and checklists — that you install into your projects as ordinary files. Agents read them locally. You review them in Git. You improve them once and reuse them everywhere.

Today the catalog ships **100 active skills** across Java, Kotlin, .NET, PHP, Rust, React, Angular, Vue, architecture review, quality gates, AI engineering, UX/UI, and technical writing, bundled into **16 install packs** for Cursor, Codex, Copilot, Claude Code, and OpenCode.

---

## What is a “skill”?

A skill is not a prompt dump. It is a small, focused package:

| Piece | Role |
| --- | --- |
| `SKILL.md` | The workflow: what to inspect, what order to work in, what to deliver |
| `skill.yaml` | Metadata: domain, planning vs coding mode, packs, agent targets |
| `references/` | Deep material — checklists, code patterns, commands — linked from the workflow |
| `eval/prompt.md` | A realistic scenario to sanity-check agent behavior (recommended) |

Example: `java-spring-boot-service` tells an agent how to build or review a REST vertical slice (DTOs, validation, transactions, tests). `java-quality-gates` tells it how to fix CI when Checkstyle or JaCoCo fails. `technical-documentation-authoring` tells it how to structure an RFC or ADR.

**AI architect skills** (planning mode) help before you write code: `llm-application-architecture` (RAG vs tools vs prompt-only, routing, memory), `ai-evaluation-architecture` (golden sets, metrics, CI gates), and `agent-orchestration-design` (multi-step agents, state, limits, human-in-the-loop). They ship in `ai-engineering-pack` and `architecture-review-pack`.

**UX/UI skills** complement framework accessibility skills: `ux-design-review` and `ui-design-system-review` for flows, heuristics, and design tokens; `frontend-ui-engineering` for semantic HTML, Tailwind, and responsive implementation. See `frontend-ux-ui-pack`.

Skills declare **modes**:

- **planning** — design, review, strategy (architecture review, migration planning, software design analysis)
- **coding** — implement, refactor, test (Spring Boot services, React components, quality gates)

That lets you install only what matches the work — for example, planning skills for design sessions and coding skills for feature branches.

---

## How it works: author once, install anywhere

The repository separates three concerns:

```text
skills/      ← you author workflows here (source of truth)
registry/    ← packs, collections, backlog (what lists and bundles skills)
dist/        ← generated output for Cursor, Copilot, Codex, Claude Code, OpenCode (never edit by hand)
```

**skillctl** (the CLI in `tools/`) validates skill structure, builds vendor-specific output, and installs packs into your project. Because **`dist/` is committed**, you can clone and install **without Python** — run the install script and copy files into your app.

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills

# Java backend into a Cursor project
./scripts/install-from-clone.sh \
  --dest /path/to/your-project \
  --pack java-backend-pack

# Codex or Copilot instead of Cursor
./scripts/install-from-clone.sh \
  --dest /path/to/your-project \
  --pack java-backend-pack \
  --target codex
```

**Packs** are curated bundles: `java-backend-pack`, `frontend-react-pack`, `architecture-review-pack`, `ai-engineering-pack`, `quality-gates-pack`, and others. See [Choosing packs](03-choosing-packs.md) for a stack picker, or run `./tools/skillctl catalog` / browse [active skills](../../dist/catalog/active-skills.md) after `make build`.

**Collections** (`java`, `backend`, `testing`, …) group skills for browsing in the catalog — they are not install units.

Nothing phones home at runtime. Skills are files on disk in your repo, same as your own rules.

---

## Who is this for?

**Application developers** who want consistent agent behavior on recurring tasks — Spring Boot APIs, React testing, security review, migrations — without authoring everything from scratch.

**Tech leads and architects** who want reviewable, shared standards: planning skills for design, quality-gate skills for CI, documentation skills for RFCs and ADRs.

**Maintainers** who treat agent instructions as engineering infrastructure: validated structure, CI, and a clear promotion path for new skills.

---

## Contributing: help the catalog grow

You do not need to understand the entire toolchain to fix a typo in a workflow. You *do* need `make check` to pass before a PR merges. Here is the mental model.

### Three zones — edit the right folder

| Zone | Path | You change… |
| --- | --- | --- |
| **Skills** | `skills/<skill-id>/` | Workflows, references, eval prompts |
| **Registry** | `registry/` | Pack/collection membership, backlog |
| **Output** | `dist/` | Nothing by hand — run `make build` |

If you change a skill, you **regenerate and commit `dist/`** in the same PR. CI fails if generated output is stale.

### Local setup (contributors)

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills
pip install -e .          # optional; or use ./tools/skillctl directly
make check                # validate, test, build, verify dist/
```

Optional pre-commit hook:

```bash
./scripts/install-git-hooks.sh
```

Full details: [Contributing](06-contributing.md).

### Ways to contribute

**1. Improve an existing skill**

- Clarify a workflow step in `SKILL.md`
- Add a reference with a concrete example
- Fix outdated commands or version guidance

Run `make validate`, then `make build`, commit source + `dist/`.

**2. Add a new skill**

- Copy `templates/canonical-skill/` into `skills/<skill-id>/`
- Fill in `SKILL.md`, `skill.yaml`, `references/`, and `eval/prompt.md`
- Register the ID in `registry/packs/` and `registry/collections/` as appropriate
- Start as `status: draft` while authoring; set `active` when ready — **no `TODO` in active skills**

Guide: [Authoring skills](04-authoring-skills.md).

**3. Propose a skill without implementing yet**

Add an entry to `registry/skill-backlog.yaml` or use taxonomy generation:

```bash
make backlog-generate
./tools/skillctl backlog promote <skill-id>   # scaffolds a draft folder
```

**4. Extend packs or tooling**

- New pack: `registry/packs/*.yaml` + docs in [Choosing packs](03-choosing-packs.md)
- CLI or validation: `tools/skillforge/` + tests under `tests/`

### Quality bar (what CI enforces)

Before a skill is **active**:

- Folder name, `skill.yaml` id, and `SKILL.md` frontmatter `name` must match
- Required metadata including **modes**, packs, collections, targets
- References linked from `SKILL.md` must exist
- **No `TODO`** in `SKILL.md` for active skills
- `make check` passes on Ubuntu, macOS, and Windows

Eval prompts are recommended; missing evals warn but do not block merge.

### PR checklist

1. Branch from `main` / `master`
2. `make check` green locally
3. Source + `dist/` in the same commit when skills changed
4. Conventional commit message (`feat:`, `fix:`, `docs:`)
5. Update user docs if install behavior or packs changed

AI agents editing this repo should read [AGENTS.md](../../AGENTS.md). Product context lives in the [BRD](architecture/01-brd.md) and [high-level architecture](architecture/02-high-level-architecture.md).

---

## A sustainable model

The catalog is designed to scale without becoming shallow:

- **Backlog** can list many proposed skills
- **Draft** folders can be scaffolded automatically
- **Active** skills require intentional, reviewed workflows

Bulk generation is fine for backlog and drafts. Marking something **active** means you trust it in production agent sessions.

That balance — breadth in planning, depth in active skills — is what makes the library useful instead of noisy.

---

## Where to go next

| Goal | Start here |
| --- | --- |
| Install skills into my project | [Getting started](01-getting-started.md) → [Install guide](02-install.md) |
| Pick a pack for my stack | [Choosing packs](03-choosing-packs.md) |
| Suggest packs from my repo | `./tools/skillctl recommend --dest /path/to/project` |
| List or search skills in the terminal | [CLI reference — Discover](05-skillctl-reference.md#discover-skills-and-packs) |
| Add or edit a skill | [Authoring skills](04-authoring-skills.md) |
| Look up CLI commands | [CLI reference](05-skillctl-reference.md) |
| Contribute a PR | [Contributing](06-contributing.md) |
| Browse every skill | [dist/catalog/active-skills.md](../../dist/catalog/active-skills.md) |

---

## Try it in five minutes

```bash
git clone git@github.com:josalero/agent-skills.git
cd agent-skills
./scripts/install-from-clone.sh --dest /path/to/your-project --pack architecture-review-pack
```

Open your project in Cursor (or your agent of choice), ask for an architecture or API design review, and notice whether the agent follows a structured workflow instead of generic advice.

If something was wrong or missing — **that is a contribution waiting to happen.**

**Shorter narrative (same voice as [AI Broke Your Definition of Done](https://my-tech-profile.dev/insights/ai-broke-your-definition-of-done)):** see the overview sections above, or share [07-introducing-agent-skills.md](07-introducing-agent-skills.md) directly.

---

*agent-skills is built for teams who treat AI agents as part of the engineering toolchain, not as a black box. Clone it, install what you need, and send PRs for what you wish existed.*
