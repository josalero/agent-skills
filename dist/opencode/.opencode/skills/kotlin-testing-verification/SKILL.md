---
name: kotlin-testing-verification
description: Design, add, review, and improve Kotlin test coverage. Use when verifying Kotlin behavior with unit tests, integration tests, Testcontainers, coroutine tests, regression tests, or CI quality gates on Kotlin code.
---

# Kotlin Testing Verification

## Workflow

1. Inspect the test framework (JUnit 5, Kotest), build tool, test naming conventions, fixtures, and CI commands.
2. Identify the behavior that must be proven, not just the lines that changed.
3. Prefer fast unit tests for pure logic and focused integration tests for boundaries.
4. Use Testcontainers or real dependencies only when mocks would hide important behavior.
5. Use `runTest` and Turbine for coroutine and Flow tests.
6. Run the smallest useful test command first, then broader verification if shared behavior changed.

## References

- Read `references/unit-tests.md` for JUnit 5 and Kotest unit test patterns.
- Read `references/integration-tests.md` for Spring slice tests, Testcontainers, and coroutine test utilities.

## Quality Checklist

- Tests assert observable behavior.
- Tests do not depend on execution order.
- Fixtures are clear and local.
- Assertions explain the contract.
- Coroutine tests use test dispatchers; no flaky timing.

## Output

Summarize behavior under test, test type chosen and rationale, files changed, commands to run, and gaps intentionally left uncovered.
