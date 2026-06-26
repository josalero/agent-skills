---
name: kotlin-persistence-performance
description: Diagnose and improve persistence performance in Kotlin backend services. Use when fixing N+1 queries, slow transactions, connection pool exhaustion, Exposed DSL inefficiencies, Hibernate fetch plans, or R2DBC reactive pipeline bottlenecks.
---

# Kotlin Persistence Performance

## Workflow

1. Start from the symptom: slow endpoints, pool timeouts, high DB CPU, memory growth, or reactive backpressure stalls.
2. Identify the persistence stack: JPA/Hibernate, Exposed, R2DBC, or mixed.
3. Collect evidence: query logs, metrics, EXPLAIN plans, Hibernate statistics, pool metrics.
4. Separate ORM mapping issues from missing indexes, lock contention, and network latency.
5. Apply targeted fixes: fetch joins, batch size, projections, query rewrites, pool tuning.
6. Verify with the same endpoint benchmark or integration test that exposed the issue.

## References

- Read `references/orm-patterns.md` for JPA/Hibernate and Exposed fetch, batch, and projection patterns.
- Read `references/reactive-and-pools.md` for R2DBC flow control, connection pools, and transaction boundaries.

## Performance Checklist

- N+1 queries identified and eliminated with fetch plans or batch fetching.
- Read paths use DTO projections instead of full entity graphs when possible.
- Transaction boundaries are minimal; no long-running work inside `@Transactional`.
- Connection pool size matches concurrency and DB limits.
- R2DBC pipelines apply backpressure; blocking calls stay off reactive threads.
- Indexes support filter and join columns used in hot queries.

## Output

Summarize symptom, evidence, root cause, query or mapping changes, expected metric improvement, and verification commands.
