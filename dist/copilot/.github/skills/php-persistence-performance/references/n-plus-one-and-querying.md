# N+1 Queries and Query Shaping

## Symptom

One query loads a parent list, then the ORM issues one query per child row when the mapper or view touches a lazy association.

## Eloquent Fix With Constrained Eager Load

```php
<?php

declare(strict_types=1);

$orders = Order::query()
    ->with(['lines:id,order_id,sku'])
    ->where('customer_id', $customerId)
    ->paginate(20);
```

Use selective columns only when you understand FK requirements and serialization needs.

## Doctrine Join Fetch (Use Sparingly)

```php
<?php

declare(strict_types=1);

return $this->createQueryBuilder('o')
    ->select('o', 'l')
    ->join('o.lines', 'l')
    ->where('o.customerId = :customerId')
    ->setParameter('customerId', $customerId)
    ->getQuery()
    ->getResult();
```

Add `DISTINCT` when join fetch multiplies parent rows.

## DTO Projection (Often Best for Read APIs)

Doctrine:

```php
<?php

declare(strict_types=1);

return $this->createQueryBuilder('o')
    ->select(sprintf(
        'NEW %s(o.id, o.status, COUNT(l.id))',
        OrderSummaryDto::class,
    ))
    ->join('o.lines', 'l')
    ->where('o.customerId = :customerId')
    ->groupBy('o.id, o.status')
    ->setParameter('customerId', $customerId)
    ->getQuery()
    ->getResult();
```

Eloquent:

```php
<?php

declare(strict_types=1);

Order::query()
    ->select(['orders.id', 'orders.status'])
    ->withCount('lines')
    ->where('customer_id', $customerId)
    ->paginate(20);
```

## Database Pagination

Before:

```php
$orders = Order::all()->filter(fn ($order) => $order->status === 'open')->slice(0, 20);
```

After:

```php
$orders = Order::query()->where('status', 'open')->paginate(20);
```

## Diagnosis Checklist

- Enable query logging or Symfony/Telescope debug only in local/dev.
- Count queries per HTTP request before and after the change.
- Watch for lazy loading inside loops, API resources, or Twig/Blade rendering.
- Confirm indexes exist on filter and foreign-key columns used in hot paths.
