# PHP Integration and Feature Tests

Use integration tests when ORM, HTTP kernel, serializer, or container wiring affects behavior.

## Laravel Database Feature Test

```php
<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Models\Order;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

final class OrderRepositoryTest extends TestCase
{
    use RefreshDatabase;

    public function testFindsOrdersByCustomer(): void
    {
        Order::factory()->create(['customer_id' => 10, 'status' => 'open']);
        Order::factory()->create(['customer_id' => 10, 'status' => 'closed']);
        Order::factory()->create(['customer_id' => 99]);

        $orders = Order::query()->where('customer_id', 10)->get();

        self::assertCount(2, $orders);
    }
}
```

## Symfony WebTestCase

```php
<?php

declare(strict_types=1);

namespace App\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

final class OrderControllerTest extends WebTestCase
{
    public function testCreateOrderReturnsCreated(): void
    {
        $client = static::createClient();
        $client->request(
            'POST',
            '/api/v1/orders',
            server: ['CONTENT_TYPE' => 'application/json'],
            content: json_encode(['sku' => 'LEATHER-001', 'quantity' => 2], JSON_THROW_ON_ERROR),
        );

        self::assertResponseStatusCodeSame(201);
        self::assertJson($client->getResponse()->getContent());
    }
}
```

## Database Isolation

| Strategy | When to use |
| --- | --- |
| Transactions per test | Fast suite with shared schema |
| RefreshDatabase / DAMA rollback | Laravel integration tests |
| Dedicated test database + migrations | Symfony, Doctrine, long-running suites |
| SQLite in-memory | Pure unit-adjacent persistence tests only when behavior matches production DB |

## CI Quality Gates

```yaml
- name: PHPUnit
  run: vendor/bin/phpunit --testsuite=unit

- name: Integration
  run: vendor/bin/phpunit --testsuite=integration

- name: Static analysis
  run: vendor/bin/phpstan analyse src --level=8
```

## Regression Test Template

```php
<?php

public function testIssue456CouponCannotBeAppliedTwice(): void
{
    $order = new Order(total: 100.0);

    $order->applyCoupon('SAVE10');
    $order->applyCoupon('SAVE10');

    self::assertSame(90.0, $order->total());
}
```
