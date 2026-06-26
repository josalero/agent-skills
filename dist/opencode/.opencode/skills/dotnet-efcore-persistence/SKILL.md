---
name: dotnet-efcore-persistence
description: Model, query, migrate, and optimize EF Core persistence. Use when fixing slow queries, N+1 loading, migrations, transaction boundaries, indexes, batch writes, connection pool issues, or reviewing EF Core data access.
---

# .NET EF Core Persistence

## Workflow

1. Inspect EF Core version, DbContext layout, migration history, connection string config, and pooling settings.
2. Reproduce or measure the issue with SQL logging, `dotnet ef`, metrics, or query counts — do not guess from code alone.
3. Classify the problem: N+1 queries, over-fetching, missing index, long transaction, lock contention, or chatty writes.
4. Prefer the smallest fix: projection, `Include`, split query, compiled query, index, batch size, or transaction scope change.
5. Avoid loading full entity graphs when a DTO projection or paginated query is enough.
6. Verify with before/after query counts, integration tests, or load check on the affected path.

## References

- Read `references/queries-and-n-plus-one.md` for N+1 diagnosis, projections, and eager loading.
- Read `references/migrations-and-transactions.md` for migrations, transactions, and write patterns.

## Performance Checklist

- Query count per request is understood and acceptable.
- Navigation properties are not accessed outside an intentional fetch plan.
- Writes use `AddRange` and batching where volume warrants it.
- Transactions are no longer than necessary.
- Pagination is applied in the database, not in memory.
- Indexes support filter and join columns used in hot queries.
- Connection pool size matches workload and downstream DB limits.

## Output

Summarize symptom and root cause (with evidence), change made, files and queries affected, verification performed, and residual risks needing DBA review.
