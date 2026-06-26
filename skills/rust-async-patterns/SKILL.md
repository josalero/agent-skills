---
name: rust-async-patterns
description: Design and implement Tokio async/await patterns for Rust backend services. Use when adding concurrent I/O, task spawning, timeouts, cancellation, channels, select!, or diagnosing async deadlocks and runtime starvation.
---

# Rust Async Patterns

## Workflow

1. Inspect runtime configuration (multi-thread vs current-thread), crate async boundaries, and existing `spawn` usage.
2. Identify I/O-bound vs CPU-bound work — offload CPU work with `spawn_blocking`.
3. Use `tokio::time::timeout` and cancellation tokens for external calls.
4. Prefer structured task trees: join handles, `JoinSet`, and explicit shutdown signals.
5. Avoid holding locks across `.await` points.
6. Verify with `#[tokio::test]` and deterministic time controls where needed.

## References

- Read `references/tokio-runtime.md` for runtime selection, spawning, and shutdown patterns.
- Read `references/channels-and-select.md` for mpsc/broadcast channels, select!, and backpressure.

## Checklist

- No blocking I/O inside async functions without `spawn_blocking`.
- Locks not held across await points.
- Timeouts on network and database calls.
- Task handles tracked for graceful shutdown.
- Errors from spawned tasks propagated or logged explicitly.
- Async tests use `#[tokio::test]` with appropriate flavor.

## Output

Summarize runtime and spawn strategy, files changed, timeout/cancellation behavior, tests added, and `cargo test` commands.
