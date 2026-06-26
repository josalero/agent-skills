# Diesel Patterns

## Schema and Models

Keep `schema.rs` generated; map to domain types at repository boundary.

## Connection Pool

```rust
let manager = ConnectionManager::<PgConnection>::new(database_url);
let pool = Pool::builder().max_size(10).build(manager)?;
```

## Query DSL

Prefer typed table columns over raw SQL for maintainability.

## Async Note

Diesel is sync — use `spawn_blocking` in async services or prefer sqlx for async-first stacks.
