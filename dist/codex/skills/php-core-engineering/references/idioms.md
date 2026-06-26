# PHP Idioms and Patterns

Prefer clarity over cleverness. Match the project's PHP version before introducing newer language features.

## Readonly Value Objects

Use readonly classes for immutable data carriers with validated invariants.

```php
<?php

declare(strict_types=1);

final readonly class MoneyAmount
{
    public function __construct(
        public string $amount,
        public string $currency,
    ) {
        if (!preg_match('/^\d+(\.\d{1,2})?$/', $amount)) {
            throw new InvalidArgumentException('amount must be a non-negative decimal');
        }
        if ($currency === '') {
            throw new InvalidArgumentException('currency is required');
        }
    }
}
```

## Enums for Closed Domain Sets

Use backed enums when a fixed set of variants is a business rule.

```php
<?php

declare(strict_types=1);

enum PaymentStatus: string
{
    case Accepted = 'accepted';
    case Declined = 'declined';
    case Pending = 'pending';

    public function message(string $reference): string
    {
        return match ($this) {
            self::Accepted => "Accepted: {$reference}",
            self::Declined => "Declined: {$reference}",
            self::Pending => "Pending: {$reference}",
        };
    }
}
```

## Nullable Boundaries, Not Ambiguous Sentinels

Use nullable return types where absence is meaningful. Avoid magic strings like `''` or `0` when `null` expresses absence.

```php
<?php

declare(strict_types=1);

interface UserRepository
{
    public function findByEmail(string $email): ?User;
}
```

## Intentional Exceptions

Catch specific exceptions. Preserve cause. Do not swallow.

```php
<?php

declare(strict_types=1);

final class InvoiceLoader
{
    public function __construct(private InvoiceRepository $repository)
    {
    }

    public function load(string $id): Invoice
    {
        try {
            return $this->repository->find($id)
                ?? throw new InvoiceNotFoundException($id);
        } catch (PDOException $exception) {
            throw new InvoiceLoadException("Failed to load invoice {$id}", 0, $exception);
        }
    }
}
```

## Readable Collection Operations

Keep array operations short. Extract named methods when logic branches.

```php
<?php

declare(strict_types=1);

final class CustomerDirectory
{
    /**
     * @param list<Customer> $customers
     * @return list<string>
     */
    public function activeEmails(array $customers): array
    {
        $emails = array_map(
            static fn (Customer $customer): string => $customer->email(),
            array_filter($customers, static fn (Customer $customer): bool => $customer->isActive())
        );

        $emails = array_values(array_unique(array_filter($emails, static fn (string $email): bool => $email !== '')));
        sort($emails);

        return $emails;
    }
}
```

## Immutability and Defensive Copies

Return copies when exposing internal arrays or objects that callers could mutate.

```php
<?php

declare(strict_types=1);

final class Order
{
    /** @param list<LineItem> $items */
    public function __construct(private array $items)
    {
    }

    /** @return list<LineItem> */
    public function lineItems(): array
    {
        return [...$this->items];
    }
}
```
