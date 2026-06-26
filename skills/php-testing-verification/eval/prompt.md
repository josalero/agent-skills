# Eval: PHP Testing Verification

## Prompt

Bug report: applying the same coupon twice reduces the order total twice. Fix the bug and add tests that would have caught it. The project uses PHPUnit.

```php
<?php

class Order
{
    private float $total;
    private bool $couponApplied = false;

    public function __construct(float $total)
    {
        $this->total = $total;
    }

    public function applyCoupon(string $code): void
    {
        if ($code === 'SAVE10') {
            $this->total *= 0.9;
            $this->couponApplied = true;
        }
    }

    public function total(): float
    {
        return $this->total;
    }
}
```

## Expected Agent Behavior

- Adds regression test reproducing double-discount failure
- Fixes logic with clear idempotency or state guard
- Uses behavior-focused assertions on `total()`, not private fields
- Runs targeted test command first
- Summarizes test type chosen and verification command

## Failure Signals

- Fixes code without regression test
- Tests private properties instead of observable behavior
- Runs entire suite without mentioning narrower command first
- Adds Dockerized database for pure unit logic
