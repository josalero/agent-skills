# Reactive Persistence and Pools

## R2DBC Transaction Boundaries

Keep transactional work short. Use `TransactionalOperator` or `@Transactional` on suspend service methods consistently.

## Backpressure

Collect large result sets with pagination — avoid `collectList()` on unbounded queries.

## Connection Pool Tuning

| Signal | Action |
| --- | --- |
| Pool timeout errors | Review pool max, query duration, leak detection |
| High DB connections | Right-size pool per instance × replica count |
| Slow queries | EXPLAIN and index first, then pool |

## Mixed Blocking and Reactive

Do not call blocking JDBC from reactive threads — isolate with dedicated dispatchers or separate modules.
