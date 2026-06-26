# PHP Unit Tests

Use behavior-focused names. Test public contracts, not private helpers unless the algorithm is business-critical.

## PHPUnit Example

```php
<?php

declare(strict_types=1);

namespace App\Tests\Unit\Billing;

use App\Billing\CouponApplier;
use PHPUnit\Framework\TestCase;

final class CouponApplierTest extends TestCase
{
    public function testAppliesTenPercentDiscountOnce(): void
    {
        $applier = new CouponApplier();

        $first = $applier->apply('SAVE10', 100.0);
        $second = $applier->apply('SAVE10', $first);

        self::assertSame(90.0, $first);
        self::assertSame(90.0, $second);
    }

    public function testIgnoresUnknownCoupon(): void
    {
        $applier = new CouponApplier();

        self::assertSame(100.0, $applier->apply('UNKNOWN', 100.0));
    }
}
```

## Pest Example

```php
<?php

declare(strict_types=1);

use App\Billing\CouponApplier;

it('applies ten percent discount once', function (): void {
    $applier = new CouponApplier();

    expect($applier->apply('SAVE10', 100.0))->toBe(90.0)
        ->and($applier->apply('SAVE10', 90.0))->toBe(90.0);
});
```

## Test Data Builders

Prefer small factories over large shared fixtures that hide intent.

```php
<?php

declare(strict_types=1);

final class OrderBuilder
{
    private string $sku = 'SKU-1';
    private int $quantity = 1;

    public function withSku(string $sku): self
    {
        $clone = clone $this;
        $clone->sku = $sku;
        return $clone;
    }

    public function build(): Order
    {
        return new Order($this->sku, $this->quantity);
    }
}
```

## Naming Convention

| Pattern | Example |
| --- | --- |
| Method + scenario + outcome | `testRejectsBlankSku` |
| Pest sentence style | `it('rejects blank sku')` |
| Regression bug id | `testIssue123DoubleDiscountIsIdempotent` |

## Verification Commands

```bash
vendor/bin/phpunit --filter CouponApplierTest
vendor/bin/pest --filter=coupon
```
