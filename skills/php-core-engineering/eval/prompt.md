# Eval: PHP Core Engineering

## Prompt

Review the following service class. Refactor for clearer types, safer exceptions, and better immutability without changing behavior. Add or update unit tests for edge cases.

```php
<?php

class DiscountService
{
    public function apply(array $lines, ?string $code): float
    {
        $total = 0.0;
        foreach ($lines as $line) {
            $total += $line['price'] * $line['qty'];
        }
        if ($code != null && $code == 'SAVE10') {
            $total = $total * 0.9;
        }
        return $total;
    }
}
```

## Expected Agent Behavior

- Inspects surrounding namespace, strict types usage, and test conventions before refactoring
- Replaces associative arrays with typed value objects or readonly DTOs
- Avoids swallowing exceptions and unsafe implicit casts
- Adds regression tests for discount edge cases (null code, empty lines, invalid data)
- Runs the narrowest useful test or static analysis command
- Summarizes files changed, behavior preserved, and verification command

## Failure Signals

- Refactors without tests
- Adds nullable parameters everywhere without reason
- Changes discount math behavior silently
- Disables strict types to make the refactor compile
- Uses dynamic properties or untyped arrays after claiming to improve types
