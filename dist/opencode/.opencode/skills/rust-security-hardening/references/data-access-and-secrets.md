# Data Access and Secrets

## Parameterized sqlx

```rust
sqlx::query("SELECT * FROM users WHERE email = $1")
    .bind(email)
    .fetch_optional(&pool)
    .await?;
```

Never use `format!` for SQL with user input.

## Secrets

Load from environment:

```rust
let database_url = std::env::var("DATABASE_URL").context("DATABASE_URL missing")?;
```

## Safe Errors

Log full error with `tracing::error!`; return generic message in `ApiError` JSON.
