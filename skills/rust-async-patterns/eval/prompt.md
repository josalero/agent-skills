# Eval: Rust Async Patterns

## Prompt

Our Axum service spawns untracked `tokio::spawn` tasks for webhooks with no timeout. Under load, tasks pile up and memory grows. Refactor to bounded concurrency with timeouts and graceful shutdown.

## Expected Agent Behavior

- Adds timeouts and bounded worker pool or semaphore
- Tracks join handles or uses JoinSet
- Implements shutdown signal handling
- Adds tokio tests for timeout behavior

## Failure Signals

- Keeps unbounded spawn without backpressure
- Holds MutexGuard across await
- No shutdown handling
