# Secrets, Logging, and Safe Errors

Never commit secrets. Never log credentials, tokens, or regulated personal data.

## Environment-Based Secrets

```php
<?php

declare(strict_types=1);

final class MailConfig
{
    public function __construct(private string $dsn)
    {
    }

    public static function fromEnvironment(): self
    {
        $dsn = getenv('MAILER_DSN') ?: '';
        if ($dsn === '') {
            throw new RuntimeException('MAILER_DSN is not configured');
        }

        return new self($dsn);
    }
}
```

Laravel: use `config/services.php` with `env()` only in config files, then reference `config('services.mail.key')` in application code.

## Redacted Logging

Before:

```php
logger()->info('login', ['email' => $email, 'password' => $password]);
```

After:

```php
logger()->info('login_attempt', [
    'email_hash' => hash('sha256', strtolower($email)),
    'outcome' => 'failed',
]);
```

## Safe API Error Response

```php
<?php

declare(strict_types=1);

final class ApiErrorRenderer
{
    public function render(Throwable $throwable, bool $debug): JsonResponse
    {
        if ($throwable instanceof ValidationException) {
            return new JsonResponse([
                'title' => 'Validation Failed',
                'errors' => $throwable->errors(),
            ], 422);
        }

        logger()->error('request_failed', [
            'exception' => $throwable::class,
            'message' => $throwable->getMessage(),
        ]);

        return new JsonResponse([
            'title' => 'Internal Server Error',
            'detail' => $debug ? $throwable->getMessage() : 'An unexpected error occurred',
        ], 500);
    }
}
```

## Dependency Vulnerability Scan

```bash
composer audit
```

Symfony:

```bash
symfony check:security
```

## Session and Cookie Hardening Checklist

| Setting | Recommended |
| --- | --- |
| `session.cookie_httponly` | `1` |
| `session.cookie_secure` | `1` in production |
| `session.cookie_samesite` | `Lax` or `Strict` |
| Session fixation | Regenerate session ID on login |
| CSRF | Enabled for state-changing browser forms |

## Security Test Example

```php
<?php

public function testGuestCannotDeleteUser(): void
{
    $target = User::factory()->create();

    $this->deleteJson("/api/users/{$target->id}")
        ->assertUnauthorized();
}
```
