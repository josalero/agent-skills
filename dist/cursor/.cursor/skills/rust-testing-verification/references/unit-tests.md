# Unit Tests

## Pure Logic

```rust
#[test]
fn applies_save10_discount() {
    let lines = vec![LineItem { price: dec!(10), quantity: 2 }];
    assert_eq!(apply_discount(&lines, Some("SAVE10")), dec!(18));
}
```

## Async Unit Test

```rust
#[tokio::test]
async fn fetches_order_status() {
    let svc = OrderService::new(mock_repo());
    assert_eq!(svc.status(id).await.unwrap(), Status::Ready);
}
```

## Mocking

Use trait objects or `mockall` for external ports — inject at construction.
