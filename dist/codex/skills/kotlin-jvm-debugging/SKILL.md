---
name: kotlin-jvm-debugging
description: Diagnose JVM runtime behavior and production issues in Kotlin services. Use when investigating memory growth, latency spikes, garbage collection, thread dumps, coroutine leaks, deadlocks, JVM flags, profiling data, or production performance symptoms.
---

# Kotlin JVM Debugging

## Workflow

1. Start from the symptom: memory, latency, CPU, blocked threads, coroutine leaks, startup, or crashes.
2. Collect available evidence before proposing fixes: logs, metrics, traces, heap data, thread dumps, GC logs, and deployment changes.
3. Separate JVM issues from database, network, dependency, and connection pool issues.
4. For coroutine-heavy services, check dispatcher saturation and unstructured scope leaks.
5. Prefer reversible, measurable changes.
6. Verify with the same metric or reproduction that showed the problem.

## References

- Read `references/symptoms-and-tools.md` for symptom-to-evidence mapping and safe collection commands.
- Read `references/gc-and-memory.md` for GC log patterns, heap analysis, and memory leak triage.

## Diagnostic Checklist

- Identify what changed before the issue.
- Compare healthy and unhealthy instances when possible.
- Check thread pools, coroutine scopes, and connection pools together.
- Treat JVM flags as production configuration, not code style.
- Avoid speculative tuning without evidence.

## Output

Summarize symptom, evidence collected, root cause hypothesis, proposed change, rollback plan, and metric to confirm recovery.
