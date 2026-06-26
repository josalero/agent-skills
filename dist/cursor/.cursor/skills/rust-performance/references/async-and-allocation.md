# Async and Allocation Tuning

## Blocking in Async

Symptom: runtime starvation, growing latency. Fix: `spawn_blocking` or dedicated blocking pool.

## Reduce Clones on Hot Path

Prefer `&str` borrows, `Cow`, or `Arc` for shared immutable data.

## Connection Pools

Right-size sqlx pool: `instances × max_connections` must not exceed DB limit.

## Batching

Replace per-row round trips with batch inserts or UNNEST queries where appropriate.
