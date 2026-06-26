# sqlx Patterns

## Pool Setup

```rust
let pool = PgPoolOptions::new()
    .max_connections(10)
    .connect(&database_url)
    .await?;
```

## Compile-time Query

```rust
let order = sqlx::query_as!(OrderRow, "SELECT id, total FROM orders WHERE id = $1", id)
    .fetch_optional(&pool)
    .await?;
```

## Transactions

```rust
let mut tx = pool.begin().await?;
// operations
tx.commit().await?;
```

## Migrations

Use `sqlx::migrate!()` in application startup or dedicated migration binary.
