# Kotlin Refactoring Guidance

## Replace Untyped Maps with Value Types

Before:

```kotlin
fun apply(lines: List<Map<String, Any>>, code: String?): Double {
    var total = 0.0
    for (line in lines) {
        total += (line["price"] as Double) * (line["qty"] as Int)
    }
    if (code == "SAVE10") total *= 0.9
    return total
}
```

After:

```kotlin
data class LineItem(val price: BigDecimal, val quantity: Int)

fun apply(lines: List<LineItem>, code: String?): BigDecimal {
    val subtotal = lines.fold(BigDecimal.ZERO) { acc, line ->
        acc + line.price.multiply(BigDecimal(line.quantity))
    }
    return if (code == "SAVE10") subtotal.multiply(BigDecimal("0.9")) else subtotal
}
```

## Review Checklist

- Unsafe casts replaced with typed models
- `var` minimized; prefer `val` and immutable collections
- Public APIs documented when contracts change
- Regression tests added for behavior-sensitive refactors
- No gratuitous `!!` or platform types leaking across module boundaries
