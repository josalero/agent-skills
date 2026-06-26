# Business Requirements Document — agent-skills

**Product:** Cross-agent engineering skill library  
**Repository:** agent-skills  
**Status:** As-built (living document)  
**Last updated:** June 2026

---

## 1. Executive summary

**agent-skills** is a version-controlled library of engineering skills for AI coding agents (Cursor, Codex, GitHub Copilot). Each skill is a structured workflow with references and optional eval prompts. Skills are authored once under `skills/`, validated by tooling, and rendered into installable bundles under `dist/`.

The product serves two audiences:

1. **Consumers** — developers who install skills into application repositories.
2. **Contributors** — maintainers who extend the catalog, registry, and tooling.

---

## 2. Problem statement

Engineering teams using multiple AI agents lack a **single, reviewable source of truth** for how agents should behave on recurring tasks (Spring Boot services, security review, migrations, frontend performance, and similar). Ad-hoc prompts and copy-pasted rules:

- Drift across projects and agent products
- Are hard to validate, version, or test
- Mix planning and implementation guidance inconsistently
- Do not compose into stack-specific install bundles

---

## 3. Goals

| # | Goal |
| --- | --- |
| G1 | Provide **reusable, high-quality skills** for common engineering workflows across Java, .NET, PHP, React, Angular, architecture, and AI engineering |
| G2 | Support **multiple agent runtimes** from one canonical skill source (Codex, Cursor, Copilot) |
| G3 | Enable **pack-based installation** so teams install only what matches their stack |
| G4 | Enforce **structural and quality gates** before skills ship (validation, CI, no TODOs on active skills) |
| G5 | Scale the catalog through **registry-driven planning** (backlog, taxonomy, waves) without auto-activating shallow content |
| G6 | Keep consumer onboarding **simple** — clone repo, install from `dist/`, no Python required when `dist/` is committed |

## 4. Non-goals

| # | Non-goal |
| --- | --- |
| NG1 | Runtime skill fetching from GitHub inside agent products |
| NG2 | Auto-generating hundreds of **active** skills without human-authored workflows |
| NG3 | Supporting every agent platform in v1 (Claude Code, Antigravity, OpenAI API bundles, npm/dotnet global tools are out of scope today) |
| NG4 | Hosting or executing agent workloads — this repo ships **files**, not a service |
| NG5 | Replacing project-specific `.cursor/rules` or team standards — skills **augment** them |

---

## 5. Stakeholders and personas

| Persona | Role | Primary need |
| --- | --- | --- |
| **Application developer** | Installs skills into a service repo | Correct pack, minimal setup, agents follow consistent workflows |
| **Tech lead / architect** | Chooses packs and reviews skill quality | Coverage by domain/mode, trust in validation and ownership |
| **Skill author** | Adds or edits skills | Clear authoring rules, fast validate/build loop |
| **Catalog maintainer** | Manages packs, collections, backlog | Registry tools, promotion flow, CI safety |
| **AI agent (Cursor/Codex/Copilot)** | Reads installed skill files | Concise routing + deep references when triggered |

---

## 6. User stories

### 6.1 Consumers

| ID | Story | Priority |
| --- | --- | --- |
| US-C1 | As a developer, I want to **install a stack-specific pack** into my project so agents use vetted workflows without authoring skills myself. | Must |
| US-C2 | As a developer, I want to **install for Cursor, Codex, or Copilot** so I can use my preferred agent. | Must |
| US-C3 | As a developer, I want to **browse active skills and packs** so I know what I am installing. | Must |
| US-C4 | As a developer, I want to **install without running Python** when the clone includes `dist/`. | Should |
| US-C5 | As a developer, I want to **filter by planning vs coding modes** when installing so review skills do not clutter implementation work. | Should |

### 6.2 Contributors

| ID | Story | Priority |
| --- | --- | --- |
| US-A1 | As an author, I want to **create a skill in one folder** (`SKILL.md`, `skill.yaml`, references, eval) so all agents share one source. | Must |
| US-A2 | As an author, I want **`skillctl validate`** to catch broken metadata, orphan references, and pack/collection mismatches before merge. | Must |
| US-A3 | As an author, I want **`make build`** to regenerate `dist/` so consumers get consistent vendor output. | Must |
| US-A4 | As an author, I want to **register a skill in packs and collections** so it appears in the right install bundles and catalog views. | Must |
| US-A5 | As a maintainer, I want to **propose and promote skills via backlog** so the catalog can grow without creating empty active folders. | Should |
| US-A6 | As a maintainer, I want **CI to fail** on validation errors, stale `dist/`, or TODO markers in active skills. | Must |

### 6.3 Agents (indirect)

| ID | Story | Priority |
| --- | --- | --- |
| US-G1 | As an agent, when a skill applies, I want a **clear workflow and linked references** so I inspect, implement, and verify in order. | Must |
| US-G2 | As an agent, I want **thin routing rules** (Cursor) that point to full skill bundles so context stays manageable. | Should |

---

## 7. Functional requirements

### 7.1 Skill content

| ID | Requirement |
| --- | --- |
| FR-1 | Each skill lives under `skills/<skill-id>/` with `SKILL.md`, `skill.yaml`, and optional `references/`, `scripts/`, `assets/`. |
| FR-2 | Each skill declares **modes**: `planning`, `coding`, or both. |
| FR-3 | Each active skill should have `eval/prompt.md` for quality checks (warning if missing). |
| FR-4 | Active skills must not contain `TODO` in `SKILL.md`. |
| FR-5 | Folder name, `skill.yaml` id, and `SKILL.md` frontmatter `name` must match. |

