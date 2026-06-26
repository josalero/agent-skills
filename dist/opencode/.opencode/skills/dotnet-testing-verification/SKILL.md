---
name: dotnet-testing-verification
description: Design, add, review, and improve .NET test coverage. Use when verifying C# behavior with xUnit, NUnit, Moq/NSubstitute, WebApplicationFactory, integration tests, regression tests, or CI quality gates for AI-generated code.
---

# .NET Testing Verification

## Workflow

1. Inspect the test framework (xUnit, NUnit), mocking library, project layout, fixtures, and CI commands.
2. Identify the behavior that must be proven, not just the lines that changed.
3. Prefer fast unit tests for pure logic and focused integration tests for HTTP, EF, or messaging boundaries.
4. Use `WebApplicationFactory`, Testcontainers, or real dependencies only when mocks would hide important behavior.
5. Include regression tests for bug fixes and edge cases.
6. Run the smallest useful test command first (`dotnet test --filter`), then broader verification if shared behavior changed.

## References

- Read `references/unit-tests.md` for xUnit patterns, naming, and mocking discipline.
- Read `references/integration-tests.md` for WebApplicationFactory, database tests, and CI commands.

## Quality Checklist

- Tests assert observable behavior, not implementation details.
- Tests do not depend on execution order or shared mutable state.
- Fixtures are clear and local; use `IAsyncLifetime` for async setup when needed.
- Assertions explain the contract (FluentAssertions or descriptive messages).
- AI-generated code is verified before trust.

## Output

Summarize behavior under test, test type chosen and rationale, files added or changed, `dotnet test` commands for local and CI, and gaps intentionally left uncovered.
