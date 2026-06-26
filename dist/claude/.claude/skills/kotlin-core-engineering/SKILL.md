---
name: kotlin-core-engineering
description: Apply modern Kotlin engineering practices for idiomatic implementation, maintainability, correctness, and code review. Use when writing, reviewing, or refactoring Kotlin code that is not primarily about coroutines, Spring Boot, migration, or production diagnostics.
---

# Kotlin Core Engineering

## Workflow

1. Inspect the Kotlin version, build tool (Gradle), package structure, tests, and local style.
2. Prefer the repository's existing idioms before introducing new patterns.
3. Keep types, null safety, exceptions, immutability, and scope functions explicit and intentional.
4. Use data classes, sealed types, value classes, and extension functions only where they make code clearer.
5. Preserve behavior while refactoring, then add or update focused tests.
6. Verify with the narrowest useful build or test command.

## References

- Read `references/idioms.md` for data classes, sealed types, null safety, scope functions, and collection patterns.
- Read `references/refactoring.md` for before/after examples and review guidance.

## Quality Checklist

- Public APIs have clear names and stable contracts.
- Nullability is explicit; avoid unsafe `!!` without justification.
- Exceptions are intentional and not swallowed.
- Mutability is limited and visible.
- Extension functions improve readability without hiding side effects.
- Tests cover important behavior and edge cases.

## Output

After changes, summarize:

- Files changed and why
- Behavior preserved or intentionally changed
- Tests added or updated
- Build or test command to run
- Residual risks or follow-ups
