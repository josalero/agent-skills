# Eval: Rust Performance

## Prompt

Our Axum API p99 latency jumped from 50ms to 800ms under 500 RPS. CPU is moderate but tokio metrics show many tasks waiting. Diagnose and fix with measurable verification.

## Expected Agent Behavior

- Uses tracing or profiler to find blocking/lock issues
- Identifies spawn_blocking or lock-across-await problems
- Proposes fix with before/after benchmark
- Documents rollback

## Failure Signals

- Random codegen or allocator flags without evidence
- Ignores async runtime metrics
- No verification benchmark
