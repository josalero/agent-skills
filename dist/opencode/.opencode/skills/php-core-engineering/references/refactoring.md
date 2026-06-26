# Refactoring and Code Review Examples

Preserve behavior first. Add or adjust tests before structural changes when risk is non-trivial.

## Replace Magic Strings with Enums

Before:

```php
<?php

if ($user->status() === 'ACTIVE') {
    $mailer->sendWelcome($user);
}
```

After:

```php
<?php

declare(strict_types=1);

enum AccountStatus: string
{
    case Active = 'active';
    case Suspended = 'suspended';
    case Closed = 'closed';
}

if ($user->status() === AccountStatus::Active) {
    $mailer->sendWelcome($user);
}
```

## Narrow Exception Handling

Before:

```php
<?php

try {
    $parser->parse($input);
} catch (Throwable) {
    error_log('parse failed');
}
```

After:

```php
<?php

declare(strict_types=1);

try {
    $parser->parse($input);
} catch (JsonException $exception) {
    throw new InvalidPayloadException('Request body is not valid JSON', 0, $exception);
}
```

## Extract Method to Clarify Intent

Before:

```php
<?php

public function eligible(Driver $driver): bool
{
    return $driver->age() >= 21
        && !array_filter($driver->violations(), static fn (Violation $v): bool => $v->severity() >= 3)
        && $driver->licenseExpiry() > new DateTimeImmutable('today');
}
```

After:

```php
<?php

declare(strict_types=1);

public function eligible(Driver $driver): bool
{
    return $this->meetsMinimumAge($driver)
        && $this->hasNoSeriousViolations($driver)
        && $this->hasValidLicense($driver);
}
```

## Review Checklist With Code Smells

| Smell | Example | Preferred direction |
| --- | --- | --- |
| God class | 800-line service doing validation, IO, mapping | Split by responsibility |
| Primitive obsession | `string $status` everywhere | Enum or value object |
| Leaking mutability | Returning internal array by reference | Copy or readonly wrapper |
| Boolean trap | `createUser(true, false, true)` | Named arguments or builder |
| Mixed concerns | SQL, HTTP, and mail in one method | Ports/adapters or layered services |

## Verification Commands

Composer with PHPUnit:

```bash
vendor/bin/phpunit --filter CoreRefactorTest
```

Pest:

```bash
vendor/bin/pest --filter=core-refactor
```

Static analysis:

```bash
vendor/bin/phpstan analyse src --level=8
```
