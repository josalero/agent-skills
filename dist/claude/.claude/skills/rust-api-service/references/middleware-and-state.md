# Middleware and State

## Shared State

```rust
#[derive(Clone)]
struct AppState {
    orders: Arc<OrderService>,
    config: Arc<Config>,
}

let app = Router::new()
    .route("/orders", post(create_order))
    .with_state(state);
```

## Auth Middleware

Validate JWT or API keys in middleware/extractor before handler execution.

## Tracing

Add `TraceLayer` for request IDs and latency; propagate trace context to downstream calls.

## Testing

```rust
let app = Router::new().route(...).with_state(test_state());
let response = app.oneshot(request).await.unwrap();
```
