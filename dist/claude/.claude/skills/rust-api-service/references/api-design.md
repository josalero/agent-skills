# API Design (Axum)

## Handler with Typed Errors

```rust
async fn create_order(
    State(state): State<AppState>,
    Json(request): Json<CreateOrderRequest>,
) -> Result<Json<OrderResponse>, ApiError> {
    request.validate()?;
    let order = state.orders.create(request).await?;
    Ok(Json(order.into()))
}
```

## Validation

Use `validator` derive macros or manual validation returning `ApiError::Validation`.

## Pagination

Return cursor or offset metadata in a stable response envelope.

## Problem Details

Map `ApiError` to consistent JSON with `status`, `title`, and optional `detail` for clients.
