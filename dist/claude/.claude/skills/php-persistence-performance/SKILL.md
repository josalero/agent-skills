---
name: php-persistence-performance
description: Diagnose and improve PHP persistence performance with Doctrine ORM, Eloquent, DBAL, PDO, transactions, and connection pools. Use when fixing slow queries, N+1 loading, missing indexes, transaction boundaries, eager loading mistakes, batch writes, or database connection exhaustion.
---

# PHP Persistence Performance

## Workflow

1. Inspect the persistence stack: Doctrine/Eloquent version, DBAL config, migration tool, datasource config, and pool settings.
2. Reproduce or measure the issue with SQL logging, slow-query logs, query counters, or profiler output — do not guess from code alone.
3. Classify the problem: N+1 queries, over-fetching, missing index, long transaction, lock contention, pool starvation, or chatty write pattern.
4. Prefer the smallest fix: eager load, join fetch, DTO projection, query rewrite, index, batch insert, or transaction scope change.
5. Avoid loading full entity graphs when a projection or paginated query is enough.
6. Verify with before/after query counts, integration tests, or load test on the affected path.

## References

- Read `references/n-plus-one-and-querying.md` for N+1 diagnosis, eager loading, join fetch, and projections in Eloquent and Doctrine.
- Read `references/transactions-and-pooling.md` for transaction boundaries, batch writes, pagination, and pool tuning.

## Performance Checklist

- Query count per request is understood and acceptable.
- Lazy associations are not accessed unintentionally in loops.
- Writes use batching where volume warrants it.
- Transactions are no longer than necessary.
- Pagination is applied at the database, not in memory.
- Indexes support filter and join columns used in hot queries.
- Connection pool size matches workload and downstream DB limits.

## Output

After persistence work, summarize:

- Symptom and root cause (with evidence: query count, SQL, metric)
- Change made and why it is the smallest safe fix
- Files and queries affected
- Verification performed (tests, logs, load check)
- Residual risks or queries still needing DBA review