### 7.2 Registry

| ID | Requirement |
| --- | --- |
| FR-6 | **Packs** (`registry/packs/`) define install bundles. |
| FR-7 | **Collections** (`registry/collections/`) group skills for browsing. |
| FR-8 | **Backlog** (`registry/skill-backlog.yaml`) tracks lifecycle: proposed → draft → active. |
| FR-9 | Taxonomy and waves support bulk backlog generation and wave promotion. |

### 7.3 Tooling (`skillctl`)

| ID | Requirement |
| --- | --- |
| FR-10 | `validate --all` validates skills, collections, packs, and backlog. |
| FR-11 | `build --target {codex,cursor,copilot,all}` renders vendor output after validation. |
| FR-12 | `install` copies generated output into a target project (pack, target, optional mode filter). |
| FR-13 | `backlog list|validate|generate|promote` supports catalog scale workflows. |
| FR-14 | `catalog build` generates human- and machine-readable reports under `dist/catalog/`. |

### 7.4 Installation

| ID | Requirement |
| --- | --- |
| FR-15 | `scripts/install-from-clone.sh` installs from a local clone without requiring pip install. |
| FR-16 | Committed `dist/` allows consumers to install immediately after clone. |

---

## 8. Non-functional requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-1 | Validation completes on full catalog in reasonable time for local dev | < 30s typical |
| NFR-2 | Build output is **deterministic** — rebuild with no source changes produces no diff | Enforced in CI |
| NFR-3 | Tooling runs on Python **3.11+** | CI matrix 3.11–3.12 |
| NFR-4 | Cross-platform CLI entry points | `skillctl`, `.cmd`, `.ps1` |
| NFR-5 | Skills are **reviewable text** — no opaque binaries in skill source | Policy |
| NFR-6 | Generated files carry headers indicating skillctl origin | Implemented |
| NFR-7 | Repository documents consumer vs contributor paths clearly | README + docs/01–06 |

---

## 9. Expectations

### 9.1 Quality bar for active skills

- Workflow steps are **actionable** (inspect → implement → verify), not generic advice.
- `description` frontmatter states **what** and **when** to use the skill.
- References hold depth; `SKILL.md` stays concise and links to them.
- Skills declare accurate **domain**, **areas**, **tags**, **packs**, and **targets**.

### 9.2 Catalog growth

- Backlog may be broad; **active** status requires intentional authoring and review.
- Promotion scaffolds start as **draft** with TODO markers; activation removes TODOs and passes validation.
- Pack membership is explicit — skills are not silently included in installs.

### 9.3 Consumer experience

- Install docs explain Cursor vs Codex vs Copilot layout differences.
- Pack picker doc maps stacks to pack IDs.
- Updates require re-clone or rebuild + reinstall — no auto-update channel in v1.

---

## 10. Acceptance criteria (release / ongoing)

The product meets requirements when all of the following hold:

| # | Criterion | Verification |
| --- | --- | --- |
| AC-1 | **≥ 50 active skills** covering agreed domains | `make list-skills` / `dist/catalog/active-skills.md` |
| AC-2 | **≥ 8 install packs** with documented stack mapping | `skillctl list --packs`, `docs/03-choosing-packs.md` |
| AC-3 | Every active skill validates with **`skillctl validate --all`** | CI + local `make validate` |
| AC-4 | **`make check`** passes: validate, backlog validate, test, build, dist diff | CI workflow |
| AC-5 | Codex, Cursor, and Copilot outputs generate for all target-enabled active skills | `make build` |
| AC-6 | No active skill contains **`TODO`** in `SKILL.md` | Validator error |
| AC-7 | Every active skill has **`modes`** declared | Validator + `test_modes.py` |
| AC-8 | Install script works for **pack** and **all skills** targets | `scripts/install-from-clone.sh --help`, install tests |
| AC-9 | **`dist/` is committed** and matches `make build` | `git diff --exit-code dist/` in CI |
| AC-10 | Consumer can install **without Python** when `dist/` present | Documented in `docs/02-install.md` |

**Current as-built status (June 2026):** AC-1 through AC-10 are met (65 active skills, 11 packs).

---

## 11. Success metrics (recommended)

| Metric | Purpose |
| --- | --- |
| Active skill count by domain | Coverage visibility (`dist/catalog/coverage-by-domain.md`) |
| Planning vs coding coverage | Mode balance (`dist/catalog/coverage-by-mode.md`) |
| Validation failure rate in CI | Catalog health |
| Time to add a new skill (author report) | Contributor experience |
| Install script usage / feedback | Consumer adoption |

---

## 12. Future considerations (not committed)

- Automated eval execution against fixtures (today: eval prompts are manual/future CI)
- Additional vendor adapters beyond Codex, Cursor, Copilot
- Versioned skill releases on a registry (npm/Maven-style distribution)
- Organization-specific pack overlays or private forks
- Skill routing evals (does the agent pick the right skill?)

---

## 13. Related documents

| Document | Purpose |
| --- | --- |
| [High-level architecture](02-high-level-architecture.md) | System structure, pipelines, components |
| [Authoring skills](../04-authoring-skills.md) | How to create and edit skills |
| [CLI reference](../05-skillctl-reference.md) | Commands and Makefile targets |
| [Contributing](../06-contributing.md) | PR workflow and enforcement |
