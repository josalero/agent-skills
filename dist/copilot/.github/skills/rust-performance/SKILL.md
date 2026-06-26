---
name: rust-performance
description: Diagnose and improve Rust service performance. Use when investigating high latency, CPU spikes, memory growth, allocator pressure, async runtime starvation, slow queries, or production profiling data for Rust backends.
---

# Rust Performance

## Workflow

1. Start from symptom: latency, throughput, CPU, memory, or tail latencies under load.
2. Collect evidence: traces, `tracing` spans, flamegraphs, heap profiles, DB metrics, and load test results.
3. Separate application issues from DB, network, and pool misconfiguration.
4. For async services, check task counts, blocking in async context, and lock contention.
5. Apply targeted fixes: algorithm changes, allocation reduction, pool tuning, batching.
6. Verify with the same benchmark or load test that exposed the issue.

## References

- Read `references/profiling-and-metrics.md` for flamegraphs, tracing, and benchmark workflow.
- Read `references/async-and-allocation.md` for runtime starvation, allocations, and lock patterns.

## Diagnostic Checklist

- Baseline metric captured before changes.
- Hot path identified with profiler evidence, not guesswork.
- Allocations and clones on hot path reviewed.
- DB query plans checked for slow endpoints.
- Fix measured against baseline; rollback plan documented.

## Output

Summarize symptom, evidence, root cause, changes made, expected improvement, benchmark command, and rollback plan.
