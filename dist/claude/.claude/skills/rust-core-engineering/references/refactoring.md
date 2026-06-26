# Rust Refactoring Guidance

## Replace Stringly-Typed APIs

Before:

```rust
fn apply_discount(lines: &[(String, f64, u32)], code: Option<&str>) -> f64 {
    let mut total = 0.0;
    for (_, price, qty) in lines {
        total += price * (*qty as f64);
    }
    if code == Some("SAVE10") { total *= 0.9; }
    total
}
```

After:

```rust
struct LineItem { price: Decimal, quantity: u32 }

fn apply_discount(lines: &[LineItem], code: Option<&str>) -> Decimal {
    let subtotal: Decimal = lines.iter().map(|l| l.price * Decimal::from(l.quantity)).sum();
    if code == Some("SAVE10") { subtotal * dec!(0.9) } else { subtotal }
}
```

## Review Checklist

- Panics replaced with `Result` at public boundaries
- Clone usage justified or eliminated
- Public types documented when contracts change
- Regression tests for behavior-sensitive refactors
