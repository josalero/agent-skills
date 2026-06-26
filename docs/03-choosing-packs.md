# Choosing packs

Packs are **install bundles**. Pick one or more packs that match your stack, then install with [Install guide](02-install.md).

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack <pack-id>
```

List all pack IDs: `./tools/skillctl list --packs`

> **Canonical skill lists** (always up to date after `make build`): [dist/catalog/packs.md](../dist/catalog/packs.md)

## Quick picker

| Your stack / need | Pack ID | Skills (approx.) |
| --- | --- | --- |
| Java / Spring Boot backend | `java-backend-pack` | 16 |
| Kotlin / Spring Boot backend | `kotlin-backend-pack` | 9 |
| .NET / ASP.NET Core backend | `dotnet-backend-pack` | 9 |
| Rust backend | `rust-backend-pack` | 9 |
| PHP / Laravel or Symfony | `php-backend-pack` | 9 |
| React frontend | `frontend-react-pack` | 10 |
| Angular frontend | `frontend-angular-pack` | 10 |
| Vue frontend | `frontend-vue-pack` | 11 |
| Architecture / API / readiness reviews | `architecture-review-pack` | 17 |
| CI quality gates (all stacks) | `quality-gates-pack` | 9 |
| Security review + hardening | `security-review-pack` | 9 |
| Testing strategy + verification | `testing-verification-pack` | 18 |
| Production diagnostics + delivery | `production-readiness-pack` | 16 |
| AI / RAG / tool-calling | `ai-engineering-pack` | 8 |
| UX / UI (flows, design system, Tailwind) | `frontend-ux-ui-pack` | 3 |
| Technical articles & documentation | `technical-writing-pack` | 3 |
| Everything | *(omit `--pack`)* | 100 |

## Pack summaries

### `java-backend-pack`

Core Java, Spring Boot services (3.5 / 4.0 / 4.1 version guides), LTS version guides, testing, JVM debugging, persistence, concurrency, security hardening, cloud delivery, migration.

**Install:**

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
```

### `kotlin-backend-pack`

Kotlin idioms, coroutines, Spring Boot services, persistence, testing, JVM debugging, security, quality gates, and migration.

### `rust-backend-pack`

Rust core engineering, Tokio async, Axum/Actix APIs, persistence, performance, testing, security, quality gates, and edition migrations.

### `dotnet-backend-pack`

C# core engineering, ASP.NET Core services, EF Core, testing, runtime diagnostics, security, cloud delivery, migration.

### `php-backend-pack`

PHP core, Laravel and Symfony services, persistence, delivery, testing, security, migration.

### `frontend-react-pack`

React components, state, performance, accessibility, security, testing, migration, AI product patterns.

### `frontend-angular-pack`

Angular apps, RxJS, state, performance, accessibility, security, testing, migration.

### `frontend-vue-pack`

Vue SFCs, composables, Pinia state, performance, accessibility, security, testing, migration, and AI product patterns.

### `architecture-review-pack`

Cross-stack planning skills: system architecture, software design analysis, technical documentation, API design, security review, production readiness, observability, migration planning, testing strategy, LLM application architecture, AI evaluation architecture, agent orchestration design, UX design review, UI design system review, RAG architecture, tool-calling design.

Most skills are **`planning`** mode. Good for design sessions and PR reviews.

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack architecture-review-pack --modes planning
```

### `security-review-pack`

Stack-specific security hardening (Java, Kotlin, .NET, PHP, Rust, React, Angular, Vue) plus cross-stack `security-review`.

### `testing-verification-pack`

Cross-stack `testing-strategy`, **AI evaluation architecture**, stack **testing verification** skills, and **quality gates** (lint, static analysis, coverage, CI) for Java, Kotlin, .NET, PHP, Rust, React, Angular, and Vue.

### `quality-gates-pack`

Focused CI quality gate skills only — same eight stack gate skills plus `testing-strategy`. Use when you already have stack packs but want gate workflows without reinstalling full backend/frontend bundles.

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack quality-gates-pack
```

### `production-readiness-pack`

Diagnostics, persistence, delivery, and readiness skills spanning Java, .NET, and PHP — overlaps with backend packs by design.

### `ai-engineering-pack`

AI-assisted engineering workflows, LLM application architecture, AI evaluation architecture, agent orchestration design, Java AI backend, React AI product, Vue AI product, RAG architecture review, tool-calling design review.

| Skill | Mode | Use when |
| --- | --- | --- |
| `llm-application-architecture` | planning | Choosing RAG vs tools, routing, memory, phased rollout |
| `ai-evaluation-architecture` | planning | Golden datasets, metrics, CI gates, production drift |
| `agent-orchestration-design` | planning | Multi-step agents, topology, state, limits, HITL |
| `rag-architecture-review` | planning | Reviewing an existing or proposed RAG design |
| `tool-calling-design-review` | planning | Reviewing tool schemas, safety, and orchestration |

**Install (planning skills only):**

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack ai-engineering-pack --modes planning
```

### `frontend-ux-ui-pack`

Cross-stack UX and UI skills: user flow and heuristic review (`ux-design-review`), design token and component consistency audit (`ui-design-system-review`), and HTML/Tailwind implementation with responsive layouts and complete states (`frontend-ui-engineering`).

Also included in `architecture-review-pack` (planning skills), `frontend-react-pack`, `frontend-angular-pack`, and `frontend-vue-pack` (implementation skill).

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack frontend-ux-ui-pack
./scripts/install-from-clone.sh --dest /path/to/project --pack frontend-ux-ui-pack --modes planning
```

### `technical-writing-pack`

Public technical articles (`technical-article-authoring`), internal specs and plans (`technical-documentation-authoring`), and design analysis for research-first pieces (`software-design-analysis`). All skills are **`planning`** mode.

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack technical-writing-pack
```

Good fit for blog repos, newsletter drafts, and agent projects that generate LinkedIn or dev content.

## Pack vs collection vs skill

| Concept | Purpose | Install? |
| --- | --- | --- |
| **Skill** | One agent workflow (`java-spring-boot-service`) | Yes — it's what gets copied |
| **Pack** | Curated bundle for install (`java-backend-pack`) | Yes — use `--pack` |
| **Collection** | Catalog grouping (`java`, `backend`, `testing`) | No — metadata only |

## Combining packs

Install multiple packs into the same project — later installs overwrite skills that appear in more than one pack:

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
./scripts/install-from-clone.sh --dest /path/to/project --pack architecture-review-pack
```

Or install everything at once:

```bash
./scripts/install-from-clone.sh --dest /path/to/project
```

## Planning vs coding

Skills have `modes` in metadata:

- **`planning`** — design, review, strategy
- **`coding`** — implement, refactor, test

Filter on install:

```bash
./tools/skillctl install --pack java-backend-pack --target cursor --dest . --modes coding
```

Full breakdown: [dist/catalog/coverage-by-mode.md](../dist/catalog/coverage-by-mode.md)

## Discovering skills without this doc

```bash
./tools/skillctl recommend --dest /path/to/your-project
./tools/skillctl list --packs
./tools/skillctl catalog
make recommend DEST=/path/to/your-project
make list-catalog
```

`recommend` inspects build files (Maven/Gradle, `package.json`, `composer.json`, `.csproj`), Docker, CI, and AI-related dependencies, then suggests install packs with reasons and copy-paste install commands.

Canonical pack membership: [dist/catalog/packs.md](../dist/catalog/packs.md). CLI details: [CLI reference — Recommend](05-skillctl-reference.md#recommend).

## See also

- [Getting started](01-getting-started.md)
- [Install guide](02-install.md)
