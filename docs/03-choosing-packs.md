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
| .NET / ASP.NET Core backend | `dotnet-backend-pack` | 9 |
| PHP / Laravel or Symfony | `php-backend-pack` | 9 |
| React frontend | `frontend-react-pack` | 9 |
| Angular frontend | `frontend-angular-pack` | 9 |
| Architecture / API / readiness reviews | `architecture-review-pack` | 12 |
| CI quality gates (all stacks) | `quality-gates-pack` | 6 |
| Security review + hardening | `security-review-pack` | 6 |
| Testing strategy + verification | `testing-verification-pack` | 11 |
| Production diagnostics + delivery | `production-readiness-pack` | 12 |
| AI / RAG / tool-calling | `ai-engineering-pack` | 5 |
| Everything | *(omit `--pack`)* | 65 |

## Pack summaries

### `java-backend-pack`

Core Java, Spring Boot services (3.5 / 4.0 / 4.1 version guides), LTS version guides, testing, JVM debugging, persistence, concurrency, security hardening, cloud delivery, migration.

**Install:**

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
```

### `dotnet-backend-pack`

C# core engineering, ASP.NET Core services, EF Core, testing, runtime diagnostics, security, cloud delivery, migration.

### `php-backend-pack`

PHP core, Laravel and Symfony services, persistence, delivery, testing, security, migration.

### `frontend-react-pack`

React components, state, performance, accessibility, security, testing, migration, AI product patterns.

### `frontend-angular-pack`

Angular apps, RxJS, state, performance, accessibility, security, testing, migration.

### `architecture-review-pack`

Cross-stack planning skills: system architecture, software design analysis, technical documentation, API design, security review, production readiness, observability, migration planning, testing strategy, RAG architecture, tool-calling design.

Most skills are **`planning`** mode. Good for design sessions and PR reviews.

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack architecture-review-pack --modes planning
```

### `security-review-pack`

Stack-specific security hardening (Java, .NET, PHP, React, Angular) plus cross-stack `security-review`.

### `testing-verification-pack`

Cross-stack `testing-strategy`, stack **testing verification** skills, and **quality gates** (lint, static analysis, coverage, CI) for Java, .NET, PHP, React, and Angular.

### `quality-gates-pack`

Focused CI quality gate skills only — same five stack gate skills plus `testing-strategy`. Use when you already have stack packs but want gate workflows without reinstalling full backend/frontend bundles.

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack quality-gates-pack
```

### `production-readiness-pack`

Diagnostics, persistence, delivery, and readiness skills spanning Java, .NET, and PHP — overlaps with backend packs by design.

### `ai-engineering-pack`

AI-assisted engineering workflows, Java AI backend, React AI product, RAG architecture review, tool-calling design review.

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

## See also

- [Getting started](01-getting-started.md)
- [Install guide](02-install.md)
