---
name: react-testing-verification
description: Write and review React tests with Testing Library, Vitest or Jest, and user-centric assertions. Use when adding component tests, fixing flaky UI tests, testing hooks, forms, async UI, or improving frontend CI verification.
---

# React Testing Verification

## Workflow

1. Inspect test runner (Vitest/Jest), Testing Library setup, MSW usage, and existing test conventions.
2. Test behavior users see — not implementation details (internal state, private hooks unless extracted).
3. Prefer `screen.getByRole`, `getByLabelText`, and accessible queries.
4. Use `userEvent` for interactions; await async UI updates with `findBy*` or `waitFor`.
5. Mock network at HTTP boundary (MSW) rather than mocking every child component.
6. Cover loading, success, error, and empty states for data-driven components.
7. Run the narrowest test command (`npm test -- OrderForm`) before full suite.

## References

- Read `references/testing-library-patterns.md` for queries, userEvent, and async patterns.
- Read `references/msw-and-hooks.md` for API mocking and hook testing.

## Checklist

- Tests describe scenario and expected outcome in the name.
- No snapshot-only tests for complex UI without supplementary assertions.
- Tests do not depend on execution order.
- Fake timers only when testing debounce/time — restored after.
- Accessibility roles used in queries where possible.
- CI uses `jsdom` or happy-dom consistently with local dev.

## Output

Summarize behaviors tested, query strategies used, mocks added, commands to run, and intentional gaps.
