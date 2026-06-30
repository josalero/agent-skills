# Choosing packs

Packs are **install bundles grouped by technology** (or cross-stack planning). Pick the pack that matches your stack, then install with [Install guide](02-install.md).

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack <pack-id>
```

List all pack IDs: `./tools/skillctl list --packs`

> **Canonical skill lists** (always up to date after `make build`): [dist/catalog/packs.md](../dist/catalog/packs.md)

## Quick picker

| Your stack / need | Pack ID | What you get |
| --- | --- | --- |
| Java / Spring Boot backend | `java-backend-pack` | Java core, Spring Boot, testing, JVM, persistence, security, delivery, migration |
| Kotlin / Spring Boot backend | `kotlin-backend-pack` | Kotlin core, coroutines, Spring Boot, testing, JVM, persistence, security |
| .NET / ASP.NET Core backend | `dotnet-backend-pack` | C#, ASP.NET Core, EF Core, testing, diagnostics, security, delivery |
| Rust backend | `rust-backend-pack` | Rust core, async, APIs, persistence, performance, testing, security |
| PHP / Laravel or Symfony | `php-backend-pack` | PHP core, Laravel/Symfony, persistence, delivery, testing, security |
| React frontend | `frontend-react-pack` | React components, state, performance, accessibility, security, testing, UI engineering |
| Angular frontend | `frontend-angular-pack` | Angular apps, RxJS, state, performance, accessibility, security, testing, UI engineering |
| Vue frontend | `frontend-vue-pack` | Vue SFCs, composables, state, performance, accessibility, security, testing, AI product |
| Architecture / API / readiness / AI planning | `architecture-review-pack` | Cross-stack planning and review skills |
| Technical articles & documentation | `technical-writing-pack` | Article, documentation, and design-analysis authoring |
| Everything | *(omit `--pack`)* | All active skills |

Mixed “all stacks” packs (quality gates, security, testing, production readiness, AI engineering, UX/UI) were removed. Those skills now live in the **technology pack for your stack**, with cross-stack planning skills in `architecture-review-pack`.

## Pack summaries

### Backend technology packs

Each backend pack is self-contained for its stack: core engineering, framework service patterns, testing verification, quality gates, security hardening, and stack-specific diagnostics/delivery skills.

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
```

Same pattern for `kotlin-backend-pack`, `dotnet-backend-pack`, `rust-backend-pack`, and `php-backend-pack`.

### Frontend technology packs

Each frontend pack includes stack-specific implementation skills plus shared `frontend-ui-engineering` (HTML/Tailwind/responsive UI).

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack frontend-react-pack
```

Same pattern for `frontend-angular-pack` and `frontend-vue-pack`.

### `architecture-review-pack`

Cross-stack **planning** skills only: system architecture, API design, security review, production readiness, observability, migration planning, testing strategy, LLM application architecture, AI evaluation, agent orchestration, RAG architecture, tool-calling design, UX/UI review.

Most skills are **`planning`** mode. Good for design sessions and PR reviews.

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack architecture-review-pack --modes planning
```

Pair a technology pack with this when you want both implementation and review workflows:

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
./scripts/install-from-clone.sh --dest /path/to/project --pack architecture-review-pack
```

### `technical-writing-pack`

Public technical articles (`technical-article-authoring`), internal specs and plans (`technical-documentation-authoring`), and design analysis for research-first pieces (`software-design-analysis`). All skills are **`planning`** mode.

```bash
./scripts/install-from-clone.sh --dest /path/to/project --pack technical-writing-pack
```

## Pack vs collection vs skill

| Concept | Purpose | Install? |
| --- | --- | --- |
| **Skill** | One agent workflow (`java-spring-boot-service`) | Yes — it's what gets copied |
| **Pack** | Technology or cross-stack install bundle | Yes — use `--pack` |
| **Collection** | Catalog label by technology (`java`, `react`, `architecture`) | No — metadata only |

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

`recommend` inspects build files (Maven/Gradle, `package.json`, `composer.json`, `.csproj`), Docker, CI, and AI-related dependencies, then suggests **technology packs** for detected stacks and **`architecture-review-pack`** as a consider-tier add-on for planning, AI, CI, and security review.

Canonical pack membership: [dist/catalog/packs.md](../dist/catalog/packs.md). CLI details: [CLI reference — Recommend](05-skillctl-reference.md#recommend).

## See also

- [Getting started](01-getting-started.md)
- [Install guide](02-install.md)
