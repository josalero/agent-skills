# PHP CI Pipeline Gates

## Canonical Composer Scripts

```json
{
  "scripts": {
    "test": "phpunit",
    "analyse": "phpstan analyse --memory-limit=1G",
    "format:check": "php-cs-fixer fix --dry-run --diff",
    "quality": [
      "@format:check",
      "@analyse",
      "@test"
    ]
  }
}
```

Laravel projects may use `./vendor/bin/pint --test` instead of PHP-CS-Fixer.

## Example CI

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: "8.3"
          coverage: xdebug
      - run: composer install --prefer-dist --no-progress
      - run: composer quality
```

## PR vs Main

| Gate | PR | Main |
| --- | --- | --- |
| PHPUnit unit | Yes | Yes |
| PHPStan/Psalm | Yes | Yes |
| Style check | Yes | Yes |
| Feature/browser tests | Optional | Nightly |

## PHP Version Matrix

Test the minimum supported PHP version in CI if the package claims compatibility — not only latest.

## Blocking Rules

Fail on: test failure, static analysis error, style diff, Composer lock out of sync (`composer validate`).

## Related Skills

- `php-delivery-operations` — deploy after quality passes
- `testing-strategy` — test layer selection
