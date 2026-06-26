# Eval: Kotlin Core Engineering

## Prompt

Review the following service function. Refactor for clearer types, safer null handling, and better immutability without changing behavior. Add or update unit tests for edge cases.

```kotlin
fun applyDiscount(lines: List<Map<String, Any>>, code: String?): Double {
    var total = 0.0
    for (line in lines) {
        total += (line["price"] as Double) * (line["qty"] as Int)
    }
    if (code != null && code == "SAVE10") {
        total *= 0.9
    }
    return total
}
```

## Expected Agent Behavior

- Inspects surrounding package and test conventions before refactoring
- Replaces primitive maps with typed data classes or value objects
- Avoids swallowing exceptions and unsafe casts
- Adds regression tests for discount edge cases (null code, empty lines, invalid data)
- Runs the narrowest useful test command
- Summarizes files changed, behavior preserved, and verification command

## Failure Signals

- Refactors without tests
- Introduces nullable types everywhere without reason
- Changes discount math behavior silently
- Overuses scope functions that reduce readability
