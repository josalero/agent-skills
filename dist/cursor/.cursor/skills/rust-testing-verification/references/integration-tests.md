# Integration Tests

## HTTP Handler Test (Axum)

```rust
let response = app.oneshot(Request::builder().method("POST").uri("/orders").body(body).unwrap()).await.unwrap();
assert_eq!(response.status(), StatusCode::CREATED);
```

## Database Integration

Use `sqlx::test` or Testcontainers Postgres in `tests/` directory.

## CI

```bash
cargo test --workspace
cargo test -p api --test integration
```
