---
name: php-testing-verification
description: Design, add, review, and improve PHP test coverage. Use when verifying PHP behavior with unit tests, integration tests, feature tests, database tests, contract tests, regression tests, static analysis gates, CI quality checks, or AI-generated code review.
---

# PHP Testing Verification

## Workflow

1. Inspect the test framework (PHPUnit, Pest), Composer scripts, fixtures, database strategy, and CI commands.
2. Identify the behavior that must be proven, not just the lines that changed.
3. Prefer fast unit tests for pure logic and focused integration or feature tests for boundaries.
4. Use real databases or containers only when mocks would hide important behavior.
5. Include regression tests for bug fixes and edge cases.
6. Run the smallest useful test command first, then broader verification if shared behavior changed.

## References

- Read `references/unit-tests.md` for PHPUnit and Pest unit test patterns and naming.
- Read `references/integration-tests.md` for Laravel/Symfony integration tests, database setup, and CI commands.

## Quality Checklist

- Tests assert observable behavior.
- Tests do not depend on execution order.
- Fixtures are clear and local.
- Assertions explain the contract.
- AI-generated code is verified before trust.

## Output

After test work, summarize:

- Behavior under test and why it matters
- Test type chosen (unit, integration, feature) and rationale
- Files added or changed
- Commands to run locally and in CI
- Gaps intentionally left uncovered
