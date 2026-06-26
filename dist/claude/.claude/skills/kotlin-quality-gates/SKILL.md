---
name: kotlin-quality-gates
description: Configure and fix Kotlin CI quality gates for Gradle projects. Use when setting up or repairing check, detekt, ktlint, SpotBugs, JaCoCo coverage thresholds, formatting verification, or PR pipeline failures on static analysis and tests.
---

# Kotlin Quality Gates

## Workflow

1. Read the build file (`build.gradle.kts`) and existing CI workflow — identify what already runs on PR vs main.
2. Map the **canonical gate command** (`./gradlew check`, `./gradlew build`, or project-specific `quality` task).
3. Classify failures: compile, test, detekt, ktlint, coverage — fix in that order.
4. Read `references/ci-pipeline-gates.md` when designing or changing pipeline stages.
5. Read `references/static-analysis-and-coverage.md` when tuning detekt, ktlint, and JaCoCo.
6. Prefer **fail the build** on new code; use baselines only with a tracked cleanup ticket.
7. Align local commands with CI so developers reproduce failures before push.

## Gate Checklist

- PR pipeline runs unit tests (and integration tests when risk warrants).
- detekt and/or ktlint run on main sources — not skipped silently in CI.
- Formatting is enforced — not optional manual cleanup.
- Coverage thresholds apply to **meaningful packages**, not blanket noise on DTOs.
- JDK/toolchain in CI matches `build` files.
- `./gradlew check` passes locally before claiming done.

## Output

Summarize gates in scope, CI jobs, files changed, verification commands, and deferred baseline work.

## Related Skills

- `kotlin-testing-verification` — test design
- `testing-strategy` — cross-stack gate policy
- `kotlin-core-engineering` — code fixes behind failures
