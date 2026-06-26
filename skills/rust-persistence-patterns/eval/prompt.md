# Eval: Rust Persistence Patterns

## Prompt

Our order list endpoint runs N+1 queries via sqlx in a loop. Refactor to a single join query, add a repository module boundary, and add an integration test against Postgres.

## Expected Agent Behavior

- Replaces loop with join or IN query
- Keeps SQL parameterized
- Adds integration test with test database
- Documents pool settings if changed

## Failure Signals

- Raw string SQL with user input
- Database calls directly in Axum handlers
- No integration test
