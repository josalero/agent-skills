---
name: rust-testing-verification
description: Design, add, review, and improve Rust test coverage. Use when verifying Rust behavior with unit tests, integration tests, property tests, API tests, regression tests, or CI quality gates on Rust code.
---

# Rust Testing Verification

## Workflow

1. Inspect test layout (`#[cfg(test)]`, `tests/` integration), fixtures, and CI commands.
2. Identify behavior that must be proven, not just lines changed.
3. Prefer fast unit tests for pure logic; integration tests for DB and HTTP boundaries.
4. Use `#[tokio::test]` for async code; `axum::test` for HTTP handlers.
5. Add regression tests for bug fixes with descriptive names.
6. Run `cargo test -p <crate>` first, then workspace when shared code changes.

## References

- Read `references/unit-tests.md` for unit test organization, mocks, and async tests.
- Read `references/integration-tests.md` for API tests, Testcontainers, and workspace test commands.

## Quality Checklist

- Tests assert observable behavior, not implementation details.
- Tests are independent — no shared mutable global state.
- Async tests specify runtime flavor explicitly.
- HTTP tests cover status codes and response bodies.
- Flaky timing avoided — use tokio time controls when needed.

## Output

Summarize behavior under test, test type and rationale, files changed, cargo commands, and intentional coverage gaps.
