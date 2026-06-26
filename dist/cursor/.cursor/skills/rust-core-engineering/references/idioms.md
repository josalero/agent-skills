# Rust Idioms

## Newtypes for Domain Safety

```rust
pub struct OrderId(Uuid);

impl OrderId {
    pub fn new(id: Uuid) -> Self { Self(id) }
    pub fn as_uuid(&self) -> &Uuid { &self.0 }
}
```

## Error Enums with thiserror

```rust
#[derive(Debug, thiserror::Error)]
pub enum OrderError {
    #[error("order {0} not found")]
    NotFound(Uuid),
    #[error(transparent)]
    Database(#[from] sqlx::Error),
}
```

## Iterator Clarity

```rust
pub fn active_emails(customers: &[Customer]) -> Vec<&str> {
    customers
        .iter()
        .filter(|c| c.active)
        .map(|c| c.email.as_str())
        .filter(|e| !e.is_empty())
        .collect()
}
```

## Option and Result at Boundaries

Return `Result` from fallible operations. Use `?` for propagation; map errors at module boundaries.
