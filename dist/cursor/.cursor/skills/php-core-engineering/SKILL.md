---
name: php-core-engineering
description: Apply modern PHP engineering practices for idiomatic implementation, maintainability, correctness, and code review. Use when writing, reviewing, or refactoring PHP code that is not primarily about a framework, migration, or production diagnostic.
---

# PHP Core Engineering

## Workflow

1. Inspect the PHP version, Composer constraints, PSR layout, static analysis config, tests, and local style.
2. Prefer the repository's existing idioms before introducing new patterns.
3. Keep types, names, exceptions, null handling, and immutability explicit.
4. Use enums, readonly classes, value objects, and `match` only where they make code clearer.
5. Preserve behavior while refactoring, then add or update focused tests.
6. Verify with the narrowest useful test or static analysis command.

## References

- Read `references/idioms.md` for enums, readonly classes, typed properties, exceptions, and collection patterns.
- Read `references/refactoring.md` for before/after examples and review guidance.

## Quality Checklist

- Public APIs have clear names and stable contracts.
- Exceptions are intentional and not swallowed.
- Mutability is limited and visible.
- Strict types are enabled in new files when the project allows it.
- Nullability is explicit in signatures and docblocks where needed.
- Tests cover important behavior and edge cases.

## Output

After changes, summarize:

- Files changed and why
- Behavior preserved or intentionally changed
- Tests added or updated
- Build, test, or analysis command to run
- Residual risks or follow-ups
