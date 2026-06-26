# PHP Version Migration Paths

Upgrade incrementally when crossing multiple majors. Run tests after each step.

## 7.4 to 8.0

Common breakages:

- Implicit nullable parameters removed — add explicit `?Type`.
- String/number loose comparisons tightened in edge cases.
- `${}` string interpolation deprecated — use `{$var}`.
- Many internal functions now throw `TypeError` or `ValueError`.

Before:

```php
function findUser(string $email = null): ?User
{
    return $repository->findByEmail($email);
}
```

After:

```php
function findUser(?string $email): ?User
{
    return $repository->findByEmail($email);
}
```

## 8.0 to 8.1

- Enums, readonly properties, first-class callable syntax become available — adopt selectively, not wholesale.
- `mysqli` and `PDO` error modes deserve review.
- Fibers and `never` return type appear — only use when the codebase already targets 8.1+.

## 8.1 to 8.2

- Dynamic properties deprecated on plain classes — mark DTOs `readonly` or add `#[AllowDynamicProperties]` only as a temporary bridge.
- `utf8_encode` / `utf8_decode` removed — replace with `mb_convert_encoding`.
- Sensitive parameter attribute available for redacted stack traces.

```php
final readonly class CustomerView
{
    public function __construct(
        public int $id,
        public string $email,
    ) {
    }
}
```

## 8.2 to 8.3 / 8.4

- Review override validation, typed class constants, and new DOM extension behavior if used.
- Re-run PHPStan/Psalm at the project's target level after bumping `composer.json` platform PHP.
- Check Laravel/Symfony release notes for supported PHP ranges before raising runtime.

## Framework Alignment Checklist

| Change | Laravel | Symfony |
| --- | --- | --- |
| Raise `php` constraint | Match supported Laravel version | Match supported Symfony LTS/current |
| Replace deprecated helpers | Search `artisan about` deprecations | Run `bin/console debug:container --deprecations` |
| Config cache | `php artisan config:clear` after deploy | Warm cache in CI smoke step |
| Test bootstrap | Update `phpunit.xml` env vars | Update `.env.test` and `APP_ENV=test` |

## Deprecation Sweep Commands

```bash
composer why-not php 8.3
vendor/bin/phpstan analyse --memory-limit=1G
php -d error_reporting=E_ALL vendor/bin/phpunit
grep -R "deprecated" storage/logs bootstrap/cache 2>/dev/null || true
```
