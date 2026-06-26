---
name: kotlin-coroutines-patterns
description: Design and implement Kotlin coroutines, Flow, and structured concurrency for backend services. Use when adding async work, parallel I/O, reactive streams, cancellation, timeouts, channel pipelines, or diagnosing coroutine leaks and deadlocks.
---

# Kotlin Coroutines Patterns

## Workflow

1. Inspect dispatcher usage, coroutine scopes, framework integration (Spring, Ktor), and existing async boundaries.
2. Identify whether work is CPU-bound, I/O-bound, or event-driven — choose dispatchers accordingly.
3. Use structured concurrency: parent scopes own child jobs; propagate `CancellationException` correctly.
4. Prefer `suspend` functions and `Flow` over blocking calls on limited thread pools.
5. Add timeouts, backpressure, and error handling at integration boundaries.
6. Verify with focused tests using `runTest`, `TestScope`, and Turbine for Flow assertions.

## References

- Read `references/structured-concurrency.md` for scopes, supervisors, cancellation, and dispatcher selection.
- Read `references/flow-and-channels.md` for Flow operators, channels, buffering, and testing patterns.

## Checklist

- No blocking I/O on `Dispatchers.Default` or event-loop threads.
- Coroutine scopes tied to lifecycle (request, application, test scope).
- `CancellationException` is not caught and swallowed.
- Timeouts applied to external calls where latency matters.
- Flow collectors handle completion and failure explicitly.
- Tests use deterministic coroutine test utilities.

## Output

Summarize scopes and dispatchers chosen, files changed, cancellation/timeout behavior, tests added, and commands to run.
