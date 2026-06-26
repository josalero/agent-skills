# Transactions, Batch Writes, and Pool Tuning

Keep transactions short. Batch writes when volume warrants it.

## Short Transaction Scope

```php
<?php

declare(strict_types=1);

final class OrderCheckoutService
{
    public function checkout(Cart $cart): Order
    {
        return DB::transaction(function () use ($cart): Order {
            $order = $this->orders->createFromCart($cart);
            $this->inventory->reserveForOrder($order);
            $cart->markCheckedOut();

            return $order;
        });
    }
}
```

Doctrine equivalent:

```php
return $this->entityManager->wrapInTransaction(function () use ($cart): Order {
    // persist + flush inside one bounded unit of work
});
```

## Batch Inserts

Eloquent:

```php
<?php

declare(strict_types=1);

foreach (array_chunk($rows, 500) as $chunk) {
    LineItem::query()->insert($chunk);
}
```

Doctrine:

```php
<?php

declare(strict_types=1);

foreach ($entities as $index => $entity) {
    $this->entityManager->persist($entity);
    if (($index + 1) % 100 === 0) {
        $this->entityManager->flush();
        $this->entityManager->clear();
    }
}
$this->entityManager->flush();
```

## Read-Only Query Hint

Doctrine:

```php
$query->setHint(Query::HINT_READ_ONLY, true);
```

Use only when no writes occur in the same request path on those entities.

## Connection Pool Signals

| Symptom | Likely cause | Direction |
| --- | --- | --- |
| `Too many connections` | Pool or PHP-FPM workers exceed DB limit | Reduce workers or pool size |
| Slow checkout under load | Long transactions holding connections | Narrow transaction scope |
| Spiky latency | Missing index on hot filter column | Add index or rewrite query |
| Memory growth in workers | Loading unbounded result sets | Paginate or stream |

## Laravel Pool Config Example

```php
'mysql' => [
    'driver' => 'mysql',
    'url' => env('DATABASE_URL'),
    'options' => extension_loaded('pdo_mysql') ? [
        PDO::ATTR_PERSISTENT => false,
    ] : [],
],
```

Avoid persistent PDO connections in FPM unless you understand worker lifecycle tradeoffs.

## Verification Commands

```bash
php artisan test --filter=OrderListPerformanceTest
symfony php bin/phpunit --filter OrderRepositoryTest
# local only: enable query log / doctrine debug stack
```
