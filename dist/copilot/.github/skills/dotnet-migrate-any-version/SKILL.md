---
name: dotnet-migrate-any-version
description: Plan and execute .NET version and toolchain migrations. Use when upgrading target framework, SDK, NuGet packages, ASP.NET Core versions, CI images, breaking API changes, or test strategy across .NET versions.
---

# .NET Migrate Any Version

## Workflow

1. Detect current target framework, SDK pin, runtime, CI image, and major dependency versions (`Microsoft.AspNetCore.*`, EF Core).
2. Identify the target .NET version and whether the upgrade includes ASP.NET Core, EF Core, or container base image changes.
3. Read the relevant migration reference before changing code.
4. Upgrade SDK and target framework in project files first, then package versions, then source incompatibilities.
5. Run `dotnet build` and `dotnet test` after each meaningful step.
6. Verify runtime behavior, publish output, CI pipeline, Docker images, and deployment configuration.

## References

- Read `references/upgrade-sequencing.md` for ordered upgrade steps and CI alignment.
- Read `references/breaking-changes.md` for common API removals and replacement patterns.

## Output

After each migration step, summarize current and target versions, configuration files changed, source or package fixes applied, tests run and results, and remaining blockers or deprecated API usage.
