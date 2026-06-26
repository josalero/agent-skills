# Eval: Java Core Engineering

## Prompt

Review the following service class. Refactor for clearer types, safer exceptions, and better immutability without changing behavior. Add or update unit tests for edge cases.

```java
public class DiscountService {
    public double apply(List<Map<String, Object>> lines, String code) {
        double total = 0;
        for (Map<String, Object> line : lines) {
            total += (Double) line.get("price") * (Integer) line.get("qty");
        }
        if (code != null && code.equals("SAVE10")) {
            total = total * 0.9;
        }
        return total;
    }
}
```

## Expected Agent Behavior

- Inspects surrounding package and test conventions before refactoring
- Replaces primitive maps with typed records or value objects
- Avoids swallowing exceptions and unsafe casts
- Adds regression tests for discount edge cases (null code, empty lines, invalid data)
- Runs the narrowest useful test command
- Summarizes files changed, behavior preserved, and verification command

## Failure Signals

- Refactors without tests
- Introduces Optional fields everywhere without reason
- Changes discount math behavior silently
- Uses streams that reduce readability
