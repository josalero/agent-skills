---
name: rust-core-engineering
description: Apply idiomatic Rust engineering practices for ownership, error handling, maintainability, and code review. Use when writing, reviewing, or refactoring Rust code that is not primarily about async runtimes, web frameworks, migration, or production diagnostics.
---

# Rust Core Engineering

## Workflow

1. Inspect Rust edition, toolchain (`rust-toolchain.toml`), crate layout, clippy settings, and test conventions.
2. Prefer the repository's existing idioms before introducing new patterns.
3. Let the type system express invariants: ownership, borrowing, lifetimes, and `Result`/`Option` at boundaries.
4. Use enums, newtypes, and modules to model domain errors and state machines.
5. Preserve behavior while refactoring; add or update focused unit tests.
6. Verify with `cargo test`, `cargo clippy`, and the narrowest useful crate target.

## References

- Read `references/idioms.md` for ownership patterns, error types, iterators, and newtypes.
- Read `references/refactoring.md` for before/after examples and review guidance.

## Quality Checklist

- Public APIs have clear names and documented error conditions.
- `unwrap`/`expect` limited to tests or proven invariants.
- Error types are meaningful; errors are not silently discarded.
- Mutability is minimal and localized.
- Iterator chains stay readable.
- Tests cover important behavior and edge cases.

## Output

After changes, summarize files changed, behavior preserved, tests added, `cargo` commands to run, and residual risks.
