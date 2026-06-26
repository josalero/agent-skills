# Eval: React Testing Verification

## Prompt

Add tests for `OrdersPage` that loads orders from `/api/v1/orders`, shows loading spinner, renders rows, and shows error banner on 500. Use existing Vitest + Testing Library setup.

## Expected Agent Behavior

- Uses findBy/waitFor for async load
- Queries by role/text accessibly
- Mocks HTTP with MSW or project standard
- Tests error and success paths with meaningful assertions
- Provides npm test command with path filter

## Failure Signals

- Tests implementation hooks only
- No error path test
- snapshot-only test
- fetch mocked at wrong layer inconsistently
