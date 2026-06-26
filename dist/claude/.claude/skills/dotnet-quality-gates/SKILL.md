---
name: dotnet-quality-gates
description: Configure and fix .NET CI quality gates for SDK-style projects. Use when setting up or repairing dotnet build, test, analyzer warnings as errors, dotnet format, StyleCop or Roslyn analyzers, nullable reference types, Coverlet coverage, or Azure DevOps/GitHub Actions pipeline failures.
---

# .NET Quality Gates

## Workflow

1. Inspect solution structure, `Directory.Build.props`, `Directory.Build.targets`, `.editorconfig`, and CI YAML.
2. Identify the **canonical gate command** — typically `dotnet build`, `dotnet test`, and optional `dotnet format --verify-no-changes`.
3. Read `references/ci-pipeline-gates.md` for pipeline staging.
4. Read `references/analyzers-format-and-coverage.md` for analyzer, nullable, and Coverlet configuration.
5. Fix compile and test failures before analyzer noise; treat new analyzer violations in touched code seriously.
6. Align `TreatWarningsAsErrors` and analyzer severities with team policy — do not globally `#pragma` suppress.
7. Verify locally with the same SDK version as CI (`global.json`).

## Gate Checklist

- `dotnet build` succeeds with configured warnings-as-errors policy.
- `dotnet test` runs unit tests; integration tests gated appropriately on PR vs main.
- `dotnet format --verify-no-changes` (or equivalent) passes when formatting is enforced.
- Nullable reference types enabled where project standard requires — no new null warnings in changed files.
- Coverage thresholds (Coverlet) apply to assemblies that contain business logic.
- CI uses pinned SDK via `global.json` when the repo defines one.

## Output

Summarize gates, CI commands, files changed, local verification commands, and any deferred baseline work.

## Related Skills

- `dotnet-testing-verification` — test design
- `testing-strategy` — cross-stack gate policy
- `dotnet-core-engineering` — code fixes behind failures
