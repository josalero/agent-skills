---
name: dotnet-core-engineering
description: Apply modern C# and .NET engineering practices for idiomatic code, maintainability, and review. Use when writing or refactoring C# that is not primarily framework-specific, migration, or production diagnostics.
---

# .NET Core Engineering

## Workflow

1. Inspect target framework (`net8.0`, `net9.0`), nullable context, analyzers, and project conventions.
2. Prefer clarity: explicit types at API boundaries, meaningful names, small methods.
3. Use records, pattern matching, `required` members, and immutability where they reduce bugs.
4. Handle errors with exceptions intentionally — avoid swallowing; use result types when project standard.
5. Keep async all the way (`async`/`await`) — no sync-over-async without documented reason.
6. Verify with focused unit tests and `dotnet test` on affected projects.

## References

- Read `references/idioms-and-types.md` for records, nullable reference types, and pattern matching.
- Read `references/async-and-errors.md` for async discipline and exception/result patterns.

## Checklist

- Nullable annotations enabled and honored at boundaries.
- Public APIs documented where project requires XML docs.
- IDisposable/IAsyncDisposable used correctly.
- No business logic in DTOs beyond validation attributes.
- Tests cover edge cases and failure paths.

## Output

Summarize files changed, behavior preserved, tests added, and `dotnet` commands to run.
