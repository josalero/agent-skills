---
name: dotnet-runtime-diagnostics
description: Diagnose .NET runtime behavior and production issues. Use when investigating memory growth, latency spikes, thread pool starvation, GC pressure, dotnet-counters, traces, dumps, or production performance symptoms in ASP.NET Core services.
---

# .NET Runtime Diagnostics

## Workflow

1. Start from the symptom: memory, latency, CPU, blocked threads, startup, or crashes.
2. Collect evidence before proposing fixes: logs, metrics, traces, `dotnet-counters`, dumps, and deployment changes.
3. Separate runtime issues from database, network, dependency, and connection pool issues.
4. Prefer reversible, measurable changes — one variable at a time.
5. Document hypothesis, evidence, change, and expected signal.
6. Verify with the same metric or reproduction that showed the problem.

## References

- Read `references/symptoms-and-tools.md` for symptom-to-tool mapping and safe collection commands.
- Read `references/memory-and-traces.md` for GC, memory leaks, and distributed trace analysis.

## Diagnostic Checklist

- Identify what changed before the issue (deploy, config, traffic, data volume).
- Compare healthy and unhealthy instances when possible.
- Check thread pool queue length and connection pools together.
- Treat `DOTNET_*` and GC settings as production configuration, not code style.
- Avoid speculative tuning without evidence.

## Output

Summarize symptom and timeline, evidence collected, root cause hypothesis and confidence, proposed change and rollback plan, and metric or command to confirm recovery.
