# Eval: .NET Core Engineering

## Prompt

Refactor a service using `.Result` on async repository calls and nullable warnings suppressed with `!`. Preserve behavior and add tests.

## Expected Agent Behavior

- Converts to async/await with CancellationToken
- Fixes null handling without blanket suppression
- Adds regression tests
- Runs dotnet test command

## Failure Signals

- Keeps sync-over-async
- Ignores nullable context
- No tests
